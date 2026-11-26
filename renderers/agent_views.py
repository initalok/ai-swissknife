from __future__ import annotations

import json
import os
from typing import Any


def render(snapshot: dict[str, Any], root: str = ".") -> None:
    ents = snapshot["entities"]
    eligible = [e for e in ents.values() if e["freshness"]["eligible_for_agents"]]
    gated_out = [e for e in ents.values() if not e["freshness"]["eligible_for_agents"] and e["lifecycle"] != "monitor-only"]

    compact = [
        f"# AI Swiss Knife — Freshness-Gated Agent Router ({snapshot['schema_version']})",
        f"> Snapshot: {snapshot['as_of']} | Active Agent-Eligible Entities: {len(eligible)} | Stale/Degraded Auto-Excluded: {len(gated_out)}",
        "> Monitor-only frontier entries (book/08-frontier-watch.md) are intentionally excluded from routing.",
        "",
        "## Active Cloud Gateways (Fresh Only)",
    ]
    for e in eligible:
        if e["kind"] == "gateway":
            compact.append(
                f"- [{e['id']}] tier:{e.get('tier')} | env:{e.get('env_key')} | base_url:{e.get('base_url')} | model:{e.get('default_model')} | verified:{e['last_verified']}"
            )

    compact.append("\n## Active Local Launch Profiles (16GB VRAM + 64GB RAM)")
    for e in eligible:
        if e["kind"] in ("model", "adapter") and e.get("launch_recipe"):
            compact.append(f"- [{e['id']}] [{e['lifecycle']}] cmd: `{e['launch_recipe']}`")

    compact.append("\n## Active Cloud Forage Chains")
    for intent, route in snapshot.get("forage_routes", {}).items():
        fresh_chain = [cid for cid in route["chain"] if ents[cid]["freshness"]["eligible_for_agents"]]
        compact.append(f"- {intent}: {' -> '.join(fresh_chain) if fresh_chain else 'NONE_FRESH'}")

    compact.append("\n## Independent Use-Case Specialist Packs (`python scripts/cli.py query pack <id>`)")
    for pid, pack in snapshot["packs"].items():
        active_ids = [
            item["id"]
            for items in pack["stack"].values()
            for item in items
            if item["freshness"]["eligible_for_agents"]
        ]
        compact.append(f"- [{pid}] ({pack['freshness']['effective_status']}) -> book/packs/{pid}.md | active_stack: {', '.join(active_ids)}")

    with open(os.path.join(root, "llms.txt"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(compact) + "\n")

    full = [f"# AI Swiss Knife — Full Machine Index ({snapshot['as_of']})\n"]
    for e in ents.values():
        f = e["freshness"]
        gate = "ELIGIBLE" if f["eligible_for_agents"] else f"GATED:{f['status'].upper()}"
        full.append(f"- [{gate}] {e['id']} ({e['kind']}/{e['lifecycle']}) | {e['name']} | verified:{e['last_verified']} | gotchas: {' ; '.join(e.get('gotchas', []))}")
    with open(os.path.join(root, "llms-full.txt"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(full) + "\n")

    dist_dir = os.path.join(root, "dist")
    os.makedirs(dist_dir, exist_ok=True)
    with open(os.path.join(dist_dir, "registry.json"), "w", encoding="utf-8") as fp:
        json.dump(snapshot, fp, indent=2)
