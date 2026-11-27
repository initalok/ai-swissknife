from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class AgentRenderer:
    """Renders strictly freshness-gated machine manifests for autonomous agents."""

    def render(self, snapshot: dict[str, Any], root: Path) -> list[Path]:
        entries = snapshot["entries"]
        eligible = [e for e in entries.values() if e["freshness"]["eligible_for_agents"]]
        excluded = [e for e in entries.values() if not e["freshness"]["eligible_for_agents"] and e["lifecycle"] != "monitor-only"]

        compact = [
            f"# AI Swiss Knife — Agent Router (v{snapshot['schema_version']})",
            f"> Verified: {snapshot['as_of']} | Active entries: {len(eligible)} | Stale/degraded auto-excluded: {len(excluded)}",
            "> Monitor-only frontier entries (research/watch-list.md) are intentionally excluded.",
            "",
            "## Hardware Profiles (`swissknife resolve <target> --profile <id>`)",
        ]
        for pid, prof in snapshot["profiles"].items():
            compact.append(f"- [{pid}] {prof['name']}: {prof['summary']}")

        compact.append("\n## Active Zero-Card Cloud Gateways")
        for e in eligible:
            if e["kind"] == "gateway":
                env_k = e.get("env_key") or "KEYLESS"
                endpoint = e.get("base_url") or e["url"]
                model = e.get("default_model") or "—"
                compact.append(f"- [{e['id']}] env:{env_k} | base_url:{endpoint} | model:{model} | verified:{e['last_verified']}")

        compact.append("\n## Active Local Launch Profiles")
        for e in eligible:
            if e["kind"] in ("model", "adapter") and (e.get("launch_recipe") or e.get("mac_launch_recipe")):
                profs = ",".join(e.get("edges", {}).get("runs_on", []))
                if e.get("launch_recipe"):
                    compact.append(f"- [{e['id']}] ({e['lifecycle']}, {e['evidence_tier']}) profiles:{profs} | cuda/llama: `{e['launch_recipe']}`")
                if e.get("mac_launch_recipe"):
                    compact.append(f"- [{e['id']}:mac] ({e['lifecycle']}, {e['evidence_tier']}) profiles:mac-apple-silicon | mlx: `{e['mac_launch_recipe']}`")

        compact.append("\n## Guides & Specialist Directories")
        for gid in snapshot["guides"]:
            compact.append(f"- [guide:{gid}] guides/{gid}.md")
        for sid, spec in snapshot["specialists"].items():
            compact.append(f"- [specialist:{sid}] guides/specialist-domains.md | upstream: {spec['upstream_directory']['url']}")

        llms_path = root / "llms.txt"
        llms_path.write_text("\n".join(compact) + "\n", encoding="utf-8")

        full = [f"# AI Swiss Knife — Full Machine Index ({snapshot['as_of']})\n"]
        for e in entries.values():
            f = e["freshness"]
            gate = "ELIGIBLE" if f["eligible_for_agents"] else f"EXCLUDED:{f['effective_status'].upper()}"
            limits = " ; ".join(e.get("limitations", []))
            full.append(
                f"- [{gate}] [{e['evidence_tier']}] {e['id']} ({e['kind']}/{e['lifecycle']}) | {e['name']} | url:{e['url']} | verified:{e['last_verified']} | limits: {limits}"
            )
        llms_full_path = root / "llms-full.txt"
        llms_full_path.write_text("\n".join(full) + "\n", encoding="utf-8")

        snap_path = root / "dist" / "catalog.json"
        snap_path.parent.mkdir(parents=True, exist_ok=True)
        snap_path.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")

        return [llms_path, llms_full_path, snap_path]
