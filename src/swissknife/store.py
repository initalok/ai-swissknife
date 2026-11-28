from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from swissknife.models import (
    DecisionRecord,
    Entry,
    ExternalRef,
    Relations,
    RetiredItem,
    Slot,
    Specialist,
    Taxonomy,
    TaxonomyItem,
    WatchItem,
    Workspace,
)
from swissknife.pages import scan_pages

DEFAULT_KINDS = ["gateway", "model", "adapter", "harness", "runtime", "tool", "mcp", "memory", "fabric", "mobile"]


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fp:
        return yaml.safe_load(fp) or {}


def _parse_tax_items(items: list[dict[str, Any]]) -> dict[str, TaxonomyItem]:
    out: dict[str, TaxonomyItem] = {}
    for idx, raw in enumerate(items):
        tid = raw.get("id")
        if tid:
            out[str(tid)] = TaxonomyItem(
                id=str(tid),
                name=str(raw.get("name", tid)),
                summary=str(raw.get("summary", "")),
                order=int(raw.get("order", idx)),
            )
    return out


def _parse_ref(raw: dict[str, Any]) -> ExternalRef:
    return ExternalRef(
        id=str(raw.get("id", "")),
        name=str(raw.get("name", "")),
        url=str(raw.get("url", "")),
        summary=str(raw.get("summary", "")),
    )


