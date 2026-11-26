← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)

# 🎯 Deep Research & Cited Literature Synthesis · 🟢 `Fresh`

> [!IMPORTANT]
> **Verdict:** Combine GPT Researcher or DeerFlow 2.0 with card-free Exa 3.0, Tavily, and keyless OpenAlex (100K/day) for high-precision cited reports.
> **Category:** `knowledge` · **Age:** `0d` (TTL `60d`)

## 1. Resolved Stack Components

| Role | Entity & Lifecycle | Live Health | Operational Gotchas |
| :--- | :--- | :--- | :--- |
| **`primary_models`** | [**Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)**](https://aistudio.google.com/)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 21d</sub> | ⚠️ Gemini 2.5 retires Dec 1, 2026; 4 Argon/Carbon/Neon, Batch, and Search Grounding are paid-only.<br>⚠️ Free tier prompts may be logged outside EU/UK/CH; redact sensitive PII. |
| **`primary_models`** | [**Qwen3.8-27B (Dense Vision+Text)**](https://huggingface.co/Qwen/Qwen3.8-27B)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Use IQ4_XS + Q8 KV cache on 16GB VRAM so it never spills across PCIe. |
| **`harnesses`** | [**Hermes Agent (v0.23.4 Self-Improving Daemon)**](https://github.com/NousResearch/hermes-agent)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Does not auto-compact aggressively like Pi by default; cap thinking/context tokens on giant repos. |
| **`harnesses`** | [**Pi Durable (SQLite Crash-Resumable Runtime)**](https://github.com/disler/durable-pi)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Adds daemon state management overhead; use plain Pi for quick one-off terminal edits. |
| **`specialist_tools`** | [**GPT Researcher (gptr-mcp & Skill)**](https://github.com/assafelovic/gpt-researcher)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Always verify primary DOIs/URLs before citing autonomous research syntheses. |
| **`specialist_tools`** | [**DeerFlow 2.0 SuperAgent Research Harness**](https://github.com/bytedance/deer-flow)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Requires Docker daemon and search API keys (pair with Exa 3.0 or Tavily free tiers). |
| **`specialist_tools`** | [**K-Dense Scientific Agent Skills**](https://github.com/K-Dense-AI/claude-scientific-skills)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Validate statistical calculations with Python scripts rather than raw LLM arithmetic. |
| **`specialist_tools`** | [**Exa 3.0 Neural Search**](https://exa.ai/)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 21d</sub> | ⚠️ Deep research mode burns monthly credits faster than Lite mode. |
| **`specialist_tools`** | [**Tavily Search API**](https://tavily.com/)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Advanced search depth consumes 2 credits per call vs 1 for basic. |
| **`specialist_tools`** | [**OpenAlex + arXiv API**](https://openalex.org/)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Pass ?mailto=you@domain.com in OpenAlex URLs to enter the fast polite pool. |

## 2. Recommended Workflow

1. Query OpenAlex polite pool and Exa 3.0 to gather primary papers, DOIs, and full-text PDFs.
2. Run GPT Researcher or DeerFlow 2.0 over both web sources and local PDF/CSV folders.
3. Audit every cited claim and statistical table against primary DOIs before publishing.

## 3. Domain Guardrails

- ⚠️ Never treat autonomous research syntheses as publication-ready without checking primary URLs and numbers.

<details>
<summary>🛠️ <b>Click to expand Resolved Launch Recipes</b></summary>
<br>

```bash
# [qwen3.8-27b]
llama-server -m Qwen3.8-27B-IQ4_XS.gguf -ngl 99 -fa on -c 32768 -ctk q8_0 -ctv q8_0
```
</details>

---

← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)
