# Changelog

## [2.0.0-beta.1] - 2026-11-26
### Added
- Reimagined repository into a unified **6-Chapter + Graveyard Field Book** (`README.md` One-Page Cover + `book/01..06-*.md` + `book/99-graveyard.md`).
- Dual machine-readable manifests: compact `llms.txt` router and complete `llms-full.txt` index.
- Unified **5-Beat Book Compiler** (`scripts/build.py`) with scoped Cloud/Local Graveyard linting and `--sync` support.
- **Google Gemini 4 Hydrogen** (Everyday, Thinking, & Task mode) across `Ch 01` and `Ch 04`.
- **Hugging Face Harness Adapters & In-Harness RL stack** (`Qwen3.8-27B` specialist + rank-96 super-adapter, `OpenEnv`, `Repo2RLEnv`/`Tasksmith`, `TRL AsyncGRPOTrainer`, `safeagents`, orthogonal LoRA merging) across `Ch 02`, `Ch 04`, and `Ch 06`.
- Healthy GitHub governance: `docs/DESIGN_SYSTEM.md`, `CONTRIBUTING.md`, PR drift-check CI (`ci_lint.yml`), and structured Issue/PR templates.

## [1.0.0-core] - 2026-11-08
### Added
- Initial progressive-density Cloud API directory (`README.md`, `llms.txt`, `scripts/build.py`, and upstream sync workflow).
