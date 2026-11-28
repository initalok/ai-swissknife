---
title: "Why This Stack (Decision Records)"
section: docs
summary: "Transparent architectural decisions explaining why we anchor on Pi, OpenCode, Qwen3.8-27B, llama.cpp/MLX, WanGP/ComfyUI, Mobile HITL, and Tailscale—including valid exceptions and reversal triggers."
order: 4
---

[Home](../README.md) / Orientation / Why This Stack

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy · 1 upstream release(s) queued ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Why This Stack (Decision Records)

Most AI directories hand you a list of links and ask for blind trust. This page documents **why** AI Swiss Knife anchors on its recurring picks (`Pi`, `OpenCode`, `Qwen3.8-27B`, `llama.cpp`, `MLX`, `WanGP`, `ComfyUI`, `Google AI Studio`, Mobile-as-HITL, and `Tailscale`).

Every decision below states **serious alternatives evaluated**, **valid situations where you should ignore our pick**, and a **falsifiable reversal trigger**—the exact real-world change that will cause us to replace an anchor. When an anchor is replaced, its old record moves to *Historical & Superseded* rather than lingering as clutter in active guides.

<!-- swissknife:begin decisions-index -->
<a id="adr-why-pi-and-opencode"></a>
### Pair OpenCode (Newcomer Anchor) with Pi (Flagship Developer Kernel) (`Accepted`)

