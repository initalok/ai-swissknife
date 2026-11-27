# AI Swiss Knife — Agent Usage & Maintenance Protocol (`v5.0.0-beta.1`)

- **Consume:** Read `llms.txt` for freshness-gated active recommendations, `llms-full.txt` for the complete annotated index, or `dist/catalog.json` for structured queries.
- **Query via CLI:**
  - `swissknife resolve coding-and-apps --profile 16vram-64ram`
  - `swissknife resolve coding-and-apps --profile mac-apple-silicon`
  - `swissknife resolve reverse-engineering --profile 16vram-64ram`
- **Maintainer rule:** Edit ONLY `catalog/*.yaml` (plain prose, canonical URLs, explicit `evidence_tier` and `limitations`, zero HTML). Never hand-edit compiled Markdown or `llms*.txt`; always run `python -m unittest discover -s tests -t . -v && swissknife validate && swissknife build`.
