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


def compute_freshness(
    item: dict[str, Any],
    health_record: dict[str, Any] | None = None,
    as_of: date | None = None,
) -> dict[str, Any]:
    today = as_of or datetime.now(timezone.utc).date()
    lifecycle = item.get("lifecycle", "operational")
    decay_class = item.get("decay_class", "operational")
    ttl_days = DECAY_TTL_DAYS.get(decay_class, 60)

    verified = date.fromisoformat(str(item["last_verified"]))
    age_days = max(0, (today - verified).days)
    ttl_ratio = round(age_days / ttl_days, 3)

    hr = health_record or {}
    fails = int(hr.get("consecutive_fails", 0))
    gh_archived = bool(hr.get("gh_archived", False))

    if lifecycle == "graveyard":
        status = "graveyard"
    elif lifecycle == "monitor-only":
        status = "monitor_only"
    elif gh_archived or fails >= 3:
        status = "degraded"
    elif age_days > ttl_days:
        status = "stale"
    elif ttl_ratio >= 0.75:
        status = "aging"
    else:
        status = "fresh"

    score = max(0, min(100, int(round((1.0 - min(ttl_ratio, 1.0)) * 100))))
    if status in ("degraded", "graveyard"):
        score = 0

    eligible_for_agents = status in ("fresh", "aging") and lifecycle not in ("monitor-only", "deprecated", "graveyard")

    return {
        "status": status,
        "score": score,
        "decay_class": decay_class,
        "ttl_days": ttl_days,
        "age_days": age_days,
        "ttl_ratio": ttl_ratio,
        "consecutive_fails": fails,
        "gh_archived": gh_archived,
        "eligible_for_agents": eligible_for_agents,
        "graveyard_candidate": gh_archived or fails >= 3,
    }


def evaluate_workspace_health(ws: dict[str, Any], as_of: date | None = None) -> dict[str, Any]:
    h_state = ws["health_state"]
    entity_health: dict[str, dict[str, Any]] = {}
    pack_health: dict[str, dict[str, Any]] = {}
    feed_health: dict[str, dict[str, Any]] = {}
    digest = {"aging": [], "stale": [], "degraded": [], "graveyard_candidates": []}

    for eid, ent in ws["entities"].items():
        f = compute_freshness(ent, h_state.get(eid), as_of=as_of)
        entity_health[eid] = f
        if f["status"] in ("aging", "stale", "degraded"):
            digest[f["status"]].append({"id": eid, "kind": ent["kind"], "age_days": f["age_days"], "ttl_days": f["ttl_days"]})
        if f["graveyard_candidate"]:
            digest["graveyard_candidates"].append({"id": eid, "fails": f["consecutive_fails"], "gh_archived": f["gh_archived"]})

    for pid, pack in ws["packs"].items():
        own = compute_freshness(pack, h_state.get(pid), as_of=as_of)
        dep_issues = []
        for role, refs in pack.get("stack", {}).items():
            for ref in refs:
                ref_status = entity_health[ref]["status"]
                if ref_status in ("stale", "degraded"):
                    dep_issues.append({"entity_id": ref, "role": role, "status": ref_status})
        own["degraded_dependencies"] = dep_issues
        own["effective_status"] = "degraded" if dep_issues and own["status"] == "fresh" else own["status"]
        pack_health[pid] = own

    for fid, feed in ws["feeds"].items():
        items_h = {}
        for item in feed.get("items", []):
            f = compute_freshness(item, h_state.get(item["id"]), as_of=as_of)
            items_h[item["id"]] = f
            if f["status"] in ("aging", "stale", "degraded"):
                digest[f["status"]].append({"id": item["id"], "kind": f"feed:{fid}", "age_days": f["age_days"], "ttl_days": f["ttl_days"]})
        feed_health[fid] = items_h

    return {
        "as_of": (as_of or datetime.now(timezone.utc).date()).isoformat(),
        "entities": entity_health,
        "packs": pack_health,
        "feeds": feed_health,
        "digest": digest,
    }


def run_lru_sweep(ws: dict[str, Any], root: str = ".", limit: int = 25, dry_run: bool = False) -> dict[str, Any]:
    state = dict(ws["health_state"])
    candidates = []

    for eid, ent in ws["entities"].items():
        url = ent.get("urls", {}).get("primary")
        if url:
            last_checked = state.get(eid, {}).get("last_checked", "1970-01-01T00:00:00Z")
            candidates.append((last_checked, eid, url))

    for feed in ws["feeds"].values():
        for item in feed.get("items", []):
            url = item.get("urls", {}).get("primary")
            if url:
                iid = item["id"]
                last_checked = state.get(iid, {}).get("last_checked", "1970-01-01T00:00:00Z")
                candidates.append((last_checked, iid, url))

    candidates.sort(key=lambda x: x[0])
    batch = candidates[:limit]
    gh_token = os.environ.get("GITHUB_TOKEN")
    gh_headers = {"Accept": "application/vnd.github+json"}
    if gh_token:
        gh_headers["Authorization"] = f"Bearer {gh_token}"

    results = []
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for _, cid, url in batch:
        if dry_run:
            results.append({"id": cid, "url": url, "action": "would_check"})
            continue

        prev = state.get(cid, {})
        fails = int(prev.get("consecutive_fails", 0))
        gh_archived = bool(prev.get("gh_archived", False))
        gh_pushed_at = prev.get("gh_pushed_at")
        http_status = None

        try:
            m = GH_REPO_RE.match(url)
            if m:
                owner, repo = m.group(1), m.group(2).removesuffix(".git")
                r = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=gh_headers, timeout=10)
                http_status = r.status_code
                if r.status_code == 200:
                    payload = r.json()
                    gh_archived = bool(payload.get("archived", False))
                    gh_pushed_at = payload.get("pushed_at")
                    fails = 0
                elif r.status_code != 403:
                    fails += 1
            else:
                r = requests.head(url, allow_redirects=True, timeout=10)
                if r.status_code in (405, 403):
                    r = requests.get(url, stream=True, allow_redirects=True, timeout=10)
                http_status = r.status_code
                fails = 0 if 200 <= r.status_code < 400 else fails + 1
        except Exception:
            fails += 1

        rec = {
            "last_checked": now_iso,
            "http_status": http_status,
            "gh_archived": gh_archived,
            "gh_pushed_at": gh_pushed_at,
            "consecutive_fails": fails,
        }
        state[cid] = rec
        results.append({"id": cid, "url": url, **rec})

    if not dry_run:
        health_dir = os.path.join(root, "health")
        os.makedirs(health_dir, exist_ok=True)
        with open(os.path.join(health_dir, "state.json"), "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, sort_keys=True)

    return {"checked_count": len(results), "dry_run": dry_run, "results": results}
