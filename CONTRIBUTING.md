# Contributing to AI Swiss Knife (`v4.0.0-beta`)

## Built-In Invariants (Enforced by `scripts/cli.py validate`)
1. **Canonical URL Law:** Every entry must link directly to a verifiable GitHub repo, Hugging Face repo/collection, or official docs URL (no `/topics/`, generic `/models`, or subreddit homepages).
2. **Hard Complexity Budgets:** Max 5 Frontier + Max 5 Community items in `graph/radar.yaml`; max 2 canonical entry points + 1 monitored `upstream_hub` per Spoke in `graph/spokes.yaml`.
3. **Headless Purity:** Zero HTML/Markdown formatting inside `graph/*.yaml`.
4. **Edit Data Only:** Update `graph/*.yaml`, then run:
```zsh
source .venv/bin/activate
python scripts/cli.py validate
python scripts/cli.py build
```
