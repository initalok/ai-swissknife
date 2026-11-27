[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; [🖥️ Local](../book/local.md) &nbsp;·&nbsp; **⚙️ Harnesses & RL** &nbsp;·&nbsp; [📘 Playbooks](../book/playbooks.md) &nbsp;·&nbsp; [🧭 Spokes](../book/spokes.md) &nbsp;·&nbsp; [📡 Radar](../book/radar.md) &nbsp;·&nbsp; [🪦 Graveyard](../book/graveyard.md)

# ⚙️ Harnesses, Backends & RL Adapters Lab Dossier

> [!IMPORTANT]
> Treat **`Pi` / `Pi Durable`** as your building-block kernel, **`DeepSeek Harness` (`dsh`)** as your Cordis plugin platform, and **`Hermes Agent`** as your persistent self-improving daemon—paired with hot-swappable RL LoRA adapters and `safeagents`.

## 1. Harness Architecture Dossiers

### [**Pi Coding Agent (+ @earendil-works/pi-durable)**](https://github.com/earendil-works/pi) · `Building-Block Kernel` · 🟢 `Fresh`
- 🏆 Minimal hackable TUI/RPC/SDK loop with /tree DAG branching, MCP + Codemode JS sandbox, and first-party pi-durable SQLite checkpoints
- 🏆 Highest-scoring HF Harness Adapter target (64.7% SWE-Pro hard-51) and Inkling 2 Mini reference harness
- ⚡ **Official Harness Adapters:** [**Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)**](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)
- ⚠️ Intentionally omits built-in per-tool approval prompts; pair with safeagents or OS sandboxes.

### [**DeepSeek Harness (dsh)**](https://github.com/deepseek-ai/deepseek-harness) · `Cordis Plugin Platform` · 🟢 `Fresh`
- 🏆 Cordis everything-is-a-plugin architecture letting you swap the agent loop itself, Creator Mode, & built-in read-only sandbox
- 🏆 First-party plugins orchestrate Claude Code & Codex as sub-agents; supports local OpenAI-compat servers
- ⚠️ Fast-moving developer preview (0.2.3-alpha.2); pin plugin versions against breaking API changes.

```bash
npx @deepseek-ai/dsh web
```

### [**Hermes Agent (v0.23.4)**](https://github.com/NousResearch/hermes-agent) · `Self-Improving Daemon` · 🟢 `Fresh`
- 🏆 #1 globally on OpenRouter token volume; persistent memory, autonomous skill creation, Telegram/cron/ACP, 40+ tools
- 🏆 Official HF Harness Adapter target (Qwen3.8-27B-hermes-adapted)
- ⚡ **Official Harness Adapters:** [**Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)**](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)
- ⚠️ Does not auto-compact aggressively like Pi by default; cap thinking/context tokens on giant repos.

### [**OpenCode CLI**](https://github.com/anomalyco/opencode) · `Vendor-Agnostic Terminal CLI` · 🟢 `Fresh`
- 🏆 Clean terminal coding agent with official HF Qwen3.8-27B-opencode-adapted LoRA
- ⚡ **Official Harness Adapters:** [**Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)**](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)
- ⚠️ Watch context length on multi-hour repos; does not auto-compact as aggressively as Pi.

## 2. Runtime Safety Proxies (`guards` Edges)

