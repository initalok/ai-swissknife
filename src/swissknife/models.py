from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

VALID_LIFECYCLES = {"mature", "experimental", "operational", "monitor-only", "deprecated", "retired"}
VALID_DECAY_CLASSES = {"volatile", "operational", "stable"}
VALID_EVIDENCE_TIERS = {"primary-eval", "official-docs", "vendor-claim", "field-note"}
VALID_DECISION_STATUSES = {"accepted", "superseded", "deprecated"}


@dataclass(frozen=True)
class TaxonomyItem:
    id: str
    name: str
    summary: str
    order: int = 0


@dataclass(frozen=True)
class Taxonomy:
    allowed_kinds: list[str]
    tracks: dict[str, TaxonomyItem]
    worlds: dict[str, TaxonomyItem]
    sections: dict[str, TaxonomyItem]
    non_goals: list[str]


@dataclass(frozen=True)
class Relations:
    runs_on: list[str] = field(default_factory=list)
    adapts: list[str] = field(default_factory=list)
    guards: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Entry:
    id: str
    kind: str
    name: str
    summary: str
    when_to_use: str
    limitations: list[str]
    evidence_tier: str
    lifecycle: str
    decay_class: str
    last_verified: str
    url: str
    tags: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    relations: Relations = field(default_factory=Relations)
    meta: dict[str, Any] = field(default_factory=dict)
    source_file: str = ""


@dataclass(frozen=True)
class Slot:
    id: str
    title: str
    role: str
    primary: str
    experimental: str | None = None
    fallbacks: list[str] = field(default_factory=list)
    decision_id: str | None = None
    world: str | None = None
    source_file: str = ""


@dataclass(frozen=True)
class ExternalRef:
    id: str
    name: str
    url: str
    summary: str = ""


@dataclass(frozen=True)
class Specialist:
    id: str
    title: str
    summary: str
    last_verified: str
    capabilities: list[str]
    privacy: str
    require_guard: bool
    direct_picks: list[ExternalRef]
    upstream_hub: ExternalRef
    guardrails: list[str]
    source_file: str = ""


@dataclass(frozen=True)
class DecisionRecord:
    id: str
    title: str
    status: str
    date: str
    job: str
    anchor_ids: list[str]
    alternatives: list[str]
    rationale: str
    exceptions: list[str]
    reversal_trigger: str
    slot_ids: list[str] = field(default_factory=list)
    superseded_by: str | None = None
    source_file: str = ""


@dataclass(frozen=True)
class WatchItem:
    id: str
    bucket: str
    name: str
    url: str
    last_verified: str
    evidence_tier: str
    summary: str
    limitations: list[str]
    source_file: str = ""


@dataclass(frozen=True)
class RetiredItem:
    area: str
    name: str
    match_pattern: str
    retired_on: str
    reason: str
    replaced_by: str | None = None


@dataclass(frozen=True)
class ManagedBlock:
    directive: str
    args: dict[str, str]
    line: int


@dataclass(frozen=True)
class PageDoc:
    path: str
    title: str
    section: str | None
    summary: str
    order: int
    track: str | None = None
    world: str | None = None
    blocks: list[ManagedBlock] = field(default_factory=list)


@dataclass
class Freshness:
    status: str
    effective_status: str
    score: int
    decay_class: str
    ttl_days: int
    age_days: int
    consecutive_fails: int
    upstream_archived: bool
    upstream_pushed_at: str | None
    latest_release_tag: str | None
    release_delta: bool
    breaking_signal: bool
    eligible_for_agents: bool
    retirement_candidate: bool
    collection_item_count: int | None = None
    upstream_alerts: list[dict[str, str]] = field(default_factory=list)


@dataclass
class Workspace:
    taxonomy: Taxonomy
    entries: dict[str, Entry]
    slots: dict[str, Slot]
    specialists: dict[str, Specialist]
    decisions: dict[str, DecisionRecord]
    watch_frontier: list[WatchItem]
    watch_models: list[WatchItem]
    watch_community: list[WatchItem]
    retired: list[RetiredItem]
    pages: list[PageDoc]
    health_state: dict[str, dict[str, Any]]
    load_errors: list[str] = field(default_factory=list)


def to_dict(obj: Any) -> Any:
    return asdict(obj)
