---
title: "Retired & Disqualified Tools"
section: reference
summary: "CI-enforced graveyard recording closed free tiers, archived extensions, and oversized models alongside their active replacements."
order: 2
---

[Home](../README.md) / Reference / Retired & Disqualified Tools

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Retired & Disqualified Tools

Free tiers close, extensions get absorbed into upstream cores (`huggingface/pi-llama` $\rightarrow$ built-in `Pi` `/llama`), and oversized checkpoints exceed consumer workstation memory. Automated validation blocks every pattern below across the entire registry so outdated advice cannot silently return.

<!-- swissknife:begin retired -->
| Area | Retired / Disqualified Item | Date | Why Cut | Active Alternative |
| :--- | :--- | :--- | :--- | :--- |
| cloud | Cerebras Cloud Legacy Free Tier | 2026-11-18 | No renewing free tier exists; the $5 / 30-day credit requires a payment method on file. | [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/) |
| cloud | Mistral La Plateforme Free Experiment Tier | 2026-11-20 | Current billing rules require pay-as-you-go activation for API keys. | [Z.ai BigModel (GLM-4.7-Flash)](https://open.bigmodel.cn/) |
| cloud | Gemini 2.5 Pro & 2.5 Flash | 2026-12-01 | Scheduled retirement on Dec 1, 2026; superseded by Gemini 4 Hydrogen and 3.8 Flash. | [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/) |
| cloud | GitHub Models (Azure Inference Endpoint) | 2026-07-30 | Officially retired July 30, 2026; endpoints are shut down. | [OpenRouter (:free Routes)](https://openrouter.ai/) |
| cloud | Brave Search API Free Tier | 2026-11-01 | Requires a credit card on file. | [Exa 3.0 Neural Search](https://exa.ai/) |
| pi-extension | huggingface/pi-llama | 2026-11-09 | Archived upstream after llama.cpp router support was built directly into Pi core (/llama). | [Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi) |
| pi-extension | cv/pi-ssh-remote | 2026-11-15 | Archived upstream; replaced by @earendil-works/pi-durable remote ExecutionEnv and Tailscale-native mobile bridges. | [pi-mobile (Multi-Box Tailscale HTTPS & Voice Mode)](https://pi.dev/packages/pi-mobile) |
| local | Wan 3.0, Wan 2.6, & FLUX 3 Video | 2026-11-26 | Closed cloud APIs with no published local open weights. | [Wan 2.2 (5B & A14B Apache-2.0 Video)](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) |
| local | Inkling 2 Small (594B) & Inkling Flagship (975B) | 2026-11-26 | Require 354-600 GB memory (cloud/API only). | [Inkling 2 Mini (26.4B Looped Transformer MoE)](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) |
| local | GLM-5.3-Flash (320B) & Kimi K2.7-Code (1T) | 2026-11-26 | Exceed the 16GB VRAM + 64GB RAM local hardware envelope. | [Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) |
| local | Qwen3.8-Flash-Next at UD-Q2_K_XL (79.6 GB) | 2026-11-26 | Leaves zero headroom for OS, MTP weights, and KV cache on 16GB+64GB. | [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B) |
<!-- swissknife:end -->

---

**Continue reading:** [Why This Stack](../docs/why-this-stack.md) · [System Status](../STATUS.md)
