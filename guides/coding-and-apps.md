---
title: "Coding & Apps"
section: guides
summary: "End-to-end web, CLI, and Apple mobile engineering pairing verified models and harnesses with Context7 live docs, Playwright QA, MobileBuildMCP, and TDD skills."
order: 2
---

[Home](../README.md) / Guides / Coding & Apps

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Coding & Apps

High-reliability software engineering with AI agents comes down to three habits: **grounding against live library docs**, **enforcing test-driven discipline**, and **verifying real runtime output** in a browser or simulator rather than trusting "looks good to me."

## Active Brain & Harness Anchors

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

<!-- swissknife:begin slot id=dev-harness -->
**Active Anchor — [Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi)**

Minimal, hackable agent kernel with built-in /llama router support, /v1/systemone decision-model discovery, /tree DAG branching, MCP + Codemode JS sandbox, and SQLite durability.

- **When to use:** Flagship developer anchor: run naked in 5 minutes, or optionally rice across 6 modular rungs (LoRA, sandbox, smart MCP, durability, mobile HITL, ComfyUI).
- **Upstream docs:** [Official setup & reference](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/llama-cpp.md)
- **Evidence:** Primary evaluation · verified 2026-11-28
- **Compatible adapters:** [Qwen3.8-27B Pi Specialist LoRA (~319 MB)](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted-GGUF), [Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)
- **Why this pick:** [Pair OpenCode (Newcomer Anchor) with Pi (Flagship Developer Kernel)](../docs/why-this-stack.md#adr-why-pi-and-opencode)
- **Limitation:** Intentionally omits built-in per-tool approval prompts; pair with gondolin, nono, or safeagents before autonomous runs.
- **Limitation:** Requires Node 22.19+; built-in MCP keeps enabled servers alive all session unless replaced with pi-mcp-adapter.
<!-- swissknife:end -->

*(Newcomers starting locally should use [`OpenCode`](../docs/start-here-newcomer.md) with built-in per-action approval prompts.)*

## Verified Engineering Tools & Skills

<!-- swissknife:begin table tag=coding-tool -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Rex Terminal & Persistent Session Server (Superlogical)](https://www.superlogical.com/rex/docs/installation) | Running a 16GB M4 Mac mini as a 24/7 remote AI cockpit alongside Pi and @earendil-works/pi-durable. | 24/7 Persistent Agent Terminal Server (Pragmatic Exception) | Official documentation | Proprietary software currently in invite/Discord public beta; pragmatic exception chosen for first-class Pi OSC 7501 integration. |
| [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) | Verifying web applications, forms, and visual regressions directly from Pi, OpenCode, or Antigravity. | Apache-2.0 | Official documentation | Accessibility snapshots cannot inspect inside closed Shadow DOM. |
| [Upstash Context7 (ctx7 & @upstash/context7-pi)](https://github.com/upstash/context7) | Working with fast-moving web, Python, or mobile SDKs. | MIT | Primary evaluation | Pin local Context7 servers to >= 2.1.3 (CVE-2026-75130) and explicitly instruct agents in AGENTS.md to call it. |
| [Sentry MobileBuildMCP](https://github.com/getsentry/MobileBuildMCP) | Native Apple Swift/iOS/macOS development on Apple Silicon Macs. | MIT | Official documentation | Stops at Apple builds and simulators; physical USB Android/iOS UI testing requires separate device tooling. |
| [obra/superpowers (15-Skill Engineering Pack)](https://github.com/obra/superpowers) | Eliminating agent drift during multi-hour autonomous coding sessions across Pi, OpenCode, Antigravity, and Hermes. | MIT | Field observation | On Hermes Agent, use the Hermes-native tool mapping port rather than raw Claude Code tool names. |
| [nicobailon/pi-mcp-adapter (Lazy & Semantic MCP)](https://github.com/nicobailon/pi-mcp-adapter) | Rung 3 of the Pi Ricing Journey once you attach more than 3-4 MCP servers and want zero context bloat. | MIT | Primary evaluation | Automatically replaces Pi's built-in MCP handler upon installation. |
<!-- swissknife:end -->

## Recommended Workflow

1. **Choose your compute world:** Use zero-card Google AI Studio (`gemini-4-hydrogen`) for public/learning repos, or local `Qwen3.8-27B` (+ HF Harness Adapter) for private repositories.
2. **Ground breaking APIs:** Add an explicit line in your repository's `AGENTS.md` instructing the agent to consult **Context7** before writing code against fast-moving 2026 SDKs (pin local Context7 servers to `>= 2.1.3`).
3. **Prevent drift on multi-hour tasks:** Enable **`obra/superpowers`** (Brainstorm $\rightarrow$ Spec $\rightarrow$ Red/Green TDD $\rightarrow$ Verification) and wrap autonomous runs in `gondolin`, `nono`, or `safeagents`.
4. **Verify real output:** Drive live browser checks with **Microsoft Playwright MCP** (keeping in mind accessibility snapshots skip closed Shadow DOM) or run native Apple builds and `XCTest` suites on macOS via **Sentry MobileBuildMCP**.

---

**Continue reading:** [Pi Ricing Workshop](pi-workshop.md) · [Persistent Memory & Knowledge Loops](memory-and-knowledge.md)
