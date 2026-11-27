from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from swissknife.health import run_lru_probe
from swissknife.renderers.agent import AgentRenderer
from swissknife.renderers.diataxis import DiataxisRenderer
from swissknife.resolver import build_snapshot, evaluate_state, resolve_target
from swissknife.store import load_catalog
from swissknife.validate import validate_catalog


def _parse_date(val: str | None) -> date | None:
    return date.fromisoformat(val) if val else None


def _emit(payload: dict[str, Any], code: int = 0) -> None:
    print(json.dumps(payload, indent=2))
    sys.exit(code)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="swissknife", description="AI Swiss Knife Headless Core CLI")
    parser.add_argument("--root", default=".", help="Repository root directory")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate")

    h = sub.add_parser("health")
    h.add_argument("--as-of", default=None)
    h.add_argument("--probe", type=int, default=0)
    h.add_argument("--dry-run", action="store_true")

    r = sub.add_parser("resolve")
    r.add_argument("target_id")
    r.add_argument("--profile", default=None)
    r.add_argument("--as-of", default=None)
    r.add_argument("--include-stale", action="store_true")

    s = sub.add_parser("snapshot")
    s.add_argument("--out", default="dist/catalog.json")
    s.add_argument("--as-of", default=None)

    b = sub.add_parser("build")
    b.add_argument("--as-of", default=None)

    d = sub.add_parser("digest")
    d.add_argument("--as-of", default=None)

    args = parser.parse_args(argv)
    root = Path(args.root)
    catalog = load_catalog(root)

    if args.cmd == "validate":
        errs = validate_catalog(catalog)
        _emit({"valid": not errs, "error_count": len(errs), "errors": errs}, 0 if not errs else 1)

    if args.cmd == "health":
        st = evaluate_state(catalog, as_of=_parse_date(args.as_of))
        out: dict[str, Any] = {"as_of": st["as_of"], "digest": st["digest"]}
        if args.probe > 0:
            out["probe"] = run_lru_probe(catalog, root=root, limit=args.probe, dry_run=args.dry_run)
        _emit(out)

    if args.cmd == "resolve":
        _emit(
            resolve_target(
                catalog,
                args.target_id,
                profile_id=args.profile,
                as_of=_parse_date(args.as_of),
                include_stale=args.include_stale,
            )
        )

    if args.cmd == "snapshot":
        errs = validate_catalog(catalog)
        if errs:
            _emit({"valid": False, "error_count": len(errs), "errors": errs}, 1)
        snap = build_snapshot(catalog, as_of=_parse_date(args.as_of))
        out_path = root / args.out
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(snap, indent=2) + "\n", encoding="utf-8")
        _emit({"written": str(out_path), "counts": snap["counts"], "digest": snap["digest"]})

    if args.cmd == "build":
        errs = validate_catalog(catalog)
        if errs:
            _emit({"valid": False, "error_count": len(errs), "errors": errs}, 1)
        snap = build_snapshot(catalog, as_of=_parse_date(args.as_of))
        written: list[str] = []
        for renderer in (DiataxisRenderer(), AgentRenderer()):
            written.extend(str(p) for p in renderer.render(snap, root))
        _emit({"built": True, "files_written": len(written), "counts": snap["counts"], "digest": snap["digest"]})

    if args.cmd == "digest":
        st = evaluate_state(catalog, as_of=_parse_date(args.as_of))
        dig = st["digest"]
        lines = [
            f"## Live Health & Freshness Digest ({st['as_of']})",
            "",
            "Automated twice-weekly audit of canonical URLs, upstream repository activity, and review windows.",
            "",
            f"- **Approaching review window (75%+):** {len(dig['aging'])}",
            f"- **Needs re-verification (excluded from `llms.txt`):** {len(dig['stale'])}",
            f"- **Upstream dependency changed:** {len(dig['reverify-upstream'])}",
            f"- **Degraded (archived or unreachable):** {len(dig['degraded'])}",
            f"- **Retirement candidates:** {len(dig['retirement_candidates'])}",
            "",
        ]
        for bucket, label in (
            ("retirement_candidates", "Retirement Candidates"),
            ("degraded", "Degraded Links / Archived Repos"),
            ("reverify-upstream", "Upstream Dependency Alerts"),
            ("stale", "Expired Review Window"),
            ("aging", "Approaching Review Window"),
        ):
            if dig[bucket]:
                lines.append(f"### {label}")
                for item in dig[bucket]:
                    lines.append(f"- `{item['id']}` — `{json.dumps(item)}`")
                lines.append("")
        print("\n".join(lines))
        sys.exit(0)


if __name__ == "__main__":
    main()
