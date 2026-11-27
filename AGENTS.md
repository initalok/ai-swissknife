# AI Swiss Knife — Agent Operating Protocol (`v4.0.0-beta`)

Lean Hub-and-Spoke, headless-first, self-policing AI Field Book:
- **Edit ONLY:** the 7 headless YAML files in `graph/*.yaml` (zero HTML/Markdown; 100% canonical URLs).
- **Never hand-edit:** `README.md`, `book/*.md`, `llms.txt`, `llms-full.txt`, or `dist/graph.json`.
- **Freshness Gating:** Expired (`volatile: 21d`, `operational: 60d`, `stable: 120d`) or archived nodes are automatically gated out of `llms.txt` and `resolve` commands until re-verified.

## Agent CLI Commands
- `python scripts/cli.py resolve coding-and-apps --profile 16vram-64ram`
- `python scripts/cli.py resolve reverse-engineering --profile 16vram-64ram`
- `python scripts/cli.py resolve unfiltered-sovereign --profile 16vram-64ram`
- `python scripts/cli.py validate && python scripts/cli.py build`
