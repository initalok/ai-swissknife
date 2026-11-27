[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; [🖥️ Local](../book/local.md) &nbsp;·&nbsp; [⚙️ Harnesses & RL](../book/harnesses-and-rl.md) &nbsp;·&nbsp; [📘 Playbooks](../book/playbooks.md) &nbsp;·&nbsp; [🧭 Spokes](../book/spokes.md) &nbsp;·&nbsp; [📡 Radar](../book/radar.md) &nbsp;·&nbsp; **🪦 Graveyard**

# 🪦 The Graveyard (CI-Enforced Cut Ledger)

> [!WARNING]
> Any active node matching a pattern below fails `python scripts/cli.py validate`.

| Category | Retired / Blocked Item | Why Cut | Active Replacement |
| :--- | :--- | :--- | :--- |
| ☁️ Cloud | ❌ **Cerebras Cloud Legacy Free Tier** | Confirmed Nov 18, 2026: no renewing free tier; $5 / 30-day credit requires a payment method. | [**Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)**](https://aistudio.google.com/) |
| ☁️ Cloud | ❌ **Mistral La Plateforme Free Experiment Tier** | Billing docs require pay-as-you-go activation for API keys. | [**Z.ai BigModel (GLM-4.7-Flash)**](https://open.bigmodel.cn/) |
| ☁️ Cloud | ❌ **Gemini 2.5 Pro & 2.5 Flash** | Retiring Dec 1, 2026; superseded by Gemini 4 Hydrogen & 3.8 Flash. | [**Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)**](https://aistudio.google.com/) |
| ☁️ Cloud | ❌ **GitHub Models (Azure Inference Endpoint)** | Officially retired July 30, 2026; endpoints are dead. | [**OpenRouter (:free)**](https://openrouter.ai/) |
| ☁️ Cloud | ❌ **Brave Search API Free Tier** | Requires a credit card on file. | [**Exa 3.0 Neural Search**](https://exa.ai/) |
| 🖥️ Local | ❌ **Wan 3.0, Wan 2.6, & FLUX 3 Video** | Closed cloud APIs with no published open weights. | [**Wan 2.2 (5B & A14B Open Video)**](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) |
| 🖥️ Local | ❌ **Inkling 2 Small (594B) & Inkling Flagship (975B)** | Require 354-600 GB memory (cloud/Tinker API only). | [**Inkling 2 Mini (26.4B Looped Transformer MoE)**](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) |
| 🖥️ Local | ❌ **GLM-5.3-Flash (320B) & Kimi K2.7-Code (1T)** | Exceed 16GB VRAM + 64GB RAM hardware ceiling. | [**Qwen3-Coder-Next (80B-A3B Sparse MoE)**](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) |
| 🖥️ Local | ❌ **Qwen3.8-Flash-Next at UD-Q2_K_XL (79.6 GB)** | Leaves zero headroom for OS, MTP weights, and KV cache on 16GB+64GB. | [**Qwen3.8-27B (Dense Vision+Text Backbone)**](https://huggingface.co/Qwen/Qwen3.8-27B) |

---

[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; [🖥️ Local](../book/local.md) &nbsp;·&nbsp; [⚙️ Harnesses & RL](../book/harnesses-and-rl.md) &nbsp;·&nbsp; [📘 Playbooks](../book/playbooks.md) &nbsp;·&nbsp; [🧭 Spokes](../book/spokes.md) &nbsp;·&nbsp; [📡 Radar](../book/radar.md) &nbsp;·&nbsp; **🪦 Graveyard**
