← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)

# Chapter 01 · Zero-Card Cloud APIs, Decisions & Grounding

> [!IMPORTANT]
> **Verdict:** Only verified card-free gateways and zero-auth grounding tools enter this chapter; stale volatile tiers are automatically gated from agents.
> **Read this chapter if:** You need $0 cloud LLMs, Gemini 4 Hydrogen, System-1 decision endpoints, or keyless RAG/search APIs.

## 1. Verified No-Card Cloud Gateways

| Gateway & Health | Capabilities & Proof | Quota & TTL | The Catch (`⚠️ Gotcha`) |
| :--- | :--- | :--- | :--- |
| [**Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)**](https://aistudio.google.com/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Gemini 4 Hydrogen (Everyday & Thinking) launched Nov 2026 across Free, Plus, Pro & Ultra<br>🏆 Gemini Decision 1 evaluates up to 1,000 typed questions per prefill pass with zero output tokens | No Card: Free per-project (4 Hydrogen, 3.8 Flash 1M ctx) + Decision 1 (200 RPM / 10K RPD)<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Gemini 2.5 retires Dec 1, 2026; 4 Argon/Carbon/Neon, Batch, and Search Grounding are paid-only.<br>⚠️ Free tier prompts may be logged outside EU/UK/CH; redact sensitive PII. |
| [**Z.ai BigModel (GLM-4.7-Flash)**](https://open.bigmodel.cn/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 GLM-4.7-Flash (MIT) scores 79.5 tau2-Bench with 200K context window | No Card: Completely Free Flash tier (200K ctx / 128K out)<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Only glm-4.7-flash is permanently free; the GLM-5.x line is billed and fails on $0 balances. |
| [**NVIDIA NIM Developer Catalog**](https://build.nvidia.com/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Hosts 552B DeepSeek-V4.1-Flash, Nemotron-3.5-Super-VL, and Nemotron-3-Ultra serverless | No Card: ~40 RPM Developer Prototyping Catalog<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Prototyping-only license with occasional cold-start queues on giant MoEs. |
| [**OpenRouter (:free)**](https://openrouter.ai/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Aggregates free frontier hosts; also offers Inkling 2 Mini via io.net at $0.08/M in, $0.35/M out | 20 RPM, 50 RPD ($0) -> 1,000 RPD (>=10 credits balance)<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Negative account balance returns HTTP 402 even on :free endpoints; poll GET /api/v1/key. |
| [**Groq Cloud LPU**](https://console.groq.com/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Verified active free LLMs: qwen/qwen3.8-27b, gpt-oss-120b, gpt-oss-20b, and Whisper-Large-v3/Turbo | No Card: LLMs 30 RPM / 1K RPD / 8K TPM; Whisper 2K RPD / 28.8K sec/day<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Strict 8,000 TPM wall on free LLMs causes 429s on coding agents; keep prompts under 6K tokens or use for STT.<br>⚠️ Llama 3.1/3.3 models moved to Contact Sales. |
| [**Cloudflare Workers AI (Clef & Clairic)**](https://developers.cloudflare.com/workers-ai/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Non-autoregressive Clef, Clef-Omni (audio/video), and Clairic (typed span extraction & 64-step forecasts) | No Card: 10,000 Neurons/day free (resets 00:00 UTC)<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Legacy Workers AI catalog models were hard-retired Nov 20, 2026 (HTTP 410). |
| [**Local Unsloth / llama-server Loopback**](https://github.com/unslothai/unsloth)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 100% air-gapped zero-retention local inference fallback | Unlimited Local Hardware (16GB VRAM + 64GB RAM; OpenAI & Anthropic APIs)<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Must be running locally on port 8000 before cloud foraging auto-detects it. |
| [**Pollinations AI**](https://pollinations.ai/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Instant zero-key fallback for sandbox chat and FLUX REST images | Keyless Zero-Auth Fair-Use IP Quota (Text, FLUX Image, Audio)<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Shared public community endpoint; never transmit credentials or sensitive data. |

## 2. Grounding, Search & RAG Tools

| Tool & Health | Capabilities & Proof | Quota & TTL | The Catch (`⚠️ Gotcha`) |
| :--- | :--- | :--- | :--- |
| [**Firecrawl (Keyless Skill & API)**](https://www.firecrawl.dev/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Lowest web-scraping token bloat on OpenBenchmarks (7,456 median tokens/task) | Keyless onboarding skill + 500 credits on signup<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Keyless mode is IP-rate-limited; pass API key for burst crawls. |
| [**Jina Reader (r.jina.ai / s.jina.ai)**](https://jina.ai/reader/)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Zero-SDK URL/PDF-to-Markdown conversion and keyless search prefix | Keyless prefix + 10M free tokens with API key<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Rate-limited without API key on high-frequency batch loops. |
| [**Exa 3.0 Neural Search**](https://exa.ai/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Resets 1st of every month (~2,500 Lite searches) with 50 concurrent agent runs | No Card: $10/mo recurring credits + $10 bonus (10 QPS search / 100 QPS contents)<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Deep research mode burns monthly credits faster than Lite mode. |
| [**Tavily Search API**](https://tavily.com/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Returns pre-chunked, relevance-scored RAG snippets ready for prompt injection | No Card: 1,000 credits/month forever + Hermes keyless mode<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Advanced search depth consumes 2 credits per call vs 1 for basic. |
| [**Cohere Embed 5 & Rerank 5**](https://cohere.com/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Shared Pro/Fast embedding space (98.4% retention) + 32K context JSON/YAML Rerank 5 | No Card: 1,000 calls/month Trial Key (10 Rerank/min)<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Trial keys are restricted to non-commercial evaluation rates. |
| [**OpenAlex + arXiv API**](https://openalex.org/)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 250M+ scholarly works, citation graphs, and open-access PDFs | Keyless: 100,000 requests/day forever<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Pass ?mailto=you@domain.com in OpenAlex URLs to enter the fast polite pool. |

<details>
<summary>🛠️ <b>Cloud Foraging CLI</b></summary>
<br>

```bash
python scripts/cli.py query cloud coding-agent
python scripts/cli.py query cloud decision-gate
```
</details>

---

← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)
