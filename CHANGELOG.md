# Changelog

## [6.0.0] - 2026-11-28
### Changed
- Promoted **AI Swiss Knife `v6.0.0`** (GA), updating `pyproject.toml`, `swissknife.__version__`, and snapshot schema metadata to `6.0.0`.
- Rebuilt [`worlds/apple-silicon.md`](worlds/apple-silicon.md) around the **base 16GB M4 Mac mini 24/7 Remote AI Server** pattern (**`Rex`** + **`Pi`** + **`@earendil-works/pi-durable`** + **`nono v0.82.0`**) with a `<= 10 GB` local MLX budget (`Qwen3.5-9B`, `Gemma 4`).
- Replaced `reference/models-and-harnesses.md` with hardware-diverse [`reference/models.md`](reference/models.md) spanning Edge/16GB Mac, 16–24GB GPUs, Hybrid/80GB servers, Research-Leading Open Frontier weights (`DeepSeek-V4.1-Flash-1017`, `Mistral Large 4`, `Kimi-K3`), and specialized OCR/speech/video/diffusion checkpoints (folding runtimes into [`docs/start-here-developer.md`](docs/start-here-developer.md)).
- Upgraded the Watch List to a **3-bucket model** (`frontier <= 8`, `models <= 10` Model News & Development Radar, `community <= 8`), demoted `deepseek-harness` to `watch:community`, pruned `deerflow`, `pollinations`, `disler-durable-pi`, and `hy-nomas-worlds`, upgraded `nono` to `v0.82.0`, and added the 5-point production checklist, minimal Tailscale ACLs, external index/CLI traps, and parked Future Scope.
- Upgraded GitHub Actions workflows (`ci.yml`, `health.yml`) to Node-24 compatible `actions/checkout@v7` and `actions/setup-python@v7`.

## [6.0.0-beta.1] - 2026-11-27
### Changed
- Rebuilt on an **Open-Closed Handbook Architecture** using single-source **In-Place Managed Blocks** (`<!-- swissknife:begin ... -->`) so adding new domains, worlds, or guides requires zero Python edits while keeping live links, slots, recipes, tables, and decisions strictly synced.
- Introduced **Dual-Track Onboarding** (`docs/start-here-newcomer.md` vs. `docs/start-here-developer.md`), **4 Separated Compute Worlds + Personal AI Fabric** (`cloud`, `mac`, `gpu-pc`, `mobile-hitl` strictly as Human Communicator/HITL), an optional **6-Rung Pi Ricing Workshop**, **Persistent Context/Memory & Knowledge Loops**, **Unified Fabric Security & Trust Boundaries**, **Why This Stack ADRs** with falsifiable reversal triggers, and an explicit **Non-Goals Charter**.
- Upgraded health automation to **Liveness + Forward Momentum** (`probes.py` tracking GitHub `releases/latest` + breaking keywords and Hugging Face Collections) feeding `health/deltas.json` and an on-demand `.agents/skills/sync-upstream/SKILL.md` Draft PR workflow.

## [5.0.0-beta.1] - 2026-11-27
- Human-first Diataxis restructure, typed `src/swissknife/` package, Evidence Tiers, and full-repo link tests.
