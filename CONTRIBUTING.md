# Contributing to AI Swiss Knife

Thank you for helping keep this handbook clear, calm, and forward-moving.

## How Editing Works (Single-Source Managed Blocks)
- **Fixing prose or adding a new page:** Edit Markdown directly in `docs/`, `worlds/`, `guides/`, `reference/`, or `research/` (using YAML frontmatter with `title`, `section`, `summary`, `order`). Never edit inside `<!-- swissknife:begin ... -->` ... `<!-- swissknife:end -->` blocks.
- **Adding or updating tools, models, slots, or decisions:** Edit `catalog/registry/*.yaml` or `catalog/decisions/*.yaml`.
- **Standards:** Every entry requires plain-English `summary` and `when_to_use`, a canonical URL (no `/topics/`, generic `/models`, or subreddit homepages), an explicit `evidence_tier`, and at least one real-world limitation.

## Verification Gate Before Opening a PR
```zsh
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests -t . -v
swissknife validate
swissknife sync
```
