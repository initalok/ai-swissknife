# AI Swiss Knife — Agent Operating Protocol (`v3.0.0-modular`)

Pace-layered, headless-first, freshness-gated AI Field Book:
- **Edit ONLY:** `entities/*.yaml`, `packs/*.yaml`, or `feeds/*.yaml` (zero HTML/Markdown allowed).
- **Never hand-edit:** `README.md`, `book/`, `llms.txt`, `llms-full.txt`, or `dist/registry.json`.
- **Freshness Gating:** Expired (`volatile: 21d`, `operational: 60d`, `stable: 120d`) or archived entities are automatically excluded from `llms.txt` and `query` commands until re-verified.

## Agent CLI Commands
- `python scripts/cli.py query cloud <intent>` (Freshness-gated cloud/local/keyless routing)
- `python scripts/cli.py query local --lifecycle mature` (Track A Mature Riced local launches)
- `python scripts/cli.py query local --lifecycle experimental` (Track B Cutting-Edge local launches)
- `python scripts/cli.py query pack <pack-id>` (`pack-web-dev`, `pack-app-dev`, `pack-game-dev`, `pack-reverse-eng`, `pack-research`, `pack-video-edit`, `pack-social-media`, `pack-promotion`, `pack-uncensored`)
- `python scripts/cli.py build` (Validate + compile all human & agent views)
