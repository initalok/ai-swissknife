← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)

# 🎯 Product Promotion, Launch Videos & Growth · 🟢 `Fresh`

> [!IMPORTANT]
> **Verdict:** Chain modular SEO/AEO/CRO skill packs with repo-to-launch video generators and Postiz scheduling for repeatable, auditable launches.
> **Category:** `growth` · **Age:** `0d` (TTL `60d`)

## 1. Resolved Stack Components

| Role | Entity & Lifecycle | Live Health | Operational Gotchas |
| :--- | :--- | :--- | :--- |
| **`primary_models`** | [**Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)**](https://aistudio.google.com/)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 21d</sub> | ⚠️ Gemini 2.5 retires Dec 1, 2026; 4 Argon/Carbon/Neon, Batch, and Search Grounding are paid-only.<br>⚠️ Free tier prompts may be logged outside EU/UK/CH; redact sensitive PII. |
| **`primary_models`** | [**Qwen3.8-27B (Dense Vision+Text)**](https://huggingface.co/Qwen/Qwen3.8-27B)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Use IQ4_XS + Q8 KV cache on 16GB VRAM so it never spills across PCIe. |
| **`harnesses`** | [**Hermes Agent (v0.23.4 Self-Improving Daemon)**](https://github.com/NousResearch/hermes-agent)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Does not auto-compact aggressively like Pi by default; cap thinking/context tokens on giant repos. |
| **`harnesses`** | [**OpenCode CLI**](https://github.com/anomalyco/opencode)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Does not auto-compact as aggressively as Pi; watch context length on multi-hour repos. |
| **`specialist_tools`** | [**Marketing & Growth Skill Packs (ericosiu / marketing-skills)**](https://github.com/topics/marketing-skills)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Audit every third-party outbound skill before connecting email/ad credentials; enforce CAN-SPAM/GDPR rate limits. |
| **`specialist_tools`** | [**Repo-to-Launch Video Skills (guizang / brag)**](https://github.com/topics/launch-video)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 21d</sub> | ⚠️ Review generated UI mockups carefully so promo videos match your real product. |
| **`specialist_tools`** | [**Postiz (Open-Source Multi-Network Scheduler)**](https://github.com/gitroomhq/postiz-app)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Always route agent posts through Postiz's human approval draft queue; unsupervised auto-posting invites bans. |
| **`safety_layer`** | [**Hugging Face safeagents Runtime Proxy**](https://github.com/huggingface/safeagents)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Configure domain plugins (e.g. hf://harness-hub/qwen-safeagents-plugin) rather than running empty defaults. |

## 2. Recommended Workflow

1. Run CRO, JSON-LD schema, and positioning audits using verified marketing SKILL.md modules.
2. Generate timed product launch reels directly from your repo and changelog.
3. Score copy variants iteratively while gating any outbound email/ad actions behind human approval.

## 3. Domain Guardrails

- ⚠️ Audit third-party outbound skills carefully and enforce CAN-SPAM, GDPR, and platform ToS limits.

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
