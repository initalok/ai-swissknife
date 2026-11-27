#!/usr/bin/env python3
"""
AI Swiss Knife v4-beta Unified CLI
Commands:
  python scripts/cli.py validate
  python scripts/cli.py health [--as-of YYYY-MM-DD] [--probe N] [--dry-run]
  python scripts/cli.py resolve <horizon_id> [--profile zero-card-cloud|16vram-64ram|mac-apple-silicon] [--as-of YYYY-MM-DD]
  python scripts/cli.py snapshot [--out dist/graph.json] [--as-of YYYY-MM-DD]
  python scripts/cli.py build [--as-of YYYY-MM-DD]
  python scripts/cli.py digest [--as-of YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.store import load_graph, validate_graph
from core.health import run_lru_probe
from core.state import evaluate_implicit_state, resolve_horizon, build_graph_snapshot
from surfaces import github_views, agent_views


def _parse_date(val: str | None) -> date | None:
    return date.fromisoformat(val) if val else None


def _emit(payload: dict, exit_code: int = 0) -> None:
    print(json.dumps(payload, indent=2))
    sys.exit(exit_code)


def main() -> None:
    p = argparse.ArgumentParser(prog="ai-swissknife-v4")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate")

    h = sub.add_parser("health")
    h.add_argument("--as-of", default=None)
    h.add_argument("--probe", type=int, default=0)
    h.add_argument("--dry-run", action="store_true")

    r = sub.add_parser("resolve")
    r.add_argument("horizon_id")
    r.add_argument("--profile", default=None)
    r.add_argument("--as-of", default=None)
    r.add_argument("--include-stale", action="store_true")

    s = sub.add_parser("snapshot")
    s.add_argument("--out", default="dist/graph.json")
    s.add_argument("--as-of", default=None)

    b = sub.add_parser("build")
    b.add_argument("--as-of", default=None)

    d = sub.add_parser("digest")
    d.add_argument("--as-of", default=None)

    args = p.parse_args()
    data = load_graph(".")

    if args.cmd == "validate":
        errs = validate_graph(data)
        _emit({"valid": not errs, "error_count": len(errs), "errors": errs}, 0 if not errs else 1)

    if args.cmd == "health":
        out = evaluate_implicit_state(data, as_of=_parse_date(args.as_of))
        if args.probe > 0:
            out["probe"] = run_lru_probe(data, limit=args.probe, dry_run=args.dry_run)
        _emit({"as_of": out["as_of"], "digest": out["digest"], "probe": out.get("probe")})

    if args.cmd == "resolve":
        _emit(resolve_horizon(data, args.horizon_id, profile_id=args.profile, as_of=_parse_date(args.as_of), include_stale=args.include_stale))

    if args.cmd == "snapshot":
        errs = validate_graph(data)
        if errs:
            _emit({"valid": False, "errors": errs}, 1)
        snap = build_graph_snapshot(data, as_of=_parse_date(args.as_of))
        out_dir = os.path.dirname(args.out)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(snap, f, indent=2)
        _emit({"written": args.out, "counts": snap["counts"], "digest": snap["digest"]})

    if args.cmd == "build":
        errs = validate_graph(data)
        if errs:
            _emit({"valid": False, "error_count": len(errs), "errors": errs}, 1)
        snap = build_graph_snapshot(data, as_of=_parse_date(args.as_of))
        github_views.render(snap, ".")
        agent_views.render(snap, ".")
        _emit({"built": True, "counts": snap["counts"], "digest": snap["digest"]})

    if args.cmd == "digest":
        st = evaluate_implicit_state(data, as_of=_parse_date(args.as_of))
        dig = st["digest"]
        lines = [
            f"## 🩺 AI Swiss Knife Live Health Digest (`{st['as_of']}`)",
            "",
            f"- **Aging (>=75% TTL):** {len(dig['aging'])}",
            f"- **Stale (Auto-excluded from `llms.txt`):** {len(dig['stale'])}",
            f"- **Re-Verify Upstream (Transitive Alert):** {len(dig['reverify_upstream'])}",
            f"- **Degraded (Archived or >=3 fails):** {len(dig['degraded'])}",
            f"- **Graveyard Candidates:** {len(dig['graveyard_candidates'])}",
            "",
        ]
        for bucket in ("graveyard_candidates", "degraded", "reverify_upstream", "stale", "aging"):
            if dig[bucket]:
                lines.append(f"### `{bucket}`")
                for item in dig[bucket]:
                    lines.append(f"- `{item['id']}` — `{json.dumps(item)}`")
                lines.append("")
        print("\n".join(lines))
        sys.exit(0)


if __name__ == "__main__":
    main()
