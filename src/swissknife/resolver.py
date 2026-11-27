from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from swissknife.health import compute_freshness
from swissknife.models import Catalog, Entry, FreshnessState, to_dict


def _is_cloud_only(entry: Entry) -> bool:
    if entry.kind == "gateway":
        return True
    runs = set(entry.edges.runs_on)
    return bool(runs) and runs == {"zero-card-cloud"}


def _build_indices(catalog: Catalog) -> dict[str, dict[str, list[str]]]:
    adapters_for: dict[str, list[str]] = {}
    guards_for: dict[str, list[str]] = {}
    by_profile: dict[str, list[str]] = {}

    for eid, entry in catalog.entries.items():
        for target in entry.edges.adapts:
            adapters_for.setdefault(target, []).append(eid)
        for target in entry.edges.guards:
            guards_for.setdefault(target, []).append(eid)
        for pid in entry.edges.runs_on:
            by_profile.setdefault(pid, []).append(eid)

    return {"adapters_for": adapters_for, "guards_for": guards_for, "by_profile": by_profile}


def evaluate_state(catalog: Catalog, as_of: date | None = None) -> dict[str, Any]:
    today = (as_of or datetime.now(timezone.utc).date()).isoformat()
    indices = _build_indices(catalog)

    freshness_map: dict[str, FreshnessState] = {
        eid: compute_freshness(
            last_verified=entry.last_verified,
            decay_class=entry.decay_class,
            lifecycle=entry.lifecycle,
            record=catalog.health_state.get(f"entry:{eid}"),
            as_of=as_of,
        )
        for eid, entry in catalog.entries.items()
    }

    digest: dict[str, list[dict[str, Any]]] = {
        "aging": [],
        "stale": [],
        "reverify-upstream": [],
        "degraded": [],
        "retirement_candidates": [],
    }

    # Core entries + transitive alerts along `adapts` edges
    for eid, entry in catalog.entries.items():
        f = freshness_map[eid]
        alerts = []
        for target in entry.edges.adapts:
            t_st = freshness_map[target].status
            if t_st in ("stale", "degraded", "retired"):
                alerts.append({"edge": "adapts", "target": target, "target_status": t_st})
        f.upstream_alerts = alerts
        if alerts and f.status == "fresh":
            f.effective_status = "reverify-upstream"

        if f.effective_status in ("aging", "stale", "reverify-upstream", "degraded"):
            digest[f.effective_status].append({"id": eid, "kind": entry.kind, "age_days": f.age_days, "ttl_days": f.ttl_days})
        if f.retirement_candidate:
            digest["retirement_candidates"].append({"id": eid, "archived": f.upstream_archived, "fails": f.consecutive_fails})

    # Supporting guide tools & specialist directories (eliminates live-health blind spot)
    external_links: list[dict[str, Any]] = []

    def _record_external(key: str, scope: str, name: str, url: str, verified: str, decay: str) -> None:
        ef = compute_freshness(
            last_verified=verified,
            decay_class=decay,
            lifecycle="operational",
            record=catalog.health_state.get(key),
            as_of=as_of,
        )
        external_links.append({
            "key": key,
            "scope": scope,
            "name": name,
            "url": url,
            "last_verified": verified,
            "freshness": to_dict(ef),
        })
        if ef.status in ("aging", "stale", "degraded"):
            digest[ef.status].append({"id": key, "kind": scope, "age_days": ef.age_days, "ttl_days": ef.ttl_days})
        if ef.retirement_candidate:
            digest["retirement_candidates"].append({"id": key, "archived": ef.upstream_archived, "fails": ef.consecutive_fails})

    for gid, guide in catalog.guides.items():
        for tool in guide.tools:
            _record_external(f"guide:{gid}:{tool.id}", f"guide:{gid}", tool.name, tool.url, guide.last_verified, guide.decay_class)

    for sid, spec in catalog.specialists.items():
        for pick in spec.direct_picks:
            _record_external(f"specialist:{sid}:{pick.id}", f"specialist:{sid}", pick.name, pick.url, spec.last_verified, "operational")
        up = spec.upstream_directory
        _record_external(f"specialist:{sid}:upstream", f"specialist:{sid} (upstream)", up.name, up.url, spec.last_verified, "operational")

    # Watch List freshness
    watch_out: dict[str, list[dict[str, Any]]] = {"frontier": [], "community": []}
    for bucket, items in (("frontier", catalog.watch_frontier), ("community", catalog.watch_community)):
        for item in items:
            wf = compute_freshness(
                last_verified=item.last_verified,
                decay_class="volatile",
                lifecycle="monitor-only" if bucket == "frontier" else "experimental",
                record=catalog.health_state.get(f"watch:{bucket}:{item.id}"),
                as_of=as_of,
            )
            watch_out[bucket].append({**to_dict(item), "freshness": to_dict(wf)})
            if wf.status in ("stale", "degraded"):
                digest[wf.status].append({"id": f"watch:{bucket}:{item.id}", "age_days": wf.age_days, "ttl_days": wf.ttl_days})

    return {
        "as_of": today,
        "indices": indices,
        "freshness": freshness_map,
        "external_links": external_links,
        "watch": watch_out,
        "digest": digest,
    }


