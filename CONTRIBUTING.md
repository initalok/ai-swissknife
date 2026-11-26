# Contributing to AI Swiss Knife (`v2.0.0-beta`)

Thanks for helping keep this Field Book lean, verified, and zero-rot!

## Core Rule: Edit Data, Never Compiled Markdown
- **Edit:** `data/01_cloud.yaml` .. `data/06_adaptation.yaml`, `data/99_graveyard.yaml`, or `data/meta.yaml`.
- **Never hand-edit:** `README.md`, `book/*.md`, `llms.txt`, or `llms-full.txt`.

## Inclusion Bar
1. **Primary Source Only:** Link official provider docs, Hugging Face model cards, GitHub releases, or arXiv papers.
2. **Real-World Gotcha Required:** Every row must include its bottleneck, license nuance, or failure mode in `c4`.
3. **4-Column Law:** Never add a 5th column; stack secondary metadata with `<br><sub>...</sub>`.
4. **Graveyard Respect:** Dead cloud tiers (`Cerebras`, `Mistral`, `GitHub Models`, `Gemini 2.5`) and >80 GB local walls belong in `data/99_graveyard.yaml`.

## Local Validation Before Opening a PR
```zsh
source .venv/bin/activate
python scripts/build.py all
git status
```
CI (`.github/workflows/ci_lint.yml`) will automatically verify schema compliance, Graveyard enforcement, and zero doc drift.
