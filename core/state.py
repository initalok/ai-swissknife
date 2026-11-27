from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from core.health import compute_freshness


def _build_edge_index(nodes: dict[str, dict[str, Any]]) -> dict[str, dict[str, list[str]]]:
    adapters_for: dict[str, list[str]] = {}
    guards_for: dict[str, list[str]] = {}
    profile_nodes: dict[str, list[str]] = {}

    for nid, node in nodes.items():
        edges = node.get("edges", {})
        for target in edges.get("adapts", []):
            adapters_for.setdefault(target, []).append(nid)
        for target in edges.get("guards", []):
            guards_for.setdefault(target, []).append(nid)
        for prof in edges.get("runs_on", []):
            profile_nodes.setdefault(prof, []).append(nid)

    return {
        "adapters_for": adapters_for,
        "guards_for": guards_for,
        "profile_nodes": profile_nodes,
    }


def evaluate_implicit_state(data: dict[str, Any], as_of: date | None = None) -> dict[str, Any]:
    today = (as_of or datetime.now(timezone.utc).date()).isoformat()
    h_state = data["health_state"]
    nodes = data["nodes"]
    idx = _build_edge_index(nodes)

    node_freshness: dict[str, dict[str, Any]] = {
        nid: compute_freshness(node, h_state.get(f"node:{nid}"), as_of=as_of)
        for nid, node in nodes.items()
    }

    digest = {"aging": [], "stale": [], "degraded": [], "reverify_upstream": [], "graveyard_candidates": []}
    for nid, node in nodes.items():
        f = node_freshness[nid]
        alerts = []
        for target in node.get("edges", {}).get("adapts", []):
            t_status = node_freshness[target]["status"]
            if t_status in ("stale", "degraded", "graveyard"):
                alerts.append({"edge": "adapts", "target": target, "target_status": t_status})
        f["upstream_alerts"] = alerts
        f["effective_status"] = "reverify_upstream" if alerts and f["status"] == "fresh" else f["status"]

        eff = f["effective_status"]
        if eff in ("aging", "stale", "degraded", "reverify_upstream"):
            digest[eff].append({"id": nid, "kind": node["kind"], "age_days": f["age_days"], "ttl_days": f["ttl_days"]})
        if f["graveyard_candidate"]:
            digest["graveyard_candidates"].append({"id": nid, "archived": f["upstream_archived"], "fails": f["consecutive_fails"]})

    radar_health: dict[str, list[dict[str, Any]]] = {"frontier": [], "community": []}
    for bucket in ("frontier", "community"):
        for item in data["radar"][bucket]:
            f = compute_freshness(
                {**item, "lifecycle": "monitor-only" if bucket == "frontier" else item.get("lifecycle", "experimental"), "decay_class": "volatile"},
                h_state.get(f"radar:{bucket}:{item['id']}"),
                as_of=as_of,
            )
            radar_health[bucket].append({**item, "freshness": f})
            if f["status"] in ("stale", "degraded"):
                digest[f["status"]].append({"id": f"radar:{bucket}:{item['id']}", "age_days": f["age_days"], "ttl_days": f["ttl_days"]})

    return {
        "as_of": today,
        "edge_index": idx,
        "node_freshness": node_freshness,
        "radar": radar_health,
        "digest": digest,
    }


