# Changelog

## [5.0.0-beta.1] - 2026-11-27
### Changed
- Rebuilt around six upstreamed standards: **Diataxis** documentation structure (`docs/`, `guides/`, `reference/`, `research/`, `STATUS.md`), Tufte data-ink restraint (zero jargon on the front page, quiet health telemetry, max 3 conceptual diagrams), explicit scientific **Evidence Tiers**, typed Python packaging (`src/swissknife/` + `pyproject.toml`), automated `unittest` suite (including full-repo internal link crawling), and GitHub issue forms.
- Upgraded Google AI Studio free tier default to `gemini-4-hydrogen` (1M unified context, 4 thinking levels, implicit-only caching, HTTP 400 gotchas) and restored Coding Agent Token Math (`~300K tokens/task`).
- Added Ollama 4K default context trap & `/v1` hang warning alongside Apple Silicon `mlx_lm.server` launch commands in `guides/local-ai-workstation.md`.
- Expanded `research/harness-adapters.md` to distinguish vendor vs. reproduced HF evaluations (`39% -> 55%` TB2.1, `2.9K -> 1.5K` tokens/task), include the 4-arm TB2.1 difficulty ablation, and include the 300-task `AutomationBench` out-of-distribution control table.
- Fixed live-health tracking so supporting guide tools and specialist upstream directories appear in `STATUS.md` and rolling digests, enforced retirement bans globally, removed unused `edges.supersedes`, and added `--root` CLI support.

## [4.0.0-beta] - 2026-11-27
- Initial 7-file Hub-and-Spoke headless graph experiment.

## [2.0.0-beta.1] - 2026-11-26
- Unified Field Book and CI drift gate.

## [1.0.0-core] - 2026-11-08
- Initial Cloud API directory.
