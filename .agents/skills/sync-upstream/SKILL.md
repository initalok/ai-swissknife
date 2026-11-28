---
name: sync-upstream
description: Triage health/deltas.json release updates, ADR review flags, and stale entries into a clean human-reviewable Draft PR.
---

# Sync Upstream Workflow

Use this skill when the maintainer asks to process `health/deltas.json` or refresh stale/updated upstream anchors.

## Rules
1. Never auto-merge changes to `main`. Always work on a dedicated branch and prepare a Draft PR for human review.
2. Read `health/deltas.json` first (`release_updates`, `decision_reviews`, `degraded`, `stale`, `retirement_candidates`).
3. For each `release_updates` item, fetch the upstream GitHub release notes or official changelog and verify whether recipes, limitations, or `last_reviewed_release` need updating in `catalog/registry/*.yaml`.
4. For any `decision_reviews` item, check its explicit `reversal_trigger` in `catalog/decisions/*.yaml`:
   - If the trigger has NOT tripped, refresh `last_verified` on the anchor after confirming current behavior.
   - If the trigger HAS tripped, update the relevant Slot pointer in `catalog/registry/slots.yaml`, add a new Decision Record, mark the old ADR `status: superseded` with `superseded_by`, and add deprecated patterns to `catalog/registry/specialists_watch_retired.yaml`.
5. Never hand-edit inside `<!-- swissknife:begin ... -->` ... `<!-- swissknife:end -->` regions, `STATUS.md`, `llms*.txt`, or `dist/catalog.json`.
6. Run the verification gate before opening the Draft PR:
   ```bash
   python -m unittest discover -s tests -t . -v
   swissknife validate
   swissknife sync
   ```
