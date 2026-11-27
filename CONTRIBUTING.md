# Contributing to AI Swiss Knife

Thank you for helping keep this field guide accurate, calm, and source-verified.

## Editorial & Technical Standards
1. **Plain English over tag dumps:** Write clear `summary` and `when_to_use` sentences in `catalog/*.yaml`. Never place HTML (`<br>`, `<sub>`, `<kbd>`) inside YAML.
2. **Name the evidence:** Every entry must carry a valid `evidence_tier` (`primary-eval`, `official-docs`, `vendor-claim`, or `field-note`) and at least one explicit limitation.
3. **Canonical URLs only:** Link directly to a verifiable GitHub repository, Hugging Face repo, or official documentation URL (no `/topics/`, generic `/models`, or subreddit homepages).
4. **Edit data, compile docs:** Never hand-edit `README.md`, `STATUS.md`, `docs/`, `guides/`, `reference/`, `research/`, or `llms*.txt`.

## Verification Commands Before Opening a PR
```zsh
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests -t . -v
swissknife validate
swissknife build
```
