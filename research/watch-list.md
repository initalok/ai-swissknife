[Home](../README.md) / Research / 21-Day Watch List

*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md))*

# 21-Day Watch List

Fast-moving developments are tracked here under strict size limits (maximum 5 frontier items and 5 community field notes) and a 21-day review window. Frontier items are strictly **monitor-only** and are excluded from automated agent routing (`llms.txt`).

## Frontier Ceiling (Monitor-Only)

Tracked to observe capability ceilings, caching/harness innovations, and signals of what will trickle down to free or local tiers next.

### [Claude Fable 5.2 & Mythos 5.2](https://www.anthropic.com/)

Sets the current ceiling for 10-12 hour autonomous audits (1M ctx / 128K out, 89.3% OSWorld 2.1, 69.9% FrontierSWE v2), with Mythos 5.2 focused on restricted security and Lean proofs.

- **Evidence:** Vendor / lab claim · **Review window:** 21 days remaining
- **Boundary:** Paid API and enterprise access only; tracked strictly as a capability ceiling.

### [GPT-6.2 Astra & GPT-6.2 Sol](https://openai.com/)

Introduces cache-preserving mid-conversation reasoning-effort and tool toggling—an API caching pattern worth watching for future local vLLM and llama.cpp harnesses.

- **Evidence:** Vendor / lab claim · **Review window:** 21 days remaining
- **Boundary:** Paid API only; monitor-only.

### [Gemini 4 Carbon & 4 Argon](https://deepmind.google/)

Leads autonomous workflow execution (53.9% AutomationBench) powering Spark Task mode; its fast sibling Gemini 4 Hydrogen has already trickled down into the free tier.

- **Evidence:** Vendor / lab claim · **Review window:** 21 days remaining
- **Boundary:** Paid Pro/Ultra and billed API only.

### [Qwen4-Max (2.4T)](https://qwenlm.github.io/)

2.4T frontier release (1M context, 262K CoT); Alibaba explicitly confirmed smaller open-weight Qwen4 releases are planned next, making this the top watchlist signal for local workstations.

- **Evidence:** Official documentation · **Review window:** 21 days remaining
- **Boundary:** Current 2.4T checkpoint is cloud API only; await smaller open-weight releases.

### [DeepSeek-V4.1-Flash (552B)](https://www.deepseek.com/)

Asymmetric Causal Encoder-Decoder (8B active in / 16B out) achieving a 1/4 HBM KV cache footprint; watch for smaller open checkpoints adopting this KV compression.

- **Evidence:** Vendor / lab claim · **Review window:** 21 days remaining
- **Boundary:** Exceeds 16GB VRAM + 64GB RAM local memory; accessible via NVIDIA NIM prototyping API.

## Community Field Observations

Reproducible workflows, runtime breakthroughs, and community tooling observed in real use.

### [obra/superpowers Multi-Harness Discipline Pack](https://github.com/obra/superpowers)

Widely adopted 15-skill pack enforcing Brainstorm -> Spec -> Red/Green TDD -> Fresh Subagent -> Verification for 2+ hour autonomous runs across Pi, Hermes, OpenCode, and Claude Code.

- **Evidence:** Field observation · **Review window:** 21 days remaining
- **Boundary:** On Hermes Agent, use the Hermes-native tool mapping port rather than raw Claude Code tool names.

### [disler/durable-pi Multi-Device Agent Showcase](https://github.com/disler/durable-pi)

Demonstrates crash-resumable SQLite agent state, atomic shared app state, and live tool hot-swapping on top of Pi.

- **Evidence:** Field observation · **Review window:** 21 days remaining
- **Boundary:** First-party @earendil-works/pi-durable is now also maintained directly inside the main Pi monorepo.

### [Tencent-Hunyuan/Hy-Nomas Walkable Worlds](https://github.com/Tencent-Hunyuan/Hy-Nomas)

Single-GPU WASD-navigable world generator chained by indie creators with LTX-2.5 for video-conditioned audio prototyping.

- **Evidence:** Field observation · **Review window:** 21 days remaining
- **Boundary:** Uses NVIDIA PixelUMM decoder (strictly non-commercial previs and pitch use only).

### [Apple Silicon MTP-Preserving MLX Harness Merges](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)

Community MLX-6bit and 4-bit merges of Hugging Face's rank-96 super-adapter preserve Qwen3.8's MTP layer, hitting ~65 tok/s on Apple Silicon unified memory.

- **Evidence:** Field observation · **Review window:** 21 days remaining
- **Boundary:** Verify checksums and benchmark retention on third-party quantized merges before production use.

---

**Continue reading:** [Home](../README.md) · [System Status](../STATUS.md)
