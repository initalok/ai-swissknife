from __future__ import annotations

import json
import re
from datetime import date
from typing import Any

from swissknife.models import (
    VALID_DECAY_CLASSES,
    VALID_DECISION_STATUSES,
    VALID_EVIDENCE_TIERS,
    VALID_LIFECYCLES,
    Workspace,
    to_dict,
)

PRESENTATION_LEAK_RE = re.compile(r"(<br\s*/?>|</?sub>|</?kbd>|<details>|```)", re.IGNORECASE)

FORBIDDEN_URL_PATTERNS = (
    re.compile(r"github\.com/topics/", re.IGNORECASE),
    re.compile(r"github\.com/search\b", re.IGNORECASE),
    re.compile(r"huggingface\.co/(models|datasets|spaces)/?$", re.IGNORECASE),
    re.compile(r"reddit\.com/r/[^/]+/?$", re.IGNORECASE),
)

BUDGETS = {
    "max_watch_frontier": 5,
    "max_watch_community": 5,
    "max_specialist_direct_picks": 2,
}

VALID_DIRECTIVES = {
    "slot",
    "recipe",
    "eval-tables",
    "table",
    "decision",
    "decisions-index",
    "specialist",
    "specialists-index",
    "watch",
    "retired",
    "nav",
    "non-goals",
    "worlds-index",
    "status-banner",
}


def _check_date(val: str, owner: str) -> list[str]:
    try:
        date.fromisoformat(val)
        return []
    except ValueError:
        return [f"[{owner}] invalid ISO date '{val}'"]


def _check_url(url: str, owner: str) -> list[str]:
    if not url or not url.startswith(("https://", "http://")):
        return [f"[{owner}] missing or invalid canonical URL '{url}'"]
    for pat in FORBIDDEN_URL_PATTERNS:
        if pat.search(url):
            return [f"[{owner}] violates Canonical URL Law (placeholder URL): '{url}'"]
    return []


def _check_retired(blob: str, patterns: list[str], owner: str) -> list[str]:
    low = blob.lower()
    return [f"[{owner}] matches retired pattern '{p}'" for p in patterns if p in low]


