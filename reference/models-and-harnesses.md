---
title: "Models, Harnesses & Runtimes Reference"
section: reference
summary: "Scannable factual index of all verified local models, agent harnesses, inference runtimes, and safety boundaries."
order: 1
---

[Home](../README.md) / Reference / Models, Harnesses & Runtimes

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy · 1 upstream release(s) queued ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Models, Harnesses & Runtimes Reference

Factual lookup tables compiled directly from the live registry. For setup walkthroughs and hardware physics, see [Apple Silicon Mac](../worlds/apple-silicon.md) and [Discrete GPU PC](../worlds/gpu-workstation.md).

## Local Models

<!-- swissknife:begin table kind=model -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Wan 2.2 (5B & A14B Apache-2.0 Video)](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | Commercial-safe local video generation on consumer NVIDIA GPUs. | 6-15 GB VRAM via WanGP MMGP v4 | Official documentation | Newer Wan 3.0 and Wan 2.6 releases remain closed cloud APIs with no published local weights. |
| [Qwen-Image-2.1 (7B DiT Native RGBA)](https://huggingface.co/Qwen/Qwen-Image-2.1) | Non-commercial design assets, typography, and layered transparent image editing. | 4.2-9.1 GB VRAM (INT8 / leejet GGUF) | Official documentation | Non-commercial license; swap to Apache-2.0 FLUX.2 Klein for commercial production graphics. |
| [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B) | Daily-driver local coding, strict instruction following, and single-backbone multi-LoRA serving. | 14.5 GB (IQ4_XS, Zone 1 16GB VRAM) / ~16 GB (Mac MLX 4-bit) | Primary evaluation | On 16GB GPUs, keep quantization at IQ4_XS with Q8 KV cache so weights never spill over PCIe. |
| [Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) | Deeper multi-file repository reasoning on 16GB GPU + 64GB RAM workstations or 64GB+ Macs. | 49 GB (UD-Q4_K_XL, Zone 2 16GB VRAM + 64GB RAM) | Official documentation | Keep -ngl 99 so Attention and KV cache stay in GPU VRAM; offload cold experts only via --n-cpu-moe. |
| [Gemma 4 Family (12B Tri-Modal & 26B-A4B Vision)](https://ai.google.dev/gemma) | 8GB-12GB laptops needing local chat/audio, or ultra-fast 16GB vision and general chat. | 8.5 GB (12B) to 14 GB (26B-A4B) | Official documentation | Only E2B, E4B, and 12B process audio; the 26B-A4B MoE checkpoint is Text + Vision only. |
| [NousResearch Hermes 4 (14B / 4.3-36B Neutral)](https://huggingface.co/NousResearch/Hermes-4-14B) | Self-hosted deployments needing predictable operator-controlled behavior rather than abliteration. | 9 GB (14B Q4) / 22 GB (36B Hybrid) | Vendor / lab claim | Always author explicit safety policies in your system prompt if exposing the endpoint beyond solo local use. |
| [Inkling 2 Mini (26.4B Looped Transformer MoE)](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) | Testing high-efficiency looped coding architectures inside 16GB-18GB memory budgets. | 13-18 GB (UD-Q3/Q4) | Vendor / lab claim | Published 79.2% SWE-bench Verified and 48.2% DeepSWE v1.1 figures are lab-reported; trails Qwen3.8-27B on strict chat. |
| [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya) | Fast zero-output-token tool-safety gating, routing, and memory relevance checks without using GPU VRAM. | 678-846 MB (CPU / NPU / WebGPU) | Official documentation | Threshold decisions on calibrated probabilities rather than raw confidence scores; optional vegaml-learn add-on is non-commercial. |
<!-- swissknife:end -->

## Agent Harnesses

<!-- swissknife:begin table kind=harness -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Google Antigravity ($0 Individual Tier)](https://antigravity.google/) | Fastest 5-minute guided entry into agentic coding for newcomers and students on any laptop. | $0/mo Individual: unlimited Tab & Command + weekly Work-Done agent quota | Official documentation | Free agent quota resets weekly with no rollover; managed Google Workspace or .edu accounts may hit entitlement walls (use a personal Google account). |
| [OpenCode CLI & Desktop](https://github.com/anomalyco/opencode) | Default local coding harness for newcomers and teams wanting safe out-of-the-box permission prompts. | Mature Newcomer & Team CLI | Primary evaluation | Place baseURL strictly inside options, name the file opencode.json (no leading dot), and never name your custom provider 'openai'. |
| [Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi) | Flagship developer anchor: run naked in 5 minutes, or optionally rice across 6 modular rungs (LoRA, sandbox, smart MCP, durability, mobile HITL, ComfyUI). | Flagship Mod-Able Developer Kernel | Primary evaluation | Intentionally omits built-in per-tool approval prompts; pair with gondolin, nono, or safeagents before autonomous runs. |
| [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness) | Experimenting with custom loop architectures, Creator Mode live UI plugins, or web/desktop sessions. | Swappable-Loop Plugin Platform | Official documentation | Rapidly iterating developer preview; pin plugin peer versions against breaking interface changes. |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Always-on background ops daemons and scheduled digests where you want messaging built in from day one. | Self-Improving Persistent Daemon | Official documentation | Foreground sessions do not auto-compact aggressively like Pi by default (though idle gateway chats now background-compact in v0.23.5); cap context lengths on massive repositories. |
<!-- swissknife:end -->

## Inference & Media Runtimes

<!-- swissknife:begin table kind=runtime -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [llama.cpp (Mainline GGUF Server & Router)](https://github.com/ggml-org/llama.cpp) | Primary local serving engine on NVIDIA workstations and built-in /llama backend for Pi. | MIT | Official documentation | --sleep-idle-seconds leaves ~600 MiB of dormant CUDA context VRAM attached per model (llama.cpp#19379); explicitly Unload via Pi /llama before heavy ComfyUI renders. |
| [Apple MLX (mlx-lm)](https://github.com/ml-explore/mlx-lm) | Primary local LLM serving engine on Apple Silicon Macs (Mac mini, MacBook Pro, Mac Studio). | MIT | Primary evaluation | Prompt prefill lags dedicated NVIDIA Tensor Cores; 32GB+ unified memory is recommended for 27B coding sessions. |
| [Unsloth Runtime & Studio](https://github.com/unslothai/unsloth) | Serving Dynamic v3.1 GGUFs, local Laya decision endpoints, or running local LoRA fine-tunes. | Apache-2.0 | Official documentation | Keep Studio updated alongside mainline llama.cpp when adopting newly released quantization formats. |
| [WanGP v20.21 (One-Stop Low-VRAM Media Studio)](https://github.com/deepbeepmeep/WanGP) | Default turnkey local media setup for newcomers and 6GB-16GB NVIDIA workstations (5.9-14.3 GiB video VRAM vs ComfyUI's 22.7-23.5 GiB). | 6-15 GB NVIDIA VRAM (MMGP v4 + Extreme Chunker) | Primary evaluation | Install WGPKernels 1.5.0 and SageGP 1.0.2 (PyTorch 2.10; Triton 3.6+ required for RTX 50-series adaptive Sage2/3). |
| [ComfyUI (Comfy-Org Programmable Node Graph)](https://github.com/Comfy-Org/ComfyUI) | Developers building reproducible multi-stage media graphs or driving local/remote GPU rendering from Pi. | 8-24 GB NVIDIA VRAM (use Comfy-Org INT8 or leejet/ComfyUI-GGUF on 16GB) | Official documentation | Official ComfyUI docs explicitly advise Mac users away from heavy local video on Apple MPS (FP8 crashes MPS); target a remote NVIDIA box or Comfy Cloud. |
<!-- swissknife:end -->

---

**Continue reading:** [Why This Stack](../docs/why-this-stack.md) · [Retired & Disqualified Tools](retired.md)
