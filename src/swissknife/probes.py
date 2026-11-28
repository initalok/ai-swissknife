from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable

import requests

from swissknife.models import Freshness, Workspace

DECAY_TTL_DAYS = {
    "volatile": 21,
    "operational": 60,
    "stable": 120,
}

GH_REPO_RE = re.compile(r"^https?://github\.com/([^/]+)/([^/#?]+)")
HF_COLLECTION_RE = re.compile(r"^https?://huggingface\.co/collections/([^/]+/[^/#?]+)")
HF_MODEL_RE = re.compile(r"^https?://huggingface\.co/(?!datasets/|spaces/|collections/|blog/)([^/]+/[^/#?]+)")
SEMVER_TAG_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
BREAKING_KEYWORDS_RE = re.compile(
    r"(breaking\s+change|breaking:|deprecated|removed\s+support|no\s+longer\s+needed|superseded|archived)",
    re.IGNORECASE,
)
HTTP_HEADERS = {"User-Agent": "ai-swissknife-health-probe/6.0 (+https://github.com/initalok/ai-swissknife)"}

ProbeFunc = Callable[[str, dict[str, Any], str | None], dict[str, Any] | None]


def compute_freshness(
    *,
    last_verified: str,
    decay_class: str,
    lifecycle: str,
    reviewed_release: str | None = None,
    record: dict[str, Any] | None = None,
    as_of: date | None = None,
) -> Freshness:
    today = as_of or datetime.now(timezone.utc).date()
    ttl_days = DECAY_TTL_DAYS.get(decay_class, 60)
    age_days = max(0, (today - date.fromisoformat(last_verified)).days)
    ratio = age_days / ttl_days

    hr = record or {}
    fails = int(hr.get("consecutive_fails", 0))
    archived = bool(hr.get("upstream_archived", False))
    latest_tag = hr.get("latest_release_tag")
    release_delta = bool(reviewed_release and latest_tag and latest_tag != reviewed_release)
    breaking_signal = bool(release_delta and hr.get("release_breaking_signal", False))

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

    return Freshness(
        status=status,
        effective_status=status,
        score=score,
        decay_class=decay_class,
        ttl_days=ttl_days,
        age_days=age_days,
        consecutive_fails=fails,
        upstream_archived=archived,
        upstream_pushed_at=hr.get("upstream_pushed_at"),
        latest_release_tag=latest_tag,
        release_delta=release_delta,
        breaking_signal=breaking_signal,
        eligible_for_agents=eligible,
        retirement_candidate=archived or fails >= 3,
        collection_item_count=hr.get("collection_item_count"),
    )


def _probe_github(url: str, prev: dict[str, Any], release_strategy: str | None) -> dict[str, Any] | None:
    m = GH_REPO_RE.match(url)
    if not m:
        return None
    owner, repo = m.group(1), m.group(2).removesuffix(".git")
    headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"

    fails = int(prev.get("consecutive_fails", 0))
    archived = bool(prev.get("upstream_archived", False))
    pushed_at = prev.get("upstream_pushed_at")
    latest_tag = prev.get("latest_release_tag")
    release_breaking = bool(prev.get("release_breaking_signal", False))

    r = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers, timeout=10)
    http_status = r.status_code
    if r.status_code == 200:
        j = r.json()
        archived = bool(j.get("archived", False))
        pushed_at = j.get("pushed_at")
        fails = 0
        if release_strategy == "highest-semver":
            rr = requests.get(
                f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=15",
                headers=headers,
                timeout=10,
            )
            if rr.status_code == 200:
                best: tuple[tuple[int, int, int], dict[str, Any]] | None = None
                for rj in rr.json():
                    if rj.get("draft") or rj.get("prerelease"):
                        continue
                    tag_name = rj.get("tag_name") or ""
                    sm = SEMVER_TAG_RE.match(tag_name)
                    if not sm:
                        continue
                    ver = (int(sm.group(1)), int(sm.group(2)), int(sm.group(3)))
                    if best is None or ver > best[0]:
                        best = (ver, rj)
                if best is not None:
                    best_rj = best[1]
                    latest_tag = best_rj.get("tag_name")
                    release_breaking = bool(BREAKING_KEYWORDS_RE.search(best_rj.get("body") or ""))
        elif release_strategy:
            rr = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest", headers=headers, timeout=10)
            if rr.status_code == 200:
                rj = rr.json()
                latest_tag = rj.get("tag_name")
                release_breaking = bool(BREAKING_KEYWORDS_RE.search(rj.get("body") or ""))
    elif r.status_code not in (403, 429):
        fails += 1

    return {
        "http_status": http_status,
        "upstream_archived": archived,
        "upstream_pushed_at": pushed_at,
        "latest_release_tag": latest_tag,
        "release_breaking_signal": release_breaking,
        "consecutive_fails": fails,
    }


