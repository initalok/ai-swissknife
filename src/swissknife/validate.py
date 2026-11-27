from __future__ import annotations

import json
import re
from datetime import date
from typing import Any

from swissknife.models import (
    Catalog,
    VALID_DECAY_CLASSES,
    VALID_EVIDENCE_TIERS,
    VALID_KINDS,
    VALID_LIFECYCLES,
    to_dict,
)

PRESENTATION_LEAK_RE = re.compile(r"(<br\s*/?>|</?sub>|</?kbd>|<details>|```)", re.IGNORECASE)

FORBIDDEN_URL_PATTERNS = (
    re.compile(r"github\.com/topics/", re.IGNORECASE),
    re.compile(r"github\.com/search\b", re.IGNORECASE),
    re.compile(r"huggingface\.co/(models|datasets|spaces)/?$", re.IGNORECASE),
    re.compile(r"reddit\.com/r/[^/]+/?$", re.IGNORECASE),
)

RESERVED_GUIDE_IDS = {"local-ai-workstation", "specialist-domains"}

BUDGETS = {
    "max_watch_frontier": 5,
    "max_watch_community": 5,
    "max_specialist_direct_picks": 2,
}


def _check_iso_date(val: str, owner: str) -> list[str]:
    try:
        date.fromisoformat(val)
        return []
    except ValueError:
        return [f"[{owner}] invalid ISO date '{val}'"]


def _check_canonical_url(url: str, owner: str) -> list[str]:
    if not url or not url.startswith(("https://", "http://")):
        return [f"[{owner}] missing or invalid canonical URL '{url}'"]
    for pat in FORBIDDEN_URL_PATTERNS:
        if pat.search(url):
            return [f"[{owner}] violates Canonical URL Law (placeholder URL): '{url}'"]
    return []


def _check_retired_patterns(searchable: str, retired_patterns: list[str], owner: str) -> list[str]:
    lower = searchable.lower()
    return [f"[{owner}] matches retired pattern '{pat}'" for pat in retired_patterns if pat in lower]


