from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from swissknife.pages import BEGIN_RE, END_RE, FENCE_RE, _parse_kv_args

EVIDENCE_LABELS = {
    "primary-eval": "Primary evaluation",
    "official-docs": "Official documentation",
    "vendor-claim": "Vendor / lab claim",
    "field-note": "Field observation",
}


def _link(name: str, url: str | None) -> str:
    return f"[{name}]({url})" if url else name


def _rel_href(page_path: Path, root: Path, target_rel: str) -> str:
    return Path(os.path.relpath(root / target_rel, start=page_path.parent)).as_posix()


def _evidence(tier: str) -> str:
    return EVIDENCE_LABELS.get(tier, tier)


def _health_note(freshness: dict[str, Any]) -> str:
    st = freshness.get("effective_status") or freshness.get("status", "fresh")
    if st in ("fresh", "monitor-only"):
        return ""
    if st == "aging":
        return f" *(approaching review: {freshness['age_days']}d / {freshness['ttl_days']}d)*"
    if st == "stale":
        return " *(needs re-verification — excluded from agent routing)*"
    if st == "reverify-upstream":
        return " *(upstream dependency changed — re-verify)*"
    if st == "degraded":
        return " *(degraded — upstream archived or unreachable)*"
    return f" *({st})*"


def _alert_total(deltas: dict[str, list[Any]]) -> int:
    return sum(len(deltas.get(k, [])) for k in ("stale", "reverify_upstream", "degraded"))


def _details(summary: str, code: str, lang: str = "bash") -> list[str]:
    return [
        "<details>",
        f"<summary>{summary}</summary>",
        "",
        f"```{lang}",
        code.rstrip(),
        "```",
        "",
        "</details>",
    ]


def _render_status_banner(snap: dict[str, Any], page_path: Path, root: Path) -> str:
    alerts = _alert_total(snap["deltas"])
    releases = len(snap["deltas"].get("release_updates", []))
    status_href = _rel_href(page_path, root, "STATUS.md")
    llms_href = _rel_href(page_path, root, "llms.txt")
    health_txt = "All tracked links healthy" if alerts == 0 else f"{alerts} item(s) flagged for review"
    rel_txt = f" · {releases} upstream release(s) queued" if releases else ""
    return f"*Last verified: {snap['as_of']} · {health_txt}{rel_txt} ([System Status]({status_href})) · [For AI Agents (`llms.txt`)]({llms_href})*"


def _render_non_goals(snap: dict[str, Any]) -> str:
    return "\n".join(f"- {item}" for item in snap["taxonomy"].get("non_goals", []))


def _render_worlds_index(snap: dict[str, Any], page_path: Path, root: Path) -> str:
    worlds = snap["taxonomy"].get("worlds", {})
    pages_by_world = {p["world"]: p for p in snap.get("pages", []) if p.get("world")}
    lines = [
        "| Compute World | What Its Physics Excels At | Guide |",
        "| :--- | :--- | :--- |",
    ]
    for wid, w in sorted(worlds.items(), key=lambda kv: kv[1].get("order", 99)):
        page = pages_by_world.get(wid)
        guide_link = _link(page["title"], _rel_href(page_path, root, page["path"])) if page else "—"
        lines.append(f"| **{w['name']}** | {w['summary']} | {guide_link} |")
    return "\n".join(lines)


def _render_nav(args: dict[str, str], snap: dict[str, Any], page_path: Path, root: Path) -> str:
    section = args.get("section")
    track = args.get("track")
    pages = [
        p for p in snap.get("pages", [])
        if p["path"] != "README.md"
        and (not section or p.get("section") == section)
        and (not track or p.get("track") == track)
    ]
    pages.sort(key=lambda p: (p.get("order", 99), p["title"]))
    if not pages:
        return "*No pages registered in this section yet.*"
    return "\n".join(
        f"- **{_link(p['title'], _rel_href(page_path, root, p['path']))}** — {p['summary']}"
        for p in pages
    )


