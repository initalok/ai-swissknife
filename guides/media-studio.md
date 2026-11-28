---
title: "Local Media Studio (WanGP & ComfyUI)"
section: guides
summary: "Unified local creative pipeline separating turnkey low-VRAM generation (WanGP) from programmable agent-driven node graphs (ComfyUI + MCP), plus code motion graphics and WebGPU speech."
order: 3
---

[Home](../README.md) / Guides / Local Media Studio

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Local Media Studio (`WanGP` & `ComfyUI`)

Instead of treating `WanGP` and `ComfyUI` as rivals, use each where its engineering actually wins:

- **`WanGP` (Turnkey Low-VRAM Studio):** Best for newcomers and 6GB–16GB NVIDIA cards. Head-to-head benchmarks show `WanGP` holding LTX-2.5 and Wan 2.2 video generation to **5.9–14.3 GiB VRAM** where `ComfyUI` peaks at **22.7–23.5 GiB**, with guided installers and one browser UI for Video, Images, Music, Speech, and 3D.
- **`ComfyUI` + Official `comfy-mcp` (Programmable Node Graph & Agent Control Plane):** Best for developers building multi-stage custom pipelines or steering local/remote NVIDIA renders directly from `Pi` or `OpenCode`.

## Active Media Slots

<!-- swissknife:begin slot id=turnkey-media -->
**Active Anchor — [WanGP v20.21 (One-Stop Low-VRAM Media Studio)](https://github.com/deepbeepmeep/WanGP)**

Guided-installer local studio covering Video (Wan 2.2, H3), Images (Qwen-Image-2.1, FLUX.2), Music, Speech, and 3D inside one browser UI starting at 6 GB VRAM, plus native MCP.

- **When to use:** Default turnkey local media setup for newcomers and 6GB-16GB NVIDIA workstations (5.9-14.3 GiB video VRAM vs ComfyUI's 22.7-23.5 GiB).
- **Footprint:** 6-15 GB NVIDIA VRAM (MMGP v4 + Extreme Chunker)
- **Evidence:** Primary evaluation · verified 2026-11-28
- **Why this pick:** [Split Local Media Into Turnkey Low-VRAM (WanGP) vs. Programmable Agent Engine (ComfyUI + MCP)](../docs/why-this-stack.md#adr-why-wangp-and-comfyui)
- **Limitation:** Install WGPKernels 1.5.0 and SageGP 1.0.2 (PyTorch 2.10; Triton 3.6+ required for RTX 50-series adaptive Sage2/3).
- **Limitation:** Heavy local video synthesis targets NVIDIA GPUs; Mac users should route heavy video to a remote GPU PC or Comfy Cloud.
- **Limitation:** GitHub /releases/latest tracks WanGP Manager (manager-v0.1.21) while core studio wgp.py ships on main at v20.21.
<!-- swissknife:end -->

<!-- swissknife:begin slot id=agent-media-mcp -->
**Active Anchor — [Comfy-Org Official comfy-mcp (Local & Cloud)](https://github.com/Comfy-Org/comfy-mcp)**

First-party open-source local MCP server (pip install comfy-mcp, zero account) and hosted Comfy Cloud MCP supporting remote Tailscale GPU hosts via COMFYUI_URL with inline media previews.

- **When to use:** Default agent-to-ComfyUI bridge for Pi, OpenCode, and Antigravity across local, Tailscale, or Comfy Cloud backends.
- **Evidence:** Official documentation · verified 2026-11-28
- **Why this pick:** [Split Local Media Into Turnkey Low-VRAM (WanGP) vs. Programmable Agent Engine (ComfyUI + MCP)](../docs/why-this-stack.md#adr-why-wangp-and-comfyui)
- **Limitation:** Local launch/restart requires comfy-cli >= 1.14.0 (>= 1.16.0 for job watching), and v0.11.0 skips local launch/restart whenever COMFYUI_URL is set for remote Tailscale hosts.
- **Limitation:** On a single 16GB GPU, explicitly unload the local LLM in Pi (/llama) before queuing heavy ComfyUI video workflows.
<!-- swissknife:end -->

<!-- swissknife:begin recipe id=comfy-mcp -->
<details>
<summary>Launch command — Comfy-Org Official comfy-mcp (Local & Cloud) (CUDA / llama.cpp / CLI)</summary>

```bash
pip install comfy-mcp && COMFYUI_URL=http://127.0.0.1:8188 comfy-mcp
```

</details>

Built-in upstream check: `comfy-mcp --help`
<!-- swissknife:end -->

## Verified Local Media Tools & Models

<!-- swissknife:begin table tag=media -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [WanGP v20.21 (One-Stop Low-VRAM Media Studio)](https://github.com/deepbeepmeep/WanGP) | Default turnkey local media setup for newcomers and 6GB-16GB NVIDIA workstations (5.9-14.3 GiB video VRAM vs ComfyUI's 22.7-23.5 GiB). | 6-15 GB NVIDIA VRAM (MMGP v4 + Extreme Chunker) | Primary evaluation | Install WGPKernels 1.5.0 and SageGP 1.0.2 (PyTorch 2.10; Triton 3.6+ required for RTX 50-series adaptive Sage2/3). |
| [ComfyUI (Comfy-Org Programmable Node Graph)](https://github.com/Comfy-Org/ComfyUI) | Developers building reproducible multi-stage media graphs or driving local/remote GPU rendering from Pi. | 8-24 GB NVIDIA VRAM (use Comfy-Org INT8 or leejet/ComfyUI-GGUF on 16GB) | Official documentation | Official ComfyUI docs explicitly advise Mac users away from heavy local video on Apple MPS (FP8 crashes MPS); target a remote NVIDIA box or Comfy Cloud. |
| [Comfy-Org Official comfy-mcp (Local & Cloud)](https://github.com/Comfy-Org/comfy-mcp) | Default agent-to-ComfyUI bridge for Pi, OpenCode, and Antigravity across local, Tailscale, or Comfy Cloud backends. | MIT | Official documentation | Local launch/restart requires comfy-cli >= 1.14.0 (>= 1.16.0 for job watching), and v0.11.0 skips local launch/restart whenever COMFYUI_URL is set for remote Tailscale hosts. |
| [artokun/comfyui-mcp (Power-User Control Plane)](https://github.com/artokun/comfyui-mcp) | Power users wanting automated workflow debugging, Mermaid graph conversion, and active VRAM management on 16GB rigs. | MIT | Field observation | Community-maintained; verify compatibility alongside Comfy-Org's first-party comfy-mcp updates. |
| [Wan 2.2 (5B & A14B Apache-2.0 Video)](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | Commercial-safe local video generation on consumer NVIDIA GPUs. | 6-15 GB VRAM via WanGP MMGP v4 | Official documentation | Newer Wan 3.0 and Wan 2.6 releases remain closed cloud APIs with no published local weights. |
| [Qwen-Image-2.1 (7B DiT Native RGBA)](https://huggingface.co/Qwen/Qwen-Image-2.1) | Non-commercial design assets, typography, and layered transparent image editing. | 4.2-9.1 GB VRAM (INT8 / leejet GGUF) | Official documentation | Non-commercial license; swap to Apache-2.0 FLUX.2 Klein for commercial production graphics. |
| [HeyGen Hyperframes](https://github.com/heygen-com/hyperframes) | Code-driven product demos and technical videos where diffusion flicker is undesirable. | MIT | Official documentation | Designed for structured UI/data motion graphics rather than photorealistic live-action video. |
| [Gradium Phonon 31M WebGPU TTS](https://github.com/blixt/phonon) | Instant zero-install local speech synthesis for students, Mac users, and browser workflows. | 64.5 MB (Browser WebGPU) | Official documentation | Compact English voice model; heavier multilingual dramatic acting requires larger server-side TTS models. |
| [Fish Audio Drama 3 (35B-A3B Multi-Speaker TTS)](https://huggingface.co/fishaudio/drama-3) | Studio-grade local multi-speaker narration and expressive TTS on 32GB-80GB GPUs (or Hybrid RAM). | 32-80 GB GPU (SGLang-Omni / vLLM-Omni) | Official documentation | Too heavy for a 16GB GPU alongside an LLM; use Phonon 31M for zero-GPU/laptop speech. |
| [Lightricks LTX-2.5 (22B Distilled Video + Synchronized Audio)](https://huggingface.co/Lightricks/LTX-2.5) | Local video generation with synchronized audio on 8GB-24GB NVIDIA GPUs. | 5.9-8.1 GiB (WanGP) / 16-24 GiB (ComfyUI) | Official documentation | Gated Hugging Face license acceptance required; use Wan 2.2 when strict Apache-2.0 licensing is mandatory. |
<!-- swissknife:end -->

## Critical Hardware & Licensing Boundaries

1. **Apple Silicon Macs:** ComfyUI's official docs advise Mac users against running heavy modern video models locally on Apple MPS (FP8 weights crash MPS). Run `Pi` + `comfy-mcp` on your Mac and point `COMFYUI_URL` at a discrete NVIDIA PC over Tailscale—or use Comfy Cloud's free trial runs.
2. **16GB NVIDIA GGUF Loader Trap:** For `Qwen-Image-2.1` inside ComfyUI on 16GB cards, use **Comfy-Org's official INT8 checkpoints** or **`leejet/ComfyUI-GGUF`** (original `city96/ComfyUI-GGUF` throws unknown architecture errors).
3. **Commercial Licensing:** `Wan 2.2`, `Phonon 31M`, and `FLUX.2 Klein` are Apache-2.0 commercial-safe; `Qwen-Image-2.1` is **non-commercial** (Qwen Research license).

---

**Continue reading:** [Discrete GPU PC](../worlds/gpu-workstation.md) · [The Personal AI Fabric](../worlds/personal-ai-fabric.md)