def _find_presentation_leaks(obj: Any, path: str) -> list[str]:
    leaks: list[str] = []
    if isinstance(obj, str):
        if PRESENTATION_LEAK_RE.search(obj):
            leaks.append(f"[{path}] contains HTML/Markdown presentation leak")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            leaks.extend(_find_presentation_leaks(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for idx, v in enumerate(obj):
            leaks.extend(_find_presentation_leaks(v, f"{path}[{idx}]"))
    return leaks


def validate_catalog(catalog: Catalog) -> list[str]:
    errors = list(catalog.load_errors)
    retired_patterns = [r.match_pattern.lower() for r in catalog.retired if r.match_pattern]

    for eid, entry in catalog.entries.items():
        owner = f"entry:{eid}"
        if entry.kind not in VALID_KINDS:
            errors.append(f"[{owner}] invalid kind '{entry.kind}'")
        if entry.lifecycle not in VALID_LIFECYCLES:
            errors.append(f"[{owner}] invalid lifecycle '{entry.lifecycle}'")
        if entry.decay_class not in VALID_DECAY_CLASSES:
            errors.append(f"[{owner}] invalid decay_class '{entry.decay_class}'")
        if entry.evidence_tier not in VALID_EVIDENCE_TIERS:
            errors.append(f"[{owner}] invalid evidence_tier '{entry.evidence_tier}'")
        if not entry.summary.strip() or not entry.when_to_use.strip():
            errors.append(f"[{owner}] requires plain-prose 'summary' and 'when_to_use'")
        if not entry.limitations:
            errors.append(f"[{owner}] must state at least one limitation / boundary condition")

        errors.extend(_check_iso_date(entry.last_verified, owner))
        errors.extend(_check_canonical_url(entry.url, owner))
        errors.extend(_find_presentation_leaks(to_dict(entry), owner))

        for pid in entry.edges.runs_on:
            if pid not in catalog.profiles:
                errors.append(f"[{owner}] edges.runs_on unknown profile '{pid}'")
        for target in entry.edges.adapts:
            if target not in catalog.entries:
                errors.append(f"[{owner}] edges.adapts unknown entry '{target}'")
        for target in entry.edges.guards:
            if target != "*" and target not in catalog.entries:
                errors.append(f"[{owner}] edges.guards unknown entry '{target}'")

        if entry.lifecycle not in ("monitor-only", "retired"):
            blob = json.dumps({"id": eid, "name": entry.name, "url": entry.url, "default_model": entry.default_model or ""})
            errors.extend(_check_retired_patterns(blob, retired_patterns, owner))

    for intent, chain in catalog.routing_chains.items():
        for ref in chain:
            if ref not in catalog.entries:
                errors.append(f"[routing:{intent}] references unknown entry '{ref}'")

    for gid, guide in catalog.guides.items():
        owner = f"guide:{gid}"
        if gid in RESERVED_GUIDE_IDS:
            errors.append(f"[{owner}] uses reserved built-in guide slug '{gid}'")
        if not guide.title.strip() or not guide.summary.strip() or not guide.steps:
            errors.append(f"[{owner}] requires title, summary, and numbered steps")
        errors.extend(_check_iso_date(guide.last_verified, owner))
        errors.extend(_find_presentation_leaks(to_dict(guide), owner))
        for ref in guide.pin_entries:
            if ref not in catalog.entries:
                errors.append(f"[{owner}] pin_entries references unknown entry '{ref}'")
        for tool in guide.tools:
            t_owner = f"{owner}:tool:{tool.id}"
            errors.extend(_check_canonical_url(tool.url, t_owner))
            errors.extend(_check_retired_patterns(f"{tool.id} {tool.name} {tool.url}", retired_patterns, t_owner))

    for sid, spec in catalog.specialists.items():
        owner = f"specialist:{sid}"
        if len(spec.direct_picks) > BUDGETS["max_specialist_direct_picks"]:
            errors.append(
                f"[{owner}] exceeds budget: {len(spec.direct_picks)} direct_picks > {BUDGETS['max_specialist_direct_picks']}"
            )
        errors.extend(_check_iso_date(spec.last_verified, owner))
        errors.extend(_find_presentation_leaks(to_dict(spec), owner))
        for pick in spec.direct_picks:
            p_owner = f"{owner}:pick:{pick.id}"
            errors.extend(_check_canonical_url(pick.url, p_owner))
            errors.extend(_check_retired_patterns(f"{pick.id} {pick.name} {pick.url}", retired_patterns, p_owner))
        u_owner = f"{owner}:upstream_directory"
        errors.extend(_check_canonical_url(spec.upstream_directory.url, u_owner))
        errors.extend(
            _check_retired_patterns(
                f"{spec.upstream_directory.id} {spec.upstream_directory.name} {spec.upstream_directory.url}",
                retired_patterns,
                u_owner,
            )
        )

    if len(catalog.watch_frontier) > BUDGETS["max_watch_frontier"]:
        errors.append(f"[watch:frontier] exceeds cap: {len(catalog.watch_frontier)} > {BUDGETS['max_watch_frontier']}")
    if len(catalog.watch_community) > BUDGETS["max_watch_community"]:
        errors.append(f"[watch:community] exceeds cap: {len(catalog.watch_community)} > {BUDGETS['max_watch_community']}")
    for item in (*catalog.watch_frontier, *catalog.watch_community):
        owner = f"watch:{item.bucket}:{item.id}"
        if item.evidence_tier not in VALID_EVIDENCE_TIERS:
            errors.append(f"[{owner}] invalid evidence_tier '{item.evidence_tier}'")
        errors.extend(_check_iso_date(item.last_verified, owner))
        errors.extend(_check_canonical_url(item.url, owner))
        errors.extend(_find_presentation_leaks(to_dict(item), owner))
        if item.bucket == "community":
            errors.extend(_check_retired_patterns(f"{item.id} {item.name} {item.url}", retired_patterns, owner))

    for r in catalog.retired:
        if r.replaced_by and r.replaced_by not in catalog.entries:
            errors.append(f"[retired:{r.name}] replaced_by '{r.replaced_by}' not found in entries")

    return errors
