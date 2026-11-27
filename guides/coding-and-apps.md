[Home](../README.md) / Guides / Coding & Apps

*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md))*

# Coding & Apps

End-to-end engineering workflow pairing verified models and harnesses with live documentation lookup, browser QA, and Apple mobile build tools.

## Recommended Stack

The components below are selected for this workflow based on verified compatibility and current link health.

### Models & Cloud Gateways

- **[Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/)** — Default zero-card cloud gateway for multi-step coding agents, full-repository ingestion, and multimodal reasoning. *(Official documentation)*
- **[Z.ai BigModel (GLM-4.7-Flash)](https://open.bigmodel.cn/)** — Secondary no-card backup for long-context coding and tool-use loops when Google AI Studio rate limits are reached. *(Official documentation)*
- **[NVIDIA NIM Developer Catalog](https://build.nvidia.com/)** — Testing giant 300B-550B open-weight models that cannot fit inside consumer workstation memory. *(Official documentation)*
- **[OpenRouter (:free Routes)](https://openrouter.ai/)** — Quick model comparisons and light fallback routing across diverse open weights. *(Official documentation)*
- **[Pollinations AI](https://pollinations.ai/)** — Last-resort keyless fallback for ephemeral sandbox testing where no API keys exist. *(Official documentation)*
- **[Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B)** — Daily-driver local coding, strict instruction following, and single-backbone multi-LoRA serving. *(Primary evaluation)*
- **[Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF)** — Larger repository reasoning and multi-file refactoring on 16GB GPU + 64GB RAM workstations or 64GB+ Macs. *(Official documentation)*
- **[Gemma 4 Family (26B-A4B Vision & 12B Tri-Modal)](https://ai.google.dev/gemma)** — High-speed local general chat, vision inspection, or local audio analysis. *(Official documentation)*
- **[Inkling 2 Mini (26.4B Looped Transformer MoE)](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF)** — Experimenting with high-efficiency looped coding architectures inside 16GB-18GB memory budgets. *(Vendor / lab claim)*

### Agent Harnesses

- **[Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi)** — When you want full control over context assembly, clean compaction, and the highest-scoring official target for Hugging Face's RL harness adapters. *(Primary evaluation)*
- **[DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness)** — Building custom agent loops, interactive Creator Mode plugins, or multi-harness web sessions. *(Official documentation)*
- **[Hermes Agent (v0.23.4)](https://github.com/NousResearch/hermes-agent)** — Always-on background assistants, scheduled research digests, and multi-surface personal operations. *(Official documentation)*
- **[OpenCode CLI](https://github.com/anomalyco/opencode)** — Straightforward terminal software engineering with zero vendor lock-in. *(Primary evaluation)*

### Inference & Media Runtimes

- **[llama.cpp (Mainline GGUF Engine)](https://github.com/ggml-org/llama.cpp)** — Primary local LLM server on NVIDIA workstations and cross-platform CLI deployments. *(Official documentation)*
- **[Unsloth Runtime & Studio](https://github.com/unslothai/unsloth)** — Serving Dynamic v3.1 GGUFs, local Laya decision endpoints, or routing Anthropic-protocol clients to local models. *(Official documentation)*
- **[Apple MLX (mlx-lm)](https://github.com/ml-explore/mlx-lm)** — Primary local serving engine on Apple Silicon Macs (M-series Mac mini, MacBook Pro, Mac Studio). *(Field observation)*

### Compatible LoRA Adapters

- **[Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)** — Serving multiple agent harnesses from one frozen 15 GB base model, or running with thinking mode enabled (xhigh). *(Primary evaluation)*

### Safety Boundaries

- **[Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya)** — Fast zero-output-token tool-safety checks, routing gates, and memory verification without occupying GPU VRAM.
- **[Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents)** — Mandatory guard layer between autonomous coding harnesses (or unfiltered local models) and shell/filesystem tools.

## Supporting Domain Tools

- **[Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp)** — Browser accessibility-tree automation with Planner, Generator, and Healer testing agents.
- **[Upstash Context7 (ctx7 & @upstash/context7-pi)](https://github.com/upstash/context7)** — Injects live version-matched library documentation directly into coding agents.
- **[Sentry MobileBuildMCP](https://github.com/getsentry/MobileBuildMCP)** — Builds Apple targets, runs XCTest suites, and attaches LLDB (formerly XcodeBuildMCP).
- **[obra/superpowers](https://github.com/obra/superpowers)** — 15 workflow skills enforcing Brainstorm -> Spec -> Red/Green TDD -> Verification before completion.

## Step-by-Step Workflow

1. Choose your inference layer: zero-card Google AI Studio (gemini-4-hydrogen) or local Qwen3.8-27B + HF Harness Adapter.
2. Add an explicit instruction in your repository AGENTS.md telling the agent to check Context7 before using fast-moving 2026 framework APIs.
3. Wrap shell-capable harnesses behind safeagents (and optionally Laya 0.5) before launching multi-hour autonomous runs.
4. Verify web UI behavior with Playwright MCP or Apple builds and XCTest suites with Sentry MobileBuildMCP.

## Limitations & Trade-Offs

- Pin local Context7 servers to >= 2.1.3 (CVE-2026-75130); Playwright accessibility snapshots cannot inspect closed Shadow DOM.
- MobileBuildMCP stops at Apple builds and simulators; physical USB Android/iOS UI testing requires separate device tooling.

---

**Continue reading:** [Local AI Workstation Guide](local-ai-workstation.md) · [Specialist Domains](specialist-domains.md)
