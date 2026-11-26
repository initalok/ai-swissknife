# Changelog

## [3.0.0-modular] - 2026-11-26
### Changed
- Re-architected into a **Pace-Layered, Headless-First Entity + Pack Registry** (`engine/` + `renderers/` + `entities/` + `packs/` + `feeds/`).
- Separated `entities/` (atomic headless records with zero HTML/Markdown leaks) from 9 auto-discovered **Use-Case Specialist Packs** (`web-dev`, `app-dev`, `game-dev`, `reverse-eng`, `research`, `video-edit`, `social-media`, `promotion`, `uncensored`).
- Added **3-Tier Decay TTLs** (`volatile: 21d`, `operational: 60d`, `stable: 120d`), strict `eligible_for_agents` gating on `llms.txt`, and twice-weekly `N=25` rolling LRU health sweeps (`health_digest.yml`) feeding a single rolling GitHub Issue.
- Added Track A **Mature Riced** vs Track B **Cutting-Edge** local split, `Pi` + `DeepSeek Harness (dsh)` + `Hermes Agent`, full HF Harness Adapters & In-Harness RL stack, `Ch 07 Community IRL`, and `Ch 08 Monitor-Only Frontier Watch`.

## [2.0.0-beta.1] - 2026-11-26
- Initial unified 6-Chapter + Graveyard Field Book.

## [1.0.0-core] - 2026-11-08
- Initial Cloud API directory.
