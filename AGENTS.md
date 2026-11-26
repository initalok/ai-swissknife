# AI Swiss Knife — Agent Operating & Foraging Protocol (`v1.1.0 / v2.0.0 / v3.0.0`)

Three isolated, non-overlapping dimensions:
- **`README.md` + `llms.txt` (`v1.1.0`):** Verified zero-card Cloud APIs, System-1 Decision Models, Multimodal routes, and Grounding/RAG tools.
- **`LOCAL_AI.md` + `llms-local.txt` (`v2.0.0`):** Local Model Roster scoped strictly to **16GB VRAM + 64GB System RAM (~80 GB pool)**.
- **`ECOSYSTEM.md` (`v3.0.0`):** Agent Harnesses, Inference Backends, 2026 Flag Bible, Skills/ACP Protocols, OS/Silicon Exclusives, and Frontier Leads.

## Autonomous Foraging Commands
- Cloud: `python scripts/build.py forage <intent>` (`coding-agent`, `repo-1m`, `deep-reason`, `fast-json`, `decision-gate`, `voice-stt`)
- Local: `python scripts/build.py forage <profile> --local` (`inkling-coding`, `qwen-27b-vram`, `qwen-flash-180b`, `flint-coding`, `laya-decision`)

## Maintainer Rules
- Never hand-edit `README.md`, `llms.txt`, `LOCAL_AI.md`, `llms-local.txt`, or `ECOSYSTEM.md`.
- Edit only `data/catalog.yaml`, `data/local_catalog.yaml`, or `data/ecosystem.yaml`, then run `python scripts/build.py all`.
- **4-Column Law:** Never exceed 4 columns in any Markdown table; stack secondary metadata with `<br><sub>...</sub>` and `<kbd>` badges.
