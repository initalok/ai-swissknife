from __future__ import annotations

import json
import os
import re
from datetime import date
from typing import Any
import yaml

VALID_KINDS = {"gateway", "model", "adapter", "harness", "backend", "tool", "mcp"}
VALID_LIFECYCLES = {"mature", "experimental", "operational", "monitor-only", "deprecated", "graveyard"}
VALID_DECAY = {"volatile", "operational", "stable"}

PRESENTATION_LEAK_RE = re.compile(r"(<br\s*/?>|</?sub>|</?kbd>|<details>|```)", re.IGNORECASE)

FORBIDDEN_URL_PATTERNS = [
    re.compile(r"github\.com/topics/", re.IGNORECASE),
    re.compile(r"github\.com/search\b", re.IGNORECASE),
    re.compile(r"huggingface\.co/(models|datasets|spaces)/?$", re.IGNORECASE),
    re.compile(r"reddit\.com/r/[^/]+/?$", re.IGNORECASE),
]

BUDGETS = {
    "max_radar_frontier": 5,
    "max_radar_community": 5,
    "max_spoke_entry_points": 2,
}


def _load_yaml(path: str) -> dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _find_leaks(obj: Any, path: str = "") -> list[str]:
    leaks: list[str] = []
    if isinstance(obj, str):
        if PRESENTATION_LEAK_RE.search(obj):
            leaks.append(f"Presentation HTML/Markdown leak at '{path}'")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            leaks.extend(_find_leaks(v, f"{path}.{k}" if path else str(k)))
    elif isinstance(obj, list):
        for idx, v in enumerate(obj):
            leaks.extend(_find_leaks(v, f"{path}[{idx}]"))
    return leaks


def _check_canonical_url(url: str | None, owner: str) -> list[str]:
    if not url:
        return [f"[{owner}] missing required canonical URL"]
    if not url.startswith(("https://", "http://")):
        return [f"[{owner}] invalid URL scheme '{url}'"]
    for pat in FORBIDDEN_URL_PATTERNS:
        if pat.search(url):
            return [f"[{owner}] violates Canonical URL Law (placeholder URL): '{url}'"]
    return []


def load_graph(root: str = ".") -> dict[str, Any]:
    gdir = os.path.join(root, "graph")
    profiles_raw = _load_yaml(os.path.join(gdir, "profiles.yaml"))
    models_cloud_raw = _load_yaml(os.path.join(gdir, "core_models_cloud.yaml"))
    engine_room_raw = _load_yaml(os.path.join(gdir, "core_engine_room.yaml"))
    playbooks_raw = _load_yaml(os.path.join(gdir, "playbooks.yaml"))
    spokes_raw = _load_yaml(os.path.join(gdir, "spokes.yaml"))
    radar_raw = _load_yaml(os.path.join(gdir, "radar.yaml"))
    graveyard_raw = _load_yaml(os.path.join(gdir, "graveyard.yaml"))

    nodes: dict[str, dict[str, Any]] = {}
    errors: list[str] = []

    for src_name, raw in (
        ("graph/core_models_cloud.yaml", models_cloud_raw),
        ("graph/core_engine_room.yaml", engine_room_raw),
    ):
        for item in raw.get("nodes", []):
            nid = item.get("id")
            if not nid:
                errors.append(f"{src_name}: node missing 'id'")
                continue
            if nid in nodes:
                errors.append(f"{src_name}: duplicate node id '{nid}'")
                continue
            item["_source"] = src_name
            nodes[nid] = item

    health_path = os.path.join(root, "health", "state.json")
    health_state = {}
    if os.path.exists(health_path):
        with open(health_path, "r", encoding="utf-8") as f:
            health_state = json.load(f)

    return {
        "profiles": {p["id"]: p for p in profiles_raw.get("profiles", []) if p.get("id")},
        "nodes": nodes,
        "forage_routes": models_cloud_raw.get("forage_routes", {}),
        "playbooks": {p["id"]: p for p in playbooks_raw.get("playbooks", []) if p.get("id")},
        "spokes": {s["id"]: s for s in spokes_raw.get("spokes", []) if s.get("id")},
        "radar": {
            "frontier": radar_raw.get("frontier", []),
            "community": radar_raw.get("community", []),
        },
        "graveyard": {
            "cloud": graveyard_raw.get("cloud", []),
            "local": graveyard_raw.get("local", []),
        },
        "health_state": health_state,
        "load_errors": errors,
    }