def _render_slot(args: dict[str, str], snap: dict[str, Any], page_path: Path, root: Path) -> str:
    slot = snap["slots"][args["id"]]
    active = slot.get("active")
    primary = slot.get("configured_primary")
    lines: list[str] = []

    if slot.get("fallback_used") and primary and active:
        lines.append(
            f"> [!WARNING]\n> Primary anchor **{primary['name']}** is currently `{primary['freshness']['effective_status']}`; automatically failing over to **{active['name']}**."
        )
        lines.append("")

    target = active or primary
    if not target:
        return f"*No active entry available for slot `{slot['slot_id']}`.*"

    note = _health_note(target["freshness"])
    lines.append(f"**Active Anchor — {_link(target['name'], target['url'])}**{note}")
    lines.append("")
    lines.append(target["summary"])
    lines.append("")
    lines.append(f"- **When to use:** {target['when_to_use']}")
    meta = target.get("meta", {})
    if meta.get("quota"):
        lines.append(f"- **Free quota:** {meta['quota']}")
    if meta.get("footprint"):
        lines.append(f"- **Footprint:** {meta['footprint']}")
    if meta.get("upstream_docs_url"):
        lines.append(f"- **Upstream docs:** {_link('Official setup & reference', meta['upstream_docs_url'])}")
    lines.append(f"- **Evidence:** {_evidence(target['evidence_tier'])} · verified {target['last_verified']}")
    if slot.get("discovered_adapters"):
        adapters = ", ".join(_link(a["name"], a["url"]) for a in slot["discovered_adapters"])
        lines.append(f"- **Compatible adapters:** {adapters}")
    if slot.get("experimental"):
        exp = slot["experimental"]
        lines.append(f"- **Experimental challenger:** {_link(exp['name'], exp['url'])} — {exp['when_to_use']}")
    if slot.get("decision"):
        dec = slot["decision"]
        why_href = _rel_href(page_path, root, "docs/why-this-stack.md")
        lines.append(f"- **Why this pick:** [{dec['title']}]({why_href}#{dec['id']})")
    for lim in target.get("limitations", []):
        lines.append(f"- **Limitation:** {lim}")
    return "\n".join(lines)


def _render_recipe(args: dict[str, str], snap: dict[str, Any]) -> str:
    entry = snap["entries"][args["id"]]
    meta = entry.get("meta", {})
    blocks: list[str] = []
    if meta.get("launch_recipe"):
        blocks.extend(_details(f"Launch command — {entry['name']} (CUDA / llama.cpp / CLI)", meta["launch_recipe"], "bash"))
        blocks.append("")
    if meta.get("mac_launch_recipe"):
        blocks.extend(_details(f"Launch command — {entry['name']} (Apple Silicon / MLX)", meta["mac_launch_recipe"], "bash"))
        blocks.append("")
    if meta.get("config_snippet"):
        title = meta.get("config_title") or f"Configuration snippet — {entry['name']}"
        lang = meta.get("config_lang") or "json"
        blocks.extend(_details(title, meta["config_snippet"], lang))
        blocks.append("")
    if meta.get("sanity_check"):
        blocks.append(f"Built-in upstream check: `{meta['sanity_check']}`")
    return "\n".join(blocks).strip() or f"*No launch recipe defined for `{entry['id']}`.*"


def _render_eval_tables(args: dict[str, str], snap: dict[str, Any]) -> str:
    entry = snap["entries"][args["id"]]
    tables = entry.get("meta", {}).get("eval_tables", [])
    if not tables:
        return f"*No evaluation tables recorded for `{entry['id']}`.*"
    lines: list[str] = []
    for tbl in tables:
        hdrs = tbl["headers"]
        lines.extend([
            f"**{tbl['title']}**",
            "",
            "| " + " | ".join(hdrs) + " |",
            "| " + " | ".join(":---" for _ in hdrs) + " |",
        ])
        for row in tbl["rows"]:
            lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
        lines.append("")
    return "\n".join(lines).strip()


