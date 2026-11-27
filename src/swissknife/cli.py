from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from swissknife.engine import build_snapshot, evaluate_workspace, query_entries, resolve_slot, resolve_specialist
from swissknife.probes import run_lru_probe
from swissknife.store import load_workspace
from swissknife.surfaces.agent import StatusAndAgentSurface
from swissknife.surfaces.blocks import ManagedBlockSyncer
from swissknife.validate import validate_workspace


def _parse_date(val: str | None) -> date | None:
    return date.fromisoformat(val) if val else None


def _emit(payload: dict[str, Any], code: int = 0) -> None:
    print(json.dumps(payload, indent=2))
    sys.exit(code)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="swissknife", description="AI Swiss Knife v6 Open-Closed Handbook CLI")
    parser.add_argument("--root", default=".", help="Repository root directory")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate")

    p = sub.add_parser("probe")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--dry-run", action="store_true")

    sl = sub.add_parser("slot")
    sl.add_argument("slot_id")
    sl.add_argument("--world", default=None)
    sl.add_argument("--as-of", default=None)
    sl.add_argument("--include-stale", action="store_true")

    sp = sub.add_parser("specialist")
    sp.add_argument("specialist_id")
    sp.add_argument("--world", default=None)
    sp.add_argument("--as-of", default=None)
    sp.add_argument("--include-stale", action="store_true")

    q = sub.add_parser("query")
    q.add_argument("--kind", default=None)
    q.add_argument("--world", default=None)
    q.add_argument("--tag", default=None)
    q.add_argument("--capability", default=None)
    q.add_argument("--privacy", choices=["any", "local-only"], default="any")
    q.add_argument("--include-stale", action="store_true")
    q.add_argument("--as-of", default=None)

    sn = sub.add_parser("snapshot")
    sn.add_argument("--out", default="dist/catalog.json")
    sn.add_argument("--deltas-out", default="health/deltas.json")
    sn.add_argument("--as-of", default=None)

    dl = sub.add_parser("deltas")
    dl.add_argument("--as-of", default=None)

    sy = sub.add_parser("sync")
    sy.add_argument("--as-of", default=None)

    dg = sub.add_parser("digest")
    dg.add_argument("--as-of", default=None)

    args = parser.parse_args(argv)
    root = Path(args.root)
    ws = load_workspace(root)

    if args.cmd == "validate":
        errs = validate_workspace(ws)
        _emit({"valid": not errs, "error_count": len(errs), "errors": errs}, 0 if not errs else 1)

    if args.cmd == "probe":
        _emit(run_lru_probe(ws, root=root, limit=args.limit, dry_run=args.dry_run))

    if args.cmd == "slot":
        _emit(resolve_slot(ws, args.slot_id, world=args.world, as_of=_parse_date(args.as_of), include_stale=args.include_stale))

    if args.cmd == "specialist":
        _emit(resolve_specialist(ws, args.specialist_id, world=args.world, as_of=_parse_date(args.as_of), include_stale=args.include_stale))

    if args.cmd == "query":
        _emit(
            query_entries(
                ws,
                kind=args.kind,
                world=args.world,
                tag=args.tag,
                capability=args.capability,
                privacy=args.privacy,
                eligible_only=not args.include_stale,
                as_of=_parse_date(args.as_of),
            )
        )

    if args.cmd == "deltas":
        st = evaluate_workspace(ws, as_of=_parse_date(args.as_of))
        _emit({"as_of": st["as_of"], "deltas": st["deltas"]})

    if args.cmd == "snapshot":
        errs = validate_workspace(ws)
        if errs:
            _emit({"valid": False, "error_count": len(errs), "errors": errs}, 1)
        snap = build_snapshot(ws, as_of=_parse_date(args.as_of))
        out_path = root / args.out
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(snap, indent=2) + "\n", encoding="utf-8")
        d_path = root / args.deltas_out
        d_path.parent.mkdir(parents=True, exist_ok=True)
        d_path.write_text(json.dumps({"as_of": snap["as_of"], "deltas": snap["deltas"]}, indent=2) + "\n", encoding="utf-8")
        _emit({"written": str(out_path), "deltas": str(d_path), "counts": snap["counts"]})

    if args.cmd == "sync":
        errs = validate_workspace(ws)
        if errs:
            _emit({"valid": False, "error_count": len(errs), "errors": errs}, 1)
        snap = build_snapshot(ws, as_of=_parse_date(args.as_of))
        written: list[str] = []
        for surface in (ManagedBlockSyncer(), StatusAndAgentSurface()):
            written.extend(str(p) for p in surface.sync(snap, root))
        _emit({"synced": True, "files_updated": len(written), "counts": snap["counts"], "deltas": snap["deltas"]})

    if args.cmd == "digest":
        st = evaluate_workspace(ws, as_of=_parse_date(args.as_of))
        d = st["deltas"]
        lines = [
            f"## Live Health & Upstream Momentum Digest ({st['as_of']})",
            "",
            "Twice-weekly automated audit of link liveness, upstream GitHub releases, HF collections, and ADR reversal triggers.",
            "",
            f"- **Upstream release updates:** {len(d['release_updates'])}",
            f"- **Decision records flagged for review:** {len(d['decision_reviews'])}",
            f"- **Upstream dependency alerts:** {len(d['reverify_upstream'])}",
            f"- **Expired review windows (excluded from `llms.txt`):** {len(d['stale'])}",
            f"- **Approaching review window (75%+):** {len(d['aging'])}",
            f"- **Degraded (archived or unreachable):** {len(d['degraded'])}",
            f"- **Retirement candidates:** {len(d['retirement_candidates'])}",
            "",
        ]
        for bucket, label in (
            ("release_updates", "Upstream Release Updates (Momentum)"),
            ("decision_reviews", "Decision Records Flagged for Review"),
            ("retirement_candidates", "Retirement Candidates"),
            ("degraded", "Degraded Links / Archived Repos"),
            ("reverify_upstream", "Upstream Dependency Alerts"),
            ("stale", "Expired Review Windows"),
            ("aging", "Approaching Review Window"),
        ):
            if d[bucket]:
                lines.append(f"### {label}")
                for item in d[bucket]:
                    lines.append(f"- `{json.dumps(item)}`")
                lines.append("")
        print("\n".join(lines))
        sys.exit(0)


if __name__ == "__main__":
    main()
