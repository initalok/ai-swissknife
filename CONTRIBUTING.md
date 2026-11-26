# Contributing to AI Swiss Knife (`v3.0.0-modular`)

## Architecture Rule: Headless Data -> Dumb Renderers
1. **Atomic Entities (`entities/*.yaml`):** Define each model, gateway, harness, or MCP once with raw domain fields (`lifecycle`, `decay_class`, `last_verified`, `gotchas`). Never write HTML (`<br>`, `<sub>`, `<kbd>`) inside YAML.
2. **Independent Use-Case Packs (`packs/*.yaml`):** Create or edit a ~30-line pack referencing existing entity IDs. Packs are auto-discovered—no compiler edits required.
3. **Verify Before PR:**
```zsh
source .venv/bin/activate
python scripts/cli.py validate
python scripts/cli.py build
```
