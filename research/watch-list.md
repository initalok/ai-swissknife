---
title: "21-Day Watch List"
section: research
summary: "Auto-expiring, hard-capped radar tracking frontier ceilings (monitor-only, excluded from llms.txt) and reproducible community field observations."
order: 2
---

[Home](../README.md) / Research / 21-Day Watch List

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# 21-Day Watch List

Fast-moving developments are tracked here under strict hard caps (**maximum 5 frontier items and 5 community field notes**) and an **auto-expiring 21-day window**. Items exist to be promoted into an active Workflow Slot or dropped cleanly without accumulating sediment. Frontier items are strictly **monitor-only** and are automatically excluded from [`llms.txt`](../llms.txt).

<!-- swissknife:begin watch -->
## Frontier Ceiling (Monitor-Only)

### [Claude Fable 5.2 & Mythos 5.2](https://www.anthropic.com/)

Sets the current ceiling for 10-12 hour autonomous audits (1M ctx / 128K out, 89.3% OSWorld 2.1, 69.9% FrontierSWE v2), with Mythos 5.2 focused on security and Lean proofs.

- **Evidence:** Vendor / lab claim · **Window:** 21 days remaining
- **Boundary:** Paid API and enterprise access only; tracked strictly as a capability ceiling.

### [GPT-6.2 Astra & GPT-6.2 Sol](https://openai.com/)

Introduces cache-preserving mid-conversation reasoning-effort and tool toggling—an API caching pattern worth watching for future local vLLM and llama.cpp harnesses.

- **Evidence:** Vendor / lab claim · **Window:** 21 days remaining
- **Boundary:** Paid API only; monitor-only.

### [Gemini 4 Carbon & 4 Argon](https://deepmind.google/)

Leads autonomous workflow execution (53.9% AutomationBench) powering Spark Task mode; its fast sibling Gemini 4 Hydrogen has already trickled down into the Free Tier.

- **Evidence:** Vendor / lab claim · **Window:** 21 days remaining
- **Boundary:** Paid Pro/Ultra and billed API only.

### [Qwen4-Max (2.4T)](https://qwenlm.github.io/)

2.4T frontier release (1M ctx, 262K CoT); Alibaba confirmed smaller open-weight Qwen4 releases are planned next, making this the primary reversal-trigger signal for Qwen3.8-27B.

- **Evidence:** Official documentation · **Window:** 21 days remaining
- **Boundary:** Current 2.4T checkpoint is cloud API only; await smaller open-weight checkpoints.

### [DeepSeek-V4.1-Flash (552B)](https://www.deepseek.com/)

Asymmetric Causal Encoder-Decoder (8B active in / 16B out) achieving a 1/4 HBM KV cache footprint; watch for smaller open weights adopting this KV compression.

- **Evidence:** Vendor / lab claim · **Window:** 21 days remaining
- **Boundary:** Exceeds 16GB VRAM + 64GB RAM local memory; accessible via NVIDIA NIM prototyping API.

## Community Field Observations

### [disler/durable-pi Multi-Device Agent Showcase](https://github.com/disler/durable-pi)

Demonstrates crash-resumable SQLite agent state, atomic shared app state, and live mid-run tool toggling on top of @earendil-works/pi-durable.

- **Evidence:** Field observation · **Window:** 21 days remaining
- **Boundary:** Reference architecture; first-party @earendil-works/pi-durable lives inside the main Pi monorepo.

### [Tencent-Hunyuan/Hy-Nomas Walkable Worlds](https://github.com/Tencent-Hunyuan/Hy-Nomas)

Single-GPU WASD-navigable world generator chained by indie creators with LTX-2.5 for video-conditioned audio prototyping.

- **Evidence:** Field observation · **Window:** 21 days remaining
- **Boundary:** Uses NVIDIA PixelUMM decoder (strictly non-commercial previs and pitch use only).

### [shaftoe/awesome-pi-coding-agent (CI-Updated Extension Index)](https://github.com/shaftoe/awesome-pi-coding-agent)

Daily CI-updated community directory indexing the broader Pi extension ecosystem so ai-swissknife can stay focused on its lean 6-rung spine.

- **Evidence:** Official documentation · **Window:** 21 days remaining
- **Boundary:** Audit third-party Pi extensions before granting shell or credential access.

### [loonshoot/agent_vault (Out-of-Band Mobile Secret Gate POC)](https://github.com/loonshoot/agent_vault)

Open-source MCP prototype keeping API keys in 1Password and blocking agent credential requests until approved on your phone with a logged reason.

- **Evidence:** Field observation · **Window:** 21 days remaining
- **Boundary:** Explicitly prototype-grade; tracked to monitor emerging mobile HITL credential-gating patterns.
<!-- swissknife:end -->

---

**Continue reading:** [Home](../README.md) · [System Status](../STATUS.md)
