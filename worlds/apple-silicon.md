---
title: "Apple Silicon Mac (16GB M4 Mac mini 24/7 Server)"
section: worlds
world: mac
summary: "Running a power-efficient 16GB M4 Mac mini as a 24/7 remote AI server built around Rex, Pi, Pi Durable, nono v0.82 sandboxing, and <=10 GB local MLX helpers."
order: 2
---

[Home](../README.md) / Compute Worlds / Apple Silicon Mac

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Apple Silicon Mac (16GB M4 Mac mini 24/7 Server)

We anchor our Apple Silicon guide on the **base 16GB M4 Mac mini**—the most accessible value-for-money entry point and an exceptionally stable, silent (~15W idle) **24/7 remote AI server**.

## Primary Role: 24/7 Remote Control Plane (`Rex` + `Pi` + `Pi Durable`)

Rather than forcing 27B–80B weights onto a 16GB unified-memory ceiling, let the Mac mini shine as your always-on **agent cockpit**:
- **`Rex` (Pragmatic Exception):** Native `libghostty` terminal and persistent session server where agent tabs live on the Mac mini—close your laptop, reconnect over built-in Tailscale (`rex server tailscale on`), and every pane is still alive. `rex skill setup` gives `Pi` native pane control and OSC 7501 status indicators (*working / blocked-on-you / done*).
- **`Pi` + `@earendil-works/pi-durable`:** Rex survives closing your laptop, **not** a full Mac reboot. Running `Pi Durable` inside Rex adds SQLite checkpoints so multi-hour tasks survive even OS updates and power cycles.
- **Production Sandboxing (`nono v0.82.0`):** Wrap 24/7 sessions in native macOS Seatbelt via `nono pull nolabs-ai/pi && nono run --profile nolabs-ai/pi -- pi` with macOS Keychain `--credential` injection and `--rollback`.

