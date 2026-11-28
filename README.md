# AI Swiss Knife

[![CI](https://github.com/initalok/ai-swissknife/actions/workflows/ci.yml/badge.svg)](https://github.com/initalok/ai-swissknife/actions/workflows/ci.yml)
[![Health & Momentum](https://github.com/initalok/ai-swissknife/actions/workflows/health.yml/badge.svg)](https://github.com/initalok/ai-swissknife/actions/workflows/health.yml)
[![License: All Rights Reserved](https://img.shields.io/badge/License-All%20Rights%20Reserved-30363D.svg)](LICENSE)

A practical, source-verified field guide to building with zero-cost cloud APIs, local AI hardware, open agent harnesses, and a private multi-device AI fabric—continuously checked against link rot and upstream drift.

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](STATUS.md)) · [For AI Agents (`llms.txt`)](llms.txt)*
<!-- swissknife:end -->

## Choose Your Track

| Who you are | Start here |
| :--- | :--- |
| **New to AI, local models, or a student?** Start with 6 plain-English terms, a 30-second hardware check, and three zero-paralysis first wins ($0 Cloud, first local coding agent, or turnkey local media). | [**Newcomer & Student Onboarding**](docs/start-here-newcomer.md) |
| **Seasoned developer or systems builder?** Jump straight to agent token math, memory physics, our flagship mod-able `Pi` harness ladder, frozen-base LoRA serving, and machine manifests. | [**Seasoned Developer Fast-Track**](docs/start-here-developer.md) |

---

## Four Compute Worlds (Plus How to Connect Them)

Instead of forcing one machine to do everything, AI Swiss Knife separates work by hardware physics and connects your devices privately when a task calls for a hybrid split.

<!-- swissknife:begin worlds-index -->
| Compute World | What Its Physics Excels At | Guide |
| :--- | :--- | :--- |
| **Zero-Card Cloud** | 1M-token context, 500B+ MoE reasoning, zero-install onboarding, and burst speech/media trials with no credit card. | [Zero-Card Cloud](worlds/cloud.md) |
| **Apple Silicon Mac** | Silent ~15W always-on control plane, unified-memory MLX inference (no PCIe split), and native Apple/Xcode builds. | [Apple Silicon Mac (16GB M4 Mac mini 24/7 Server)](worlds/apple-silicon.md) |
| **Discrete GPU PC (16GB VRAM + 64GB RAM)** | Fast CUDA prefill, hybrid sparse MoE offloading, and all heavy local image, video, and 3D generation. | [Discrete GPU PC (16GB VRAM + 64GB RAM)](worlds/gpu-workstation.md) |
| **Mobile (Human Communicator & HITL)** | Approval gates, voice steering, camera/share-sheet capture, and zero-port remote pings—never brute-force inference. | [Mobile as Human Communicator (HITL)](worlds/mobile-hitl.md) |
<!-- swissknife:end -->

Want to bridge your Mac mini, discrete GPU PC, Android phone, and zero-card cloud without opening a single router port? Read [**The Personal AI Fabric**](worlds/personal-ai-fabric.md).

---

## Full Contents

### Orientation & Philosophy
<!-- swissknife:begin nav section=docs -->
- **[Newcomer & Student Onboarding](docs/start-here-newcomer.md)** — Six essential terms, a 30-second hardware check, and three zero-paralysis first wins ($0 Cloud, Local Coding, or Local Media).
- **[Seasoned Developer Fast-Track](docs/start-here-developer.md)** — 60-second hardware physics, harness selection leading into Pi's optional 6-rung ricing ladder, frozen-base LoRAs, and machine manifests.
- **[How a Modern AI Stack Fits Together](docs/mental-model.md)** — A 3-minute plain-English primer explaining models, LoRA adapters, inference runtimes, safety boundaries, and agent harnesses.
- **[Why This Stack (Decision Records)](docs/why-this-stack.md)** — Transparent architectural decisions explaining why we anchor on Pi, OpenCode, Qwen3.8-27B, llama.cpp/MLX, WanGP/ComfyUI, Mobile HITL, and Tailscale—including valid exceptions and reversal triggers.
- **[Security & Trust Boundaries](docs/security-and-trust.md)** — Three calm safety habits for newcomers and a six-boundary threat model for connecting Cloud, Mac, GPU PC, Mobile HITL, and Knowledge Vaults.
- **[How This Guide Is Maintained](docs/architecture.md)** — Maintainer handbook: single-source in-place managed blocks, auto-discovered registry, upstream release momentum watchers, and the sync-upstream agent skill.
<!-- swissknife:end -->

### Compute Worlds & Fabric
<!-- swissknife:begin nav section=worlds -->
- **[Zero-Card Cloud](worlds/cloud.md)** — Verified $0 credit-card-free cloud gateways, coding-agent token math, search grounding APIs, and fallback order.
- **[Apple Silicon Mac (16GB M4 Mac mini 24/7 Server)](worlds/apple-silicon.md)** — Running a power-efficient 16GB M4 Mac mini as a 24/7 remote AI server built around Rex, Pi, Pi Durable, nono v0.82 sandboxing, and <=10 GB local MLX helpers.
- **[Discrete GPU PC (16GB VRAM + 64GB RAM)](worlds/gpu-workstation.md)** — Understanding the Zone 1 / Zone 2 memory split, llama-server router flags, Ollama's 4K context trap, and 16GB VRAM coexistence with ComfyUI.
- **[Mobile as Human Communicator (HITL)](worlds/mobile-hitl.md)** — Using your phone strictly as a Human-in-the-Loop approval gate, voice steering surface, and capture bridge—never as a brute-force LLM runner.
- **[The Personal AI Fabric](worlds/personal-ai-fabric.md)** — How to connect Zero-Card Cloud, Apple Silicon Mac, Discrete GPU PC, and Mobile HITL privately with zero open router ports.
<!-- swissknife:end -->

### Practical Guides
<!-- swissknife:begin nav section=guides -->
- **[Pi Ricing Workshop (Optional 6-Rung Ladder)](guides/pi-workshop.md)** — Progressive, 100% optional journey taking Pi Coding Agent from naked in 5 minutes to adapted local GGUF, sandboxing, smart MCP, durability, mobile HITL, and ComfyUI.
- **[Coding & Apps](guides/coding-and-apps.md)** — End-to-end web, CLI, and Apple mobile engineering pairing verified models and harnesses with Context7 live docs, Playwright QA, MobileBuildMCP, and TDD skills.
- **[Local Media Studio (WanGP & ComfyUI)](guides/media-studio.md)** — Unified local creative pipeline separating turnkey low-VRAM generation (WanGP) from programmable agent-driven node graphs (ComfyUI + MCP), plus code motion graphics and WebGPU speech.
- **[Persistent Context, Memory & Knowledge Loops](guides/memory-and-knowledge.md)** — Four clean layers for durable agent and personal memory using AGENTS.md/SKILL.md, Pi Durable, plain-Markdown Obsidian vaults, local qmd hybrid search, and KV-cache-stable injection.
- **[Research & Writing](guides/research-and-writing.md)** — Cited literature synthesis combining OpenAlex academic graphs, Exa 3.0 neural search, Firecrawl Markdown extraction, and open research harnesses.
- **[Specialist Domains](guides/specialist-domains.md)** — Upstream-federated starting stacks (max 2 direct picks + 1 monitored upstream directory) for Reverse Engineering, Game Dev & 3D, Growth & Social, and Unfiltered Local AI.
<!-- swissknife:end -->

### Reference
<!-- swissknife:begin nav section=reference -->
- **[Models Reference (Across Hardware Tiers & Special Use Cases)](reference/models.md)** — Core model fundamentals spanning Edge/16GB M4 Mac, 16-24GB GPUs, Hybrid/80GB servers, research-leading open frontier weights, and specialized OCR/speech/video/diffusion checkpoints.
- **[Retired & Disqualified Tools](reference/retired.md)** — CI-enforced graveyard recording closed free tiers, archived extensions, and oversized models alongside their active replacements.
<!-- swissknife:end -->

### Research & Horizon
<!-- swissknife:begin nav section=research -->
- **[Harness Adapters & In-Harness RL](research/harness-adapters.md)** — Primary empirical evidence showing why lightweight per-harness LoRAs on frozen Qwen3.8-27B outperform larger unadapted checkpoints, including difficulty ablations and AutomationBench controls.
- **[21-Day Watch List](research/watch-list.md)** — Auto-expiring, hard-capped radar tracking frontier ceilings (monitor-only, excluded from llms.txt) and reproducible community field observations.
<!-- swissknife:end -->

---

## Editorial Standards & Non-Goals

Every recommendation names its evidence tier (*Primary evaluation*, *Official documentation*, *Vendor / lab claim*, or *Field observation*), states explicit limitations, and explains its falsifiable reversal trigger in [Why This Stack](docs/why-this-stack.md). To stay lean and forward-moving, this project explicitly enforces these boundaries:

<!-- swissknife:begin non-goals -->
- No enterprise GPU cluster orchestration (multi-node Kubernetes/Slurm farms or commercial MLOps stacks).
- No brute-force mobile LLM inference (phones are documented strictly as human communicators, HITL gates, and capture surfaces).
- No paid-only SaaS directories (closed paid frontier models live only on the 21-day monitor-only Watch List).
- No custom benchmarking or smoke-test frameworks (rely on primary evaluations and 1-line upstream built-in sanity checks).
- No mirroring upstream installation manuals (own curated paths, cross-tool glue, real-world traps, and canonical upstream deep-links).
- No museum of legacy options (one active anchor per Workflow Slot; superseded picks move cleanly to Retired and Superseded ADR history).
<!-- swissknife:end -->
