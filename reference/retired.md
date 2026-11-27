[Home](../README.md) / Reference / Retired & Disqualified Tools

*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md))*

# Retired & Disqualified Tools

Free tiers close, endpoints deprecate, and some open models exceed consumer workstation memory. Items below are blocked by automated validation across core entries, guides, specialist directories, and community notes so outdated advice cannot creep back into the guide.

| Area | Item | Retired / Verified | Why Disqualified | Active Alternative |
| :--- | :--- | :--- | :--- | :--- |
| Cloud | Cerebras Cloud Legacy Free Tier | 2026-11-18 | No renewing free tier exists; the $5 / 30-day credit requires a payment method on file. | [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/) |
| Cloud | Mistral La Plateforme Free Experiment Tier | 2026-11-20 | Current billing rules require pay-as-you-go activation for API keys. | [Z.ai BigModel (GLM-4.7-Flash)](https://open.bigmodel.cn/) |
| Cloud | Gemini 2.5 Pro & 2.5 Flash | 2026-12-01 | Scheduled retirement on Dec 1, 2026; superseded by Gemini 4 Hydrogen and 3.8 Flash. | [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/) |
| Cloud | GitHub Models (Azure Inference Endpoint) | 2026-07-30 | Officially retired July 30, 2026; endpoints are shut down. | [OpenRouter (:free Routes)](https://openrouter.ai/) |
| Cloud | Brave Search API Free Tier | 2026-11-01 | Requires a credit card on file. | [Exa 3.0 Neural Search](https://exa.ai/) |
| Local | Wan 3.0, Wan 2.6, & FLUX 3 Video | 2026-11-26 | Closed cloud APIs with no published local open weights. | [Wan 2.2 (5B & A14B Open Video)](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) |
| Local | Inkling 2 Small (594B) & Inkling Flagship (975B) | 2026-11-26 | Require 354-600 GB memory (cloud/API only). | [Inkling 2 Mini (26.4B Looped Transformer MoE)](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) |
| Local | GLM-5.3-Flash (320B) & Kimi K2.7-Code (1T) | 2026-11-26 | Exceed the 16GB VRAM + 64GB RAM local hardware envelope. | [Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) |
| Local | Qwen3.8-Flash-Next at UD-Q2_K_XL (79.6 GB) | 2026-11-26 | Leaves zero headroom for OS, MTP weights, and KV cache on 16GB+64GB. | [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B) |

---

**Continue reading:** [Zero-Card Cloud Free Tiers](cloud-free-tiers.md) · [System Status](../STATUS.md)
