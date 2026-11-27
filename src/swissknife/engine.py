from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from swissknife.models import Entry, Freshness, Workspace, to_dict
from swissknife.probes import compute_freshness


def _is_cloud_only(entry: Entry) -> bool:
    if entry.kind == "gateway":
        return True
    runs = set(entry.relations.runs_on)
    return bool(runs) and runs == {"cloud"}


def _build_indices(ws: Workspace) -> dict[str, dict[str, list[str]]]:
    adapters_for: dict[str, list[str]] = {}
    guards_for: dict[str, list[str]] = {}
    by_world: dict[str, list[str]] = {}

    for eid, entry in ws.entries.items():
        for target in entry.relations.adapts:
            adapters_for.setdefault(target, []).append(eid)
        for target in entry.relations.guards:
            guards_for.setdefault(target, []).append(eid)
        for wid in entry.relations.runs_on:
            by_world.setdefault(wid, []).append(eid)

    return {"adapters_for": adapters_for, "guards_for": guards_for, "by_world": by_world}


def evaluate_workspace(ws: Workspace, as_of: date | None = None) -> dict[str, Any]:
    today = (as_of or datetime.now(timezone.utc).date()).isoformat()
    indices = _build_indices(ws)

    fmap: dict[str, Freshness] = {
        eid: compute_freshness(
            last_verified=entry.last_verified,
            decay_class=entry.decay_class,
            lifecycle=entry.lifecycle,
            reviewed_release=entry.meta.get("last_reviewed_release"),
            record=ws.health_state.get(f"entry:{eid}"),
            as_of=as_of,
        )
        for eid, entry in ws.entries.items()
    }

    deltas: dict[str, list[dict[str, Any]]] = {
        "release_updates": [],
        "decision_reviews": [],
        "reverify_upstream": [],
        "stale": [],
        "aging": [],
        "degraded": [],
        "retirement_candidates": [],
    }

    for eid, entry in ws.entries.items():
        f = fmap[eid]
        alerts = []
        for target in entry.relations.adapts:
            t_st = fmap[target].status
            if t_st in ("stale", "degraded", "retired"):
                alerts.append({"relation": "adapts", "target": target, "target_status": t_st})
        f.upstream_alerts = alerts
        if alerts and f.status == "fresh":
            f.effective_status = "reverify-upstream"

        if f.release_delta:
            deltas["release_updates"].append({
                "id": eid,
                "name": entry.name,
                "reviewed_release": entry.meta.get("last_reviewed_release"),
                "latest_release": f.latest_release_tag,
                "breaking_signal": f.breaking_signal,
                "url": entry.url,
            })
        if f.effective_status == "reverify-upstream":
            deltas["reverify_upstream"].append({"id": eid, "alerts": alerts})
        elif f.effective_status in ("aging", "stale", "degraded"):
            deltas[f.effective_status].append({"id": eid, "kind": entry.kind, "age_days": f.age_days, "ttl_days": f.ttl_days})
        if f.retirement_candidate:
            deltas["retirement_candidates"].append({"id": eid, "archived": f.upstream_archived, "fails": f.consecutive_fails})

    decision_states: dict[str, dict[str, Any]] = {}
    for did, dec in ws.decisions.items():
        triggers: list[dict[str, Any]] = []
        if dec.status == "accepted":
            for aid in dec.anchor_ids:
                if aid not in fmap:
                    continue
                af = fmap[aid]
                if af.effective_status in ("stale", "degraded", "reverify-upstream") or af.breaking_signal:
                    triggers.append({
                        "anchor_id": aid,
                        "status": af.effective_status,
                        "release_delta": af.release_delta,
                        "breaking_signal": af.breaking_signal,
                    })
        needs_review = bool(triggers)
        decision_states[did] = {**to_dict(dec), "needs_review": needs_review, "review_triggers": triggers}
        if needs_review:
            deltas["decision_reviews"].append({
                "decision_id": did,
                "title": dec.title,
                "reversal_trigger": dec.reversal_trigger,
                "triggers": triggers,
            })

    external_links: list[dict[str, Any]] = []
    for spid, sp in ws.specialists.items():
        for key, ref, scope in (
            *[(f"specialist:{spid}:{p.id}", p, f"specialist:{spid}") for p in sp.direct_picks],
            (f"specialist:{spid}:upstream", sp.upstream_hub, f"specialist:{spid}:upstream"),
        ):
            ef = compute_freshness(
                last_verified=sp.last_verified,
                decay_class="operational",
                lifecycle="operational",
                record=ws.health_state.get(key),
                as_of=as_of,
            )
            external_links.append({"key": key, "scope": scope, **to_dict(ref), "last_verified": sp.last_verified, "freshness": to_dict(ef)})
            if ef.status in ("aging", "stale", "degraded"):
                deltas[ef.status].append({"id": key, "kind": scope, "age_days": ef.age_days, "ttl_days": ef.ttl_days})
            if ef.retirement_candidate:
                deltas["retirement_candidates"].append({"id": key, "archived": ef.upstream_archived, "fails": ef.consecutive_fails})

    watch_active: dict[str, list[dict[str, Any]]] = {"frontier": [], "community": []}
    watch_expired: list[dict[str, Any]] = []
    for bucket, items in (("frontier", ws.watch_frontier), ("community", ws.watch_community)):
        for w in items:
            wf = compute_freshness(
                last_verified=w.last_verified,
                decay_class="volatile",
                lifecycle="monitor-only" if bucket == "frontier" else "experimental",
                record=ws.health_state.get(f"watch:{bucket}:{w.id}"),
                as_of=as_of,
            )
            payload = {**to_dict(w), "freshness": to_dict(wf)}
            if wf.age_days > wf.ttl_days or wf.status == "degraded":
                watch_expired.append(payload)
                deltas["stale"].append({"id": f"watch:{bucket}:{w.id}", "kind": "watch-expired", "age_days": wf.age_days, "ttl_days": wf.ttl_days})
            else:
                watch_active[bucket].append(payload)

    return {
        "as_of": today,
        "indices": indices,
        "freshness": fmap,
        "decisions": decision_states,
        "external_links": external_links,
        "watch_active": watch_active,
        "watch_expired": watch_expired,
        "deltas": deltas,
    }


