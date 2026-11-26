← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)

# Chapter 04 · Agent Harnesses, Protocols & Safety

> [!IMPORTANT]
> **Verdict:** Use Pi / Pi Durable as your minimal building-block kernel, DeepSeek Harness (dsh) for Cordis plugin composability, and Hermes Agent for self-improving persistence—shielded by safeagents.
> **Read this chapter if:** You are choosing an agent harness, wiring Skills/MCP, or sandboxing autonomous tool calls.

## 1. Agent Harnesses by Architectural Role

| Harness & Health | Architecture & Capabilities | License & TTL | Pairing & Gotcha |
| :--- | :--- | :--- | :--- |
| [**Pi Coding Agent (Building-Block Kernel)**](https://pi.dev/)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Minimalist TUI/RPC/SDK kernel with /tree DAG branching and built-in MCP + Codemode JS sandbox<br>🏆 Highest-scoring HF Harness Adapter target (64.7% SWE-Pro hard-51) and Inkling 2 Mini reference harness | `MIT`<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Intentionally omits built-in per-tool approval gates; pair with safeagents or OS sandboxes. |
| [**Pi Durable (SQLite Crash-Resumable Runtime)**](https://github.com/disler/durable-pi)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 SQLite/JSONL crash-resumable agent network, atomic shared app state, background compaction (200K/250K), live tool hot-swap | `MIT`<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Adds daemon state management overhead; use plain Pi for quick one-off terminal edits. |
| [**DeepSeek Harness (dsh / Cordis Platform)**](https://github.com/deepseek-ai/deepseek-harness)<br><sub>`experimental` · 🟢 `Fresh`</sub> | 🏆 Cordis everything-is-a-plugin architecture letting you replace the agent loop itself, Creator Mode, built-in read-only sandbox<br>🏆 First-party plugins orchestrate Claude Code & Codex as sub-agents; supports local OpenAI-compat servers | `MIT`<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Rapidly iterating developer preview (0.2.3-alpha.2); pin plugin versions against breaking API changes. |
| [**Hermes Agent (v0.23.4 Self-Improving Daemon)**](https://github.com/NousResearch/hermes-agent)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 #1 globally on OpenRouter token volume; persistent memory, autonomous skill creation, Telegram/cron/ACP, 40+ tools<br>🏆 Official HF Harness Adapter target (Qwen3.8-27B-hermes-adapted) | `MIT`<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Does not auto-compact aggressively like Pi by default; cap thinking/context tokens on giant repos. |
| [**Google Antigravity (2.0 Desktop, CLI & SDK)**](https://aistudio.google.com/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Unified GUI+CLI harness running Gemini 4 Hydrogen (Everyday/Thinking + Task mode), 3.8 Flash, & 4 Argon/Carbon/Neon | `Proprietary`<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Tied to Google auth/billing for paid frontier nodes; configure local fallback for offline sessions. |
| [**Zed Editor + ACP Registry**](https://zed.dev/)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Unifies Pi, Claude Agent, Codex, Gemini CLI, OpenCode, and Cursor inside one native multi-file diff UI with zero telemetry | `Apache-2.0`<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Requires ACP-compatible agent binary installed locally. |
| [**OpenCode CLI**](https://github.com/anomalyco/opencode)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Vendor-agnostic terminal coding agent with official HF Qwen3.8-27B-opencode-adapted LoRA | `MIT`<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Does not auto-compact as aggressively as Pi; watch context length on multi-hour repos. |

## 2. Safety Proxies & Core Protocols

| Tool / Pattern | What It Solves | License & TTL | Production Guardrail |
| :--- | :--- | :--- | :--- |
| [**Hugging Face safeagents Runtime Proxy**](https://github.com/huggingface/safeagents)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Transparent OpenAI/Anthropic proxy with atif-scan (10-20ms on Apple Silicon) & Decision Model judge<br>🏆 Audited 1.3M tool calls and blocked 647 suspicious calls during HF harness-adapter RL training | `Apache-2.0`<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Configure domain plugins (e.g. hf://harness-hub/qwen-safeagents-plugin) rather than running empty defaults. |
| [**Progressive Skills (SKILL.md) & AGENTS.md**](https://agents.md/)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Loads tool instructions on demand to preserve KV prompt cache instead of dumping 30+ MCP schemas upfront | `Open-Standard`<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Keep AGENTS.md under 500 tokens; offload heavy domain instructions into on-demand SKILL.md modules. |
| [**Retrieval Context Archival (vs Lossy Summaries)**](https://github.com/unslothai/unsloth)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Archives old turns to searchable SQLite/vector history at 200K tokens instead of destructive summarization | `Open-Pattern`<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Pair with Laya + all-MiniLM-L6-v2 (23 MB) if you need auditable fact-invalidation ledgers. |

<details>
<summary>🛠️ <b>DeepSeek Harness & safeagents Quickstart</b></summary>
<br>

```bash
npx @deepseek-ai/dsh web
safeagents start http://localhost:8000 --plugin hf://harness-hub/qwen-safeagents-plugin
```
</details>

---

← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)
