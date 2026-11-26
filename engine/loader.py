from __future__ import annotations

import glob
import json
import os
import re
from datetime import date
from typing import Any
import yaml

VALID_KINDS = {"gateway", "model", "adapter", "harness", "tool", "mcp"}
VALID_LIFECYCLES = {"mature", "experimental", "operational", "monitor-only", "deprecated", "graveyard"}
VALID_DECAY = {"volatile", "operational", "stable"}
PRESENTATION_LEAK_RE = re.compile(r"(<br\s*/?>|</?sub>|</?kbd>|<details>|```)", re.IGNORECASE)


def _load_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _find_presentation_leaks(obj: Any, path: str = "") -> list[str]:
    leaks: list[str] = []
    if isinstance(obj, str):
        if PRESENTATION_LEAK_RE.search(obj):
            leaks.append(f"Presentation HTML/Markdown leak at '{path}'")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            leaks.extend(_find_presentation_leaks(v, f"{path}.{k}" if path else str(k)))
    elif isinstance(obj, list):
        for idx, v in enumerate(obj):
            leaks.extend(_find_presentation_leaks(v, f"{path}[{idx}]"))
    return leaks


def load_workspace(root: str = ".") -> dict[str, Any]:
    entities: dict[str, dict[str, Any]] = {}
    packs: dict[str, dict[str, Any]] = {}
    feeds: dict[str, dict[str, Any]] = {}
    graveyard: dict[str, list[dict[str, Any]]] = {"cloud": [], "local": []}
    forage_routes: dict[str, dict[str, Any]] = {}
    errors: list[str] = []

    grave_path = os.path.join(root, "entities", "graveyard.yaml")
    if os.path.exists(grave_path):
        g_raw = _load_yaml(grave_path)
        graveyard["cloud"] = g_raw.get("cloud", [])
        graveyard["local"] = g_raw.get("local", [])

    for path in sorted(glob.glob(os.path.join(root, "entities", "*.yaml"))):
        if os.path.basename(path) == "graveyard.yaml":
            continue
        raw = _load_yaml(path)
        if "forage_routes" in raw:
            forage_routes.update(raw["forage_routes"])
        for item in raw.get("entities", []):
            eid = item.get("id")
            if not eid:
                errors.append(f"{path}: entity missing 'id'")
                continue
            if eid in entities:
                errors.append(f"{path}: duplicate entity id '{eid}'")
                continue
            item["_source"] = os.path.relpath(path, root)
            entities[eid] = item

    for path in sorted(glob.glob(os.path.join(root, "packs", "*.yaml"))):
        pack = _load_yaml(path)
        pid = pack.get("id")
        if not pid:
            errors.append(f"{path}: pack missing 'id'")
            continue
        if pid in packs:
            errors.append(f"{path}: duplicate pack id '{pid}'")
            continue
        pack["_source"] = os.path.relpath(path, root)
        packs[pid] = pack

    for path in sorted(glob.glob(os.path.join(root, "feeds", "*.yaml"))):
        feed = _load_yaml(path)
        fid = feed.get("id")
        if not fid:
            errors.append(f"{path}: feed missing 'id'")
            continue
        feed["_source"] = os.path.relpath(path, root)
        feeds[fid] = feed

    health_path = os.path.join(root, "health", "state.json")
    health_state = {}
    if os.path.exists(health_path):
        with open(health_path, "r", encoding="utf-8") as f:
            health_state = json.load(f)

    return {
        "entities": entities,
        "packs": packs,
        "feeds": feeds,
        "graveyard": graveyard,
        "forage_routes": forage_routes,
        "health_state": health_state,
        "load_errors": errors,
    }


def validate_workspace(ws: dict[str, Any]) -> list[str]:
    errors = list(ws["load_errors"])
    entities = ws["entities"]
    grave_patterns = [
        g["match_pattern"].lower()
        for bucket in ("cloud", "local")
        for g in ws["graveyard"].get(bucket, [])
        if g.get("match_pattern")
    ]

    for eid, ent in entities.items():
        for req in ("kind", "name", "lifecycle", "decay_class", "last_verified", "gotchas"):
            if req not in ent:
                errors.append(f"[entity:{eid}] missing required field '{req}'")
        if ent.get("kind") not in VALID_KINDS:
            errors.append(f"[entity:{eid}] invalid kind '{ent.get('kind')}'")
        if ent.get("lifecycle") not in VALID_LIFECYCLES:
            errors.append(f"[entity:{eid}] invalid lifecycle '{ent.get('lifecycle')}'")
        if ent.get("decay_class") not in VALID_DECAY:
            errors.append(f"[entity:{eid}] invalid decay_class '{ent.get('decay_class')}'")
        if not isinstance(ent.get("gotchas"), list) or not ent["gotchas"]:
            errors.append(f"[entity:{eid}] must provide at least one gotcha")
        try:
            date.fromisoformat(str(ent.get("last_verified", "")))
        except ValueError:
            errors.append(f"[entity:{eid}] invalid ISO date last_verified='{ent.get('last_verified')}'")

        base_ref = ent.get("base_ref")
        if base_ref and base_ref not in entities:
            errors.append(f"[entity:{eid}] base_ref '{base_ref}' not found in entities")
        for h_ref in ent.get("compatible_harnesses", []):
            if h_ref not in entities:
                errors.append(f"[entity:{eid}] compatible_harness '{h_ref}' not found in entities")

        errors.extend(_find_presentation_leaks(ent, f"entity:{eid}"))

        if ent.get("lifecycle") not in ("monitor-only", "graveyard"):
            searchable = json.dumps({
                "id": eid,
                "name": ent.get("name"),
                "urls": ent.get("urls", {}),
                "default_model": ent.get("default_model", ""),
            }).lower()
            for pat in grave_patterns:
                if pat in searchable:
                    errors.append(f"[entity:{eid}] violates Graveyard ban '{pat}'")

    for intent, route in ws["forage_routes"].items():
        for ref in route.get("chain", []):
            if ref not in entities:
                errors.append(f"[forage:{intent}] references unknown entity '{ref}'")
            elif entities[ref].get("lifecycle") == "graveyard":
                errors.append(f"[forage:{intent}] references graveyard entity '{ref}'")

    for pid, pack in ws["packs"].items():
        for req in ("title", "category", "lifecycle", "decay_class", "last_verified", "verdict", "stack", "gotchas"):
            if req not in pack:
                errors.append(f"[pack:{pid}] missing required field '{req}'")
        errors.extend(_find_presentation_leaks(pack, f"pack:{pid}"))
        for role, refs in pack.get("stack", {}).items():
            for ref in refs:
                if ref not in entities:
                    errors.append(f"[pack:{pid}] stack.{role} references unknown entity '{ref}'")
                elif entities[ref].get("lifecycle") == "graveyard":
                    errors.append(f"[pack:{pid}] stack.{role} references graveyard entity '{ref}'")

    for fid, feed in ws["feeds"].items():
        errors.extend(_find_presentation_leaks(feed, f"feed:{fid}"))
        for item in feed.get("items", []):
            iid = item.get("id", "missing-id")
            for req in ("id", "name", "lifecycle", "decay_class", "last_verified", "gotchas"):
                if req not in item:
                    errors.append(f"[feed:{fid}:{iid}] missing required field '{req}'")
            try:
                date.fromisoformat(str(item.get("last_verified", "")))
            except ValueError:
                errors.append(f"[feed:{fid}:{iid}] invalid ISO date last_verified")

    return errors