def _probe_hf_collection(url: str, prev: dict[str, Any], release_strategy: str | None) -> dict[str, Any] | None:
    m = HF_COLLECTION_RE.match(url)
    if not m:
        return None
    fails = int(prev.get("consecutive_fails", 0))
    pushed_at = prev.get("upstream_pushed_at")
    item_count = prev.get("collection_item_count")

    r = requests.get(f"https://huggingface.co/api/collections/{m.group(1)}", timeout=10)
    if r.status_code == 200:
        j = r.json()
        pushed_at = j.get("lastUpdated") or pushed_at
        item_count = len(j.get("items", []))
        fails = 0
    elif r.status_code != 429:
        fails += 1

    return {
        "http_status": r.status_code,
        "upstream_archived": False,
        "upstream_pushed_at": pushed_at,
        "latest_release_tag": f"items:{item_count}" if item_count is not None else None,
        "collection_item_count": item_count,
        "release_breaking_signal": False,
        "consecutive_fails": fails,
    }


def _probe_huggingface(url: str, prev: dict[str, Any], release_strategy: str | None) -> dict[str, Any] | None:
    m = HF_MODEL_RE.match(url)
    if not m:
        return None
    fails = int(prev.get("consecutive_fails", 0))
    archived = bool(prev.get("upstream_archived", False))
    pushed_at = prev.get("upstream_pushed_at")

    r = requests.get(f"https://huggingface.co/api/models/{m.group(1)}", timeout=10)
    if r.status_code == 200:
        j = r.json()
        archived = bool(j.get("disabled", False))
        pushed_at = j.get("lastModified")
        fails = 0
    elif r.status_code != 429:
        fails += 1

    return {
        "http_status": r.status_code,
        "upstream_archived": archived,
        "upstream_pushed_at": pushed_at,
        "latest_release_tag": prev.get("latest_release_tag"),
        "release_breaking_signal": False,
        "consecutive_fails": fails,
    }


def _probe_http(url: str, prev: dict[str, Any], release_strategy: str | None) -> dict[str, Any]:
    fails = int(prev.get("consecutive_fails", 0))
    r = requests.head(url, headers=HTTP_HEADERS, allow_redirects=True, timeout=10)
    if r.status_code in (403, 405):
        r = requests.get(url, headers=HTTP_HEADERS, stream=True, allow_redirects=True, timeout=10)
    if 200 <= r.status_code < 400:
        fails = 0
    elif r.status_code != 429:
        fails += 1
    return {
        "http_status": r.status_code,
        "upstream_archived": False,
        "upstream_pushed_at": prev.get("upstream_pushed_at"),
        "latest_release_tag": None,
        "release_breaking_signal": False,
        "consecutive_fails": fails,
    }


PROBE_CHAIN: list[ProbeFunc] = [_probe_github, _probe_hf_collection, _probe_huggingface, _probe_http]


def collect_targets(ws: Workspace) -> list[tuple[str, str, str | None]]:
    targets: list[tuple[str, str, str | None]] = []
    for eid, entry in ws.entries.items():
        track = bool(entry.meta.get("last_reviewed_release") or entry.meta.get("track_releases"))
        strategy = str(entry.meta.get("release_strategy", "latest")) if track else None
        targets.append((f"entry:{eid}", entry.url, strategy))
    for spid, sp in ws.specialists.items():
        for pick in sp.direct_picks:
            targets.append((f"specialist:{spid}:{pick.id}", pick.url, None))
        targets.append((f"specialist:{spid}:upstream", sp.upstream_hub.url, None))
    for w in (*ws.watch_frontier, *ws.watch_models, *ws.watch_community):
        targets.append((f"watch:{w.bucket}:{w.id}", w.url, None))
    return targets


def run_lru_probe(ws: Workspace, root: str | Path = ".", limit: int = 20, dry_run: bool = False) -> dict[str, Any]:
    state = dict(ws.health_state)
    candidates = [
        (state.get(key, {}).get("last_checked", "1970-01-01T00:00:00Z"), key, url, strategy)
        for key, url, strategy in collect_targets(ws)
    ]
    candidates.sort(key=lambda x: x[0])
    batch = candidates[:limit]
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    results: list[dict[str, Any]] = []

    for _, key, url, strategy in batch:
        if dry_run:
            results.append({"key": key, "url": url, "release_strategy": strategy, "action": "would_probe"})
            continue
        prev = state.get(key, {})
        rec: dict[str, Any] | None = None
        try:
            for probe in PROBE_CHAIN:
                rec = probe(url, prev, strategy)
                if rec is not None:
                    break
        except Exception:
            rec = {
                "http_status": None,
                "upstream_archived": bool(prev.get("upstream_archived", False)),
                "upstream_pushed_at": prev.get("upstream_pushed_at"),
                "latest_release_tag": prev.get("latest_release_tag"),
                "release_breaking_signal": False,
                "consecutive_fails": int(prev.get("consecutive_fails", 0)) + 1,
            }
        assert rec is not None
        rec["last_checked"] = now_iso
        state[key] = rec
        results.append({"key": key, "url": url, **rec})

    if not dry_run:
        hpath = Path(root) / "health" / "state.json"
        hpath.parent.mkdir(parents=True, exist_ok=True)
        hpath.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {"probed_count": len(results), "total_targets": len(candidates), "dry_run": dry_run, "results": results}