def resolve_target(
    catalog: Catalog,
    target_id: str,
    *,
    profile_id: str | None = None,
    as_of: date | None = None,
    include_stale: bool = False,
) -> dict[str, Any]:
    is_guide = target_id in catalog.guides
    is_specialist = target_id in catalog.specialists
    if not (is_guide or is_specialist):
        return {
            "error": f"Unknown target '{target_id}'",
            "available_guides": sorted(catalog.guides.keys()),
            "available_specialists": sorted(catalog.specialists.keys()),
        }

    st = evaluate_state(catalog, as_of=as_of)
    fmap: dict[str, FreshnessState] = st["freshness"]
    idx = st["indices"]

    spec = catalog.guides[target_id] if is_guide else catalog.specialists[target_id]
    req_caps = set(spec.capabilities)
    pin_set = set(spec.pin_entries) if is_guide else set()

    models_gateways, harnesses, runtimes, adapters, guards, excluded = [], [], [], [], [], []
    selected_ids: set[str] = set()

    for eid, entry in catalog.entries.items():
        if entry.kind == "adapter":
            continue
        if spec.privacy == "local-only" and _is_cloud_only(entry):
            continue
        if profile_id and entry.edges.runs_on and profile_id not in entry.edges.runs_on:
            continue

        matched_caps = sorted(req_caps & set(entry.capabilities))
        pinned = eid in pin_set
        if not (pinned or matched_caps):
            continue

        f = fmap[eid]
        if not include_stale and not f.eligible_for_agents:
            excluded.append({"id": eid, "reason": f"freshness:{f.effective_status}", "age_days": f.age_days})
            continue

        item = {
            "id": eid,
            "name": entry.name,
            "kind": entry.kind,
            "lifecycle": entry.lifecycle,
            "evidence_tier": entry.evidence_tier,
            "match_reason": "pinned" if pinned else f"capabilities:{','.join(matched_caps)}",
            "url": entry.url,
            "launch_recipe": entry.launch_recipe,
            "mac_launch_recipe": entry.mac_launch_recipe,
            "freshness": to_dict(f),
        }
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
            a_entry = catalog.entries[aid]
            if profile_id and a_entry.edges.runs_on and profile_id not in a_entry.edges.runs_on:
                continue
            if req_caps and a_entry.capabilities and not (req_caps & set(a_entry.capabilities)):
                continue
            af = fmap[aid]
            if not include_stale and not af.eligible_for_agents:
                excluded.append({"id": aid, "reason": f"adapter_freshness:{af.effective_status}"})
                continue
            seen_adapters.add(aid)
            adapters.append({
                "id": aid,
                "name": a_entry.name,
                "adapts": a_entry.edges.adapts,
                "evidence_tier": a_entry.evidence_tier,
                "url": a_entry.url,
                "launch_recipe": a_entry.launch_recipe,
                "mac_launch_recipe": a_entry.mac_launch_recipe,
                "freshness": to_dict(af),
            })

    if spec.require_guard:
        guard_ids = set(idx["guards_for"].get("*", []))
        for sid in selected_ids:
            guard_ids.update(idx["guards_for"].get(sid, []))
        for gid in sorted(guard_ids):
            g_entry = catalog.entries[gid]
            if spec.privacy == "local-only" and _is_cloud_only(g_entry):
                continue
            gf = fmap[gid]
            if include_stale or gf.eligible_for_agents:
                guards.append({"id": gid, "name": g_entry.name, "url": g_entry.url, "freshness": to_dict(gf)})

    extra: dict[str, Any] = {}
    if is_guide:
        g_spec = catalog.guides[target_id]
        extra["tools"] = [
            {
                **to_dict(t),
                "freshness": to_dict(compute_freshness(
                    last_verified=g_spec.last_verified,
                    decay_class=g_spec.decay_class,
                    lifecycle="operational",
                    record=catalog.health_state.get(f"guide:{target_id}:{t.id}"),
                    as_of=as_of,
                )),
            }
            for t in g_spec.tools
        ]
        extra["steps"] = g_spec.steps
        extra["limitations"] = g_spec.limitations
    else:
        s_spec = catalog.specialists[target_id]
        extra["direct_picks"] = [
            {
                **to_dict(p),
                "freshness": to_dict(compute_freshness(
                    last_verified=s_spec.last_verified,
                    decay_class="operational",
                    lifecycle="operational",
                    record=catalog.health_state.get(f"specialist:{target_id}:{p.id}"),
                    as_of=as_of,
                )),
            }
            for p in s_spec.direct_picks
        ]
        extra["upstream_directory"] = {
            **to_dict(s_spec.upstream_directory),
            "freshness": to_dict(compute_freshness(
                last_verified=s_spec.last_verified,
                decay_class="operational",
                lifecycle="operational",
                record=catalog.health_state.get(f"specialist:{target_id}:upstream"),
                as_of=as_of,
            )),
        }
        extra["limitations"] = s_spec.guardrails

    return {
        "id": target_id,
        "type": "guide" if is_guide else "specialist",
        "title": spec.title,
        "summary": spec.summary,
        "profile_filter": profile_id or "all",
        "resolved": {
            "models_and_gateways": models_gateways,
            "harnesses": harnesses,
            "runtimes": runtimes,
            "adapters": adapters,
            "guards": guards,
        },
        "excluded_stale": excluded,
        **extra,
    }