def validate_graph(data: dict[str, Any]) -> list[str]:
    errors = list(data["load_errors"])
    nodes = data["nodes"]
    profiles = data["profiles"]

    grave_patterns = [
        g["match_pattern"].lower()
        for bucket in ("cloud", "local")
        for g in data["graveyard"].get(bucket, [])
        if g.get("match_pattern")
    ]

    for nid, node in nodes.items():
        for req in ("kind", "name", "lifecycle", "decay_class", "last_verified", "url", "gotchas"):
            if req not in node:
                errors.append(f"[node:{nid}] missing required field '{req}'")
        if node.get("kind") not in VALID_KINDS:
            errors.append(f"[node:{nid}] invalid kind '{node.get('kind')}'")
        if node.get("lifecycle") not in VALID_LIFECYCLES:
            errors.append(f"[node:{nid}] invalid lifecycle '{node.get('lifecycle')}'")
        if node.get("decay_class") not in VALID_DECAY:
            errors.append(f"[node:{nid}] invalid decay_class '{node.get('decay_class')}'")
        if not isinstance(node.get("gotchas"), list) or not node["gotchas"]:
            errors.append(f"[node:{nid}] must list at least one gotcha")
        try:
            date.fromisoformat(str(node.get("last_verified", "")))
        except ValueError:
            errors.append(f"[node:{nid}] invalid ISO date last_verified='{node.get('last_verified')}'")

        errors.extend(_check_canonical_url(node.get("url"), f"node:{nid}"))
        errors.extend(_find_leaks(node, f"node:{nid}"))

        edges = node.get("edges", {})
        for pid in edges.get("runs_on", []):
            if pid not in profiles:
                errors.append(f"[node:{nid}] edge.runs_on references unknown profile '{pid}'")
        for target in edges.get("adapts", []):
            if target not in nodes:
                errors.append(f"[node:{nid}] edge.adapts references unknown node '{target}'")
        for target in edges.get("guards", []):
            if target not in nodes and target != "*":
                errors.append(f"[node:{nid}] edge.guards references unknown node '{target}'")

        if node.get("lifecycle") not in ("monitor-only", "graveyard"):
            searchable = json.dumps({
                "id": nid,
                "name": node.get("name"),
                "url": node.get("url"),
                "default_model": node.get("default_model", ""),
            }).lower()
            for pat in grave_patterns:
                if pat in searchable:
                    errors.append(f"[node:{nid}] violates Graveyard ban '{pat}'")

    for intent, route in data["forage_routes"].items():
        for ref in route.get("chain", []):
            if ref not in nodes:
                errors.append(f"[route:{intent}] references unknown node '{ref}'")

    for pid, pb in data["playbooks"].items():
        for req in ("title", "verdict", "last_verified", "decay_class", "constraints", "workflow", "gotchas"):
            if req not in pb:
                errors.append(f"[playbook:{pid}] missing required field '{req}'")
        errors.extend(_find_leaks(pb, f"playbook:{pid}"))
        for ref in pb.get("pin_nodes", []):
            if ref not in nodes:
                errors.append(f"[playbook:{pid}] pin_nodes references unknown node '{ref}'")
        for tool in pb.get("domain_tools", []):
            tid = tool.get("id", "missing")
            errors.extend(_check_canonical_url(tool.get("url"), f"playbook:{pid}:tool:{tid}"))

    for sid, sp in data["spokes"].items():
        for req in ("title", "verdict", "last_verified", "constraints", "entry_points", "upstream_hub", "guardrails"):
            if req not in sp:
                errors.append(f"[spoke:{sid}] missing required field '{req}'")
        errors.extend(_find_leaks(sp, f"spoke:{sid}"))
        entries = sp.get("entry_points", [])
        if len(entries) > BUDGETS["max_spoke_entry_points"]:
            errors.append(
                f"[spoke:{sid}] exceeds budget: {len(entries)} entry_points > max {BUDGETS['max_spoke_entry_points']}"
            )
        for ep in entries:
            errors.extend(_check_canonical_url(ep.get("url"), f"spoke:{sid}:entry:{ep.get('id', 'missing')}"))
        hub = sp.get("upstream_hub", {})
        errors.extend(_check_canonical_url(hub.get("url"), f"spoke:{sid}:upstream_hub"))

    frontier = data["radar"]["frontier"]
    community = data["radar"]["community"]
    if len(frontier) > BUDGETS["max_radar_frontier"]:
        errors.append(f"[radar:frontier] exceeds cap: {len(frontier)} > {BUDGETS['max_radar_frontier']}")
    if len(community) > BUDGETS["max_radar_community"]:
        errors.append(f"[radar:community] exceeds cap: {len(community)} > {BUDGETS['max_radar_community']}")
    for bucket, items in (("frontier", frontier), ("community", community)):
        for item in items:
            iid = item.get("id", "missing")
            errors.extend(_check_canonical_url(item.get("url"), f"radar:{bucket}:{iid}"))
            errors.extend(_find_leaks(item, f"radar:{bucket}:{iid}"))

    for bucket in ("cloud", "local"):
        for g in data["graveyard"].get(bucket, []):
            rep = g.get("replaced_by")
            if rep and rep not in nodes:
                errors.append(f"[graveyard:{bucket}] replaced_by '{rep}' not found in core nodes")

    return errors