def _render_table(args: dict[str, str], snap: dict[str, Any]) -> str:
    world = args.get("world")
    kind = args.get("kind")
    tag = args.get("tag")
    capability = args.get("capability")
    lifecycle = args.get("lifecycle")

    rows: list[dict[str, Any]] = []
    for entry in snap["entries"].values():
        if world and world not in entry.get("relations", {}).get("runs_on", []):
            continue
        if kind and entry["kind"] != kind:
            continue
        if tag and tag not in entry.get("tags", []):
            continue
        if capability and capability not in entry.get("capabilities", []):
            continue
        if lifecycle and entry["lifecycle"] != lifecycle:
            continue
        rows.append(entry)

    if not rows:
        return "*No matching entries currently registered.*"

    lines = [
        "| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for e in rows:
        meta = e.get("meta", {})
        spec = meta.get("quota") or meta.get("footprint") or meta.get("role") or meta.get("license") or e["kind"]
        lim = e["limitations"][0] if e.get("limitations") else "—"
        lines.append(
            f"| {_link(e['name'], e['url'])}{_health_note(e['freshness'])} | {e['when_to_use']} | {spec} | {_evidence(e['evidence_tier'])} | {lim} |"
        )
    return "\n".join(lines)


def _format_decision(dec: dict[str, Any], snap: dict[str, Any]) -> list[str]:
    anchors = ", ".join(
        _link(snap["entries"][aid]["name"], snap["entries"][aid]["url"])
        for aid in dec.get("anchor_ids", [])
        if aid in snap["entries"]
    ) or "—"
    alts = ", ".join(dec.get("alternatives", [])) or "—"
    review_flag = " *(review flagged — see Status)*" if dec.get("needs_review") else ""
    status_label = dec["status"].title()
    if dec["status"] == "superseded" and dec.get("superseded_by"):
        status_label = f"Superseded by `{dec['superseded_by']}`"

    lines = [
        f"<a id=\"{dec['id']}\"></a>",
        f"### {dec['title']} (`{status_label}`){review_flag}",
        "",
        f"- **The job:** {dec['job']}",
        f"- **Current anchor:** {anchors}",
        f"- **Alternatives evaluated:** {alts}",
        f"- **Why this leads today:** {dec['rationale']}",
    ]
    for exc in dec.get("exceptions", []):
        lines.append(f"- **When to choose an alternative:** {exc}")
    lines.append(f"- **Reversal trigger:** {dec['reversal_trigger']}")
    lines.append(f"- *Recorded {dec['date']}*")
    return lines


def _render_decision(args: dict[str, str], snap: dict[str, Any]) -> str:
    return "\n".join(_format_decision(snap["decisions"][args["id"]], snap))


def _render_decisions_index(snap: dict[str, Any]) -> str:
    active = [d for d in snap["decisions"].values() if d["status"] == "accepted"]
    historical = [d for d in snap["decisions"].values() if d["status"] != "accepted"]
    lines: list[str] = []
    for dec in active:
        lines.extend(_format_decision(dec, snap))
        lines.append("")
    if historical:
        lines.extend(["## Historical & Superseded Decisions", ""])
        for dec in historical:
            lines.extend(_format_decision(dec, snap))
            lines.append("")
    return "\n".join(lines).strip()


def _format_specialist(sp: dict[str, Any]) -> list[str]:
    res = sp.get("resolved", {})
    hub = sp["upstream_hub"]
    pushed = hub.get("freshness", {}).get("upstream_pushed_at")
    pushed_txt = f" *(upstream updated {pushed[:10]})*" if pushed else ""

    models = ", ".join(_link(m["name"], m["url"]) for m in res.get("models_and_gateways", [])) or "See Local Models Reference"
    adapters = ", ".join(_link(a["name"], a["url"]) for a in res.get("adapters", []))
    guards = ", ".join(_link(g["name"], g["url"]) for g in res.get("guards", []))

    lines = [
        f"### {sp['title']}",
        "",
        sp["summary"],
        "",
        f"- **Recommended base stack:** {models}",
    ]
    if adapters:
        lines.append(f"- **Compatible adapters:** {adapters}")
    if guards:
        lines.append(f"- **Mandatory safety layer:** {guards}")
    lines.append("- **Direct starting tools (max 2):**")
    for pick in sp.get("direct_picks", []):
        desc = f" — {pick['summary']}" if pick.get("summary") else ""
        lines.append(f"  - **{_link(pick['name'], pick['url'])}**{_health_note(pick['freshness'])}{desc}")
    lines.append(f"- **Monitored upstream directory:** **{_link(hub['name'], hub['url'])}**{_health_note(hub['freshness'])}{pushed_txt}")
    for g in sp.get("guardrails", []):
        lines.append(f"- **Guardrail:** {g}")
    return lines


def _render_specialist(args: dict[str, str], snap: dict[str, Any]) -> str:
    return "\n".join(_format_specialist(snap["specialists"][args["id"]]))


def _render_specialists_index(snap: dict[str, Any]) -> str:
    lines: list[str] = []
    for sp in snap["specialists"].values():
        lines.extend(_format_specialist(sp))
        lines.append("")
    return "\n".join(lines).strip()


def _render_watch(snap: dict[str, Any]) -> str:
    lines = ["## Frontier Ceiling (Monitor-Only)", ""]
    frontier = snap["watch"].get("frontier", [])
    if not frontier:
        lines.append("*No active frontier watch entries within the 21-day window.*\n")
    for w in frontier:
        f = w["freshness"]
        left = max(0, f["ttl_days"] - f["age_days"])
        lines.append(f"### {_link(w['name'], w['url'])}")
        lines.append("")
        lines.append(w["summary"])
        lines.append("")
        lines.append(f"- **Evidence:** {_evidence(w['evidence_tier'])} · **Window:** {left} days remaining")
        for lim in w.get("limitations", []):
            lines.append(f"- **Boundary:** {lim}")
        lines.append("")

    lines.extend(["## Community Field Observations", ""])
    community = snap["watch"].get("community", [])
    if not community:
        lines.append("*No active community field notes within the 21-day window.*\n")
    for w in community:
        f = w["freshness"]
        left = max(0, f["ttl_days"] - f["age_days"])
        lines.append(f"### {_link(w['name'], w['url'])}{_health_note(f)}")
        lines.append("")
        lines.append(w["summary"])
        lines.append("")
        lines.append(f"- **Evidence:** {_evidence(w['evidence_tier'])} · **Window:** {left} days remaining")
        for lim in w.get("limitations", []):
            lines.append(f"- **Boundary:** {lim}")
        lines.append("")
    return "\n".join(lines).strip()


def _render_retired(snap: dict[str, Any]) -> str:
    entries = snap["entries"]
    lines = [
        "| Area | Retired / Disqualified Item | Date | Why Cut | Active Alternative |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for r in snap.get("retired", []):
        rep_id = r.get("replaced_by")
        rep = _link(entries[rep_id]["name"], entries[rep_id]["url"]) if rep_id and rep_id in entries else "—"
        lines.append(f"| {r['area']} | {r['name']} | {r['retired_on'] or '—'} | {r['reason']} | {rep} |")
    return "\n".join(lines)


def _render_directive(directive: str, args: dict[str, str], snap: dict[str, Any], page_path: Path, root: Path) -> str:
    if directive == "status-banner":
        return _render_status_banner(snap, page_path, root)
    if directive == "non-goals":
        return _render_non_goals(snap)
    if directive == "worlds-index":
        return _render_worlds_index(snap, page_path, root)
    if directive == "nav":
        return _render_nav(args, snap, page_path, root)
    if directive == "slot":
        return _render_slot(args, snap, page_path, root)
    if directive == "recipe":
        return _render_recipe(args, snap)
    if directive == "eval-tables":
        return _render_eval_tables(args, snap)
    if directive == "table":
        return _render_table(args, snap)
    if directive == "decision":
        return _render_decision(args, snap)
    if directive == "decisions-index":
        return _render_decisions_index(snap)
    if directive == "specialist":
        return _render_specialist(args, snap)
    if directive == "specialists-index":
        return _render_specialists_index(snap)
    if directive == "watch":
        return _render_watch(snap)
    if directive == "retired":
        return _render_retired(snap)
    raise ValueError(f"Unsupported directive: {directive}")


class ManagedBlockSyncer:
    """Updates ONLY fenced <!-- swissknife:begin ... --> regions in-place; human prose stays untouched."""

    def sync(self, snapshot: dict[str, Any], root: Path) -> list[Path]:
        updated: list[Path] = []
        for page in snapshot.get("pages", []):
            if not page.get("blocks"):
                continue
            page_path = root / page["path"]
            original = page_path.read_text(encoding="utf-8")
            out_lines: list[str] = []
            in_fence = False
            skipping = False

            for line in original.splitlines():
                if not skipping and FENCE_RE.match(line):
                    in_fence = not in_fence
                    out_lines.append(line)
                    continue
                if in_fence:
                    out_lines.append(line)
                    continue

                if not skipping:
                    m_begin = BEGIN_RE.match(line)
                    if m_begin:
                        directive, raw_args = m_begin.group(1), m_begin.group(2)
                        kv, _ = _parse_kv_args(raw_args, page["path"])
                        rendered = _render_directive(directive, kv, snapshot, page_path, root)
                        out_lines.append(line)
                        if rendered:
                            out_lines.append(rendered)
                        skipping = True
                        continue
                    out_lines.append(line)
                else:
                    if END_RE.match(line):
                        out_lines.append(line)
                        skipping = False

            new_text = "\n".join(out_lines).rstrip() + "\n"
            if new_text != original:
                page_path.write_text(new_text, encoding="utf-8")
                updated.append(page_path)
        return updated
