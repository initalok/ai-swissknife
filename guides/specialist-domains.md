---
title: "Specialist Domains"
section: guides
summary: "Upstream-federated starting stacks (max 2 direct picks + 1 monitored upstream directory) for Reverse Engineering, Game Dev & 3D, Growth & Social, and Unfiltered Local AI."
order: 6
---

[Home](../README.md) / Guides / Specialist Domains

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Specialist Domains

Rather than duplicating fast-moving niche tool directories—which quickly go stale—each domain below pairs your verified compute stack with **at most two direct starting tools** and **one live-monitored upstream directory** for deeper exploration.

<!-- swissknife:begin specialists-index -->
### Game Development & Local 16GB 3D Assets

Connect local sparse coding models to engine MCP bridges and generate MIT-licensed 3D blockout meshes locally inside 16GB VRAM.

- **Recommended base stack:** [Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF), [Inkling 2 Mini (26.4B Looped Transformer MoE)](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF)
- **Mandatory safety layer:** [earendil-works/gondolin (libkrun Micro-VM + Secret Proxy)](https://github.com/earendil-works/gondolin), [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya), [nolabs-ai/nono (macOS Seatbelt & Linux Landlock Sandbox)](https://github.com/nolabs-ai/nono), [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents)
- **Direct starting tools (max 2):**
  - **[CoplayDev Unity MCP](https://github.com/CoplayDev/unity-mcp)** — MIT-licensed Unity bridge enabling agents to inspect and modify scene hierarchies and scripts.
  - **[ahujasid Blender MCP](https://github.com/ahujasid/blender-mcp)** — Live Blender integration for constructing, texturing, and iterating 3D scenes from an agent.
- **Monitored upstream directory:** **[Microsoft TRELLIS v1 (MIT 16GB 3D)](https://github.com/microsoft/TRELLIS)** *(upstream updated 2026-10-27)*
- **Guardrail:** Commit binary scene files before automated MCP edits; TRELLIS.2 requires 24GB VRAM officially (use v1 on 16GB).

### Social Media, Launch Promotion & Growth

Pair persistent agents with an open-source multi-network approval calendar and copy-polishing skills while keeping a human gate on publishing.

- **Recommended base stack:** [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/), [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B)
- **Mandatory safety layer:** [earendil-works/gondolin (libkrun Micro-VM + Secret Proxy)](https://github.com/earendil-works/gondolin), [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya), [nolabs-ai/nono (macOS Seatbelt & Linux Landlock Sandbox)](https://github.com/nolabs-ai/nono), [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents)
- **Direct starting tools (max 2):**
  - **[Postiz](https://github.com/gitroomhq/postiz-app)** — Self-hostable scheduler for 30+ social networks with REST API, agent CLI, and visual human approval queue.
  - **[blader/humanizer](https://github.com/blader/humanizer)** — Skill that strips repetitive AI phrasing from drafts before human review.
- **Monitored upstream directory:** **[ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills)** *(upstream updated 2026-11-26)*
- **Guardrail:** Always route agent drafts through Postiz's human approval calendar; audit outbound skills for CAN-SPAM and GDPR compliance.

### Reverse Engineering & Binary Triage

Run air-gapped local coding models wired to decompiler MCPs for rapid static renaming and triage while keeping dynamic debugging human-led.

- **Recommended base stack:** [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B), [Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF)
- **Compatible adapters:** [Qwen3.8-27B Pi Specialist LoRA (~319 MB)](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted-GGUF), [Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)
- **Mandatory safety layer:** [earendil-works/gondolin (libkrun Micro-VM + Secret Proxy)](https://github.com/earendil-works/gondolin), [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya), [nolabs-ai/nono (macOS Seatbelt & Linux Landlock Sandbox)](https://github.com/nolabs-ai/nono), [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents)
- **Direct starting tools (max 2):**
  - **[LaurieWired GhidraMCP](https://github.com/LaurieWired/GhidraMCP)** — Interactive Ghidra MCP bridge for function renaming, xref mapping, and triage.
  - **[LLNL OGhidra](https://github.com/LLNL/OGhidra)** — Adaptive Ghidra analysis loop with automated MITRE ATT&CK pattern alerts.
- **Monitored upstream directory:** **[zhuyansen/awesome-ai-reverse-engineering](https://github.com/zhuyansen/awesome-ai-reverse-engineering)** *(upstream updated 2026-11-27)*
- **Guardrail:** Disable all outbound cloud API endpoints before analyzing proprietary or sensitive binaries.
- **Guardrail:** Strictly audit binaries or APKs you own or have explicit legal authorization to analyze.

### Unfiltered & Operator-Aligned Local Stacks

Skip brittle jailbreak prompts: use neutral-aligned Hermes 4 for operator-controlled policies, or load a 26 MB abliterated LoRA on frozen Qwen3.8-27B behind mandatory safety proxies.

- **Recommended base stack:** [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B), [NousResearch Hermes 4 (14B / 4.3-36B Neutral)](https://huggingface.co/NousResearch/Hermes-4-14B)
- **Compatible adapters:** [Qwen3.8-27B 26MB Uncensored LoRA (Rank-3)](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated)
- **Mandatory safety layer:** [earendil-works/gondolin (libkrun Micro-VM + Secret Proxy)](https://github.com/earendil-works/gondolin), [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya), [nolabs-ai/nono (macOS Seatbelt & Linux Landlock Sandbox)](https://github.com/nolabs-ai/nono), [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents)
- **Direct starting tools (max 2):**
  - **[NousResearch Hermes 4 (Neutral Alignment)](https://huggingface.co/NousResearch/Hermes-4-14B)** — Obeys custom operator system prompts cleanly without weight-surgery degradation.
  - **[Securelayer7 Qwen3.8-27B 26MB Uncensored LoRA](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated)** — Rank-3 hot-swappable LoRA sharing the same frozen Qwen3.8-27B base weights.
- **Monitored upstream directory:** **[huihui-ai/Huihui-Qwen3.8-27B-abliterated](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated)** *(upstream updated 2026-08-24)*
- **Guardrail:** Abliterated weights cannot refuse destructive commands; never wire them to local shell tools without safeagents and Laya 0.5.
<!-- swissknife:end -->

---

**Continue reading:** [Security & Trust Boundaries](../docs/security-and-trust.md) · [21-Day Watch List](../research/watch-list.md)