- **The job:** Give newcomers safe, frictionless local coding on day one while giving developers a minimal, infinitely mod-able harness.
- **Current anchor:** [Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi), [OpenCode CLI & Desktop](https://github.com/anomalyco/opencode)
- **Alternatives evaluated:** Google Antigravity, Hermes Agent, DeepSeek Harness (dsh), Claude Code
- **Why this leads today:** OpenCode wins beginner onboarding with 1-line install, built-in per-action approval prompts, and offline share-disabled mode. Pi wins as our long-term developer anchor because it is a minimal loop you own, ships built-in /llama router support and /tree DAG branching, achieves the highest HF RL LoRA lift (39.2% -> 64.7% SWE-Pro hard-51), and scales cleanly across an optional 6-rung ricing ladder.
- **When to choose an alternative:** Start with Google Antigravity if you want a $0 zero-install cloud IDE/CLI.
- **When to choose an alternative:** Choose Hermes Agent if you want an always-on self-improving personal daemon with native messaging out of the box.
- **When to choose an alternative:** Choose DeepSeek Harness (dsh) if you want a desktop/web platform where the core agent loop itself is a swappable plugin.
- **Reversal trigger:** Another MIT-licensed harness matches Pi's transparency, built-in llama.cpp/LoRA ecosystem, and modular durability with lower operational friction.
- *Recorded 2026-11-28*

<a id="adr-why-qwen38-27b"></a>
### Standardize Local Coding on Frozen Qwen3.8-27B + Hot-Swappable LoRAs (`Accepted`)

- **The job:** Deliver reliable local coding, vision, and agentic tool use inside 16GB VRAM or 32GB+ Apple Silicon without PCIe bottlenecks.
- **Current anchor:** [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B)
- **Alternatives evaluated:** Inkling 2 Mini (26.4B Looped MoE), Qwen3-Coder-Next (80B-A3B), Gemma 4 (12B / 26B), Dense 70B models
- **Why this leads today:** At IQ4_XS (~14.5 GB) with Q8 KV cache, Qwen3.8-27B stays 100% resident in 16GB VRAM and acts as one frozen backbone for multiple lightweight adapters: HF's pi LoRA lifted reproduced TB2.1 from 39% -> 55% pass@1 while cutting tokens nearly in half (2.9K -> 1.5K/task), and 26 MB abliterated LoRAs share the exact same base file.
- **When to choose an alternative:** On 8GB-12GB student laptops, use $0 Cloud or Gemma 4 12B (~8.5 GB) instead of OOMing on a 27B checkpoint.
- **When to choose an alternative:** On 16GB VRAM + 64GB DDR5 workstations needing deeper multi-file MoE capacity, add Qwen3-Coder-Next (80B-A3B).
- **When to choose an alternative:** For local audio understanding, use Gemma 4 12B.
- **Reversal trigger:** An Apache-2.0 successor (such as an open-weight Qwen4 <= 32B or mature Inkling follow-up) beats adapted Qwen3.8-27B inside 16GB VRAM with stable runtime support.
- *Recorded 2026-11-28*

<a id="adr-why-llama-cpp-and-mlx"></a>
### Use llama.cpp (NVIDIA/Cross-Platform) & MLX (Apple Silicon) Over Ollama Defaults (`Accepted`)

- **The job:** Serve local GGUF and unified-memory checkpoints with explicit context lengths, hybrid MoE control, and runtime LoRA loading.
- **Current anchor:** [llama.cpp (Mainline GGUF Server & Router)](https://github.com/ggml-org/llama.cpp), [Apple MLX (mlx-lm)](https://github.com/ml-explore/mlx-lm)
- **Alternatives evaluated:** Ollama, vLLM, LM Studio, ik_llama.cpp
- **Why this leads today:** llama.cpp exposes explicit context flags (-c), sparse MoE offloading (--n-cpu-moe), runtime --lora loading, and router mode (llama serve) integrated natively into Pi. Apple MLX beats llama.cpp by 46%-3x on Apple Silicon unified memory. Together they avoid Ollama's silent 4,096-token default context trap below 24 GiB VRAM and reported /v1 hangs on qwen3.8:27b.
- **When to choose an alternative:** Use LM Studio + LM Link when you want a zero-config GUI or zero-VPN home GPU sharing.
- **When to choose an alternative:** Use vLLM on multi-user Linux servers with 48GB+ dedicated VRAM.
- **Reversal trigger:** Ollama defaults to agent-safe context sizes (>=32K) and resolves /v1 tool-calling stability, or a unified engine surpasses both llama.cpp and MLX.
- *Recorded 2026-11-28*

<a id="adr-why-wangp-and-comfyui"></a>
### Split Local Media Into Turnkey Low-VRAM (WanGP) vs. Programmable Agent Engine (ComfyUI + MCP) (`Accepted`)

- **The job:** Give newcomers an easy 6-16GB all-in-one local media studio while giving developers an agent-controllable node-graph server.
- **Current anchor:** [WanGP v20.21 (One-Stop Low-VRAM Media Studio)](https://github.com/deepbeepmeep/WanGP), [ComfyUI (Comfy-Org Programmable Node Graph)](https://github.com/Comfy-Org/ComfyUI), [Comfy-Org Official comfy-mcp (Local & Cloud)](https://github.com/Comfy-Org/comfy-mcp), [Wan 2.2 (5B & A14B Apache-2.0 Video)](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B)
- **Alternatives evaluated:** ComfyUI alone, Separate standalone video/image/TTS repos, Closed cloud video APIs (Wan 3.0)
- **Why this leads today:** Head-to-head benchmarks show WanGP holding video generation to 5.9-14.3 GiB VRAM where ComfyUI peaks at 22.7-23.5 GiB, with guided installers starting at 6 GB VRAM. Meanwhile, Comfy-Org/ComfyUI (v0.46+) plus first-party comfy-mcp (Nov 2026) and artokun/comfyui-mcp excel as a programmable node-graph server driven remotely by Pi over Tailscale. Wan 2.2 provides an Apache-2.0 commercial-safe base.
- **When to choose an alternative:** For commercial still graphics, use Apache-2.0 FLUX.2 Klein rather than non-commercial Qwen-Image-2.1.
- **When to choose an alternative:** On Apple Silicon Macs, avoid heavy local video on MPS; route comfy-mcp to a remote NVIDIA PC or Comfy Cloud.
- **Reversal trigger:** ComfyUI matches WanGP's out-of-the-box 6-8GB VRAM memory management, or a newer permissive open video model supersedes Wan 2.2 on 16GB cards.
- *Recorded 2026-11-28*

<a id="adr-why-google-cloud"></a>
### Anchor Zero-Card Cloud on Google AI Studio (Gemini 4 Hydrogen) & Antigravity (`Accepted`)

- **The job:** Provide genuinely usable $0 cloud compute for beginners, students, and multi-step coding agents without a credit card.
- **Current anchor:** [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/), [Google Antigravity ($0 Individual Tier)](https://antigravity.google/)
- **Alternatives evaluated:** Z.ai BigModel, OpenRouter :free, Groq Cloud, NVIDIA NIM
- **Why this leads today:** Real coding agents consume ~20,000 input tokens per step across ~15 steps (~300,000 tokens/task). Groq's 8K TPM cap fails Step 1 and unverified OpenRouter (50 RPD) runs out in ~3 tasks. Google AI Studio's Free Tier (gemini-4-hydrogen, 1M unified context) plus Antigravity's $0 Individual tier is the only zero-card entry that sustains real agent loops out of the box.
- **When to choose an alternative:** Never send private repos or credentials to free cloud tiers; switch to local Qwen3.8-27B.
- **When to choose an alternative:** Use Groq specifically for fast <6K-token routers and free Whisper-Large-v3 speech transcription.
- **Reversal trigger:** Google requires a credit card on AI Studio Free Tier or reduces free token throughput below multi-step coding agent viability.
- *Recorded 2026-11-28*

<a id="adr-why-mobile-hitl"></a>
### Treat Mobile Strictly as Human Communicator & HITL Steering Surface (`Accepted`)

- **The job:** Keep human judgment, approvals, voice intent, and camera capture in your pocket while heavy compute stays on Mac/PC/Cloud.
- **Current anchor:** [pi-mobile (Multi-Box Tailscale HTTPS & Voice Mode)](https://pi.dev/packages/pi-mobile), [ayagmar/pi-mobile (Native Android Compose Client)](https://github.com/ayagmar/pi-mobile), [smixs/pi-durable-telegram (Durable Async Telegram Bot)](https://github.com/smixs/pi-durable-telegram)
- **Alternatives evaluated:** Brute-force on-phone LLM apps, Publicly exposed web terminals
- **Why this leads today:** Running 27B coding models or 1080p video on phone batteries yields poor speed and thermals. Using phones for what they excel at—push pings (ntfy), async messaging HITL (Telegram long-poll), and E2E Tailscale live steering (pi-mobile Voice Mode / Android Compose)—eliminates babysitting your terminal while keeping heavy weights on desktop silicon.
- **When to choose an alternative:** Use lightweight native dictation, camera photos, and OS share-sheets on mobile strictly as inputs into your home durable session.
- **Reversal trigger:** Mobile NPUs and unified RAM sustain 16GB+ workstation-class memory bandwidth without thermal throttling.
- *Recorded 2026-11-28*

<a id="adr-why-tailscale-and-lm-link"></a>
### Connect Compute Worlds via Loopback + Tailscale Serve (Dev) & LM Link (Zero-Config) (`Accepted`)

- **The job:** Bridge Mac mini, discrete GPU PC, and mobile HITL clients securely with zero open router ports.
- **Current anchor:** [Tailscale Serve (Loopback-to-Tailnet HTTPS Mesh)](https://tailscale.com/kb/1312/serve), [LM Link (Tailscale tsnet Zero-VPN GPU Sharing)](https://lmstudio.ai/docs/lmlink)
- **Alternatives evaluated:** Router port-forwarding, Binding 0.0.0.0 on LAN, Raw WireGuard / Headscale
- **Why this leads today:** Binding local AI services strictly to 127.0.0.1 and publishing through tailscale serve provides automatic HTTPS, zero exposed LAN ports, and device ACL tags. LM Link (powered by tsnet) gives newcomers a zero-VPN bridge to borrow a home desktop GPU from a thin laptop.
- **When to choose an alternative:** Self-hosted purists avoiding any third-party coordination server should run raw WireGuard or self-hosted Headscale.
- **Reversal trigger:** LM Link leaves free preview with restrictive pricing (affecting newcomers), or an open zero-trust mesh standard supersedes Tailscale.
- *Recorded 2026-11-28*

<a id="adr-why-sandboxes-and-safety"></a>
### Layer OS/VM Isolation (gondolin / nono) with Tool-Call Auditing (safeagents / Laya) (`Accepted`)

- **The job:** Prevent credential exfiltration and destructive shell mistakes when running autonomous or unfiltered local agents.
- **Current anchor:** [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents), [earendil-works/gondolin (libkrun Micro-VM + Secret Proxy)](https://github.com/earendil-works/gondolin), [nolabs-ai/nono (macOS Seatbelt & Linux Landlock Sandbox)](https://github.com/nolabs-ai/nono), [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya)
- **Alternatives evaluated:** Running agents unsandboxed, Docker-only containers, Manual human approval of every read-only command
- **Why this leads today:** Pi intentionally omits built-in approval prompts, and abliterated LoRAs cannot refuse destructive commands. gondolin provides lightweight libkrun micro-VMs with host placeholder secret injection (the VM never sees real tokens); nono provides zero-VM macOS Seatbelt/Linux Landlock for native builds; safeagents + Laya 0.5 audit tool calls in ~10-20ms without occupying GPU VRAM.
- **When to choose an alternative:** Beginners starting in OpenCode on disposable sample repos can rely on OpenCode's built-in per-action prompts before adopting full sandboxes.
- **Reversal trigger:** OS vendors ship native, zero-config capability sandboxes with built-in HTTP secret injection directly in macOS and Linux shells.
- *Recorded 2026-11-28*

<a id="adr-why-markdown-memory"></a>
### Keep Long-Term Agent Memory in Plain Markdown Vaults with KV-Cache-Stable Injection (`Accepted`)

- **The job:** Build durable personal and project memory that humans can read, edit, and sync across devices without destroying local inference speed.
- **Current anchor:** [Obsidian Official Agent Skills (1.2.3 + defuddle + obsidian-headless)](https://github.com/obsidianmd/obsidian-skills), [tobi/qmd (Local BM25 + Vector Markdown Search & MCP)](https://github.com/tobi/qmd), [pi-obsidian-memory (KV-Cache-Stable Vault Memory for Pi)](https://github.com/the-matt-moo/pi-obsidian-memory)
- **Alternatives evaluated:** Opaque cloud memory SaaS, Per-turn system-prompt mutation, Synced binary vector databases
- **Why this leads today:** Plain Markdown (AGENTS.md, SKILL.md, Obsidian vaults via obsidianmd/obsidian-skills) stays inspectable in Git and portable across 46+ agents. Pairing local tobi/qmd retrieval with KV-cache-stable session snapshots prevents llama.cpp and MLX from re-prefilling the entire prompt every turn, while keeping vector indexes machine-local prevents sync corruption.
- **When to choose an alternative:** Large multi-user engineering teams may still need a shared server-backed wiki or issue tracker alongside repo-local AGENTS.md.
- **Reversal trigger:** Local inference runtimes support arbitrary non-prefix KV-cache reuse without prefill latency penalties.
- *Recorded 2026-11-28*

## Historical & Superseded Decisions

<a id="adr-000-pi-llama-extension"></a>
### Use huggingface/pi-llama Extension for Local llama.cpp in Pi (`Superseded by `adr-why-pi-and-opencode``)

- **The job:** Connect Pi Coding Agent to local llama.cpp servers.
- **Current anchor:** —
- **Alternatives evaluated:** Manual OpenAI provider config
- **Why this leads today:** Historically required an external extension before native /llama router support landed in Pi core; archived upstream on Nov 9, 2026.
- **When to choose an alternative:** None; use Pi's built-in /llama integration.
- **Reversal trigger:** Superseded—preserved strictly as immutable architectural history.
- *Recorded 2026-11-09*
<!-- swissknife:end -->

---

**Continue reading:** [Security & Trust Boundaries](security-and-trust.md) · [Retired & Disqualified Tools](../reference/retired.md) · [System Status](../STATUS.md)
