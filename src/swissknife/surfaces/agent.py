from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _link(name: str, url: str | None) -> str:
    return f"[{name}]({url})" if url else name


class StatusAndAgentSurface:
    """Generates STATUS.md, freshness-gated llms*.txt, dist/catalog.json, and health/deltas.json."""

    def sync(self, snapshot: dict[str, Any], root: Path) -> list[Path]:
        written: list[Path] = []
        written.append(self._write_status(snapshot, root))
        written.extend(self._write_agent_manifests(snapshot, root))
        written.extend(self._write_json_artifacts(snapshot, root))
        return written

    def _write_status(self, snap: dict[str, Any], root: Path) -> Path:
        c = snap["counts"]
        d = snap["deltas"]
        lines = [
            "[Home](README.md) / System Status",
            "",
            "# System Status & Upstream Momentum Ledger",
            "",
            f"Snapshot date: **{snap['as_of']}** · Tracked entries: **{c['entries']}** ({c['agent_eligible']} eligible for `llms.txt`) · Workflow slots: **{c['slots']}** · Active decisions: **{c['decisions']}**.",
            "",
            "This ledger is maintained automatically by the rolling link and upstream release verifier. Healthy handbook pages stay quiet; release updates, stale links, and flagged decisions collect here.",
            "",
            "## Health & Momentum Summary",
            "",
            "| Signal | Count | Meaning |",
            "| :--- | :---: | :--- |",
            f"| Upstream release updates | {len(d['release_updates'])} | Tracked anchor shipped a newer GitHub release than last reviewed. |",
            f"| Decision records to review | {len(d['decision_reviews'])} | An accepted ADR's anchor degraded, went stale, or had a breaking release. |",
            f"| Upstream dependency alerts | {len(d['reverify_upstream'])} | A base model or harness adapted by a LoRA has changed or degraded. |",
            f"| Needs re-verification | {len(d['stale'])} | Past review window; automatically omitted from `llms.txt`. |",
            f"| Approaching review window | {len(d['aging'])} | Past 75% of scheduled review interval; still active. |",
            f"| Degraded / retirement queue | {len(d['degraded'])} | Upstream archived or unreachable for 3+ checks. |",
            "",
        ]

        if d["release_updates"]:
            lines.extend([
                "## Queued Upstream Release Updates",
                "",
                "| Anchor | Last Reviewed | Latest Upstream | Breaking Keyword? |",
                "| :--- | :--- | :--- | :---: |",
            ])
            for rel in d["release_updates"]:
                flag = "Yes" if rel["breaking_signal"] else "No"
                lines.append(
                    f"| {_link(rel['name'], rel['url'])} | `{rel['reviewed_release']}` | `{rel['latest_release']}` | {flag} |"
                )
            lines.append("")

        if d["decision_reviews"]:
            lines.extend(["## Decision Records Flagged for Review", ""])
            for dr in d["decision_reviews"]:
                lines.append(f"- **[{dr['title']}](docs/why-this-stack.md#{dr['decision_id']})** — Reversal trigger: *{dr['reversal_trigger']}*")
            lines.append("")

        lines.extend([
            "## Core Registry Entries",
            "",
            "| Entry | Kind | Status | Verified | Window | Upstream Activity / Release |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ])
        for entry in snap["entries"].values():
            f = entry["freshness"]
            pushed = f.get("upstream_pushed_at")
            rel_tag = f.get("latest_release_tag")
            activity = f"`{rel_tag}`" if rel_tag else (pushed[:10] if pushed else "Not yet probed")
            lines.append(
                f"| {_link(entry['name'], entry['url'])} | `{entry['kind']}` | `{f['effective_status']}` | {entry['last_verified']} | {f['ttl_days']}d | {activity} |"
            )

        if snap.get("external_links"):
            lines.extend([
                "",
                "## Specialist Tools & Upstream Directories",
                "",
                "| Resource | Scope | Status | Verified | Upstream Activity |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ])
            for ext in snap["external_links"]:
                ef = ext["freshness"]
                pushed = ef.get("upstream_pushed_at")
                pushed_str = pushed[:10] if pushed else "Not yet probed"
                lines.append(
                    f"| {_link(ext['name'], ext['url'])} | `{ext['scope']}` | `{ef['effective_status']}` | {ext['last_verified']} | {pushed_str} |"
                )

        path = root / "STATUS.md"
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return path

    def _write_agent_manifests(self, snap: dict[str, Any], root: Path) -> list[Path]:
        entries = snap["entries"]
        eligible = [e for e in entries.values() if e["freshness"]["eligible_for_agents"]]
        excluded = [e for e in entries.values() if not e["freshness"]["eligible_for_agents"] and e["lifecycle"] != "monitor-only"]

        compact = [
            f"# AI Swiss Knife — Freshness-Gated Agent Router (v{snap['schema_version']})",
            f"> Verified: {snap['as_of']} | Active entries: {len(eligible)} | Stale/degraded auto-excluded: {len(excluded)}",
            "> Monitor-only frontier entries (research/watch-list.md) are intentionally excluded.",
            "",
            "## Compute Worlds (`swissknife query --world <id>`)",
        ]
        for wid, w in sorted(snap["taxonomy"].get("worlds", {}).items(), key=lambda kv: kv[1].get("order", 99)):
            compact.append(f"- [{wid}] {w['name']}: {w['summary']}")

        compact.append("\n## Active Workflow Slots (`swissknife slot <id>`)")
        for sid, sl in snap["slots"].items():
            act = sl.get("active")
            if not act:
                continue
            fb_tag = " [FAILOVER]" if sl.get("fallback_used") else ""
            compact.append(f"- [{sid}]{fb_tag} -> {act['id']} ({act['name']}) | {act['url']}")

        compact.append("\n## Active Zero-Card Cloud Gateways")
        for e in eligible:
            if e["kind"] == "gateway":
                m = e.get("meta", {})
                compact.append(
                    f"- [{e['id']}] env:{m.get('env_key') or 'KEYLESS'} | base_url:{m.get('base_url') or e['url']} | model:{m.get('default_model') or '—'} | verified:{e['last_verified']}"
                )

        compact.append("\n## Active Local Launch Recipes")
        for e in eligible:
            m = e.get("meta", {})
            if e["kind"] in ("model", "adapter") and (m.get("launch_recipe") or m.get("mac_launch_recipe")):
                worlds = ",".join(e.get("relations", {}).get("runs_on", []))
                if m.get("launch_recipe"):
                    compact.append(f"- [{e['id']}] ({e['lifecycle']}, {e['evidence_tier']}) worlds:{worlds} | cmd: `{m['launch_recipe']}`")
                if m.get("mac_launch_recipe"):
                    compact.append(f"- [{e['id']}:mac] ({e['lifecycle']}, {e['evidence_tier']}) worlds:mac | mlx: `{m['mac_launch_recipe']}`")

        compact.append("\n## Handbook Pages")
        for p in sorted(snap.get("pages", []), key=lambda x: (x.get("section") or "", x.get("order", 99), x["path"])):
            if p["path"] == "README.md":
                continue
            compact.append(f"- [{p['path']}] {p['title']}: {p['summary']}")

        llms_path = root / "llms.txt"
        llms_path.write_text("\n".join(compact).rstrip() + "\n", encoding="utf-8")

        full = [f"# AI Swiss Knife — Full Machine Index ({snap['as_of']})\n"]
        for e in entries.values():
            f = e["freshness"]
            gate = "ELIGIBLE" if f["eligible_for_agents"] else f"EXCLUDED:{f['effective_status'].upper()}"
            limits = " ; ".join(e.get("limitations", []))
            full.append(
                f"- [{gate}] [{e['evidence_tier']}] {e['id']} ({e['kind']}/{e['lifecycle']}) | {e['name']} | url:{e['url']} | verified:{e['last_verified']} | limits: {limits}"
            )
        llms_full_path = root / "llms-full.txt"
        llms_full_path.write_text("\n".join(full).rstrip() + "\n", encoding="utf-8")

        return [llms_path, llms_full_path]

    def _write_json_artifacts(self, snap: dict[str, Any], root: Path) -> list[Path]:
        cat_path = root / "dist" / "catalog.json"
        cat_path.parent.mkdir(parents=True, exist_ok=True)
        cat_path.write_text(json.dumps(snap, indent=2) + "\n", encoding="utf-8")

        deltas_path = root / "health" / "deltas.json"
        deltas_path.parent.mkdir(parents=True, exist_ok=True)
        deltas_path.write_text(json.dumps({"as_of": snap["as_of"], "deltas": snap["deltas"]}, indent=2) + "\n", encoding="utf-8")

        return [cat_path, deltas_path]
