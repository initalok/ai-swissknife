[Home](../README.md) / Guides / Research & Writing

*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md))*

# Research & Writing

High-precision literature synthesis combining open academic graphs, semantic search, and cited draft generation.

## Recommended Stack

The components below are selected for this workflow based on verified compatibility and current link health.

### Models & Cloud Gateways

- **[Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/)** — Default zero-card cloud gateway for multi-step coding agents, full-repository ingestion, and multimodal reasoning. *(Official documentation)*
- **[NVIDIA NIM Developer Catalog](https://build.nvidia.com/)** — Testing giant 300B-550B open-weight models that cannot fit inside consumer workstation memory. *(Official documentation)*
- **[OpenRouter (:free Routes)](https://openrouter.ai/)** — Quick model comparisons and light fallback routing across diverse open weights. *(Official documentation)*
- **[Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B)** — Daily-driver local coding, strict instruction following, and single-backbone multi-LoRA serving. *(Primary evaluation)*
- **[Gemma 4 Family (26B-A4B Vision & 12B Tri-Modal)](https://ai.google.dev/gemma)** — High-speed local general chat, vision inspection, or local audio analysis. *(Official documentation)*

### Agent Harnesses

- **[Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi)** — When you want full control over context assembly, clean compaction, and the highest-scoring official target for Hugging Face's RL harness adapters. *(Primary evaluation)*
- **[Hermes Agent (v0.23.4)](https://github.com/NousResearch/hermes-agent)** — Always-on background assistants, scheduled research digests, and multi-surface personal operations. *(Official documentation)*

## Supporting Domain Tools

- **[GPT Researcher](https://github.com/assafelovic/gpt-researcher)** — Open-source research synthesizer (gptr-mcp and skill) covering both web sources and local PDF/CSV folders.
- **[DeerFlow 2.0](https://github.com/bytedance/deer-flow)** — Open-source deep research harness running inside an isolated Docker sandbox.

## Step-by-Step Workflow

1. Gather primary scholarly works and DOIs from OpenAlex (polite pool) and current technical documentation via Exa 3.0 or Firecrawl.
2. Run GPT Researcher or DeerFlow 2.0 across retrieved web pages and local PDF/CSV source folders.
3. Audit every cited claim, date, and quantitative figure against primary sources before publishing.

## Limitations & Trade-Offs

- Never treat autonomous research syntheses as publication-ready without checking primary DOIs and URLs manually.

---

**Continue reading:** [Local AI Workstation Guide](local-ai-workstation.md) · [Specialist Domains](specialist-domains.md)
