[Home](../README.md) / Guides / Specialist Domains

*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md))*

# Specialist Domains

Rather than duplicating fast-moving niche tool catalogs, each domain below pairs your verified local or cloud stack with at most two direct starting tools and a monitored upstream directory for deeper exploration.

## Game Development & Local 16GB 3D Assets

Connect local sparse coding models to engine MCP bridges and generate MIT-licensed 3D blockout meshes locally inside 16GB VRAM.

- **Recommended base stack:** [Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF), [Inkling 2 Mini (26.4B Looped Transformer MoE)](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF)
- **Recommended safety layer:** [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya), [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents)
- **Direct starting tools:**
  - **[CoplayDev Unity MCP](https://github.com/CoplayDev/unity-mcp)** — MIT-licensed Unity bridge enabling agents to inspect and modify scene hierarchies and scripts.
  - **[ahujasid Blender MCP](https://github.com/ahujasid/blender-mcp)** — Live Blender integration for constructing, texturing, and iterating 3D scenes from an agent.
- **Broader upstream directory:** **[Microsoft TRELLIS v1 (MIT 16GB 3D)](https://github.com/microsoft/TRELLIS)**
- **Guardrail:** Commit binary scene files before automated MCP edits; TRELLIS.2 requires 24GB VRAM officially (use v1 on 16GB).

## Social Media, Launch Promotion & Growth

Pair persistent agents with an open-source multi-network approval calendar and copy-polishing skills while keeping a human gate on publishing.

- **Recommended base stack:** [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/), [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B)
- **Recommended safety layer:** [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya), [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents)
- **Direct starting tools:**
  - **[Postiz](https://github.com/gitroomhq/postiz-app)** — Self-hostable scheduler for 30+ social networks with REST API, agent CLI, and visual human approval queue.
  - **[blader/humanizer](https://github.com/blader/humanizer)** — Skill that strips repetitive AI phrasing from drafts before human review.
- **Broader upstream directory:** **[ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills)**
- **Guardrail:** Always route agent drafts through Postiz's human approval calendar; audit third-party outbound skills for CAN-SPAM and GDPR compliance.

## Reverse Engineering & Binary Triage

Run air-gapped local coding models wired to decompiler MCPs for rapid static renaming and triage while keeping dynamic debugging human-led.

- **Recommended base stack:** [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B), [Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF)
- **Compatible adapters:** [Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)
- **Recommended safety layer:** [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya), [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents)
- **Direct starting tools:**
  - **[LaurieWired GhidraMCP](https://github.com/LaurieWired/GhidraMCP)** — Widely adopted Ghidra MCP server for interactive function renaming, xref mapping, and triage.
  - **[LLNL OGhidra](https://github.com/LLNL/OGhidra)** — Adaptive reverse-engineering loop over Ghidra with automated MITRE ATT&CK malware pattern alerts.
- **Broader upstream directory:** **[zhuyansen/awesome-ai-reverse-engineering](https://github.com/zhuyansen/awesome-ai-reverse-engineering)**
- **Guardrail:** Disable all outbound cloud API endpoints before analyzing proprietary or sensitive binaries.
- **Guardrail:** Strictly audit binaries or APKs you own or have explicit legal authorization to analyze.

## Unfiltered & Operator-Aligned Local Stacks

Skip brittle jailbreak prompts: use neutral-aligned Hermes 4 for operator-controlled policies, or load a 26 MB abliterated LoRA on frozen Qwen3.8-27B behind mandatory safety proxies.

- **Recommended base stack:** [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B), [NousResearch Hermes 4 (14B / 4.3-36B Neutral)](https://huggingface.co/NousResearch/Hermes-4-14B)
- **Compatible adapters:** [Qwen3.8-27B 26MB Uncensored LoRA (Rank-3)](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated)
- **Recommended safety layer:** [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya), [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents)
- **Direct starting tools:**
  - **[NousResearch Hermes 4 (Neutral Alignment)](https://huggingface.co/NousResearch/Hermes-4-14B)** — Obeys custom operator system prompts cleanly without weight-surgery degradation.
  - **[Securelayer7 Qwen3.8-27B 26MB Uncensored LoRA](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated)** — Rank-3 hot-swappable LoRA sharing the same frozen Qwen3.8-27B base weights.
- **Broader upstream directory:** **[huihui-ai/Huihui-Qwen3.8-27B-abliterated](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated)**
- **Guardrail:** Abliterated weights cannot refuse destructive commands; never wire them to local shell tools without safeagents and Laya 0.5.

---

**Continue reading:** [Local Models Reference](../reference/local-models.md) · [21-Day Watch List](../research/watch-list.md)
