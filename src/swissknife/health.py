from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
import requests

from swissknife.models import Catalog, FreshnessState

DECAY_TTL_DAYS = {
    "volatile": 21,
    "operational": 60,
    "stable": 120,
}

GH_REPO_RE = re.compile(r"^https?://github\.com/([^/]+)/([^/#?]+)")
HF_MODEL_RE = re.compile(r"^https?://huggingface\.co/(?!datasets/|spaces/|collections/|blog/)([^/]+/[^/#?]+)")


def compute_freshness(
    *,
    last_verified: str,
    decay_class: str,
    lifecycle: str,
    record: dict[str, Any] | None = None,
    as_of: date | None = None,
) -> FreshnessState:
    today = as_of or datetime.now(timezone.utc).date()
    ttl_days = DECAY_TTL_DAYS.get(decay_class, 60)
    age_days = max(0, (today - date.fromisoformat(last_verified)).days)
    ratio = age_days / ttl_days

    hr = record or {}
    fails = int(hr.get("consecutive_fails", 0))
    archived = bool(hr.get("upstream_archived", False))

    if lifecycle == "retired":
        status = "retired"
    elif lifecycle == "monitor-only":
        status = "monitor-only"
    elif archived or fails >= 3:
        status = "degraded"
    elif age_days > ttl_days:
        status = "stale"
    elif ratio >= 0.75:
        status = "aging"
    else:
        status = "fresh"

    score = 0 if status in ("degraded", "retired") else max(0, min(100, int(round((1.0 - min(ratio, 1.0)) * 100))))
    eligible = status in ("fresh", "aging") and lifecycle not in ("monitor-only", "deprecated", "retired")

    return FreshnessState(
        status=status,
        effective_status=status,
        score=score,
        decay_class=decay_class,
        ttl_days=ttl_days,
        age_days=age_days,
        consecutive_fails=fails,
        upstream_archived=archived,
        upstream_pushed_at=hr.get("upstream_pushed_at"),
        eligible_for_agents=eligible,
        retirement_candidate=archived or fails >= 3,
    )


def collect_probe_targets(catalog: Catalog) -> list[tuple[str, str]]:
    targets: list[tuple[str, str]] = []
    for eid, entry in catalog.entries.items():
        targets.append((f"entry:{eid}", entry.url))
    for gid, guide in catalog.guides.items():
        for tool in guide.tools:
            targets.append((f"guide:{gid}:{tool.id}", tool.url))
    for sid, spec in catalog.specialists.items():
        for pick in spec.direct_picks:
            targets.append((f"specialist:{sid}:{pick.id}", pick.url))
        targets.append((f"specialist:{sid}:upstream", spec.upstream_directory.url))
    for item in (*catalog.watch_frontier, *catalog.watch_community):
        targets.append((f"watch:{item.bucket}:{item.id}", item.url))
    return targets


def run_lru_probe(catalog: Catalog, root: str | Path = ".", limit: int = 20, dry_run: bool = False) -> dict[str, Any]:
    state = dict(catalog.health_state)
    candidates = [
        (state.get(key, {}).get("last_checked", "1970-01-01T00:00:00Z"), key, url)
        for key, url in collect_probe_targets(catalog)
    ]
    candidates.sort(key=lambda x: x[0])
    batch = candidates[:limit]

    gh_headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        gh_headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    results: list[dict[str, Any]] = []

    for _, key, url in batch:
        if dry_run:
            results.append({"key": key, "url": url, "action": "would_probe"})
            continue

        prev = state.get(key, {})
        fails = int(prev.get("consecutive_fails", 0))
        archived = bool(prev.get("upstream_archived", False))
        pushed_at = prev.get("upstream_pushed_at")
        http_status: int | None = None

        try:
            m_gh = GH_REPO_RE.match(url)
            m_hf = HF_MODEL_RE.match(url)
            if m_gh:
                owner, repo = m_gh.group(1), m_gh.group(2).removesuffix(".git")
                r = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=gh_headers, timeout=10)
                http_status = r.status_code
                if r.status_code == 200:
                    payload = r.json()
                    archived = bool(payload.get("archived", False))
                    pushed_at = payload.get("pushed_at")
                    fails = 0
                elif r.status_code not in (403, 429):
                    fails += 1
            elif m_hf:
                r = requests.get(f"https://huggingface.co/api/models/{m_hf.group(1)}", timeout=10)
                http_status = r.status_code
                if r.status_code == 200:
                    payload = r.json()
                    archived = bool(payload.get("disabled", False))
                    pushed_at = payload.get("lastModified")
                    fails = 0
                elif r.status_code != 429:
                    fails += 1
            else:
                r = requests.head(url, allow_redirects=True, timeout=10)
                if r.status_code in (403, 405):
                    r = requests.get(url, stream=True, allow_redirects=True, timeout=10)
                http_status = r.status_code
                if 200 <= r.status_code < 400:
                    fails = 0
                elif r.status_code != 429:
                    fails += 1
        except Exception:
            fails += 1

        rec = {
            "last_checked": now_iso,
            "http_status": http_status,
            "upstream_archived": archived,
            "upstream_pushed_at": pushed_at,
            "consecutive_fails": fails,
        }
        state[key] = rec
        results.append({"key": key, "url": url, **rec})

    if not dry_run:
        health_file = Path(root) / "health" / "state.json"
        health_file.parent.mkdir(parents=True, exist_ok=True)
        health_file.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {"probed_count": len(results), "total_targets": len(candidates), "dry_run": dry_run, "results": results}
