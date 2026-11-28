# AI Swiss Knife — Agent Usage & Maintenance Protocol (`v6.0.0`)

- **Consume:** Read `llms.txt` for freshness-gated active slots and recipes, `llms-full.txt` for the full annotated index, or `dist/catalog.json` for structured queries.
- **Query via CLI:**
  - `swissknife slot dev-harness --world mac`
  - `swissknife specialist reverse-engineering --world gpu-pc`
  - `swissknife query --world cloud --kind gateway`
  - `swissknife deltas`
- **Maintainer & AI-agent protocol:**
  - **Branch & PR isolation:** AI coding agents (`Antigravity`, `Pi`, `OpenCode`) MUST always work on feature/chore branches and open PRs into `main`—never force-push or commit directly to `main` (`main` is protected against force-push and deletion while permitting automated `health.yml` telemetry pushes).
  - Edit structured facts in `catalog/taxonomy.yaml`, `catalog/registry/*.yaml`, and `catalog/decisions/*.yaml` (canonical URLs, explicit `evidence_tier` and `limitations`, zero HTML).
  - Edit timeless human prose directly in `README.md`, `docs/`, `worlds/`, `guides/`, `reference/`, and `research/` — never hand-edit inside fenced `<!-- swissknife:begin ... -->` blocks or generated files (`STATUS.md`, `llms*.txt`, `dist/catalog.json`).
  - Use `.agents/skills/sync-upstream/SKILL.md` to triage `health/deltas.json`.
  - Before opening any PR, run the full local gate: `ruff check src tests && zizmor --no-online-audits .github/workflows/ && python -m unittest discover -s tests -t . -v && swissknife validate && swissknife sync`.
