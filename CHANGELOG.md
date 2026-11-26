# Changelog

## [2.1.0] - 2026-11-26
### Added
- Split `Ch 02` Local AI into **Track A: Mature & Fully Riced** (`Qwen3.8-27B` + HF Harness Adapters, `Qwen3-Coder-Next`, `Gemma 4`) vs. **Track B: Cutting-Edge Local** (`Inkling 2 Mini`, `varloop`, `Qwen3.8-Flash-Next`, `DiffusionGemma`, `Muse Glimmer`), with `track` tags in `forage --local`.
- Restructured `Ch 04` Harnesses around **`Pi` / `Pi Durable`** (Building-Block Kernel), **`DeepSeek Harness` (`dsh`)** (Cordis Plugin Platform), and **`Hermes Agent` (`v0.23.4`)** (Self-Improving Daemon).
- Deepened `Ch 06` with the complete Hugging Face Harness Adapters & In-Harness RL recipe (`OpenEnv`, `Repo2RLEnv`/`Tasksmith`, `AsyncGRPOTrainer`, `safeagents`, specialist vs. rank-96 super-adapter, cross-harness transfer, thinking leakage, & MOPD).
- Added **Part III · Field & Horizon**: **`Ch 07 · Community Field Notes (IRL Builds)`** (`Basalt`, `RustingStrata`, `pecera-engine`, `obra/superpowers`, `pi-subagents-community`, `dsh-toolbox`, Hermes SRE/Obsidian/digest ops, `WanGP Showrunner`, `Hy-Nomas` + `LTX-2.5`, `CADMAGEDDON`) and **`Ch 08 · Frontier Watch`** (`monitor_only: true` apex radar for `Claude Fable/Mythos 5.2`, `GPT-6.2 Astra/Sol`, `Gemini 4 Carbon`, `Qwen4-Max 2.4T`, `DeepSeek-V4.1`).
- Expanded `.github/workflows/ci_lint.yml` to run automatically on all `v2*` branches.

## [2.0.0-beta.1] - 2026-11-26
### Added
- Unified 6-Chapter + Graveyard Field Book (`README.md`, `book/01..06`, `book/99-graveyard.md`, `llms.txt`, `llms-full.txt`), 5-Beat compiler, and CI drift gate.

## [1.0.0-core] - 2026-11-08
### Added
- Initial Cloud API directory (`README.md`, `llms.txt`, `scripts/build.py`).
