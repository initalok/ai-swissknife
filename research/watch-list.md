---
title: "21-Day Watch List"
section: research
summary: "Auto-expiring, hard-capped radar tracking frontier ceilings (monitor-only, excluded from llms.txt) and reproducible community field observations."
order: 2
---

[Home](../README.md) / Research / 21-Day Watch List

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# 21-Day Watch List

Fast-moving developments are tracked here under flexible 3-bucket caps (**up to 8 frontier ceilings, up to 10 Model News & Development Radar entries, and up to 8 community/independent harnesses**) and an **auto-expiring 21-day window**. Items exist to be promoted into an active Workflow Slot or dropped cleanly without accumulating sediment. Frontier items are strictly **monitor-only** and are automatically excluded from [`llms.txt`](../llms.txt).

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

## Model News & Development Radar

### [Thinking Machines TML-d24-varloop-research (Variable-Pass Looped MoE)](https://huggingface.co/thinkingmachines/TML-d24-varloop-research)

Open-weight research counterpart to Inkling 2 Mini (26.4B, NVFP4/MXFP8, 1M ctx) letting you vary middle-layer passes (1-5 loops, 3.4B-7.4B effective active) at inference time.

- **Evidence:** Official documentation · **Window:** 21 days remaining
- **Boundary:** Research checkpoint requiring ~20 GB VRAM (32GB+ card or 32GB+ Mac recommended).

### [inclusionAI Ling-3.2-air (124B-A5.5B Hybrid-Linear Workflow MoE)](https://huggingface.co/inclusionAI/Ling-3.2-air)

Nov 23, 2026 multimodal MoE (35 KDA + 7 Gated MLA layers, only 5.5B active) jumping to 61% AutomationBench-AA and 1340 Elo on AA-Briefcase v1.1 for document/workflow automation.

- **Evidence:** Vendor / lab claim · **Window:** 21 days remaining
- **Boundary:** 124B total parameters require high-RAM hybrid offloading or server GPUs; specialized toward document/workflow reasoning.

### [Meta Muse Glimmer Collection (BF16 + GGUF + ExecuTorch + DFlash)](https://huggingface.co/collections/meta-models/muse-glimmer)

Tracks Meta's 30B local agentic family and its 3B DFlash 16-token block-diffusion speculative drafter across GGUF and Apple Metal ExecuTorch formats.

- **Evidence:** Official documentation · **Window:** 21 days remaining
- **Boundary:** Watch for smaller 12B-16B DFlash derivatives that fit inside single 16GB cards.

## Community & Independent Harnesses

### [DeepSeek Harness (dsh — Independent Swappable-Loop Platform)](https://github.com/deepseek-ai/deepseek-harness)

Cordis plugin-everything agent platform where even the core agent loop is a swappable plugin, shipping a read-only-by-default sandbox and desktop/web preview. Demoted from active slots while maturing independently.

- **Evidence:** Official documentation · **Window:** 21 days remaining
- **Boundary:** Rapidly iterating developer preview; independent from our primary Pi/OpenCode spine.

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
