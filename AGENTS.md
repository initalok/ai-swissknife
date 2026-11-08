# AI Swiss Knife — Agent & Maintainer Schema Rules (Karpathy LLM Wiki Pattern)

This repository treats curated YAML files in `data/` as source code, `upstream/snapshots/` as raw immutable inputs, and `modules/*.md` + `README.md` as compiled artifacts.

## Core Operating Rules for AI Agents (Antigravity)
1. **Never manually edit `README.md` or `modules/*.md`.** Always edit `data/core_*.yaml` and run `python scripts/engine.py compile`.
2. **Relational Integrity:** Every `provider_id` referenced in `core_02`, `core_03`, or `core_04` MUST exist in `data/core_01_providers.yaml`.
3. **Always Lint Before Commit:** Run `python scripts/engine.py lint` before any `git commit`. Fix any broken provider references or schema violations.
4. **High-Signal Filter:**
   - Do not add dead endpoints (e.g., GitHub Models retired July 2026) or card-gated "free" tiers without flagging them.
   - Always record `bottleneck`, `effective_free_context`, `trains_on_data`, and `real_world_gotcha` in `core_01_providers.yaml`.
