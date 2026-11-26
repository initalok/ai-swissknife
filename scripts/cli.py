#!/usr/bin/env python3
"""
AI Swiss Knife v3-modular Unified CLI
Commands:
  python scripts/cli.py validate
  python scripts/cli.py health [--as-of YYYY-MM-DD] [--sweep N] [--dry-run]
  python scripts/cli.py query pack <pack_id> [--as-of YYYY-MM-DD] [--include-stale]
  python scripts/cli.py query cloud <intent> [--as-of YYYY-MM-DD] [--include-stale]
  python scripts/cli.py query local [entity_id] [--lifecycle mature|experimental] [--as-of YYYY-MM-DD]
  python scripts/cli.py snapshot [--out dist/registry.json] [--as-of YYYY-MM-DD]
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

from engine.loader import load_workspace, validate_workspace
from engine.health import evaluate_workspace_health, run_lru_sweep
from engine.forager import resolve_pack, forage_cloud, forage_local, build_snapshot
from renderers import github_book, agent_views


def _parse_date(val: str | None) -> date | None:
    return date.fromisoformat(val) if val else None


def _emit(payload: dict, exit_code: int = 0) -> None:
    print(json.dumps(payload, indent=2))
    sys.exit(exit_code)


def main() -> None:
    p = argparse.ArgumentParser(prog="ai-swissknife")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate")

    h = sub.add_parser("health")
    h.add_argument("--as-of", default=None)
    h.add_argument("--sweep", type=int, default=0)
    h.add_argument("--dry-run", action="store_true")

    q = sub.add_parser("query")
    q_sub = q.add_subparsers(dest="qtype", required=True)

    qp = q_sub.add_parser("pack")
    qp.add_argument("pack_id")
    qp.add_argument("--as-of", default=None)
    qp.add_argument("--include-stale", action="store_true")

    qc = q_sub.add_parser("cloud")
    qc.add_argument("intent")
    qc.add_argument("--as-of", default=None)
    qc.add_argument("--include-stale", action="store_true")

    ql = q_sub.add_parser("local")
    ql.add_argument("entity_id", nargs="?", default=None)
    ql.add_argument("--lifecycle", choices=["mature", "experimental"], default=None)
    ql.add_argument("--as-of", default=None)
    ql.add_argument("--include-stale", action="store_true")

    s = sub.add_parser("snapshot")
    s.add_argument("--out", default="dist/registry.json")
    s.add_argument("--as-of", default=None)

    b = sub.add_parser("build")
    b.add_argument("--as-of", default=None)

    d = sub.add_parser("digest")
    d.add_argument("--as-of", default=None)

    args = p.parse_args()
    ws = load_workspace(".")

    if args.cmd == "validate":
        errs = validate_workspace(ws)
        _emit({"valid": not errs, "error_count": len(errs), "errors": errs}, 0 if not errs else 1)

    if args.cmd == "health":
        out = evaluate_workspace_health(ws, as_of=_parse_date(args.as_of))
        if args.sweep > 0:
            out["sweep"] = run_lru_sweep(ws, limit=args.sweep, dry_run=args.dry_run)
        _emit(out)

    if args.cmd == "query":
        as_of = _parse_date(args.as_of)
        if args.qtype == "pack":
            _emit(resolve_pack(ws, args.pack_id, as_of=as_of, include_stale=args.include_stale))
        elif args.qtype == "cloud":
            _emit(forage_cloud(ws, args.intent, as_of=as_of, include_stale=args.include_stale))
        elif args.qtype == "local":
            _emit(forage_local(ws, args.entity_id, lifecycle=args.lifecycle, as_of=as_of, include_stale=args.include_stale))

    if args.cmd == "snapshot":
        errs = validate_workspace(ws)
        if errs:
            _emit({"valid": False, "errors": errs}, 1)
        snap = build_snapshot(ws, as_of=_parse_date(args.as_of))
        out_dir = os.path.dirname(args.out)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(snap, f, indent=2)
        _emit({"written": args.out, "counts": snap["counts"], "digest": snap["digest"]})

    if args.cmd == "build":
        errs = validate_workspace(ws)
        if errs:
            _emit({"valid": False, "errors": errs}, 1)
        snap = build_snapshot(ws, as_of=_parse_date(args.as_of))
        github_book.render(snap, ".")
        agent_views.render(snap, ".")
        _emit({"built": True, "counts": snap["counts"], "digest": snap["digest"]})

    if args.cmd == "digest":
        h_out = evaluate_workspace_health(ws, as_of=_parse_date(args.as_of))
        dig = h_out["digest"]
        lines = [
            f"## 🩺 AI Swiss Knife Rolling Health Digest (`{h_out['as_of']}`)",
            "",
            f"- **Aging (>=75% TTL):** {len(dig['aging'])}",
            f"- **Stale (Auto-excluded from `llms.txt`):** {len(dig['stale'])}",
            f"- **Degraded (Archived or >=3 HTTP fails):** {len(dig['degraded'])}",
            f"- **Graveyard Candidates:** {len(dig['graveyard_candidates'])}",
            "",
        ]
        for bucket in ("graveyard_candidates", "degraded", "stale", "aging"):
            if dig[bucket]:
                lines.append(f"### `{bucket}`")
                for item in dig[bucket]:
                    lines.append(f"- `{item['id']}` — {json.dumps(item)}")
                lines.append("")
        print("\n".join(lines))
        sys.exit(0)


if __name__ == "__main__":
    main()
