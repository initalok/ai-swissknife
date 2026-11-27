---
title: "Zero-Card Cloud"
section: worlds
world: cloud
summary: "Verified $0 credit-card-free cloud gateways, coding-agent token math, search grounding APIs, and fallback order."
order: 1
---

[Home](../README.md) / Compute Worlds / Zero-Card Cloud

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Zero-Card Cloud

Every API listed here has been verified to work with **$0 and no credit card on file**. Because free quotas shift quickly, cloud gateways carry a 21-day review window and are automatically gated out of [`llms.txt`](../llms.txt) if they expire.

## Coding-Agent Token Math (Why Most Free Tiers Fail)

A real autonomous coding agent (`Pi`, `OpenCode`, `Antigravity`, `Hermes Agent`) sends roughly **20,000 input tokens per step** and takes **~15 steps per bug fix (~300,000 tokens per task)**.

- **Groq's 8,000 TPM free limit** hits HTTP 429 on Step 1 of a coding loop—reserve Groq strictly for fast `<6K`-token classifiers and free Whisper-Large-v3 speech transcription.
- **Unverified OpenRouter (`50 RPD`)** exhausts its daily cap in roughly three multi-step coding tasks.
- **Google AI Studio (`gemini-4-hydrogen`, 1M unified context)** and **Z.ai (`glm-4.7-flash`)** are the primary card-free cloud gateways capable of sustaining real multi-step repository loops.

---

## Primary Cloud Slot

<!-- swissknife:begin slot id=cloud-flagship -->
**Active Anchor — [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/)**

Google's primary card-free developer API gateway serving Gemini 4 Hydrogen with a 1,048,576-token unified context window, multimodal inputs, and four thinking levels alongside Gemini Decision 1.

- **When to use:** Default zero-card cloud gateway for multi-step coding agents, full-repository ingestion, and multimodal reasoning.
- **Free quota:** No card: Free Tier (gemini-4-hydrogen 1M unified ctx, implicit caching) + Decision 1 (200 RPM / 10K RPD)
- **Upstream docs:** [Official setup & reference](https://ai.google.dev/gemini-api/docs)
- **Evidence:** Official documentation · verified 2026-11-28
- **Why this pick:** [Anchor Zero-Card Cloud on Google AI Studio (Gemini 4 Hydrogen) & Antigravity](../docs/why-this-stack.md#adr-why-google-cloud)
- **Limitation:** Free Tier prompts are used to improve products outside EU/UK/CH; never paste secrets or proprietary source code.
- **Limitation:** Search Grounding, Maps Grounding, Batch API, and explicit context caching are paid-tier only on Gemini 4 Hydrogen.
- **Limitation:** Passing thinking_level=minimal or out-of-range temperature/top_p/top_k returns HTTP 400 on gemini-4-hydrogen.
<!-- swissknife:end -->

## Verified Card-Free Language & Decision Gateways

<!-- swissknife:begin table world=cloud kind=gateway -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/) | Default zero-card cloud gateway for multi-step coding agents, full-repository ingestion, and multimodal reasoning. | No card: Free Tier (gemini-4-hydrogen 1M unified ctx, implicit caching) + Decision 1 (200 RPM / 10K RPD) | Official documentation | Free Tier prompts are used to improve products outside EU/UK/CH; never paste secrets or proprietary source code. |
| [Z.ai BigModel (GLM-4.7-Flash)](https://open.bigmodel.cn/) | Secondary card-free backup for long-context coding and tool-use loops when Google AI Studio limits are hit. | No card: permanently free GLM-4.7-Flash tier (200K ctx / 128K out) | Official documentation | Only glm-4.7-flash is permanently free; newer GLM-5.x endpoints are billed and fail on $0 accounts. |
| [NVIDIA NIM Developer Catalog](https://build.nvidia.com/) | Prototyping giant 300B-550B open-weight models that exceed consumer workstation memory. | No card: ~40 RPM developer prototyping catalog | Official documentation | Restricted to developer prototyping rather than production workloads, with occasional cold-start queues on large MoEs. |
| [OpenRouter (:free Routes)](https://openrouter.ai/) | Quick side-by-side model comparisons and light fallback routing across diverse open weights. | 20 RPM, 50 RPD ($0 balance) -> 1,000 RPD (>=10 credits balance) | Official documentation | 50 RPD on unverified $0 accounts runs out in roughly three multi-step coding tasks; negative balances return HTTP 402 even on :free routes. |
| [Groq Cloud LPU](https://console.groq.com/) | Sub-second small-prompt JSON routing (<6K tokens) and free audio transcription (2,000 requests/day). | No card: LLMs 30 RPM / 1K RPD / 8K TPM; Whisper 2K RPD / 28.8K audio sec/day | Official documentation | Strict 8,000 TPM cap on free LLMs causes immediate HTTP 429 failures on 20K-token coding agent prompts. |
| [Cloudflare Workers AI (Clef & Clairic)](https://developers.cloudflare.com/workers-ai/) | Zero-output-token edge classification, moderation, and typed extraction. | No card: 10,000 Neurons/day free (resets 00:00 UTC) | Official documentation | Legacy Workers AI generative catalog models were hard-retired on Nov 20, 2026 (HTTP 410). |
| [Pollinations AI](https://pollinations.ai/) | Last-resort keyless fallback for throwaway public sandbox tests where no API keys exist. | Keyless fair-use IP quota (text and image) | Official documentation | Shared public community service; never transmit private code, credentials, or personal data. |
<!-- swissknife:end -->

## Search, Scraping & Academic Grounding

<!-- swissknife:begin table tag=grounding -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Firecrawl](https://www.firecrawl.dev/) | Turning modern dynamic documentation sites into clean Markdown for research and RAG. | Keyless onboarding skill + 500 starter credits | Primary evaluation | Keyless usage is strictly IP-rate-limited; create a free API key for multi-page crawls. |
| [Jina Reader (r.jina.ai / s.jina.ai)](https://jina.ai/reader/) | One-line URL reading inside shell scripts and lightweight agents. | Keyless prefix + 10M free tokens with free API key | Official documentation | Unauthenticated prefix requests throttle quickly under automated batch loops. |
| [Exa 3.0 Neural Search](https://exa.ai/) | High-precision web discovery for research agents and technical literature scouting. | No card: $10/mo recurring credits (~2,500 Lite searches) | Official documentation | Deep search modes exhaust monthly free credits much faster than Lite searches. |
| [OpenAlex Academic Graph](https://openalex.org/) | Primary literature review, DOI verification, and academic citation mapping. | Keyless: 100,000 requests/day forever | Official documentation | Pass ?mailto=you@domain.com in queries to enter the fast polite pool. |
<!-- swissknife:end -->

## Recommended Fallback Order by Task

- **Coding agent loops:** Google AI Studio (`gemini-4-hydrogen`) $\rightarrow$ Z.ai BigModel (`glm-4.7-flash`) $\rightarrow$ OpenRouter `:free` $\rightarrow$ NVIDIA NIM $\rightarrow$ Pollinations
- **1M-token repo / PDF ingestion:** Google AI Studio $\rightarrow$ Z.ai BigModel
- **Fast small-prompt JSON & Speech-to-Text:** Groq Cloud $\rightarrow$ Google AI Studio $\rightarrow$ Cloudflare Workers AI
- **Decision gates:** Google AI Studio (Gemini Decision 1) $\rightarrow$ Cloudflare Workers AI (`Clef` / `Clairic`)

---

**Continue reading:** [The Personal AI Fabric](personal-ai-fabric.md) · [Retired & Disqualified Tools](../reference/retired.md)
