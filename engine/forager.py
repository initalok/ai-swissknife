from __future__ import annotations

import os
from datetime import date
from typing import Any
import requests

from engine.health import evaluate_workspace_health


def resolve_pack(
    ws: dict[str, Any],
    pack_id: str,
    as_of: date | None = None,
    include_stale: bool = False,
) -> dict[str, Any]:
    if pack_id not in ws["packs"]:
        return {"error": f"Unknown pack '{pack_id}'", "available_packs": sorted(ws["packs"].keys())}

    health = evaluate_workspace_health(ws, as_of=as_of)
    pack = ws["packs"][pack_id]
    hydrated_stack: dict[str, list[dict[str, Any]]] = {}
    excluded_stale: list[dict[str, Any]] = []

    for role, refs in pack.get("stack", {}).items():
        resolved = []
        for ref in refs:
            ent = ws["entities"][ref]
            f = health["entities"][ref]
            if not include_stale and not f["eligible_for_agents"]:
                excluded_stale.append({"id": ref, "role": role, "status": f["status"], "age_days": f["age_days"]})
                continue
            resolved.append({
                "id": ref,
                "name": ent["name"],
                "kind": ent["kind"],
                "lifecycle": ent["lifecycle"],
                "freshness": f,
                "urls": ent.get("urls", {}),
                "launch_recipe": ent.get("launch_recipe"),
                "gotchas": ent.get("gotchas", []),
            })
        hydrated_stack[role] = resolved

    return {
        "pack_id": pack_id,
        "title": pack["title"],
        "category": pack["category"],
        "verdict": pack["verdict"],
        "freshness": health["packs"][pack_id],
        "stack": hydrated_stack,
        "excluded_stale": excluded_stale,
        "workflow_steps": pack.get("workflow_steps", []),
        "gotchas": pack.get("gotchas", []),
    }


def forage_cloud(
    ws: dict[str, Any],
    intent: str,
    as_of: date | None = None,
    include_stale: bool = False,
) -> dict[str, Any]:
    routes = ws["forage_routes"]
    if intent not in routes:
        return {"error": f"Unknown cloud intent '{intent}'", "available_intents": sorted(routes.keys())}

    health = evaluate_workspace_health(ws, as_of=as_of)
    skipped = []
    selected = None
    reason = ""

    for eid in routes[intent]["chain"]:
        ent = ws["entities"][eid]
        f = health["entities"][eid]
        if not include_stale and not f["eligible_for_agents"]:
            skipped.append({"id": eid, "reason": f"freshness:{f['status']}", "age_days": f["age_days"]})
            continue

        tier = ent.get("tier")
        env_key = ent.get("env_key")
        if tier == "tier2-cloud-free" and env_key and os.environ.get(env_key):
            selected, reason = ent, f"active_env:{env_key}"
            break
        elif tier == "tier1-local":
            try:
                if requests.get(f"{ent['base_url']}/models", timeout=1.0).status_code == 200:
                    selected, reason = ent, "local_runtime_online"
                    break
            except Exception:
                skipped.append({"id": eid, "reason": "local_server_offline"})
        elif tier == "tier0-keyless":
            selected, reason = ent, "keyless_fallback"
            break

    if not selected:
        for eid in routes[intent]["chain"]:
            if include_stale or health["entities"][eid]["eligible_for_agents"]:
                selected = ws["entities"][eid]
                reason = f"default_primary_needs_env:{selected.get('env_key')}"
                break

    if not selected:
        return {"intent": intent, "selected": None, "error": "all_candidates_stale_or_unavailable", "skipped": skipped}

    return {
        "intent": intent,
        "selected_id": selected["id"],
        "provider": selected["name"],
        "reason": reason,
        "freshness": health["entities"][selected["id"]],
        "connection": {
            "base_url": selected.get("base_url"),
            "default_model": selected.get("default_model"),
            "env_key": selected.get("env_key"),
        },
        "skipped": skipped,
    }


def forage_local(
    ws: dict[str, Any],
    entity_id: str | None = None,
    lifecycle: str | None = None,
    as_of: date | None = None,
    include_stale: bool = False,
) -> dict[str, Any]:
    health = evaluate_workspace_health(ws, as_of=as_of)
    local_items = []
    for eid, ent in ws["entities"].items():
        if ent.get("kind") not in ("model", "adapter") or not ent.get("launch_recipe"):
            continue
        if lifecycle and ent.get("lifecycle") != lifecycle:
            continue
        f = health["entities"][eid]
        if not include_stale and not f["eligible_for_agents"]:
            continue
        local_items.append({
            "id": eid,
            "name": ent["name"],
            "lifecycle": ent["lifecycle"],
            "hardware": ent.get("hardware", {}),
            "freshness": f,
            "launch_recipe": ent["launch_recipe"],
            "gotchas": ent.get("gotchas", []),
        })

    if entity_id:
        match = next((x for x in local_items if x["id"] == entity_id), None)
        if not match:
            return {"error": f"Local profile '{entity_id}' not found or gated as stale", "available": [x["id"] for x in local_items]}
        return match
    return {"count": len(local_items), "profiles": local_items}


def build_snapshot(ws: dict[str, Any], as_of: date | None = None) -> dict[str, Any]:
    health = evaluate_workspace_health(ws, as_of=as_of)
    return {
        "schema_version": "3.0.0-modular",
        "as_of": health["as_of"],
        "counts": {
            "entities": len(ws["entities"]),
            "packs": len(ws["packs"]),
            "feeds": len(ws["feeds"]),
            "agent_eligible_entities": sum(1 for v in health["entities"].values() if v["eligible_for_agents"]),
        },
        "forage_routes": ws["forage_routes"],
        "entities": {
            eid: {**ent, "freshness": health["entities"][eid]}
            for eid, ent in ws["entities"].items()
        },
        "packs": {
            pid: resolve_pack(ws, pid, as_of=as_of, include_stale=True)
            for pid in sorted(ws["packs"].keys())
        },
        "feeds": {
            fid: {
                **feed,
                "items": [
                    {**item, "freshness": health["feeds"][fid][item["id"]]}
                    for item in feed.get("items", [])
                ],
            }
            for fid, feed in ws["feeds"].items()
        },
        "graveyard": ws["graveyard"],
        "digest": health["digest"],
    }
