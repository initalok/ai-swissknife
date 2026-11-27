---
title: "Pi Ricing Workshop (Optional 6-Rung Ladder)"
section: guides
track: developer
summary: "Progressive, 100% optional journey taking Pi Coding Agent from naked in 5 minutes to adapted local GGUF, sandboxing, smart MCP, durability, mobile HITL, and ComfyUI."
order: 1
---

[Home](../README.md) / Guides / Pi Ricing Workshop

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Pi Ricing Workshop (Optional 6-Rung Ladder)

We anchor our developer workflows on **`Pi`** because you can stop at **any rung** and stay productive. Never feel pressured to install all six layers on day one—bolt on each rung only when you hit the exact pain point it solves.

<!-- swissknife:begin slot id=dev-harness -->
**Active Anchor — [Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi)**

Minimal, hackable agent kernel with built-in /llama router support, /v1/systemone decision-model discovery, /tree DAG branching, MCP + Codemode JS sandbox, and SQLite durability.

- **When to use:** Flagship developer anchor: run naked in 5 minutes, or optionally rice across 6 modular rungs (LoRA, sandbox, smart MCP, durability, mobile HITL, ComfyUI).
- **Upstream docs:** [Official setup & reference](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/llama-cpp.md)
- **Evidence:** Primary evaluation · verified 2026-11-28
- **Compatible adapters:** [Qwen3.8-27B Pi Specialist LoRA (~319 MB)](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted-GGUF), [Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)
- **Experimental challenger:** [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness) — Experimenting with custom loop architectures, Creator Mode live UI plugins, or web/desktop sessions.
- **Why this pick:** [Pair OpenCode (Newcomer Anchor) with Pi (Flagship Developer Kernel)](../docs/why-this-stack.md#adr-why-pi-and-opencode)
- **Limitation:** Intentionally omits built-in per-tool approval prompts; pair with gondolin, nono, or safeagents before autonomous runs.
- **Limitation:** Requires Node 22.19+; built-in MCP keeps enabled servers alive all session unless replaced with pi-mcp-adapter.
<!-- swissknife:end -->

---

## Rung 0 · Running Naked (5 Minutes)

Install `Pi` (requires Node `22.19+`), log into a cloud provider (`/login`) or connect directly to a local `llama serve` router via built-in `/llama` *(note: the old `huggingface/pi-llama` extension was archived once `Pi` absorbed `llama.cpp` natively)*, and learn `/tree` DAG session branching to rewind failed paths without restarting.

<!-- swissknife:begin recipe id=pi -->
<details>
<summary>Launch command — Pi Coding Agent (+ @earendil-works/pi-durable) (CUDA / llama.cpp / CLI)</summary>

```bash
curl -fsSL https://pi.dev/install.sh | sh && pi
```

</details>

Built-in upstream check: `pi --version`
<!-- swissknife:end -->

> **Stop here if** you just want a fast, transparent terminal coding loop in a disposable or low-risk repository. *(Remember: naked `Pi` omits built-in approval prompts.)*

---

## Rung 1 · Adapting Local `Qwen3.8-27B` for `Pi`

Attach Hugging Face's RL-trained `Pi` specialist LoRA (~319 MB) to your frozen `Qwen3.8-27B` base model when running with thinking **OFF** (lifted reproduced TB2.1 `39% -> 55%` pass@1 while halving token usage), or use the 912 MiB rank-96 super-adapter if you run thinking **ON** or share weights across harnesses.

<!-- swissknife:begin recipe id=qwen38-pi-lora -->
<details>
<summary>Launch command — Qwen3.8-27B Pi Specialist LoRA (~319 MB) (CUDA / llama.cpp / CLI)</summary>

```bash
llama-server -m Qwen3.8-27B-IQ4_XS.gguf --lora Qwen3.8-27B-pi-lora-F16.gguf -ngl 99 -fa on -c 65536 -ctk q8_0 -ctv q8_0 --host 127.0.0.1 --port 8080
```

</details>
<!-- swissknife:end -->

*(Pair with `llama serve --no-models-autoload -ngl all -c 32768 --host 127.0.0.1 --port 9931` so `/llama` inside `Pi` can load, unload, and discover System-1 decision models like `Laya` via `/v1/systemone`.)*

---

## Rung 2 · Sandboxing & Safety Boundaries

Before letting `Pi` run unsupervised, pick the isolation layer matching your workload:
- **Untrusted code & strict secret protection:** [`gondolin`](https://github.com/earendil-works/gondolin) (`libkrun` micro-VM on Apple Silicon & Linux KVM; host injects real secrets only on allow-listed HTTP domains).
- **Native macOS/Linux host builds (`xcodebuild`, `swift`, Homebrew):** [`nono`](https://github.com/nolabs-ai/nono) (macOS Seatbelt / Linux Landlock).
- **Tool-call auditing across any harness:** [`safeagents`](https://github.com/huggingface/safeagents) proxy (`atif-scan` + plugin) and/or `Laya 0.5`.

See [Security & Trust Boundaries](../docs/security-and-trust.md) for the complete trust matrix.

---

## Rung 3 · Skills, Live Docs & Smart MCP

- **Disciplined engineering habits:** Add [`obra/superpowers`](https://github.com/obra/superpowers) (15 TDD/spec/verification skills) and [`@upstash/context7-pi`](https://github.com/upstash/context7) (pin local Context7 servers to `>= 2.1.3`).
- **Context-friendly MCP:** Start with built-in `pi mcp add` + Codemode JS sandbox. Once you run 4+ MCP servers and want lazy startup, 10-minute idle shutdown, OS keychain OAuth, and semantic tool ranking, install [`nicobailon/pi-mcp-adapter`](https://github.com/nicobailon/pi-mcp-adapter).

---

## Rung 4 · Durability (`Pi Durable`)

When multi-hour sessions need to survive crashes, reboots, and laptop sleeps, step up to first-party **`@earendil-works/pi-durable`** (SQLite/JSONL checkpoints, background compaction at 200K/250K, `search_history`, atomic shared JSON app state, and live mid-run Read-Only tool toggles). Reference multi-device showcase: [`disler/durable-pi`](https://github.com/disler/durable-pi).

---

## Rung 5 · Remote & Mobile HITL Steering

Steer your home Mac mini or Linux rig from your pocket with zero open router ports:
- **Multi-box Tailscale HTTPS + Voice Mode:** [`pi-mobile`](https://pi.dev/packages/pi-mobile) (`/remote add <box>`, unified *"who needs you"* queue, spoken summaries + verbal confirmations).
- **Native Android Compose + `/tree` forking:** [`ayagmar/pi-mobile`](https://github.com/ayagmar/pi-mobile) over Tailscale `*.ts.net` QR pairing.
- **Zero-extra-app durable Telegram:** [`smixs/pi-durable-telegram`](https://github.com/smixs/pi-durable-telegram) (outbound long-poll, photos/PDFs/voice notes/file delivery).

Full breakdown in [Mobile as Human Communicator](../worlds/mobile-hitl.md).

---

## Rung 6 · Driving `ComfyUI` & `WanGP` From `Pi`

Attach ComfyUI's official MCP server (`Comfy-Org/comfy-mcp`) or the power-user `artokun/comfyui-mcp` control plane so `Pi` can inspect models, wire node graphs, preview thumbnails, and debug broken workflows locally or over Tailscale.

<!-- swissknife:begin slot id=agent-media-mcp -->
**Active Anchor — [Comfy-Org Official comfy-mcp (Local & Cloud)](https://github.com/Comfy-Org/comfy-mcp)**

First-party open-source local MCP server (pip install comfy-mcp, zero account) and hosted Comfy Cloud MCP supporting remote Tailscale GPU hosts via COMFYUI_URL with inline media previews.

- **When to use:** Default agent-to-ComfyUI bridge for Pi, OpenCode, and Antigravity across local, Tailscale, or Comfy Cloud backends.
- **Evidence:** Official documentation · verified 2026-11-28
- **Why this pick:** [Split Local Media Into Turnkey Low-VRAM (WanGP) vs. Programmable Agent Engine (ComfyUI + MCP)](../docs/why-this-stack.md#adr-why-wangp-and-comfyui)
- **Limitation:** On a single 16GB GPU, explicitly unload the local LLM in Pi (/llama) before queuing heavy ComfyUI video workflows.
<!-- swissknife:end -->

> **Single 16GB GPU reminder:** Run `/llama` $\rightarrow$ **Unload** before queueing heavy `ComfyUI` video workflows so dormant CUDA context doesn't trigger an OOM, or run `Pi` on your Mac mini targeting a remote GPU PC over Tailscale.

*Looking for the broader long tail of community `Pi` extensions?* Browse the daily CI-updated upstream directory [`shaftoe/awesome-pi-coding-agent`](https://github.com/shaftoe/awesome-pi-coding-agent).

---

**Continue reading:** [Coding & Apps](coding-and-apps.md) · [Persistent Memory & Knowledge Loops](memory-and-knowledge.md) · [Local Media Studio](media-studio.md)
