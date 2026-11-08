# AI Swiss Knife Knowledge Base (`v0.1.0-core`)
> A lean, modular, benchmark-filtered, and upstream-synced AI resource database.

## Core Architecture (4-Pillar Relational Database)
- **[Pillar 1: Verified API Gateways & Runtimes](modules/01-providers.md)** — Cloud gateways + Unsloth local runtime with rate-limit bottlenecks, effective context caps, and privacy audits.
- **[Pillar 2: Task-Routed Text & Coding Models](modules/02-text-and-code.md)** — Benchmark-verified frontier generalists & niche specialists (SWE-bench, Terminal-Bench 2.1, GPQA Diamond).
- **[Pillar 3: Multimodal Specialty APIs & Open Weights](modules/03-multimodal.md)** — Audio (STT/TTS/Duplex), Document OCR, Image (`FLUX.2`/`Kontext`), Video (`FLUX 3 Max`/`Seedance 2.5`/`Wan 3.0`), & Music.
- **[Pillar 4: Search, Scraping, Reranking & Academic Grounding](modules/04-grounding-rag.md)** — Card-free agent grounding (`Firecrawl Keyless`, `Jina Reader`, `Exa 3.0`, `Tavily`, `Cohere Embed/Rerank 5`, `OpenAlex`).

## Engine CLI (`Ingest -> Lint -> Compile`)
```bash
python scripts/engine.py ingest   # Pull latest upstream READMEs & generate diff report
python scripts/engine.py lint     # Audit relational integrity & schema rules
python scripts/engine.py compile  # Auto-generate modules/*.md and README.md
python scripts/engine.py all      # Run full pipeline
```