def build_snapshot(catalog: Catalog, as_of: date | None = None) -> dict[str, Any]:
    st = evaluate_state(catalog, as_of=as_of)
    fmap: dict[str, FreshnessState] = st["freshness"]

    return {
        "schema_version": "5.0.0-beta.1",
        "as_of": st["as_of"],
        "counts": {
            "profiles": len(catalog.profiles),
            "entries": len(catalog.entries),
            "agent_eligible": sum(1 for f in fmap.values() if f.eligible_for_agents),
            "external_links": len(st["external_links"]),
            "guides": len(catalog.guides),
            "specialists": len(catalog.specialists),
            "watch_frontier": len(catalog.watch_frontier),
            "watch_community": len(catalog.watch_community),
        },
        "profiles": {pid: to_dict(p) for pid, p in catalog.profiles.items()},
        "indices": st["indices"],
        "entries": {eid: {**to_dict(e), "freshness": to_dict(fmap[eid])} for eid, e in catalog.entries.items()},
        "external_links": st["external_links"],
        "routing_chains": catalog.routing_chains,
        "guides": {gid: resolve_target(catalog, gid, as_of=as_of, include_stale=True) for gid in sorted(catalog.guides.keys())},
        "specialists": {sid: resolve_target(catalog, sid, as_of=as_of, include_stale=True) for sid in sorted(catalog.specialists.keys())},
        "watch": st["watch"],
        "retired": [to_dict(r) for r in catalog.retired],
        "digest": st["digest"],
    }
