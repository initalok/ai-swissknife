---
title: "Seasoned Developer Fast-Track"
section: docs
track: developer
summary: "60-second hardware physics, harness selection leading into Pi's optional 6-rung ricing ladder, frozen-base LoRAs, and machine manifests."
order: 2
---

[Home](../README.md) / Orientation / Seasoned Developer Fast-Track

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Seasoned Developer Fast-Track

Skip the introductory glossary. This page summarizes the **hard engineering constraints**, our **flagship mod-able harness**, and how to consume this repository programmatically.

---

## 1. Sixty Seconds of Hard Physics & Real Failure Modes

- **Coding-Agent Token Math:** Real autonomous loops (`Pi`, `OpenCode`, `Antigravity`, `Hermes Agent`) average **~20,000 input tokens/step** over **~15 steps (~300,000 tokens/task)**. Free tiers with small TPM caps (like Groq's 8K TPM) fail on Step 1; use [Zero-Card Cloud](../worlds/cloud.md) routing chains built around `gemini-4-hydrogen` and `glm-4.7-flash`.
- **VRAM Bandwidth vs. Hybrid Sparse MoE:** Dense models that spill out of 16GB VRAM onto DDR5 crawl (~2–4 tok/s). Stay 100% resident in Zone 1 (`Qwen3.8-27B` `IQ4_XS` + Q8 KV cache) or use sparse MoEs (`Qwen3-Coder-Next`, 3B active) with `-ngl 99 --n-cpu-moe` in Zone 2. On Apple Silicon, unified memory eliminates the PCIe split (`mlx-lm` beats `llama.cpp` by 46%–3×).
- **Avoid Silent Runtime Traps:** Below 24 GiB VRAM, Ollama defaults to a **4,096-token context window** (silently breaking agent system prompts) and exhibits `/v1` hangs on `qwen3.8:27b`. Also note `llama-server --sleep-idle-seconds` leaks ~600 MiB of dormant CUDA context per model (`llama.cpp#19379`)—explicitly unload via `Pi`'s `/llama` before heavy `ComfyUI` renders.

---

## 2. Flagship Developer Harness (`Pi`) & Peer Comparison

We standardize developer workflows around **`Pi`** because it is a minimal, transparent loop you own—usable naked in 5 minutes and optionally extensible across 6 modular rungs in the [**Pi Ricing Workshop**](../guides/pi-workshop.md).

<!-- swissknife:begin slot id=dev-harness -->
**Active Anchor — [Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi)**

Minimal, hackable agent kernel with built-in /llama router support, /v1/systemone decision-model discovery, /tree DAG branching, MCP + Codemode JS sandbox, and SQLite durability.

- **When to use:** Flagship developer anchor: run naked in 5 minutes, or optionally rice across 6 modular rungs (LoRA, sandbox, smart MCP, durability, mobile HITL, ComfyUI).
- **Upstream docs:** [Official setup & reference](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/llama-cpp.md)
- **Evidence:** Primary evaluation · verified 2026-11-28
- **Compatible adapters:** [Qwen3.8-27B Pi Specialist LoRA (~319 MB)](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted-GGUF), [Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)
- **Why this pick:** [Pair OpenCode (Newcomer Anchor) with Pi (Flagship Developer Kernel)](why-this-stack.md#adr-why-pi-and-opencode)
- **Limitation:** Intentionally omits built-in per-tool approval prompts; pair with gondolin, nono, or safeagents before autonomous runs.
- **Limitation:** Requires Node 22.19+; built-in MCP keeps enabled servers alive all session unless replaced with pi-mcp-adapter.
<!-- swissknife:end -->

### Harness Landscape by Architectural Role

<!-- swissknife:begin table kind=harness -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Google Antigravity ($0 Individual Tier)](https://antigravity.google/) | Fastest 5-minute guided entry into agentic coding for newcomers and students on any laptop. | $0/mo Individual: unlimited Tab & Command + weekly Work-Done agent quota | Official documentation | Free agent quota resets weekly with no rollover; managed Google Workspace or .edu accounts may hit entitlement walls (use a personal Google account). |
| [OpenCode CLI & Desktop](https://github.com/anomalyco/opencode) | Default local coding harness for newcomers and teams wanting safe out-of-the-box permission prompts. | Mature Newcomer & Team CLI | Primary evaluation | Place baseURL strictly inside options, name the file opencode.json (no leading dot), and never name your custom provider 'openai'. |
| [Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi) | Flagship developer anchor: run naked in 5 minutes, or optionally rice across 6 modular rungs (LoRA, sandbox, smart MCP, durability, mobile HITL, ComfyUI). | Flagship Mod-Able Developer Kernel | Primary evaluation | Intentionally omits built-in per-tool approval prompts; pair with gondolin, nono, or safeagents before autonomous runs. |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Always-on background ops daemons and scheduled digests where you want messaging built in from day one. | Self-Improving Persistent Daemon | Official documentation | Foreground sessions do not auto-compact aggressively like Pi by default (though idle gateway chats now background-compact in v0.23.5); cap context lengths on massive repositories. |
<!-- swissknife:end -->

### Inference & Media Runtimes

<!-- swissknife:begin table kind=runtime -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [llama.cpp (Mainline GGUF Server & Router)](https://github.com/ggml-org/llama.cpp) | Primary local serving engine on NVIDIA workstations and built-in /llama backend for Pi. | MIT | Official documentation | --sleep-idle-seconds leaves ~600 MiB of dormant CUDA context VRAM attached per model (llama.cpp#19379); explicitly Unload via Pi /llama before heavy ComfyUI renders. |
| [Apple MLX (mlx-lm)](https://github.com/ml-explore/mlx-lm) | Primary local LLM serving engine on Apple Silicon Macs (Mac mini, MacBook Pro, Mac Studio). | MIT | Primary evaluation | On 16GB Macs (~10.7 GB default wired GPU limit), run 4B-12B MLX models locally; 27B MLX checkpoints require 24-32GB+ unified memory. |
| [Unsloth Runtime & Studio](https://github.com/unslothai/unsloth) | Serving Dynamic v3.1 GGUFs, local Laya decision endpoints, or running local LoRA fine-tunes. | Apache-2.0 | Official documentation | Keep Studio updated alongside mainline llama.cpp when adopting newly released quantization formats. |
| [WanGP v20.21 (One-Stop Low-VRAM Media Studio)](https://github.com/deepbeepmeep/WanGP) | Default turnkey local media setup for newcomers and 6GB-16GB NVIDIA workstations (5.9-14.3 GiB video VRAM vs ComfyUI's 22.7-23.5 GiB). | 6-15 GB NVIDIA VRAM (MMGP v4 + Extreme Chunker) | Primary evaluation | Install WGPKernels 1.5.0 and SageGP 1.0.2 (PyTorch 2.10; Triton 3.6+ required for RTX 50-series adaptive Sage2/3). |
| [ComfyUI (Comfy-Org Programmable Node Graph)](https://github.com/Comfy-Org/ComfyUI) | Developers building reproducible multi-stage media graphs or driving local/remote GPU rendering from Pi. | 8-24 GB NVIDIA VRAM (use Comfy-Org INT8 or leejet/ComfyUI-GGUF on 16GB) | Official documentation | Official ComfyUI docs explicitly advise Mac users away from heavy local video on Apple MPS (FP8 crashes MPS); target a remote NVIDIA box or Comfy Cloud. |
<!-- swissknife:end -->

---

## 3. High-Leverage Architecture: One Frozen Base + Hot-Swappable LoRAs + Runtime Safety

Instead of hoarding five 15 GB checkpoints, serve **one frozen `Qwen3.8-27B` backbone** and hot-swap tiny adapters:
- **Single-harness, thinking OFF:** Load the ~319 MB `Qwen3.8-27B` Pi specialist LoRA (HF reproduced TB2.1 `39% -> 55%` pass@1 while cutting tokens `2.9K -> 1.5K/task`).
- **Multi-harness fleet or thinking ON (`xhigh`):** Load the 912 MiB Rank-96 Super-Adapter (`55.5% -> 63.5%` mean pass@1, `-31%` to `-48%` SWE-Pro tool calls). See [Harness Adapters Research](../research/harness-adapters.md).
- **Mandatory Safety Layer:** Because `Pi` omits built-in per-tool approval prompts, pair autonomous runs with OS/VM isolation (`gondolin` or `nono`) and tool-call auditing:

<!-- swissknife:begin slot id=runtime-safety -->
**Active Anchor — [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents)**

Transparent OpenAI/Anthropic runtime proxy auditing every tool call via fast local scanning (atif-scan, ~10-20ms on Apple Silicon) and optional decision-model judges.

- **When to use:** Auditing autonomous coding harnesses and unfiltered local LoRAs at the tool-call layer.
- **Evidence:** Primary evaluation · verified 2026-11-28
- **Why this pick:** [Layer OS/VM Isolation (gondolin / nono) with Tool-Call Auditing (safeagents / Laya)](why-this-stack.md#adr-why-sandboxes-and-safety)
- **Limitation:** Audits API tool calls rather than isolating local OS binaries; pair with gondolin or nono for filesystem isolation.
<!-- swissknife:end -->

---

## 4. Multi-Machine Fabric & Programmatic Consumption

- **Split Compute by Physics:** Keep a quiet ~15W Apple Silicon Mac mini as your always-on `Pi Durable` control plane, drive a discrete 16GB GPU PC over `tailscale serve` for heavy CUDA/ComfyUI work, and use your Android/iOS phone strictly as a Human-in-the-Loop steering surface. See [The Personal AI Fabric](../worlds/personal-ai-fabric.md) and [Mobile as Human Communicator](../worlds/mobile-hitl.md).
- **Consume This Repo Headlessly:**
  - Freshness-gated agent manifest: [`llms.txt`](../llms.txt) (expired/degraded entries auto-excluded)
  - Structured JSON snapshot: `dist/catalog.json`
  - Live CLI queries:
    ```bash
    swissknife slot dev-harness --world gpu-pc
    swissknife specialist reverse-engineering --world gpu-pc
    swissknife query --kind memory
    swissknife deltas
    ```

---

**Continue reading:** [Pi Ricing Workshop](../guides/pi-workshop.md) · [Why This Stack](why-this-stack.md) · [Security & Trust Boundaries](security-and-trust.md)
