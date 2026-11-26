← [🏠 Field Book Cover](../README.md)

# 🪦 Appendix · The Graveyard (CI-Enforced Cut List)

> [!WARNING]
> Any active entity or Use-Case Pack referencing these patterns fails `python scripts/cli.py validate`.

## 🌐 Cloud API Graveyard
- ❌ **Cerebras Cloud Legacy Free Tier:** Confirmed Nov 18, 2026: no renewing free tier exists; the $5 / 30-day credit requires a valid payment method.
- ❌ **Mistral La Plateforme Free Experiment Tier:** Current billing docs require pay-as-you-go activation for API keys, disqualifying it from our strict no-card pool.
- ❌ **Gemini 2.5 Pro & 2.5 Flash:** Retiring Dec 1, 2026 (auto-routing to Gemini 3.8 Flash / 3.5 Flash-Lite). GCP $300 trials no longer cover Vertex/Gemini.
- ❌ **GitHub Models (Azure Inference Endpoint):** Officially retired July 30, 2026; endpoints are dead.
- ❌ **SambaNova Cloud & Together AI Free Tiers:** Restricted free access; frontier weights require payment methods or one-time starter credits.
- ❌ **Brave Search API Free Tier:** Requires a credit card on file (replaced by Firecrawl Keyless, Jina, Exa 3.0, and Tavily).

## 🖥️ Local Hardware Wall Graveyard (`16GB VRAM + 64GB RAM`)
- ❌ **Wan 3.0, Wan 2.6, and FLUX 3 Video:** Closed cloud APIs with no published weights. Use Wan 2.2, LTX-2.5, or Kandinsky 6.0 Lite locally.
- ❌ **Inkling 2 Small (594B) & Inkling Flagship (975B):** Require 354-600 GB NVFP4/4-bit memory (cloud/Tinker API only). Use Inkling 2 Mini (26.4B) locally.
- ❌ **GLM-5.3-Flash (320B), Kimi K2.7-Code (1T), DeepSeek-V4.1-Flash (552B):** Smallest usable checkpoints need 100-584 GB memory, exceeding your 80 GB total pool. Use via Ch 01 Cloud APIs.
- ❌ **Qwen3.8-Flash-Next at UD-Q2_K_XL (79.6 GB) or Larger:** Leaves zero headroom for OS, MTP weights (2 GB), and KV cache on 16GB+64GB. Cap strictly at UD-IQ1_S/IQ1_M/Q2_0.
- ❌ **Nemotron-3.5-Super-VL (120B) & Dense 70B Offloads:** Super-VL requires 82 GB+ RAM; dense 70B CPU offloading crawls at 2-4 tok/s.
