## Summary
<!-- Briefly describe what changed and why. -->

## Checklist
- [ ] Structured data edited in `catalog/taxonomy.yaml`, `catalog/registry/*.yaml`, or `catalog/decisions/*.yaml` (canonical URLs, explicit `evidence_tier`, explicit `limitations`, zero HTML).
- [ ] Prose edited directly in `README.md`, `docs/`, `worlds/`, `guides/`, `reference/`, or `research/` **outside** fenced `<!-- swissknife:begin ... -->` blocks.
- [ ] Did **not** hand-edit `STATUS.md`, `llms.txt`, `llms-full.txt`, `dist/catalog.json`, or `health/deltas.json`.
- [ ] Verified locally with:
  ```bash
  python -m unittest discover -s tests -t . -v
  swissknife validate
  swissknife sync
  ```
