# AI Swiss Knife — Agent Operating & Foraging Protocol (`v2.0.0-beta.1`)

This repository is a dual-interface AI Field Book compiled from modular YAML sources (`data/*.yaml`):
- **Humans** navigate the One-Page Cover (`README.md`) and 6 uniform 5-beat chapters (`book/01..06-*.md`) + Graveyard (`book/99-graveyard.md`).
- **AI Agents** read `llms.txt` (compact router) or `llms-full.txt` (complete index), or invoke `scripts/build.py forage`.

## Autonomous Foraging CLI
- Cloud/local/keyless auto-routing: `python scripts/build.py forage <intent>` (`coding-agent`, `repo-1m`, `deep-reason`, `fast-json`, `decision-gate`, `voice-stt`)
- Local 16GB VRAM + 64GB RAM launch profiles: `python scripts/build.py forage <profile> --local` (`inkling-coding`, `qwen-27b-super-adapter`, `qwen-27b-pi-specialist`, `qwen-27b-vram`, `qwen-flash-180b`, `flint-coding`, `laya-decision`)

## Maintainer Invariants
1. Never hand-edit `README.md`, `book/*.md`, `llms.txt`, or `llms-full.txt`. Edit `data/*.yaml` only.
2. Obey the **4-Column Table Law** (`c1`..`c4`) and **5-Beat Chapter Contract** (`docs/DESIGN_SYSTEM.md`).
3. Run `python scripts/build.py all` before committing; `.github/workflows/ci_lint.yml` blocks any doc drift or Graveyard leak.
