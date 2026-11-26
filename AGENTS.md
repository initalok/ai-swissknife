# AI Swiss Knife — Agent Operating & Foraging Protocol (`v2.1.0`)

3-Part, 8-Chapter + Graveyard dual-interface AI Field Book compiled from modular YAML (`data/*.yaml`):
- **Humans:** One-Page Cover (`README.md`) -> Part I (`book/01..03`), Part II (`book/04..06`), Part III (`book/07` IRL Builds & `book/08` Monitor-Only Frontier Watch), & Appendix (`book/99-graveyard.md`).
- **AI Agents:** Read `llms.txt` (compact router) or `llms-full.txt` (complete index), or run `scripts/build.py forage`.

## Autonomous Foraging CLI
- Cloud/local/keyless auto-routing: `python scripts/build.py forage <intent>` (`coding-agent`, `repo-1m`, `deep-reason`, `fast-json`, `decision-gate`, `voice-stt`)
- Local 16GB VRAM + 64GB RAM profiles (Mature vs. Cutting-Edge): `python scripts/build.py forage --local`

## Maintainer Invariants
1. Never hand-edit `README.md`, `book/*.md`, `llms.txt`, or `llms-full.txt`. Edit `data/*.yaml` only.
2. Obey the **4-Column Law**, **5-Beat Chapter Contract**, and keep paid/rack-scale models strictly inside `Ch 08` (`monitor_only: true`).
3. Run `python scripts/build.py all` before committing; `.github/workflows/ci_lint.yml` enforces zero doc drift.