def resolve_slot(
    ws: Workspace,
    slot_id: str,
    *,
    world: str | None = None,
    as_of: date | None = None,
    include_stale: bool = False,
) -> dict[str, Any]:
    if slot_id not in ws.slots:
        return {"error": f"Unknown slot '{slot_id}'", "available_slots": sorted(ws.slots.keys())}

    st = evaluate_workspace(ws, as_of=as_of)
    fmap: dict[str, Freshness] = st["freshness"]
    idx = st["indices"]
    slot = ws.slots[slot_id]
    effective_world = world or slot.world

    configured_primary = {**to_dict(ws.entries[slot.primary]), "freshness": to_dict(fmap[slot.primary])}
    candidates = [slot.primary, *slot.fallbacks]
    selected_id: str | None = None
    fallback_used = False
    skipped: list[dict[str, Any]] = []

    for pos, eid in enumerate(candidates):
        entry = ws.entries[eid]
        f = fmap[eid]
        if effective_world and entry.relations.runs_on and effective_world not in entry.relations.runs_on:
            skipped.append({"id": eid, "reason": f"world_mismatch:{effective_world}"})
            continue
        if not include_stale and not f.eligible_for_agents:
            skipped.append({"id": eid, "reason": f"freshness:{f.effective_status}"})
            continue
        selected_id = eid
        fallback_used = pos > 0
        break

    active = None
    discovered_adapters: list[dict[str, Any]] = []
    if selected_id:
        e = ws.entries[selected_id]
        active = {**to_dict(e), "freshness": to_dict(fmap[selected_id])}
        for aid in idx["adapters_for"].get(selected_id, []):
            a_entry = ws.entries[aid]
            if effective_world and a_entry.relations.runs_on and effective_world not in a_entry.relations.runs_on:
                continue
            af = fmap[aid]
            if include_stale or af.eligible_for_agents:
                discovered_adapters.append({**to_dict(a_entry), "freshness": to_dict(af)})

    experimental = None
    if slot.experimental:
        exp_entry = ws.entries[slot.experimental]
        ef = fmap[slot.experimental]
        world_ok = not effective_world or not exp_entry.relations.runs_on or effective_world in exp_entry.relations.runs_on
        if world_ok and (include_stale or ef.eligible_for_agents):
            experimental = {**to_dict(exp_entry), "freshness": to_dict(ef)}

    return {
        "slot_id": slot.id,
        "title": slot.title,
        "role": slot.role,
        "world_filter": effective_world or "all",
        "fallback_used": fallback_used,
        "configured_primary": configured_primary,
        "active": active,
        "experimental": experimental,
        "discovered_adapters": discovered_adapters,
        "decision": st["decisions"].get(slot.decision_id) if slot.decision_id else None,
        "skipped": skipped,
    }


