← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)

# 🎯 Social Media Automation & Audience Ops · 🟢 `Fresh`

> [!IMPORTANT]
> **Verdict:** Run persistent Hermes or Pi Durable agents feeding Postiz's 30+ network approval calendar, polished with blader/humanizer and gated by Laya.
> **Category:** `growth` · **Age:** `0d` (TTL `60d`)

## 1. Resolved Stack Components

| Role | Entity & Lifecycle | Live Health | Operational Gotchas |
| :--- | :--- | :--- | :--- |
| **`primary_models`** | [**Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)**](https://aistudio.google.com/)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 21d</sub> | ⚠️ Gemini 2.5 retires Dec 1, 2026; 4 Argon/Carbon/Neon, Batch, and Search Grounding are paid-only.<br>⚠️ Free tier prompts may be logged outside EU/UK/CH; redact sensitive PII. |
| **`primary_models`** | [**Qwen3.8-27B (Dense Vision+Text)**](https://huggingface.co/Qwen/Qwen3.8-27B)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Use IQ4_XS + Q8 KV cache on 16GB VRAM so it never spills across PCIe. |
| **`primary_models`** | [**Laya Local Decision Models (678-846 MB)**](https://huggingface.co/convaiinnovations)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Threshold on probabilities (not confidence); route borderline superseded-vs-contradicted memory cases to review. |
| **`harnesses`** | [**Hermes Agent (v0.23.4 Self-Improving Daemon)**](https://github.com/NousResearch/hermes-agent)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Does not auto-compact aggressively like Pi by default; cap thinking/context tokens on giant repos. |
| **`harnesses`** | [**Pi Durable (SQLite Crash-Resumable Runtime)**](https://github.com/disler/durable-pi)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Adds daemon state management overhead; use plain Pi for quick one-off terminal edits. |
| **`specialist_tools`** | [**Postiz (Open-Source Multi-Network Scheduler)**](https://github.com/gitroomhq/postiz-app)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Always route agent posts through Postiz's human approval draft queue; unsupervised auto-posting invites bans. |
| **`specialist_tools`** | [**blader/humanizer & Listmonk**](https://github.com/blader/humanizer)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Never let humanizer rewrites alter verified technical numbers or claims. |
| **`safety_layer`** | [**Hugging Face safeagents Runtime Proxy**](https://github.com/huggingface/safeagents)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Configure domain plugins (e.g. hf://harness-hub/qwen-safeagents-plugin) rather than running empty defaults. |

## 2. Recommended Workflow

1. Generate channel-specific drafts from verified changelogs or source notes.
2. Pass copy through blader/humanizer to strip repetitive AI phrasing without altering facts.
3. Push drafts via Postiz REST API into the visual human approval calendar before publishing.

## 3. Domain Guardrails

- ⚠️ Never allow unsupervised auto-posting to live brand accounts; keep human approval in the loop.

<details>
<summary>🛠️ <b>Click to expand Resolved Launch Recipes</b></summary>
<br>

```bash
# [qwen3.8-27b]
llama-server -m Qwen3.8-27B-IQ4_XS.gguf -ngl 99 -fa on -c 32768 -ctk q8_0 -ctv q8_0

# [laya-decisions]
unsloth serve-decision convaiinnovations/laya-typed-decisions --port 8888
```
</details>

---

← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)
