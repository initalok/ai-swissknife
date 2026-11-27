# AI Swiss Knife — Agent Usage & Maintenance Protocol (`v6.0.0-beta.1`)

- **Consume:** Read `llms.txt` for freshness-gated active slots and recipes, `llms-full.txt` for the full annotated index, or `dist/catalog.json` for structured queries.
- **Query via CLI:**
  - `swissknife slot dev-harness --world mac`
  - `swissknife specialist reverse-engineering --world gpu-pc`
  - `swissknife query --world cloud --kind gateway`
  - `swissknife deltas`
- **Maintainer protocol:**
  - Edit structured facts in `catalog/taxonomy.yaml`, `catalog/registry/*.yaml`, and `catalog/decisions/*.yaml` (canonical URLs, explicit `evidence_tier` and `limitations`, zero HTML).
  - Edit timeless human prose directly in `README.md`, `docs/`, `worlds/`, `guides/`, `reference/`, and `research/` — never hand-edit inside fenced `<!-- swissknife:begin ... -->` blocks or generated files (`STATUS.md`, `llms*.txt`, `dist/catalog.json`).
  - Use `.agents/skills/sync-upstream/SKILL.md` to triage `health/deltas.json`.
  - Always verify with `python -m unittest discover -s tests -t . -v && swissknife validate && swissknife sync`.
