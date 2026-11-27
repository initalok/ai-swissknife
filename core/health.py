from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, timezone
from typing import Any
import requests

DECAY_TTL_DAYS = {
    "volatile": 21,
    "operational": 60,
    "stable": 120,
}

GH_REPO_RE = re.compile(r"^https?://github\.com/([^/]+)/([^/#?]+)")
HF_MODEL_RE = re.compile(r"^https?://huggingface\.co/(?!datasets/|spaces/|collections/|blog/)([^/]+/[^/#?]+)")
HF_COLL_RE = re.compile(r"^https?://huggingface\.co/collections/([^/]+/[^/#?]+)")


def compute_freshness(
    item: dict[str, Any],
    record: dict[str, Any] | None = None,
    as_of: date | None = None,
) -> dict[str, Any]:
    today = as_of or datetime.now(timezone.utc).date()
    lifecycle = item.get("lifecycle", "operational")
    decay_class = item.get("decay_class", "operational")
    ttl_days = DECAY_TTL_DAYS.get(decay_class, 60)

    verified = date.fromisoformat(str(item["last_verified"]))
    age_days = max(0, (today - verified).days)
    ttl_ratio = round(age_days / ttl_days, 3)

    hr = record or {}
    fails = int(hr.get("consecutive_fails", 0))
    archived = bool(hr.get("upstream_archived", False))

    if lifecycle == "graveyard":
        status = "graveyard"
    elif lifecycle == "monitor-only":
        status = "monitor_only"
    elif archived or fails >= 3:
        status = "degraded"
    elif age_days > ttl_days:
        status = "stale"
    elif ttl_ratio >= 0.75:
        status = "aging"
    else:
        status = "fresh"

    score = 0 if status in ("degraded", "graveyard") else max(0, min(100, int(round((1.0 - min(ttl_ratio, 1.0)) * 100))))
    eligible_for_agents = status in ("fresh", "aging") and lifecycle not in ("monitor-only", "deprecated", "graveyard")

    return {
        "status": status,
        "score": score,
        "decay_class": decay_class,
        "ttl_days": ttl_days,
        "age_days": age_days,
        "consecutive_fails": fails,
        "upstream_archived": archived,
        "upstream_pushed_at": hr.get("upstream_pushed_at"),
        "eligible_for_agents": eligible_for_agents,
        "graveyard_candidate": archived or fails >= 3,
    }


def collect_probe_targets(data: dict[str, Any]) -> list[tuple[str, str]]:
    targets: list[tuple[str, str]] = []
    for nid, node in data["nodes"].items():
        targets.append((f"node:{nid}", node["url"]))
    for pid, pb in data["playbooks"].items():
        for tool in pb.get("domain_tools", []):
            targets.append((f"playbook:{pid}:{tool['id']}", tool["url"]))
    for sid, sp in data["spokes"].items():
        for ep in sp.get("entry_points", []):
            targets.append((f"spoke:{sid}:{ep['id']}", ep["url"]))
        targets.append((f"spoke:{sid}:upstream_hub", sp["upstream_hub"]["url"]))
    for bucket in ("frontier", "community"):
        for item in data["radar"][bucket]:
            targets.append((f"radar:{bucket}:{item['id']}", item["url"]))
    return targets


def run_lru_probe(data: dict[str, Any], root: str = ".", limit: int = 20, dry_run: bool = False) -> dict[str, Any]:
    state = dict(data["health_state"])
    candidates = []
    for key, url in collect_probe_targets(data):
        last_checked = state.get(key, {}).get("last_checked", "1970-01-01T00:00:00Z")
        candidates.append((last_checked, key, url))

    candidates.sort(key=lambda x: x[0])
    batch = candidates[:limit]

    gh_headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        gh_headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    results = []

    for _, key, url in batch:
        if dry_run:
            results.append({"key": key, "url": url, "action": "would_probe"})
            continue

        prev = state.get(key, {})
        fails = int(prev.get("consecutive_fails", 0))
        archived = bool(prev.get("upstream_archived", False))
        pushed_at = prev.get("upstream_pushed_at")
        http_status = None

        try:
            m_gh = GH_REPO_RE.match(url)
            m_hf = HF_MODEL_RE.match(url)
            if m_gh:
                owner, repo = m_gh.group(1), m_gh.group(2).removesuffix(".git")
                r = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=gh_headers, timeout=10)
                http_status = r.status_code
                if r.status_code == 200:
                    j = r.json()
                    archived = bool(j.get("archived", False))
                    pushed_at = j.get("pushed_at")
                    fails = 0
                elif r.status_code != 403:
                    fails += 1
            elif m_hf and not HF_COLL_RE.match(url):
                r = requests.get(f"https://huggingface.co/api/models/{m_hf.group(1)}", timeout=10)
                http_status = r.status_code
                if r.status_code == 200:
                    j = r.json()
                    archived = bool(j.get("disabled", False))
                    pushed_at = j.get("lastModified")
                    fails = 0
                else:
                    fails += 1
            else:
                r = requests.head(url, allow_redirects=True, timeout=10)
                if r.status_code in (403, 405):
                    r = requests.get(url, stream=True, allow_redirects=True, timeout=10)
                http_status = r.status_code
                fails = 0 if 200 <= r.status_code < 400 else fails + 1
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
        os.makedirs(os.path.join(root, "health"), exist_ok=True)
        with open(os.path.join(root, "health", "state.json"), "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, sort_keys=True)

    return {"probed_count": len(results), "total_targets": len(candidates), "dry_run": dry_run, "results": results}