def resolve_specialist(
    ws: Workspace,
    specialist_id: str,
    *,
    world: str | None = None,
    as_of: date | None = None,
    include_stale: bool = False,
) -> dict[str, Any]:
    if specialist_id not in ws.specialists:
        return {"error": f"Unknown specialist '{specialist_id}'", "available_specialists": sorted(ws.specialists.keys())}

    st = evaluate_workspace(ws, as_of=as_of)
    fmap: dict[str, Freshness] = st["freshness"]
    idx = st["indices"]
    sp = ws.specialists[specialist_id]
    req_caps = set(sp.capabilities)

    models_gateways, harnesses, runtimes, adapters, guards = [], [], [], [], []
    selected_ids: set[str] = set()

    for eid, entry in ws.entries.items():
        if entry.kind == "adapter":
            continue
        if sp.privacy == "local-only" and _is_cloud_only(entry):
            continue
        if world and entry.relations.runs_on and world not in entry.relations.runs_on:
            continue
        if not (req_caps & set(entry.capabilities)):
            continue
        f = fmap[eid]
        if not include_stale and not f.eligible_for_agents:
            continue
        item = {"id": eid, "name": entry.name, "kind": entry.kind, "url": entry.url, "freshness": to_dict(f)}
        selected_ids.add(eid)
        if entry.kind in ("model", "gateway"):
            models_gateways.append(item)
        elif entry.kind == "harness":
            harnesses.append(item)
        elif entry.kind == "runtime":
            runtimes.append(item)

    seen_adapters: set[str] = set()
    for sid in list(selected_ids):
        for aid in idx["adapters_for"].get(sid, []):
            if aid in seen_adapters:
                continue
            a_entry = ws.entries[aid]
            if world and a_entry.relations.runs_on and world not in a_entry.relations.runs_on:
                continue
            if req_caps and a_entry.capabilities and not (req_caps & set(a_entry.capabilities)):
                continue
            af = fmap[aid]
            if not include_stale and not af.eligible_for_agents:
                continue
            seen_adapters.add(aid)
            adapters.append({"id": aid, "name": a_entry.name, "url": a_entry.url, "freshness": to_dict(af)})

    if sp.require_guard:
        guard_ids = set(idx["guards_for"].get("*", []))
        for sid in selected_ids:
            guard_ids.update(idx["guards_for"].get(sid, []))
        for gid in sorted(guard_ids):
            g_entry = ws.entries[gid]
            if sp.privacy == "local-only" and _is_cloud_only(g_entry):
                continue
            gf = fmap[gid]
            if include_stale or gf.eligible_for_agents:
                guards.append({"id": gid, "name": g_entry.name, "url": g_entry.url, "freshness": to_dict(gf)})

    hydrated_picks = [
        {
            **to_dict(p),
            "freshness": to_dict(
                compute_freshness(
                    last_verified=sp.last_verified,
                    decay_class="operational",
                    lifecycle="operational",
                    record=ws.health_state.get(f"specialist:{specialist_id}:{p.id}"),
                    as_of=as_of,
                )
            ),
        }
        for p in sp.direct_picks
    ]
    hydrated_hub = {
        **to_dict(sp.upstream_hub),
        "freshness": to_dict(
            compute_freshness(
                last_verified=sp.last_verified,
                decay_class="operational",
                lifecycle="operational",
                record=ws.health_state.get(f"specialist:{specialist_id}:upstream"),
                as_of=as_of,
            )
        ),
    }

    return {
        "id": sp.id,
        "title": sp.title,
        "summary": sp.summary,
        "last_verified": sp.last_verified,
        "privacy": sp.privacy,
        "world_filter": world or "all",
        "resolved": {
            "models_and_gateways": models_gateways,
            "harnesses": harnesses,
            "runtimes": runtimes,
            "adapters": adapters,
            "guards": guards,
        },
        "direct_picks": hydrated_picks,
        "upstream_hub": hydrated_hub,
        "guardrails": sp.guardrails,
    }


