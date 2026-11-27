from __future__ import annotations

import json
import os
from typing import Any


def render(snapshot: dict[str, Any], root: str = ".") -> None:
    nodes = snapshot["nodes"]
    eligible = [n for n in nodes.values() if n["freshness"]["eligible_for_agents"]]
    gated = [n for n in nodes.values() if not n["freshness"]["eligible_for_agents"] and n["lifecycle"] != "monitor-only"]

    compact = [
        f"# AI Swiss Knife — Freshness-Gated Agent Router (v{snapshot['schema_version']})",
        f"> Snapshot: {snapshot['as_of']} | Active Agent-Eligible Nodes: {len(eligible)} | Stale/Degraded Auto-Excluded: {len(gated)}",
        "> Monitor-only Frontier Watch entries (book/radar.md) are excluded from routing.",
        "",
        "## Hardware Profiles (`python scripts/cli.py resolve <horizon> --profile <id>`)",
    ]
    for pid, prof in snapshot["profiles"].items():
        compact.append(f"- [{pid}] {prof['name']}: {prof['summary']}")

    compact.append("\n## Active Zero-Card Cloud Gateways (Fresh Only)")
    for n in eligible:
        if n["kind"] == "gateway":
            env_k = n.get("env_key") or "KEYLESS"
            endpoint = n.get("base_url") or n["url"]
            d_model = n.get("default_model", "—")
            compact.append(
                f"- [{n['id']}] env:{env_k} | base_url:{endpoint} | model:{d_model} | verified:{n['last_verified']}"
            )

    compact.append("\n## Active Local Launch Profiles (Fresh Only)")
    for n in eligible:
        if n["kind"] in ("model", "adapter") and n.get("launch_recipe"):
            profs = ",".join(n.get("edges", {}).get("runs_on", []))
            compact.append(f"- [{n['id']}] [{n['lifecycle']}] profiles:{profs} | cmd: `{n['launch_recipe']}`")

    compact.append("\n## Core Playbooks & Upstreamed Spokes")
    for pid, pb in snapshot["playbooks"].items():
        tools = ", ".join(t["id"] for t in pb.get("domain_tools", []))
        compact.append(f"- [playbook:{pid}] book/playbooks.md | tools: {tools}")
    for sid, sp in snapshot["spokes"].items():
        hub = sp["upstream_hub"]
        compact.append(f"- [spoke:{sid}] book/spokes.md | upstream: {hub['url']}")

    with open(os.path.join(root, "llms.txt"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(compact) + "\n")

    full = [f"# AI Swiss Knife — Full Machine Index ({snapshot['as_of']})\n"]
    for n in nodes.values():
        f = n["freshness"]
        tag = "ELIGIBLE" if f["eligible_for_agents"] else f"GATED:{f['effective_status'].upper()}"
        gotchas_s = " ; ".join(n.get("gotchas", []))
        full.append(
            f"- [{tag}] {n['id']} ({n['kind']}/{n['lifecycle']}) | {n['name']} | url:{n['url']} | verified:{n['last_verified']} | gotchas: {gotchas_s}"
        )
    with open(os.path.join(root, "llms-full.txt"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(full) + "\n")

    dist_dir = os.path.join(root, "dist")
    os.makedirs(dist_dir, exist_ok=True)
    with open(os.path.join(dist_dir, "graph.json"), "w", encoding="utf-8") as fp:
        json.dump(snapshot, fp, indent=2)
