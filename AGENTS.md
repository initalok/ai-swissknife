# AI Swiss Knife — Agent Operating & Foraging Protocol (`v1.0.0`)

This repository is a dual-interface AI knowledge instrument:
- **Humans** read `README.md` (designed with progressive disclosure, native Mermaid circuits, 4-column breathable typography, and collapsible drawers).
- **AI Agents** read `llms.txt` or execute `python scripts/build.py forage <intent>` to autonomously self-provision free/keyless LLM, Multimodal, and Grounding endpoints.

## 1. How Agents "Find Their Lunch" (Self-Foraging)
If you are an autonomous agent needing an LLM, OCR, Search, or Audio API:
1. Run `python scripts/build.py forage <intent>` (`coding-agent`, `repo-1m`, `deep-reason`, `fast-json`, `fim-ide`, `voice-stt`, `rag-grounding`).
2. The script inspects local environment keys (`ZHIPU_API_KEY`, `GEMINI_API_KEY`, `MISTRAL_API_KEY`, `CEREBRAS_API_KEY`, `GROQ_API_KEY`, `NVIDIA_API_KEY`, `OPENROUTER_API_KEY`), probes local hardware (`http://localhost:8000/v1` for Unsloth), and automatically falls back to **Tier 0 Keyless Endpoints** (`Pollinations`, `Jina Reader`, `Firecrawl Keyless`, `OpenAlex`) so you never halt on missing credentials.

## 2. Maintainer Rules for Antigravity
- **Never hand-edit `README.md` or `llms.txt`.** Edit `data/catalog.yaml` only, then run `python scripts/build.py all`.
- **4-Column Table Law:** Never exceed 4 columns in any Markdown table. Stack secondary metadata using `<br><sub>...</sub>` and `<kbd>` badges to prevent horizontal scrollbars and ugly text wrapping on GitHub.
- **Graveyard Enforcement:** Never add any URL or provider listed in the `graveyard` section of `data/catalog.yaml`.
