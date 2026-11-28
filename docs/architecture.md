---
title: "How This Guide Is Maintained"
section: docs
summary: "Maintainer handbook: single-source in-place managed blocks, auto-discovered registry, upstream release momentum watchers, and the sync-upstream agent skill."
order: 6
---

[Home](../README.md) / Orientation / How This Guide Is Maintained

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# How This Guide Is Maintained

This page is for contributors and maintainers. Everyday readers do not need to understand these internals to use the handbook.

## Open-Closed Design (Zero Python Edits to Expand)

1. **Single-Source In-Place Managed Blocks:** Every Markdown file lives in **one place** (`README.md`, `docs/`, `worlds/`, `guides/`, `reference/`, `research/`). Humans write and edit timeless prose directly in the live file; `swissknife sync` deterministically refreshes only fenced `<!-- swissknife:begin ... -->` regions. Adding a new guide or 2027 domain requires creating one Markdown file with YAML frontmatter—zero Python edits.
2. **Auto-Discovered Registry (`catalog/registry/**/*.yaml`):** Dropping a new domain YAML file into `catalog/registry/` or a new ADR into `catalog/decisions/` is automatically validated and exposed to every page and CLI query.
3. **Half-Life Decoupling via Workflow Slots:** Follow-along guides reference stable role slots (`catalog/registry/slots.yaml`) rather than hardcoding volatile tool names across six files. Swapping one slot winner fast-forwards every guide atomically.
4. **Liveness + Forward Momentum Watchers:** Twice weekly, CI checks canonical URLs for 404s/archives **and** tracks GitHub `releases/latest` tags and Hugging Face collections, writing actionable queues to `health/deltas.json` and [`STATUS.md`](../STATUS.md). When a breaking release or stale anchor hits an accepted ADR, it is automatically flagged for human review.
5. **Human-in-the-Loop Upstream Triage:** Run the repo's `.agents/skills/sync-upstream/SKILL.md` skill inside `Pi`, `OpenCode`, or `Antigravity` to read `health/deltas.json`, inspect upstream release notes, and open a clean Draft PR—keeping human judgment as the final merge gate.

Example managed-block syntax (ignored by the syncer when inside fenced code blocks):

```markdown
<!-- swissknife:begin slot id=dev-harness -->
<!-- swissknife:end -->
```

## Non-Goals Enforced by Governance

<!-- swissknife:begin non-goals -->
- No enterprise GPU cluster orchestration (multi-node Kubernetes/Slurm farms or commercial MLOps stacks).
- No brute-force mobile LLM inference (phones are documented strictly as human communicators, HITL gates, and capture surfaces).
- No paid-only SaaS directories (closed paid frontier models live only on the 21-day monitor-only Watch List).
- No custom benchmarking or smoke-test frameworks (rely on primary evaluations and 1-line upstream built-in sanity checks).
- No mirroring upstream installation manuals (own curated paths, cross-tool glue, real-world traps, and canonical upstream deep-links).
- No museum of legacy options (one active anchor per Workflow Slot; superseded picks move cleanly to Retired and Superseded ADR history).
<!-- swissknife:end -->

## Local Maintainer Commands

```bash
pip install -e .
python -m unittest discover -s tests -t . -v
swissknife validate
swissknife sync
swissknife deltas
```

---

**Continue reading:** [Contributing Guidelines](../CONTRIBUTING.md) · [System Status](../STATUS.md)