- [**Laya 0.5 (Multimodal System-1 Decision Model)**](https://github.com/NandhaKishorM/laya) · 🟢 `Fresh` — Evaluates 64 typed decisions per pass in <100-500ms; v0.5 reads text, images, audio & video up to 73,728 tokens; Installs cleanly via pip install -U laya; serves via Unsloth Decision API (localhost:8888)
  - ⚠️ Threshold on probabilities (not confidence); vegaml-learn continuous learning add-on is non-commercial.
- [**Hugging Face safeagents Runtime Proxy**](https://github.com/huggingface/safeagents) · 🟢 `Fresh` — Transparent OpenAI/Anthropic proxy with atif-scan (10-20ms on Apple Silicon) & optional Decision Model judge; Audited 1.3M RL tool calls and blocked 647 suspicious calls during HF harness-adapter training
  - ⚠️ Configure a domain plugin (e.g. hf://harness-hub/qwen-safeagents-plugin) rather than running empty defaults.

## 3. Harness Adapters & In-Harness RL Lab Notebook

### [**Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)**](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter) · 🟢 `Fresh`
**Targets:** `qwen3.8-27b`, `pi`, `hermes-agent`, `opencode` · **License:** `Apache-2.0` · *Verified `2026-11-27`*

- 🏆 Zero-retraining orthogonal rank-96 merge (PEFT cat, wt 0.5) of pi, Hermes, & OpenCode RL LoRAs (cosine sim 0.01-0.02)
- 🏆 GGUF LoRA adds only +912 MiB (+304 MiB for single-harness specialist) on top of frozen Qwen3.8-27B
- ⚠️ Decision rule: single harness + thinking off -> use specialist LoRA; thinking on or multi-harness -> use super-adapter.
- ⚠️ Trained on BF16; verify GGUF quant fidelity and expect mild pre-tool reasoning leakage (arXiv:2610.14270).

**HF Harness Adapters Summary: Base vs. Specialist vs. Rank-96 Super-Adapter (Qwen3.8-27B)**

| Mode / Benchmark | Base Qwen3.8-27B | Best Specialist LoRA | Rank-96 Super-Adapter | Tool-Call Reduction |
| :--- | :--- | :--- | :--- | :--- |
| Thinking Off · Mean across 6 pairs | 39.5% | pi SWE-Pro: 64.7% (vs 39.2%) | 49.0% (beats base 6/6) | -53% to -73% calls |
| Thinking On (xhigh) · Mean across 6 pairs | 55.5% | Trained w/ thinking off | 63.5% (wins 5/6, ties 1) | -31% to -48% SWE-Pro |
| Cross-Harness Transfer (pi LoRA -> others) | 44.8% OC / 46.3% Hermes | 54.0% OC / 56.1% Hermes | Transfers to Swift-1.5 too | ~45% fewer calls |

```bash
llama-server -m Qwen3.8-27B-IQ4_XS.gguf --lora Qwen3.8-27B-super-adapter-F16.gguf -ngl 99 -fa on -c 65536 -ctk q8_0 -ctv q8_0
```

### [**Qwen3.8-27B 26MB Uncensored LoRA (Rank-3)**](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated) · 🟢 `Fresh`
**Targets:** `qwen3.8-27b` · **License:** `Apache-2.0` · *Verified `2026-11-27`*

- 🏆 Tiny 26 MB rank-3 LoRA (built on Apple Silicon) hot-swapping over the exact same frozen Qwen3.8-27B backbone
- ⚠️ Abliterated adapters cannot refuse harmful tool actions; always isolate behind safeagents + Laya 0.5.

### [**HF In-Harness RL Recipe (OpenEnv + Harbor + TRL AsyncGRPO)**](https://huggingface.co/blog/harness-adapters-at-scale) · 🟢 `Fresh`
**Targets:** Core RL Pipeline · **License:** `Apache-2.0` · *Verified `2026-11-27`*

- 🏆 Trains LoRAs directly inside unmodified shipping harnesses via token/logprob capture proxy (echoing Agent Lightning v1.0)
- 🏆 openenv validate passed 858/1,127 tasks; base-model difficulty filtering drove the largest GRPO reward lift
- ⚠️ Use all-linear LoRA, LR 2e-5 (1e-4 collapses rollouts), tool bonus 0.1, & never train GRPO on all-pass/all-fail tasks.

**TB2.1 Lift Experiment (Qwen3.8-27B · LoRA AsyncGRPO · 32 tasks/arm · 8xH200 · Base TB2.1 pass@1: 35.9%)**

| Arm | Task Filtering Rule | Steps Reached | Train Reward (Steps 1-5 -> Last 5) |
| :--- | :--- | :--- | :--- |
| A1 Unvalidated | 24 accepted + 8 failed validation | 40 (timed out step 48) | 0.64 -> 0.67 |
| A2 Validated | 32 accepted, no difficulty filter | 50 (completed) | 0.56 -> 0.70 |
| A3 Unqualified | 32 accepted base always/never solves | 25 (timed out step 26) | 0.60 -> 0.63 |
| A4 Qualified | 32 accepted base solves sometimes | 50 (completed) | 0.62 -> 0.81 |

## 4. Inference Backends & 2026 Flag Reference

| Backend & Health | Breakthroughs & Target | Critical Gotcha |
| :--- | :--- | :--- |
| [**llama.cpp (Mainline GGUF + Looped Layers)**](https://github.com/ggml-org/llama.cpp) · 🟢 `Fresh` | Universal CUDA/Metal/Vulkan/ROCm engine with --n-cpu-moe offload, --lora hot-loading, --load-mode, & PR #32218 Inkling looped support | ⚠️ --no-mmap is deprecated (use --load-mode none); add -cuda graphs=0 if partial MoE offload outputs gibberish. |
| [**Unsloth Runtime & Studio**](https://github.com/unslothai/unsloth) · 🟢 `Fresh` | 3x faster VRAM-exceeding MoE GGUFs, Anthropic-compatible local API for Claude Code, Decision API, & Bwrap/Seatbelt/MXC sandboxes | ⚠️ Keep Studio updated alongside mainline llama.cpp for newest Dynamic v3.1 quant support. |
| [**Apple MLX (mlx-lm)**](https://github.com/ml-explore/mlx-lm) · 🟢 `Fresh` | Zero PCIe copy bottleneck on Mac mini/Studio unified memory (~65 tok/s on 4-bit Qwen3.8-27B super-adapter) | ⚠️ Prompt prefill lags dedicated NVIDIA Tensor Cores; 32GB+ unified memory recommended for 27B MLX. |
| [**WanGP v20.12 (MMGP v4 + SageGP 1.0.2)**](https://github.com/deepbeepmeep/WanGP) · 🟢 `Fresh` | Extreme Chunker fits 15s of 1080p Hailuo H3 video into 5.9 GB VRAM; runs Wan 2.2, LTX-2.5, Qwen-Image-2.1, & native MCP | ⚠️ Install WGPKernels 1.5.0 & SageGP 1.0.2 (PyTorch 2.10; Triton 3.6+ for RTX 50xx adaptive Sage2/3). |

---

[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; [🖥️ Local](../book/local.md) &nbsp;·&nbsp; **⚙️ Harnesses & RL** &nbsp;·&nbsp; [📘 Playbooks](../book/playbooks.md) &nbsp;·&nbsp; [🧭 Spokes](../book/spokes.md) &nbsp;·&nbsp; [📡 Radar](../book/radar.md) &nbsp;·&nbsp; [🪦 Graveyard](../book/graveyard.md)