def _check_leaks(obj: Any, path: str) -> list[str]:
    leaks: list[str] = []
    if isinstance(obj, str):
        if PRESENTATION_LEAK_RE.search(obj):
            leaks.append(f"[{path}] contains HTML/Markdown presentation leak")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            leaks.extend(_check_leaks(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for idx, v in enumerate(obj):
            leaks.extend(_check_leaks(v, f"{path}[{idx}]"))
    return leaks


def validate_workspace(ws: Workspace) -> list[str]:
    errors = list(ws.load_errors)
    allowed_kinds = set(ws.taxonomy.allowed_kinds)
    valid_worlds = set(ws.taxonomy.worlds.keys())
    retired_patterns = [r.match_pattern.lower() for r in ws.retired if r.match_pattern]

    for field_name, coll in (
        ("worlds", ws.taxonomy.worlds),
        ("tracks", ws.taxonomy.tracks),
        ("sections", ws.taxonomy.sections),
        ("non_goals", ws.taxonomy.non_goals),
    ):
        if not coll:
            errors.append(f"[taxonomy] required section '{field_name}' is empty")

    for eid, entry in ws.entries.items():
        owner = f"entry:{eid}"
        if entry.kind not in allowed_kinds:
            errors.append(f"[{owner}] kind '{entry.kind}' not in taxonomy.allowed_kinds")
        if entry.lifecycle not in VALID_LIFECYCLES:
            errors.append(f"[{owner}] invalid lifecycle '{entry.lifecycle}'")
        if entry.decay_class not in VALID_DECAY_CLASSES:
            errors.append(f"[{owner}] invalid decay_class '{entry.decay_class}'")
        if entry.evidence_tier not in VALID_EVIDENCE_TIERS:
            errors.append(f"[{owner}] invalid evidence_tier '{entry.evidence_tier}'")
        if not entry.summary.strip() or not entry.when_to_use.strip():
            errors.append(f"[{owner}] requires plain-prose 'summary' and 'when_to_use'")
        if not entry.limitations:
            errors.append(f"[{owner}] must declare at least one limitation")

        errors.extend(_check_date(entry.last_verified, owner))
        errors.extend(_check_url(entry.url, owner))
        errors.extend(_check_leaks(to_dict(entry), owner))

        for wid in entry.relations.runs_on:
            if wid not in valid_worlds:
                errors.append(f"[{owner}] relations.runs_on unknown world '{wid}'")
        for target in entry.relations.adapts:
            if target not in ws.entries:
                errors.append(f"[{owner}] relations.adapts unknown entry '{target}'")
        for target in entry.relations.guards:
            if target != "*" and target not in ws.entries:
                errors.append(f"[{owner}] relations.guards unknown entry '{target}'")

        if entry.lifecycle not in ("monitor-only", "retired"):
            blob = json.dumps({"id": eid, "name": entry.name, "url": entry.url, "default_model": entry.meta.get("default_model", "")})
            errors.extend(_check_retired(blob, retired_patterns, owner))

    for sid, slot in ws.slots.items():
        owner = f"slot:{sid}"
        if slot.primary not in ws.entries:
            errors.append(f"[{owner}] primary entry '{slot.primary}' not found")
        if slot.experimental and slot.experimental not in ws.entries:
            errors.append(f"[{owner}] experimental entry '{slot.experimental}' not found")
        for fb in slot.fallbacks:
            if fb not in ws.entries:
                errors.append(f"[{owner}] fallback entry '{fb}' not found")
        if slot.decision_id and slot.decision_id not in ws.decisions:
            errors.append(f"[{owner}] decision_id '{slot.decision_id}' not found")
        if slot.world and slot.world not in valid_worlds:
            errors.append(f"[{owner}] unknown world '{slot.world}'")

    for did, dec in ws.decisions.items():
        owner = f"decision:{did}"
        if dec.status not in VALID_DECISION_STATUSES:
            errors.append(f"[{owner}] invalid status '{dec.status}'")
        if not dec.rationale.strip() or not dec.reversal_trigger.strip():
            errors.append(f"[{owner}] requires both 'rationale' and falsifiable 'reversal_trigger'")
        errors.extend(_check_date(dec.date, owner))
        errors.extend(_check_leaks(to_dict(dec), owner))
        for aid in dec.anchor_ids:
            if dec.status == "accepted" and aid not in ws.entries:
                errors.append(f"[{owner}] accepted ADR references unknown anchor '{aid}'")
        for sid in dec.slot_ids:
            if sid not in ws.slots:
                errors.append(f"[{owner}] references unknown slot '{sid}'")
        if dec.status == "superseded" and (not dec.superseded_by or dec.superseded_by not in ws.decisions):
            errors.append(f"[{owner}] superseded ADR must point to valid 'superseded_by' decision")

    for spid, sp in ws.specialists.items():
        owner = f"specialist:{spid}"
        if len(sp.direct_picks) > BUDGETS["max_specialist_direct_picks"]:
            errors.append(f"[{owner}] exceeds budget: {len(sp.direct_picks)} direct_picks > {BUDGETS['max_specialist_direct_picks']}")
        errors.extend(_check_date(sp.last_verified, owner))
        errors.extend(_check_leaks(to_dict(sp), owner))
        for pick in sp.direct_picks:
            p_owner = f"{owner}:pick:{pick.id}"
            errors.extend(_check_url(pick.url, p_owner))
            errors.extend(_check_retired(f"{pick.id} {pick.name} {pick.url}", retired_patterns, p_owner))
        u_owner = f"{owner}:upstream_hub"
        errors.extend(_check_url(sp.upstream_hub.url, u_owner))
        errors.extend(_check_retired(f"{sp.upstream_hub.id} {sp.upstream_hub.name} {sp.upstream_hub.url}", retired_patterns, u_owner))

    if len(ws.watch_frontier) > BUDGETS["max_watch_frontier"]:
        errors.append(f"[watch:frontier] exceeds cap: {len(ws.watch_frontier)} > {BUDGETS['max_watch_frontier']}")
    if len(ws.watch_community) > BUDGETS["max_watch_community"]:
        errors.append(f"[watch:community] exceeds cap: {len(ws.watch_community)} > {BUDGETS['max_watch_community']}")
    for w in (*ws.watch_frontier, *ws.watch_community):
        owner = f"watch:{w.bucket}:{w.id}"
        if w.evidence_tier not in VALID_EVIDENCE_TIERS:
            errors.append(f"[{owner}] invalid evidence_tier '{w.evidence_tier}'")
        errors.extend(_check_date(w.last_verified, owner))
        errors.extend(_check_url(w.url, owner))
        errors.extend(_check_leaks(to_dict(w), owner))
        if w.bucket == "community":
            errors.extend(_check_retired(f"{w.id} {w.name} {w.url}", retired_patterns, owner))

    for r in ws.retired:
        if r.replaced_by:
            if r.replaced_by not in ws.entries:
                errors.append(f"[retired:{r.name}] replaced_by '{r.replaced_by}' not found in entries")
            elif ws.entries[r.replaced_by].lifecycle in ("retired", "deprecated"):
                errors.append(f"[retired:{r.name}] replaced_by '{r.replaced_by}' is itself {ws.entries[r.replaced_by].lifecycle}")

    for page in ws.pages:
        p_owner = f"page:{page.path}"
        if page.path != "README.md":
            if not page.section or page.section not in ws.taxonomy.sections:
                errors.append(f"[{p_owner}] invalid or missing frontmatter section '{page.section}'")
            if not page.summary.strip():
                errors.append(f"[{p_owner}] missing frontmatter 'summary'")
        if page.track and page.track not in ws.taxonomy.tracks:
            errors.append(f"[{p_owner}] unknown frontmatter track '{page.track}'")
        if page.world and page.world not in ws.taxonomy.worlds:
            errors.append(f"[{p_owner}] unknown frontmatter world '{page.world}'")

        for blk in page.blocks:
            b_owner = f"{p_owner}:{blk.line}:{blk.directive}"
            if blk.directive not in VALID_DIRECTIVES:
                errors.append(f"[{b_owner}] unknown managed-block directive '{blk.directive}'")
                continue
            if blk.directive == "slot" and blk.args.get("id") not in ws.slots:
                errors.append(f"[{b_owner}] unknown slot id '{blk.args.get('id')}'")
            elif blk.directive in ("recipe", "eval-tables") and blk.args.get("id") not in ws.entries:
                errors.append(f"[{b_owner}] unknown entry id '{blk.args.get('id')}'")
            elif blk.directive == "decision" and blk.args.get("id") not in ws.decisions:
                errors.append(f"[{b_owner}] unknown decision id '{blk.args.get('id')}'")
            elif blk.directive == "specialist" and blk.args.get("id") not in ws.specialists:
                errors.append(f"[{b_owner}] unknown specialist id '{blk.args.get('id')}'")
            elif blk.directive == "table":
                if blk.args.get("kind") and blk.args["kind"] not in allowed_kinds:
                    errors.append(f"[{b_owner}] unknown kind '{blk.args['kind']}'")
                if blk.args.get("world") and blk.args["world"] not in valid_worlds:
                    errors.append(f"[{b_owner}] unknown world '{blk.args['world']}'")
            elif blk.directive == "nav":
                if blk.args.get("section") and blk.args["section"] not in ws.taxonomy.sections:
                    errors.append(f"[{b_owner}] unknown section '{blk.args['section']}'")
                if blk.args.get("track") and blk.args["track"] not in ws.taxonomy.tracks:
                    errors.append(f"[{b_owner}] unknown track '{blk.args['track']}'")

    return errors