def load_workspace(root: str | Path = ".") -> Workspace:
    root_path = Path(root)
    cdir = root_path / "catalog"
    errors: list[str] = []

    tax_raw = _load_yaml(cdir / "taxonomy.yaml")
    taxonomy = Taxonomy(
        allowed_kinds=list(tax_raw.get("allowed_kinds") or DEFAULT_KINDS),
        tracks=_parse_tax_items(tax_raw.get("tracks", [])),
        worlds=_parse_tax_items(tax_raw.get("worlds", [])),
        sections=_parse_tax_items(tax_raw.get("sections", [])),
        non_goals=list(tax_raw.get("non_goals", [])),
    )

    entries: dict[str, Entry] = {}
    slots: dict[str, Slot] = {}
    specialists: dict[str, Specialist] = {}
    watch_frontier: list[WatchItem] = []
    watch_models: list[WatchItem] = []
    watch_community: list[WatchItem] = []
    seen_watch: set[tuple[str, str]] = set()
    retired: list[RetiredItem] = []

    reg_dir = cdir / "registry"
    if reg_dir.exists():
        for path in sorted(reg_dir.rglob("*.yaml")):
            rel = path.relative_to(root_path).as_posix()
            raw = _load_yaml(path)

            for item in raw.get("entries", []):
                eid = item.get("id")
                if not eid:
                    errors.append(f"{rel}: entry missing 'id'")
                    continue
                if eid in entries:
                    errors.append(f"{rel}: duplicate entry id '{eid}'")
                    continue
                r_raw = item.get("relations") or {}
                entries[str(eid)] = Entry(
                    id=str(eid),
                    kind=str(item.get("kind", "")),
                    name=str(item.get("name", "")),
                    summary=str(item.get("summary", "")),
                    when_to_use=str(item.get("when_to_use", "")),
                    limitations=list(item.get("limitations", [])),
                    evidence_tier=str(item.get("evidence_tier", "")),
                    lifecycle=str(item.get("lifecycle", "")),
                    decay_class=str(item.get("decay_class", "")),
                    last_verified=str(item.get("last_verified", "")),
                    url=str(item.get("url", "")),
                    tags=list(item.get("tags", [])),
                    capabilities=list(item.get("capabilities", [])),
                    relations=Relations(
                        runs_on=list(r_raw.get("runs_on", [])),
                        adapts=list(r_raw.get("adapts", [])),
                        guards=list(r_raw.get("guards", [])),
                    ),
                    meta=dict(item.get("meta") or {}),
                    source_file=rel,
                )

            for s in raw.get("slots", []):
                sid = s.get("id")
                if not sid:
                    errors.append(f"{rel}: slot missing 'id'")
                    continue
                if sid in slots:
                    errors.append(f"{rel}: duplicate slot id '{sid}'")
                    continue
                slots[str(sid)] = Slot(
                    id=str(sid),
                    title=str(s.get("title", "")),
                    role=str(s.get("role", "")),
                    primary=str(s.get("primary", "")),
                    experimental=s.get("experimental"),
                    fallbacks=list(s.get("fallbacks", [])),
                    decision_id=s.get("decision_id"),
                    world=s.get("world"),
                    source_file=rel,
                )

            for sp in raw.get("specialists", []):
                spid = sp.get("id")
                if not spid:
                    errors.append(f"{rel}: specialist missing 'id'")
                    continue
                if spid in specialists:
                    errors.append(f"{rel}: duplicate specialist id '{spid}'")
                    continue
                c = sp.get("constraints") or {}
                specialists[str(spid)] = Specialist(
                    id=str(spid),
                    title=str(sp.get("title", "")),
                    summary=str(sp.get("summary", "")),
                    last_verified=str(sp.get("last_verified", "")),
                    capabilities=list(c.get("capabilities", [])),
                    privacy=str(c.get("privacy", "any")),
                    require_guard=bool(c.get("require_guard", False)),
                    direct_picks=[_parse_ref(p) for p in sp.get("direct_picks", [])],
                    upstream_hub=_parse_ref(sp.get("upstream_hub") or {}),
                    guardrails=list(sp.get("guardrails", [])),
                    source_file=rel,
                )

            watch_raw = raw.get("watch") or {}
            default_tiers = {"frontier": "vendor-claim", "models": "official-docs", "community": "field-note"}
            for bucket, dest in (("frontier", watch_frontier), ("models", watch_models), ("community", watch_community)):
                for w in watch_raw.get(bucket, []):
                    wid = str(w.get("id", ""))
                    if not wid:
                        errors.append(f"{rel}: watch:{bucket} item missing 'id'")
                        continue
                    if (bucket, wid) in seen_watch:
                        errors.append(f"{rel}: duplicate watch id '{bucket}:{wid}'")
                        continue
                    seen_watch.add((bucket, wid))
                    dest.append(
                        WatchItem(
                            id=wid,
                            bucket=bucket,
                            name=str(w.get("name", "")),
                            url=str(w.get("url", "")),
                            last_verified=str(w.get("last_verified", "")),
                            evidence_tier=str(w.get("evidence_tier", default_tiers[bucket])),
                            summary=str(w.get("summary", "")),
                            limitations=list(w.get("limitations", [])),
                            source_file=rel,
                        )
                    )

            for r in raw.get("retired", []):
                retired.append(
                    RetiredItem(
                        area=str(r.get("area", "general")),
                        name=str(r.get("name", "")),
                        match_pattern=str(r.get("match_pattern", "")),
                        retired_on=str(r.get("retired_on", "")),
                        reason=str(r.get("reason", "")),
                        replaced_by=r.get("replaced_by"),
                    )
                )

    decisions: dict[str, DecisionRecord] = {}
    dec_dir = cdir / "decisions"
    if dec_dir.exists():
        for path in sorted(dec_dir.rglob("*.yaml")):
            rel = path.relative_to(root_path).as_posix()
            raw = _load_yaml(path)
            items = raw.get("decisions") or ([raw["decision"]] if "decision" in raw else [])
            for d in items:
                did = d.get("id")
                if not did:
                    errors.append(f"{rel}: decision missing 'id'")
                    continue
                if did in decisions:
                    errors.append(f"{rel}: duplicate decision id '{did}'")
                    continue
                decisions[str(did)] = DecisionRecord(
                    id=str(did),
                    title=str(d.get("title", "")),
                    status=str(d.get("status", "accepted")),
                    date=str(d.get("date", "")),
                    job=str(d.get("job", "")),
                    anchor_ids=list(d.get("anchor_ids", [])),
                    alternatives=list(d.get("alternatives", [])),
                    rationale=str(d.get("rationale", "")),
                    exceptions=list(d.get("exceptions", [])),
                    reversal_trigger=str(d.get("reversal_trigger", "")),
                    slot_ids=list(d.get("slot_ids", [])),
                    superseded_by=d.get("superseded_by"),
                    source_file=rel,
                )

    pages, page_errs = scan_pages(root_path, taxonomy)
    errors.extend(page_errs)

    health_path = root_path / "health" / "state.json"
    health_state: dict[str, dict[str, Any]] = {}
    if health_path.exists():
        health_state = json.loads(health_path.read_text(encoding="utf-8"))

    return Workspace(
        taxonomy=taxonomy,
        entries=entries,
        slots=slots,
        specialists=specialists,
        decisions=decisions,
        watch_frontier=watch_frontier,
        watch_models=watch_models,
        watch_community=watch_community,
        retired=retired,
        pages=pages,
        health_state=health_state,
        load_errors=errors,
    )