def resolve_horizon(
    data: dict[str, Any],
    horizon_id: str,
    profile_id: str | None = None,
    as_of: date | None = None,
    include_stale: bool = False,
) -> dict[str, Any]:
    is_playbook = horizon_id in data["playbooks"]
    is_spoke = horizon_id in data["spokes"]
    if not (is_playbook or is_spoke):
        return {
            "error": f"Unknown horizon '{horizon_id}'",
            "available_playbooks": sorted(data["playbooks"].keys()),
            "available_spokes": sorted(data["spokes"].keys()),
        }

    state = evaluate_implicit_state(data, as_of=as_of)
    nodes = data["nodes"]
    idx = state["edge_index"]
    nf = state["node_freshness"]
    h_state = data["health_state"]

    spec = data["playbooks"][horizon_id] if is_playbook else data["spokes"][horizon_id]
    c = spec.get("constraints", {})
    req_caps = set(c.get("capabilities", []))
    privacy = c.get("privacy", "any")
    require_guard = bool(c.get("require_guard", False))

    resolved_models, resolved_harnesses, resolved_backends, resolved_adapters, resolved_guards = [], [], [], [], []
    excluded: list[dict[str, Any]] = []

    def _profile_ok(node: dict[str, Any]) -> bool:
        runs_on = node.get("edges", {}).get("runs_on", [])
        if not profile_id or not runs_on:
            return True
        return profile_id in runs_on

    selected_ids: set[str] = set()
    for nid, node in nodes.items():
        f = nf[nid]
        if node["kind"] == "adapter":
            continue
        if privacy == "local-only" and (node["kind"] == "gateway" or "zero-card-cloud" in node.get("edges", {}).get("runs_on", [])):
            continue
        if not _profile_ok(node):
            continue

        node_caps = set(node.get("capabilities", []))
        pinned = nid in spec.get("pin_nodes", [])
        matched = pinned or bool(req_caps & node_caps)
        if not matched:
            continue

        if not include_stale and not f["eligible_for_agents"]:
            excluded.append({"id": nid, "reason": f"freshness:{f['effective_status']}", "age_days": f["age_days"]})
            continue

        entry = {
            "id": nid,
            "name": node["name"],
            "lifecycle": node["lifecycle"],
            "reason": "pinned" if pinned else f"matched_caps:{sorted(req_caps & node_caps)}",
            "freshness": f,
            "launch_recipe": node.get("launch_recipe"),
        }
        selected_ids.add(nid)
        if node["kind"] in ("model", "gateway"):
            resolved_models.append(entry)
        elif node["kind"] == "harness":
            resolved_harnesses.append(entry)
        elif node["kind"] == "backend":
            resolved_backends.append(entry)

    seen_adapters: set[str] = set()
    for sid in list(selected_ids):
        for aid in idx["adapters_for"].get(sid, []):
            if aid in seen_adapters:
                continue
            a_node = nodes[aid]
            a_caps = set(a_node.get("capabilities", []))
            if req_caps and a_caps and not (req_caps & a_caps):
                continue
            af = nf[aid]
            if not include_stale and not af["eligible_for_agents"]:
                excluded.append({"id": aid, "reason": f"adapter_freshness:{af['effective_status']}"})
                continue
            seen_adapters.add(aid)
            resolved_adapters.append({
                "id": aid,
                "name": a_node["name"],
                "adapts": a_node.get("edges", {}).get("adapts", []),
                "freshness": af,
                "launch_recipe": a_node.get("launch_recipe"),
            })

    if require_guard:
        guard_ids = set(idx["guards_for"].get("*", []))
        for sid in selected_ids:
            guard_ids.update(idx["guards_for"].get(sid, []))
        for gid in sorted(guard_ids):
            gf = nf[gid]
            if include_stale or gf["eligible_for_agents"]:
                resolved_guards.append({"id": gid, "name": nodes[gid]["name"], "url": nodes[gid]["url"], "freshness": gf})

    degraded_deps = [x for x in excluded if x["reason"].startswith(("freshness:stale", "freshness:degraded"))]
    extra: dict[str, Any] = {}
    if is_spoke:
        hub = spec["upstream_hub"]
        hub_f = compute_freshness(
            {"last_verified": spec["last_verified"], "decay_class": "operational", "lifecycle": "operational"},
            h_state.get(f"spoke:{horizon_id}:upstream_hub"),
            as_of=as_of,
        )
        hydrated_entries = [
            {
                **ep,
                "freshness": compute_freshness(
                    {"last_verified": spec["last_verified"], "decay_class": "operational", "lifecycle": "operational"},
                    h_state.get(f"spoke:{horizon_id}:{ep['id']}"),
                    as_of=as_of,
                ),
            }
            for ep in spec.get("entry_points", [])
        ]
        extra["entry_points"] = hydrated_entries
        extra["upstream_hub"] = {**hub, "freshness": hub_f}
    else:
        hydrated_tools = [
            {
                **tool,
                "freshness": compute_freshness(
                    {"last_verified": spec["last_verified"], "decay_class": spec.get("decay_class", "operational"), "lifecycle": "operational"},
                    h_state.get(f"playbook:{horizon_id}:{tool['id']}"),
                    as_of=as_of,
                ),
            }
            for tool in spec.get("domain_tools", [])
        ]
        extra["domain_tools"] = hydrated_tools
        extra["workflow"] = spec.get("workflow", [])

    return {
        "horizon_id": horizon_id,
        "tier": "playbook" if is_playbook else "spoke",
        "title": spec["title"],
        "verdict": spec["verdict"],
        "profile_filter": profile_id or "all",
        "implicit_core": {
            "models_and_gateways": resolved_models,
            "harnesses": resolved_harnesses,
            "backends": resolved_backends,
            "discovered_adapters": resolved_adapters,
            "guards": resolved_guards,
        },
        "excluded_stale": excluded,
        "degraded_dependency_count": len(degraded_deps),
        **extra,
        "guardrails": spec.get("gotchas") or spec.get("guardrails", []),
    }


def build_graph_snapshot(data: dict[str, Any], as_of: date | None = None) -> dict[str, Any]:
    state = evaluate_implicit_state(data, as_of=as_of)
    nf = state["node_freshness"]

    return {
        "schema_version": "4.0.0-beta",
        "as_of": state["as_of"],
        "counts": {
            "profiles": len(data["profiles"]),
            "core_nodes": len(data["nodes"]),
            "agent_eligible_nodes": sum(1 for v in nf.values() if v["eligible_for_agents"]),
            "playbooks": len(data["playbooks"]),
            "spokes": len(data["spokes"]),
            "radar_frontier": len(data["radar"]["frontier"]),
            "radar_community": len(data["radar"]["community"]),
        },
        "profiles": data["profiles"],
        "by_profile": state["edge_index"]["profile_nodes"],
        "adapters_for": state["edge_index"]["adapters_for"],
        "guards_for": state["edge_index"]["guards_for"],
        "nodes": {nid: {**node, "freshness": nf[nid]} for nid, node in data["nodes"].items()},
        "forage_routes": data["forage_routes"],
        "playbooks": {pid: resolve_horizon(data, pid, as_of=as_of, include_stale=True) for pid in sorted(data["playbooks"].keys())},
        "spokes": {sid: resolve_horizon(data, sid, as_of=as_of, include_stale=True) for sid in sorted(data["spokes"].keys())},
        "radar": state["radar"],
        "graveyard": data["graveyard"],
        "digest": state["digest"],
    }
