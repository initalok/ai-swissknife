← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)

# Chapter 03 · Multimodal, Voice, Video, 3D & World Models

> [!IMPORTANT]
> **Verdict:** Use free cloud STT/vision where fast, and pivot locally for RGBA editing, directed multi-speaker TTS, 3D meshes, and 5.9 GB 1080p video.
> **Read this chapter if:** You are building image, video, audio, OCR, 3D asset, or interactive world pipelines.

## 1. Verified Multimodal & 3D Stack

| Model & Health | Strengths & Proof | License, Footprint & TTL | Hardware / License Gotcha |
| :--- | :--- | :--- | :--- |
| [**Qwen-Image-2.1 (7B DiT)**](https://huggingface.co/Qwen/Qwen-Image-2.1)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 #1 VDEBench; native RGBA layer output and 2048px typography in 9.1 GB VRAM (Q4_K_M via sd.cpp) | `Qwen Research (Non-Commercial)` · <kbd>zone1-16gb-vram</kbd> · ~9.1 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Non-commercial Qwen Research license; separate from nvidia/Qwen-Image-Flash (20.4B DiT needing RAM offload). |
| [**FLUX.2 Klein**](https://huggingface.co/black-forest-labs)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Permissive Apache-2.0 commercial-safe image generator fitting cleanly inside 16GB VRAM | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~10.0 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Use FLUX.2 Klein instead of Qwen-Image-2.1 for commercial product graphics. |
| [**Wan 2.2 (5B & A14B Video)**](https://huggingface.co/Wan-AI)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Top permissive Apache-2.0 open-weight video model accelerated by WanGP v20.12 MMGP v4 | `Apache-2.0` · <kbd>zone1-2-hybrid</kbd> · ~8.0 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Wan 3.0 and Wan 2.6 remain closed APIs with no published weights. |
| [**LTX-2.5 (22B Video + Sync Audio)**](https://huggingface.co/Lightricks)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Synchronized video + audio generation; pairs with Hy-Nomas for video-conditioned world sound | `LTX-Community` · <kbd>zone2-64gb-hybrid</kbd> · ~14.0 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Requires 64GB RAM block-swapping on 16GB GPUs; verify LTX Community commercial thresholds. |
| [**Tencent Hy-Nomas (Interactive World Model)**](https://github.com/Tencent-Hunyuan/Hy-Nomas)<br><sub>`experimental` · 🟢 `Fresh`</sub> | 🏆 Open-weight WASD-walkable interactive world generator with single-GPU inference and LoRA support | `Non-Commercial (PixelUMM)` · <kbd>zone1-16gb-vram</kbd> · ~12.0 GB<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Uses NVIDIA PixelUMM decoder (non-commercial previs/pitch use only). |
| [**Fish Audio Drama 3 (35B-A3B TTS)**](https://fish.audio/)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 16-speaker tags, single-word Audio Inpainting, #1 Pronunciation Robustness (93.2%) via SGLang-Omni | `Fish Community (<$500K/yr)` · <kbd>zone2-64gb-hybrid</kbd> · ~20.0 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Free commercial cap at $500K annual revenue; runs in Zone 2 hybrid on 16GB+64GB. |
| [**Gradium Phonon 31M WebGPU TTS**](https://github.com/blixt/phonon)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 64.5 MB q8.gguf running inside browser WebGPU at 115-130x real-time with 4.9ms first-audio latency | `Apache-2.0` · <kbd>browser-webgpu</kbd> · ~0.11 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ English-only; larger 5-language Phonon 40M checkpoints are CC BY-NC 4.0 non-commercial. |
| [**Qwen3-ASR (1.7B) + ForcedAligner-0.6B**](https://huggingface.co/Qwen)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Local 10x real-time speech recognition with single-pass word-level timestamp alignment | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~3.0 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ For zero-VRAM cloud bursts, Groq Whisper-Large-v3 offers 2,000 free RPD. |
| [**DeepSeek-OCR 2 (3B)**](https://huggingface.co/deepseek-ai)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Visual Causal Flow restores human reading order across multi-column PDFs, LaTeX, and tables | `MIT` · <kbd>zone1-16gb-vram</kbd> · ~3.8 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Run locally on sensitive PDFs instead of free cloud vision APIs. |
| [**EmbeddingGemma 2 (Multimodal RAG)**](https://huggingface.co/google)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Text + image retrieval pinned in 64GB DDR5 RAM so RAG consumes 0 MB VRAM | `Apache-2.0` · <kbd>cpu-ram-0vram</kbd><br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Keep chunk sizes disciplined when mixing high-res PDF crops with text. |
| [**Microsoft TRELLIS v1 (3D Asset Gen)**](https://github.com/microsoft/TRELLIS)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 MIT-licensed structured 3D latent asset generator fitting inside 16GB VRAM | `MIT` · <kbd>zone1-16gb-vram</kbd> · ~15.5 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ TRELLIS.2 officially demands 24GB VRAM; stick to TRELLIS v1 or quantized ComfyUI builds on 16GB. |
| [**Hunyuan3D 2.0 / 2mini (PBR 3D)**](https://github.com/Tencent/Hunyuan3D-2)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 High-detail PBR-textured 3D mesh generation in 6-16 GB VRAM | `Tencent Community (Geo-Restricted)` · <kbd>zone1-16gb-vram</kbd> · ~12.0 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Tencent Community License is invalid in EU, UK, and South Korea; HY 3D 3.0/3.1 are closed API-only. |

---

← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)
