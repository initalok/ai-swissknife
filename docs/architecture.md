[Home](../README.md) / Orientation / How This Guide Is Maintained

*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md))*

# How This Guide Is Maintained

This page is for maintainers and contributors. Readers do not need to understand these internals to use the guide.

## Design Principles

- **Headless data, declarative views:** All factual entries live in seven plain-data YAML files under `catalog/`. Markdown pages and `llms.txt` are compiled from a single typed JSON snapshot (`dist/catalog.json`) and are never hand-edited.
- **Canonical URL Law:** Automated validation rejects uncheckable placeholder URLs (such as GitHub `/topics/` pages, generic model directories, or subreddit homepages) so every link can be verified programmatically.
- **Review Windows & Freshness Gating:** Each entry carries a decay class (`volatile`: 21 days, `operational`: 60 days, `stable`: 120 days). When an entry passes its review window or fails 3 consecutive health checks, it is automatically omitted from `llms.txt` until re-verified.
- **Relational Compatibility:** Entries declare three lightweight relationships (`runs_on`, `adapts`, `guards`). When a base model or harness degrades, adapters referencing it automatically raise an upstream review alert.

## Local Maintainer Workflow

```bash
pip install -e .
python -m unittest discover -s tests -t . -v
swissknife validate
swissknife build
```

---

**Continue reading:** [Contributing Guidelines](../CONTRIBUTING.md) · [System Status](../STATUS.md)
