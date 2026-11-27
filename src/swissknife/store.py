from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import yaml

from swissknife.models import (
    Catalog,
    Edges,
    Entry,
    ExternalLink,
    GuideSpec,
    HardwareProfile,
    RetiredItem,
    SpecialistSpec,
    WatchItem,
)


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fp:
        return yaml.safe_load(fp) or {}


def _parse_link(raw: dict[str, Any]) -> ExternalLink:
    return ExternalLink(
        id=str(raw.get("id", "")),
        name=str(raw.get("name", "")),
        url=str(raw.get("url", "")),
        summary=str(raw.get("summary", "")),
        evidence_tier=str(raw.get("evidence_tier", "official-docs")),
    )


def load_catalog(root: str | Path = ".") -> Catalog:
    root_path = Path(root)
    cdir = root_path / "catalog"
    errors: list[str] = []

    profiles_raw = _load_yaml(cdir / "profiles.yaml")
    profiles = {
        p["id"]: HardwareProfile(id=p["id"], name=p["name"], summary=p["summary"])
        for p in profiles_raw.get("profiles", [])
        if p.get("id")
    }

    models_cloud = _load_yaml(cdir / "models_and_cloud.yaml")
    harnesses_tools = _load_yaml(cdir / "harnesses_and_tools.yaml")

    entries: dict[str, Entry] = {}
    for rel, raw in (
        ("catalog/models_and_cloud.yaml", models_cloud),
        ("catalog/harnesses_and_tools.yaml", harnesses_tools),
    ):
        for item in raw.get("entries", []):
            eid = item.get("id")
            if not eid:
                errors.append(f"{rel}: entry missing 'id'")
                continue
            if eid in entries:
                errors.append(f"{rel}: duplicate entry id '{eid}'")
                continue
            e_raw = item.get("edges") or {}
            entries[eid] = Entry(
                id=eid,
                kind=str(item.get("kind", "")),
                category=str(item.get("category", "")),
                name=str(item.get("name", "")),
                summary=str(item.get("summary", "")),
                when_to_use=str(item.get("when_to_use", "")),
                limitations=list(item.get("limitations", [])),
                evidence_tier=str(item.get("evidence_tier", "")),
                lifecycle=str(item.get("lifecycle", "")),
                decay_class=str(item.get("decay_class", "")),
                last_verified=str(item.get("last_verified", "")),
                url=str(item.get("url", "")),
                capabilities=list(item.get("capabilities", [])),
                edges=Edges(
                    runs_on=list(e_raw.get("runs_on", [])),
                    adapts=list(e_raw.get("adapts", [])),
                    guards=list(e_raw.get("guards", [])),
                ),
                license=item.get("license"),
                footprint=item.get("footprint"),
                quota=item.get("quota"),
                env_key=item.get("env_key"),
                base_url=item.get("base_url"),
                default_model=item.get("default_model"),
                role=item.get("role"),
                evidence_notes=list(item.get("evidence_notes", [])),
                eval_tables=list(item.get("eval_tables", [])),
                launch_recipe=item.get("launch_recipe"),
                mac_launch_recipe=item.get("mac_launch_recipe"),
                source_file=rel,
            )

    guides_raw = _load_yaml(cdir / "guides.yaml")
    guides: dict[str, GuideSpec] = {}
    for g in guides_raw.get("guides", []):
        gid = g.get("id")
        if not gid:
            errors.append("catalog/guides.yaml: guide missing 'id'")
            continue
        c = g.get("constraints") or {}
        guides[gid] = GuideSpec(
            id=gid,
            title=str(g.get("title", "")),
            summary=str(g.get("summary", "")),
            last_verified=str(g.get("last_verified", "")),
            decay_class=str(g.get("decay_class", "operational")),
            capabilities=list(c.get("capabilities", [])),
            privacy=str(c.get("privacy", "any")),
            require_guard=bool(c.get("require_guard", False)),
            pin_entries=list(g.get("pin_entries", [])),
            tools=[_parse_link(t) for t in g.get("tools", [])],
            steps=list(g.get("steps", [])),
            limitations=list(g.get("limitations", [])),
        )

    spec_raw = _load_yaml(cdir / "specialists.yaml")
    specialists: dict[str, SpecialistSpec] = {}
    for s in spec_raw.get("specialists", []):
        sid = s.get("id")
        if not sid:
            errors.append("catalog/specialists.yaml: specialist missing 'id'")
            continue
        c = s.get("constraints") or {}
        specialists[sid] = SpecialistSpec(
            id=sid,
            title=str(s.get("title", "")),
            summary=str(s.get("summary", "")),
            last_verified=str(s.get("last_verified", "")),
            capabilities=list(c.get("capabilities", [])),
            privacy=str(c.get("privacy", "any")),
            require_guard=bool(c.get("require_guard", False)),
            direct_picks=[_parse_link(p) for p in s.get("direct_picks", [])],
            upstream_directory=_parse_link(s.get("upstream_directory") or {}),
            guardrails=list(s.get("guardrails", [])),
        )

    watch_raw = _load_yaml(cdir / "watch.yaml")
    watch_frontier = [
        WatchItem(
            id=str(w.get("id", "")),
            bucket="frontier",
            name=str(w.get("name", "")),
            url=str(w.get("url", "")),
            last_verified=str(w.get("last_verified", "")),
            evidence_tier=str(w.get("evidence_tier", "vendor-claim")),
            summary=str(w.get("summary", "")),
            limitations=list(w.get("limitations", [])),
        )
        for w in watch_raw.get("frontier", [])
    ]
    watch_community = [
        WatchItem(
            id=str(w.get("id", "")),
            bucket="community",
            name=str(w.get("name", "")),
            url=str(w.get("url", "")),
            last_verified=str(w.get("last_verified", "")),
            evidence_tier=str(w.get("evidence_tier", "field-note")),
            summary=str(w.get("summary", "")),
            limitations=list(w.get("limitations", [])),
        )
        for w in watch_raw.get("community", [])
    ]

    retired_raw = _load_yaml(cdir / "retired.yaml")
    retired: list[RetiredItem] = []
    for cat in ("cloud", "local"):
        for r in retired_raw.get(cat, []):
            retired.append(
                RetiredItem(
                    category=cat,
                    name=str(r.get("name", "")),
                    match_pattern=str(r.get("match_pattern", "")),
                    retired_on=str(r.get("retired_on", "")),
                    reason=str(r.get("reason", "")),
                    replaced_by=r.get("replaced_by"),
                )
            )

    health_path = root_path / "health" / "state.json"
    health_state: dict[str, dict[str, Any]] = {}
    if health_path.exists():
        with health_path.open("r", encoding="utf-8") as fp:
            health_state = json.load(fp)

    return Catalog(
        profiles=profiles,
        entries=entries,
        routing_chains=dict(models_cloud.get("routing_chains", {})),
        guides=guides,
        specialists=specialists,
        watch_frontier=watch_frontier,
        watch_community=watch_community,
        retired=retired,
        health_state=health_state,
        load_errors=errors,
    )
