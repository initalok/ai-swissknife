[Home](../README.md) / Guides / Local Media Studio

*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md))*

# Local Media Studio

Unified local creative pipeline for 16GB video synthesis, transparent RGBA image editing, code-driven motion graphics, NLE automation, and browser voiceovers.

## Recommended Stack

The components below are selected for this workflow based on verified compatibility and current link health.

### Models & Cloud Gateways

- **[Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/)** — Default zero-card cloud gateway for multi-step coding agents, full-repository ingestion, and multimodal reasoning. *(Official documentation)*
- **[Groq Cloud LPU](https://console.groq.com/)** — Sub-second small-prompt JSON routing (<6K tokens) and free audio transcription (2,000 requests/day). *(Official documentation)*
- **[Qwen-Image-2.1 (7B DiT Native RGBA)](https://huggingface.co/Qwen/Qwen-Image-2.1)** — Non-commercial local design assets, typography, and layered transparent image editing. *(Official documentation)*
- **[Wan 2.2 (5B & A14B Open Video)](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B)** — Commercial-safe local video synthesis on 8GB-16GB NVIDIA workstations. *(Official documentation)*

### Agent Harnesses

- **[Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi)** — When you want full control over context assembly, clean compaction, and the highest-scoring official target for Hugging Face's RL harness adapters. *(Primary evaluation)*
- **[DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness)** — Building custom agent loops, interactive Creator Mode plugins, or multi-harness web sessions. *(Official documentation)*

### Inference & Media Runtimes

- **[WanGP v20.12 (MMGP v4 + SageGP 1.0.2)](https://github.com/deepbeepmeep/WanGP)** — Running Wan 2.2, LTX-2.5, and Qwen-Image-2.1 on 8GB-16GB consumer GPUs. *(Official documentation)*

## Supporting Domain Tools

- **[HeyGen Hyperframes](https://github.com/heygen-com/hyperframes)** — Programmatic HTML-to-MP4 studio ideal for crisp UI demos, explainers, and launch motion graphics.
- **[DaVinci Resolve MCP (Free & Studio Bridge)](https://github.com/hiteshK03/davinci-resolve-mcp)** — Community internal script bridge exposing 155/162 DaVinci Resolve timeline, color, and audio tools even on the Free edition.
- **[Gradium Phonon 31M WebGPU TTS](https://github.com/blixt/phonon)** — 64.5 MB Apache-2.0 voice synthesis running directly in browser WebGPU at 4.9ms first-audio latency.

## Step-by-Step Workflow

1. Generate deterministic product demos and data graphics in code using HeyGen Hyperframes.
2. Produce local AI footage inside 5.9-15 GB VRAM using WanGP v20.12 with Wan 2.2 (Apache-2.0) or Qwen-Image-2.1 (non-commercial).
3. Automate timeline cuts and grading via DaVinci Resolve MCP and render fast English voiceovers locally with Phonon 31M.

## Limitations & Trade-Offs

- Qwen-Image-2.1 is licensed non-commercially; swap to Apache-2.0 FLUX.2 Klein for commercial graphics.
- Official external DaVinci Resolve scripting remains Studio-only; verify community internal bridge compatibility after Resolve updates.

---

**Continue reading:** [Local AI Workstation Guide](local-ai-workstation.md) · [Specialist Domains](specialist-domains.md)
