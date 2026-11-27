from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

EntryKind = Literal["gateway", "model", "adapter", "harness", "runtime", "tool"]
Lifecycle = Literal["mature", "experimental", "operational", "monitor-only", "deprecated", "retired"]
DecayClass = Literal["volatile", "operational", "stable"]
EvidenceTier = Literal["primary-eval", "official-docs", "vendor-claim", "field-note"]

VALID_KINDS = {"gateway", "model", "adapter", "harness", "runtime", "tool"}
VALID_LIFECYCLES = {"mature", "experimental", "operational", "monitor-only", "deprecated", "retired"}
VALID_DECAY_CLASSES = {"volatile", "operational", "stable"}
VALID_EVIDENCE_TIERS = {"primary-eval", "official-docs", "vendor-claim", "field-note"}


@dataclass(frozen=True)
class HardwareProfile:
    id: str
    name: str
    summary: str


@dataclass(frozen=True)
class Edges:
    runs_on: list[str] = field(default_factory=list)
    adapts: list[str] = field(default_factory=list)
    guards: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Entry:
    id: str
    kind: str
    category: str
    name: str
    summary: str
    when_to_use: str
    limitations: list[str]
    evidence_tier: str
    lifecycle: str
    decay_class: str
    last_verified: str
    url: str
    capabilities: list[str] = field(default_factory=list)
    edges: Edges = field(default_factory=Edges)
    license: str | None = None
    footprint: str | None = None
    quota: str | None = None
    env_key: str | None = None
    base_url: str | None = None
    default_model: str | None = None
    role: str | None = None
    evidence_notes: list[str] = field(default_factory=list)
    eval_tables: list[dict[str, Any]] = field(default_factory=list)
    launch_recipe: str | None = None
    mac_launch_recipe: str | None = None
    source_file: str = ""


@dataclass(frozen=True)
class ExternalLink:
    id: str
    name: str
    url: str
    summary: str = ""
    evidence_tier: str = "official-docs"


@dataclass(frozen=True)
class GuideSpec:
    id: str
    title: str
    summary: str
    last_verified: str
    decay_class: str
    capabilities: list[str]
    privacy: str
    require_guard: bool
    pin_entries: list[str]
    tools: list[ExternalLink]
    steps: list[str]
    limitations: list[str]


@dataclass(frozen=True)
class SpecialistSpec:
    id: str
    title: str
    summary: str
    last_verified: str
    capabilities: list[str]
    privacy: str
    require_guard: bool
    direct_picks: list[ExternalLink]
    upstream_directory: ExternalLink
    guardrails: list[str]


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


@dataclass(frozen=True)
class RetiredItem:
    category: str
    name: str
    match_pattern: str
    retired_on: str
    reason: str
    replaced_by: str | None = None


@dataclass
class FreshnessState:
    status: str
    effective_status: str
    score: int
    decay_class: str
    ttl_days: int
    age_days: int
    consecutive_fails: int
    upstream_archived: bool
    upstream_pushed_at: str | None
    eligible_for_agents: bool
    retirement_candidate: bool
    upstream_alerts: list[dict[str, str]] = field(default_factory=list)


@dataclass
class Catalog:
    profiles: dict[str, HardwareProfile]
    entries: dict[str, Entry]
    routing_chains: dict[str, list[str]]
    guides: dict[str, GuideSpec]
    specialists: dict[str, SpecialistSpec]
    watch_frontier: list[WatchItem]
    watch_community: list[WatchItem]
    retired: list[RetiredItem]
    health_state: dict[str, dict[str, Any]]
    load_errors: list[str] = field(default_factory=list)


def to_dict(obj: Any) -> Any:
    return asdict(obj)
