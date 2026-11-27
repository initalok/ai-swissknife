[Home](../README.md) / Reference / Zero-Card Cloud Free Tiers

*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md))*

# Zero-Card Cloud Free Tiers

Every API listed here has been verified to work without a credit card on file. Because free quotas change frequently, entries carry a 21-day review window and are automatically removed from `llms.txt` if they expire.

## Coding Agent Token Math (Why Most Free Tiers Fail)

A real autonomous coding agent (`Pi`, `Hermes Agent`, `OpenCode`, or `DeepSeek Harness`) sends roughly **20,000 input tokens per step** and takes **~15 steps per bug fix (~300,000 tokens per task)**.

- **Groq's 8,000 TPM free limit** hits HTTP 429 on Step 1 of a coding loop—reserve Groq for fast `<6K`-token classifiers and free Whisper audio transcription.
- **Unverified OpenRouter (`50 RPD`)** exhausts a day's allowance in roughly three multi-step coding tasks.
- **Google AI Studio (`gemini-4-hydrogen` / `3.8 Flash`)** and **Z.ai (`glm-4.7-flash`)** are the primary card-free cloud gateways that can sustain multi-step repository loops.

## Language & Decision Gateways

| Provider | Default Model | Free Quota | Key Limitation |
| :--- | :--- | :--- | :--- |
| [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/) | `gemini-4-hydrogen` | No card: Free Tier (gemini-4-hydrogen 1M unified ctx, implicit caching) + Decision 1 (200 RPM / 10K RPD) | Free Tier prompts are used to improve products outside EU/UK/CH; redact credentials and sensitive data. |
| [Z.ai BigModel (GLM-4.7-Flash)](https://open.bigmodel.cn/) | `glm-4.7-flash` | No card: permanently free GLM-4.7-Flash tier (200K ctx / 128K out) | Only glm-4.7-flash is permanently free; the newer GLM-5.x models are billed and fail on $0 accounts. |
| [NVIDIA NIM Developer Catalog](https://build.nvidia.com/) | `deepseek-ai/deepseek-v4.1-flash` | No card: ~40 RPM developer prototyping catalog | Restricted to developer prototyping rather than production traffic, with occasional cold-start queues on large MoEs. |
| [OpenRouter (:free Routes)](https://openrouter.ai/) | `openrouter/free` | 20 RPM, 50 RPD ($0 balance) -> 1,000 RPD (>=10 credits balance) | 50 RPD on unverified $0 accounts runs out in roughly three multi-step coding tasks; negative balances return HTTP 402 even on :free routes. |
| [Groq Cloud LPU](https://console.groq.com/) | `qwen/qwen3.8-27b` | No card: LLMs 30 RPM / 1K RPD / 8K TPM; Whisper 2K RPD / 28.8K audio sec/day | Strict 8,000 TPM cap on free LLMs causes immediate HTTP 429 failures on 20K-token coding agent prompts. |
| [Cloudflare Workers AI (Clef & Clairic)](https://developers.cloudflare.com/workers-ai/) | `@cf/cloudflare/clef` | No card: 10,000 Neurons/day free (resets 00:00 UTC) | Legacy Workers AI generative catalog models were hard-retired on Nov 20, 2026 (HTTP 410). |
| [Pollinations AI](https://pollinations.ai/) | `openai` | Keyless fair-use IP quota (text and image) | Shared public community service; never transmit private code, credentials, or personal data. |

## Gateway Details

### [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/)

Google's primary card-free developer gateway, now serving Gemini 4 Hydrogen with a 1,048,576-token unified context window, multimodal inputs, and four thinking levels alongside Gemini Decision 1.

- **When to use:** Default zero-card cloud gateway for multi-step coding agents, full-repository ingestion, and multimodal reasoning.
- **OpenAI-compatible endpoint:** `https://generativelanguage.googleapis.com/v1beta/openai/` (env: `GEMINI_API_KEY`)
- **Evidence:** Official documentation · verified 2026-11-27
- **Limitation:** Free Tier prompts are used to improve products outside EU/UK/CH; redact credentials and sensitive data.
- **Limitation:** Search Grounding, Maps Grounding, Batch API, and explicit context caching are paid-tier only on Gemini 4 Hydrogen.
- **Limitation:** Passing thinking_level=minimal or out-of-range temperature/top_p/top_k returns HTTP 400 on gemini-4-hydrogen.

### [Z.ai BigModel (GLM-4.7-Flash)](https://open.bigmodel.cn/)

Card-free Chinese developer API offering a permanently free MIT-licensed GLM-4.7-Flash endpoint with a 200K context window and 128K output cap.

- **When to use:** Secondary no-card backup for long-context coding and tool-use loops when Google AI Studio rate limits are reached.
- **OpenAI-compatible endpoint:** `https://open.bigmodel.cn/api/paas/v4/` (env: `ZHIPU_API_KEY`)
- **Evidence:** Official documentation · verified 2026-11-27
- **Limitation:** Only glm-4.7-flash is permanently free; the newer GLM-5.x models are billed and fail on $0 accounts.

### [NVIDIA NIM Developer Catalog](https://build.nvidia.com/)

Serverless prototyping catalog hosting rack-scale open-weight models—including 552B DeepSeek-V4.1-Flash and Nemotron-3.5-Super-VL—without requiring a credit card.

- **When to use:** Testing giant 300B-550B open-weight models that cannot fit inside consumer workstation memory.
- **OpenAI-compatible endpoint:** `https://integrate.api.nvidia.com/v1` (env: `NVIDIA_API_KEY`)
- **Evidence:** Official documentation · verified 2026-11-27
- **Limitation:** Restricted to developer prototyping rather than production traffic, with occasional cold-start queues on large MoEs.

### [OpenRouter (:free Routes)](https://openrouter.ai/)

Unified OpenAI-compatible router aggregating community-sponsored free model endpoints behind one API key.

- **When to use:** Quick model comparisons and light fallback routing across diverse open weights.
- **OpenAI-compatible endpoint:** `https://openrouter.ai/api/v1` (env: `OPENROUTER_API_KEY`)
- **Evidence:** Official documentation · verified 2026-11-27
- **Limitation:** 50 RPD on unverified $0 accounts runs out in roughly three multi-step coding tasks; negative balances return HTTP 402 even on :free routes.

### [Groq Cloud LPU](https://console.groq.com/)

Ultra-low-latency LPU inference offering free tiers for compact LLMs (qwen/qwen3.8-27b, gpt-oss-120b) and high-quota Whisper-Large-v3 speech transcription.

- **When to use:** Sub-second small-prompt JSON routing (<6K tokens) and free audio transcription (2,000 requests/day).
- **OpenAI-compatible endpoint:** `https://api.groq.com/openai/v1` (env: `GROQ_API_KEY`)
- **Evidence:** Official documentation · verified 2026-11-27
- **Limitation:** Strict 8,000 TPM cap on free LLMs causes immediate HTTP 429 failures on 20K-token coding agent prompts.

### [Cloudflare Workers AI (Clef & Clairic)](https://developers.cloudflare.com/workers-ai/)

Edge inference offering 10,000 daily free Neurons for non-autoregressive Clef decision models and Clairic structured extraction.

- **When to use:** Zero-output-token edge classification, moderation, and typed span extraction.
- **OpenAI-compatible endpoint:** `https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai/v1` (env: `CLOUDFLARE_API_TOKEN`)
- **Evidence:** Official documentation · verified 2026-11-27
- **Limitation:** Legacy Workers AI generative catalog models were hard-retired on Nov 20, 2026 (HTTP 410).

### [Pollinations AI](https://pollinations.ai/)

Keyless community OpenAI-compatible text and FLUX image endpoint requiring zero signup or authentication.

- **When to use:** Last-resort keyless fallback for ephemeral sandbox testing where no API keys exist.
- **OpenAI-compatible endpoint:** `https://text.pollinations.ai/openai` (env: `Keyless`)
- **Evidence:** Official documentation · verified 2026-11-27
- **Limitation:** Shared public community service; never transmit private code, credentials, or personal data.

## Search, Scraping & Academic Grounding

| Service | Free Allocation | Best Used For | Limitation |
| :--- | :--- | :--- | :--- |
| [Firecrawl](https://www.firecrawl.dev/) | Keyless onboarding skill + 500 starter credits | Converting modern JavaScript-rendered documentation pages into clean Markdown for RAG or research. | Keyless usage is strictly IP-rate-limited; create a free key for multi-page crawls. |
| [Jina Reader (r.jina.ai / s.jina.ai)](https://jina.ai/reader/) | Keyless prefix + 10M free tokens with free API key | Instant one-line URL reading in shell scripts and lightweight agents. | Unauthenticated prefix requests throttle quickly under automated batch loops. |
| [Exa 3.0 Neural Search](https://exa.ai/) | No card: $10/mo recurring credits (~2,500 Lite searches) | High-precision web discovery for deep research agents and technical literature scouting. | Deep research search modes exhaust monthly free credits much faster than Lite searches. |
| [OpenAlex Academic Graph](https://openalex.org/) | Keyless: 100,000 requests/day forever | Primary literature review, DOI verification, and academic citation mapping. | Include ?mailto=you@domain.com in queries to enter the fast polite pool. |

## Suggested Fallback Order by Task

- **`coding-agent`:** Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash) -> Z.ai BigModel (GLM-4.7-Flash) -> OpenRouter (:free Routes) -> NVIDIA NIM Developer Catalog -> Pollinations AI
- **`long-context-1m`:** Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash) -> Z.ai BigModel (GLM-4.7-Flash)
- **`deep-reasoning`:** NVIDIA NIM Developer Catalog -> Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash) -> OpenRouter (:free Routes) -> Pollinations AI
- **`fast-json-and-stt`:** Groq Cloud LPU -> Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash) -> Cloudflare Workers AI (Clef & Clairic) -> Pollinations AI
- **`decision-gate`:** Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash) -> Cloudflare Workers AI (Clef & Clairic)

---

**Continue reading:** [Local AI Workstation Guide](../guides/local-ai-workstation.md) · [Retired & Disqualified Tools](retired.md)