def query_entries(
    ws: Workspace,
    *,
    kind: str | None = None,
    world: str | None = None,
    tag: str | None = None,
    capability: str | None = None,
    privacy: str = "any",
    eligible_only: bool = True,
    as_of: date | None = None,
) -> dict[str, Any]:
    st = evaluate_workspace(ws, as_of=as_of)
    fmap: dict[str, Freshness] = st["freshness"]
    matches: list[dict[str, Any]] = []

    for eid, entry in ws.entries.items():
        if kind and entry.kind != kind:
            continue
        if world and entry.relations.runs_on and world not in entry.relations.runs_on:
            continue
        if tag and tag not in entry.tags:
            continue
        if capability and capability not in entry.capabilities:
            continue
        if privacy == "local-only" and _is_cloud_only(entry):
            continue
        f = fmap[eid]
        if eligible_only and not f.eligible_for_agents:
            continue
        matches.append({**to_dict(entry), "freshness": to_dict(f)})

    return {"as_of": st["as_of"], "count": len(matches), "entries": matches}


def build_snapshot(ws: Workspace, as_of: date | None = None) -> dict[str, Any]:
    st = evaluate_workspace(ws, as_of=as_of)
    fmap: dict[str, Freshness] = st["freshness"]

    return {
        "schema_version": "6.0.0-beta.1",
        "as_of": st["as_of"],
        "counts": {
            "worlds": len(ws.taxonomy.worlds),
            "entries": len(ws.entries),
            "agent_eligible": sum(1 for f in fmap.values() if f.eligible_for_agents),
            "slots": len(ws.slots),
            "decisions": len(ws.decisions),
            "specialists": len(ws.specialists),
            "pages": len(ws.pages),
            "watch_active": len(st["watch_active"]["frontier"]) + len(st["watch_active"]["community"]),
            "watch_expired": len(st["watch_expired"]),
        },
        "taxonomy": to_dict(ws.taxonomy),
        "indices": st["indices"],
        "entries": {eid: {**to_dict(e), "freshness": to_dict(fmap[eid])} for eid, e in ws.entries.items()},
        "slots": {sid: resolve_slot(ws, sid, as_of=as_of, include_stale=False) for sid in sorted(ws.slots.keys())},
        "decisions": st["decisions"],
        "specialists": {spid: resolve_specialist(ws, spid, as_of=as_of, include_stale=False) for spid in sorted(ws.specialists.keys())},
        "pages": [to_dict(p) for p in ws.pages],
        "external_links": st["external_links"],
        "watch": st["watch_active"],
        "watch_expired": st["watch_expired"],
        "retired": [to_dict(r) for r in ws.retired],
        "deltas": st["deltas"],
    }
