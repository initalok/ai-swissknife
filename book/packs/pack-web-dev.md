← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)

# 🎯 Web Development & Visual QA · 🟢 `Fresh`

> [!IMPORTANT]
> **Verdict:** Pair Qwen3.8-27B + Harness Adapter (or Gemini 4 Hydrogen) with Context7 live docs, Playwright browser agents, and anti-slop UI skills.
> **Category:** `engineering` · **Age:** `0d` (TTL `60d`)

## 1. Resolved Stack Components

| Role | Entity & Lifecycle | Live Health | Operational Gotchas |
| :--- | :--- | :--- | :--- |
| **`primary_models`** | [**Qwen3.8-27B (Dense Vision+Text)**](https://huggingface.co/Qwen/Qwen3.8-27B)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Use IQ4_XS + Q8 KV cache on 16GB VRAM so it never spills across PCIe. |
| **`primary_models`** | [**Qwen3.8-27B Super-Adapter (Rank-96 PEFT Cat)**](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ If using a single harness with thinking off, prefer its specialist LoRA; mild pre-tool reasoning leakage occurs (arXiv:2610.14270). |
| **`primary_models`** | [**Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)**](https://aistudio.google.com/)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 21d</sub> | ⚠️ Gemini 2.5 retires Dec 1, 2026; 4 Argon/Carbon/Neon, Batch, and Search Grounding are paid-only.<br>⚠️ Free tier prompts may be logged outside EU/UK/CH; redact sensitive PII. |
| **`harnesses`** | [**Pi Coding Agent (Building-Block Kernel)**](https://pi.dev/)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Intentionally omits built-in per-tool approval gates; pair with safeagents or OS sandboxes. |
| **`harnesses`** | [**Google Antigravity (2.0 Desktop, CLI & SDK)**](https://aistudio.google.com/)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Tied to Google auth/billing for paid frontier nodes; configure local fallback for offline sessions. |
| **`harnesses`** | [**Zed Editor + ACP Registry**](https://zed.dev/)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Requires ACP-compatible agent binary installed locally. |
| **`specialist_tools`** | [**Playwright MCP & CLI Agents**](https://github.com/microsoft/playwright-mcp)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Accessibility snapshots cannot pierce closed Shadow DOM trees. |
| **`specialist_tools`** | [**Upstash Context7 MCP (Live Version Docs)**](https://github.com/upstash/context7)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Agents skip it unless explicitly reminded in AGENTS.md; pin local servers >= 2.1.3 (CVE-2026-75130). |
| **`specialist_tools`** | [**Anti-Slop UI Skills (taste-skill / impeccable / emilkowalski)**](https://github.com/Leonxlnx/taste-skill)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Load selectively as on-demand skills so frontend rules do not bloat backend coding sessions. |
| **`safety_layer`** | [**Hugging Face safeagents Runtime Proxy**](https://github.com/huggingface/safeagents)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Configure domain plugins (e.g. hf://harness-hub/qwen-safeagents-plugin) rather than running empty defaults. |

## 2. Recommended Workflow

1. Pin 'Always check Context7 MCP for 2026 framework APIs' inside repo AGENTS.md.
2. Load anti-slop UI skills only during frontend/design phases to protect KV cache.
3. Verify every layout and interaction end-to-end with Playwright Planner/Generator/Healer agents.

## 3. Domain Guardrails

- ⚠️ Pin local Context7 MCP >= 2.1.3 (CVE-2026-75130); Playwright accessibility trees cannot pierce closed Shadow DOM.

<details>
<summary>🛠️ <b>Click to expand Resolved Launch Recipes</b></summary>
<br>

```bash
# [qwen3.8-27b]
llama-server -m Qwen3.8-27B-IQ4_XS.gguf -ngl 99 -fa on -c 32768 -ctk q8_0 -ctv q8_0

# [qwen38-27b-super-adapter]
llama-server -m Qwen3.8-27B-IQ4_XS.gguf --lora Qwen3.8-27B-super-adapter-F16.gguf -ngl 99 -fa on -c 65536 -ctk q8_0 -ctv q8_0
```
</details>

---

← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)
