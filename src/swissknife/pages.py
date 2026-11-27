from __future__ import annotations

import re
import shlex
from pathlib import Path
from typing import Any
import yaml

from swissknife.models import ManagedBlock, PageDoc, Taxonomy

BEGIN_RE = re.compile(r"^\s*<!--\s*swissknife:begin\s+([a-z0-9-]+)(?:\s+(.*?))?\s*-->\s*$")
END_RE = re.compile(r"^\s*<!--\s*swissknife:end\s*-->\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def _parse_frontmatter(text: str, rel: str) -> tuple[dict[str, Any], str, list[str]]:
    if not text.startswith("---\n"):
        return {}, text, []
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text, [f"[page:{rel}] unclosed YAML frontmatter"]
    raw_fm = text[4:end]
    body = text[end + 5 :]
    try:
        parsed = yaml.safe_load(raw_fm) or {}
        if not isinstance(parsed, dict):
            return {}, body, [f"[page:{rel}] frontmatter must be a YAML mapping"]
        return parsed, body, []
    except yaml.YAMLError as exc:
        return {}, body, [f"[page:{rel}] invalid YAML frontmatter: {exc}"]


def _parse_kv_args(arg_str: str | None, owner: str) -> tuple[dict[str, str], list[str]]:
    if not arg_str or not arg_str.strip():
        return {}, []
    args: dict[str, str] = {}
    errors: list[str] = []
    try:
        tokens = shlex.split(arg_str)
    except ValueError as exc:
        return {}, [f"[{owner}] malformed directive arguments: {exc}"]
    for tok in tokens:
        if "=" not in tok:
            errors.append(f"[{owner}] directive arg '{tok}' must use key=value syntax")
            continue
        k, v = tok.split("=", 1)
        args[k.strip()] = v.strip()
    return args, errors


def scan_pages(root: Path, taxonomy: Taxonomy) -> tuple[list[PageDoc], list[str]]:
    pages: list[PageDoc] = []
    errors: list[str] = []

    candidates: list[Path] = []
    readme = root / "README.md"
    if readme.exists():
        candidates.append(readme)
    for sec_id in sorted(taxonomy.sections.keys()):
        sec_dir = root / sec_id
        if sec_dir.exists() and sec_dir.is_dir():
            candidates.extend(sorted(sec_dir.rglob("*.md")))

    for path in candidates:
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        fm, body, fm_errs = _parse_frontmatter(text, rel)
        errors.extend(fm_errs)

        blocks: list[ManagedBlock] = []
        in_fence = False
        open_block: tuple[str, dict[str, str], int] | None = None

        for lineno, line in enumerate(body.splitlines(), start=1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            m_begin = BEGIN_RE.match(line)
            if m_begin:
                if open_block is not None:
                    errors.append(f"[page:{rel}:{lineno}] nested swissknife:begin inside unclosed '{open_block[0]}'")
                    continue
                directive, raw_args = m_begin.group(1), m_begin.group(2)
                kv, arg_errs = _parse_kv_args(raw_args, f"page:{rel}:{lineno}")
                errors.extend(arg_errs)
                open_block = (directive, kv, lineno)
                continue

            if END_RE.match(line):
                if open_block is None:
                    errors.append(f"[page:{rel}:{lineno}] stray swissknife:end without matching begin")
                else:
                    blocks.append(ManagedBlock(directive=open_block[0], args=open_block[1], line=open_block[2]))
                    open_block = None

        if open_block is not None:
            errors.append(f"[page:{rel}:{open_block[2]}] unclosed swissknife:begin '{open_block[0]}'")

        pages.append(
            PageDoc(
                path=rel,
                title=str(fm.get("title", path.stem)),
                section=fm.get("section"),
                summary=str(fm.get("summary", "")),
                order=int(fm.get("order", 99)),
                track=fm.get("track"),
                world=fm.get("world"),
                blocks=blocks,
            )
        )

    return pages, errors