<!-- swissknife:begin slot id=mac-server -->
**Active Anchor — [Rex Terminal & Persistent Session Server (Superlogical)](https://www.superlogical.com/rex/docs/installation)**

Native libghostty terminal and persistent server by Mitchell Hashimoto where agent tabs live on your Mac/Linux host, survive laptop disconnects, integrate natively with Pi (rex skill setup + OSC 7501 status tabs), and include built-in Tailscale networking.

- **When to use:** Running a 16GB M4 Mac mini as a 24/7 remote AI cockpit alongside Pi and @earendil-works/pi-durable.
- **Evidence:** Official documentation · verified 2026-11-28
- **Limitation:** Proprietary software currently in invite/Discord public beta; pragmatic exception chosen for first-class Pi OSC 7501 integration.
- **Limitation:** Rex sessions survive closing your laptop/client but NOT a full host reboot—pair with @earendil-works/pi-durable for reboot durability.
<!-- swissknife:end -->

<!-- swissknife:begin recipe id=rex -->
<details>
<summary>Launch command — Rex Terminal & Persistent Session Server (Superlogical) (CUDA / llama.cpp / CLI)</summary>

```bash
rex skill setup && rex server tailscale on
```

</details>

Built-in upstream check: `rex --version`
<!-- swissknife:end -->

## Honest 16GB Unified-Memory Physics (`<= 10 GB` Local Budget)

macOS reserves roughly **~10.7 GB** as the default wired GPU memory ceiling on a 16GB Mac. Keep local on-Mac inference inside `<= 10 GB` so `Rex`, `Pi`, and macOS stay responsive 24/7:
- **Fast local helpers on 16GB M4:** [`Qwen3.5-9B`](../reference/models.md) (~5.6 GB 4-bit MLX, 262K ctx, 25–35 tok/s) and [`Gemma 4 E4B / 12B`](../reference/models.md) for quick edits, screenshots, and local OCR (`DeepSeek-OCR-2`).
- **Heavy 27B–80B coding & ComfyUI video:** Route from your Mac mini's `Pi` session over Tailscale to a 16GB NVIDIA GPU PC (`LLAMA_BASE_URL` / `COMFYUI_URL`) or `$0` Cloud (`gemini-4-hydrogen`). *(Higher-RAM 32GB–64GB Macs can serve `Qwen3.8-27B` MLX locally at ~65 tok/s.)*

<!-- swissknife:begin recipe id=mlx-lm -->
<details>
<summary>Launch command — Apple MLX (mlx-lm) (Apple Silicon / MLX)</summary>

```bash
mlx_lm.server --model mlx-community/Qwen3.5-9B-4bit --host 127.0.0.1 --port 8080
```

</details>
<!-- swissknife:end -->

> [!WARNING]
> **Avoid Heavy Local Video on Apple MPS:** ComfyUI's own docs advise Mac users against running heavy modern video models locally on Apple GPUs (FP8 weights crash MPS). Keep heavy rendering on a remote NVIDIA GPU PC or Comfy Cloud via [The Personal AI Fabric](personal-ai-fabric.md).

## Verified 16GB Mac mini 24/7 Server Stack

<!-- swissknife:begin table tag=mac-16gb -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Tailscale Serve (Loopback-to-Tailnet HTTPS Mesh)](https://tailscale.com/kb/1312/serve) | Developer standard for connecting Mac mini, NVIDIA GPU PC, and Android/iOS phones without opening router ports. | Encrypted Private Mesh (Dev Standard) | Official documentation | Automatic Let's Encrypt HTTPS certificates log machine.<tailnet>.ts.net hostnames in public CT logs; use neutral box names (e.g., box-a). |
| [OpenCode CLI & Desktop](https://github.com/anomalyco/opencode) | Default local coding harness for newcomers and teams wanting safe out-of-the-box permission prompts. | Mature Newcomer & Team CLI | Primary evaluation | Place baseURL strictly inside options, name the file opencode.json (no leading dot), and never name your custom provider 'openai'. |
| [Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi) | Flagship developer anchor: run naked in 5 minutes, or optionally rice across 6 modular rungs (LoRA, sandbox, smart MCP, durability, mobile HITL, ComfyUI). | Flagship Mod-Able Developer Kernel | Primary evaluation | Intentionally omits built-in per-tool approval prompts; pair with gondolin, nono, or safeagents before autonomous runs. |
| [Apple MLX (mlx-lm)](https://github.com/ml-explore/mlx-lm) | Primary local LLM serving engine on Apple Silicon Macs (Mac mini, MacBook Pro, Mac Studio). | MIT | Primary evaluation | On 16GB Macs (~10.7 GB default wired GPU limit), run 4B-12B MLX models locally; 27B MLX checkpoints require 24-32GB+ unified memory. |
| [Rex Terminal & Persistent Session Server (Superlogical)](https://www.superlogical.com/rex/docs/installation) | Running a 16GB M4 Mac mini as a 24/7 remote AI cockpit alongside Pi and @earendil-works/pi-durable. | 24/7 Persistent Agent Terminal Server (Pragmatic Exception) | Official documentation | Proprietary software currently in invite/Discord public beta; pragmatic exception chosen for first-class Pi OSC 7501 integration. |
| [Gemma 4 Family (12B Tri-Modal & 26B-A4B Vision)](https://ai.google.dev/gemma) | 8GB-12GB laptops needing local chat/audio, or ultra-fast 16GB vision and general chat. | 8.5 GB (12B) to 14 GB (26B-A4B) | Official documentation | Only E2B, E4B, and 12B process audio; the 26B-A4B MoE checkpoint is Text + Vision only. |
| [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya) | Fast zero-output-token tool-safety gating, routing, and memory relevance checks without using GPU VRAM. | 678-846 MB (CPU / NPU / WebGPU) | Official documentation | Threshold decisions on calibrated probabilities rather than raw confidence scores; optional vegaml-learn add-on is non-commercial. |
| [Qwen3.5-9B (Multimodal Hybrid DeltaNet)](https://huggingface.co/Qwen/Qwen3.5-9B) | Fast local helper, screenshot triage, and offline coding/edits on a base 16GB M4 Mac mini or 8GB-12GB GPU laptop. | ~5.6 GB (4-bit MLX / Q4 GGUF, 262K native ctx) | Official documentation | Trails 27B+ backbones on complex multi-file refactors; route heavy coding tasks to GPU PC or $0 Cloud. |
| [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents) | Auditing autonomous coding harnesses and unfiltered local LoRAs at the tool-call layer. | Apache-2.0 | Primary evaluation | Audits API tool calls rather than isolating local OS binaries; pair with gondolin or nono for filesystem isolation. |
| [nolabs-ai/nono v0.82 (macOS Seatbelt & Linux Landlock Sandbox)](https://github.com/nolabs-ai/nono) | Production-grade least-privilege sandboxing for 24/7 Mac mini servers and native macOS/Linux host toolchains. | Apache-2.0 | Official documentation | Shares the host kernel; for heavily untrusted code execution or strict zero-secret micro-VM isolation, pair with gondolin. |
<!-- swissknife:end -->

---

**Continue reading:** [The Personal AI Fabric](personal-ai-fabric.md) · [Security & Trust Boundaries](../docs/security-and-trust.md) · [Pi Ricing Workshop](../guides/pi-workshop.md)
