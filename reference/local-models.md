[Home](../README.md) / Reference / Local Models

*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md))*

# Local Models Reference

Factual index of verified open-weight models fitting within the starter hardware envelopes (`16GB VRAM + 64GB RAM` or `Apple Silicon Mac`). For memory-layout concepts and setup walkthroughs, see the [Local AI Workstation Guide](../guides/local-ai-workstation.md).

| Model | Track | Footprint | License | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B) | `mature` | 14.5 GB (IQ4_XS, Zone 1 16GB VRAM) / ~16 GB (Mac MLX 4-bit) | `Apache-2.0` | Primary evaluation | On 16GB GPUs, keep quantization at IQ4_XS with Q8 KV cache so weights never spill over PCIe. |
| [Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) | `mature` | 49 GB (UD-Q4_K_XL, Zone 2 16GB VRAM + 64GB RAM) | `Apache-2.0` | Official documentation | Keep -ngl 99 so Attention and KV cache stay on GPU; offload cold experts only via --n-cpu-moe. |
| [Gemma 4 Family (26B-A4B Vision & 12B Tri-Modal)](https://ai.google.dev/gemma) | `mature` | 8.5 GB (12B) to 14 GB (26B-A4B, Zone 1 16GB VRAM) | `Apache-2.0` | Official documentation | Only E2B, E4B, and 12B process audio—the 26B-A4B MoE checkpoint is Text + Vision only. |
| [NousResearch Hermes 4 (14B / 4.3-36B Neutral)](https://huggingface.co/NousResearch/Hermes-4-14B) | `mature` | 9 GB (14B Q4) / 22 GB (36B Hybrid) | `Apache-2.0` | Vendor / lab claim | Always write explicit safety boundaries in your system prompt if exposing the model beyond solo local use. |
| [Inkling 2 Mini (26.4B Looped Transformer MoE)](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) | `experimental` | 13-18 GB (UD-Q3/Q4 + DSpark drafter) | `Apache-2.0 + AUP` | Vendor / lab claim | Published 79.2% SWE-bench Verified and 48.2% DeepSWE v1.1 scores are lab-reported; trails Qwen3.8-27B on strict chat (50% MultiChallenge). |
| [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya) | `mature` | 678-846 MB (CPU / NPU / WebGPU) | `Apache-2.0` | Official documentation | Threshold decisions on calibrated probabilities rather than raw confidence scores; the optional vegaml-learn add-on is non-commercial. |
| [Qwen-Image-2.1 (7B DiT Native RGBA)](https://huggingface.co/Qwen/Qwen-Image-2.1) | `mature` | 9.1 GB VRAM (Q4_K_M) | `Qwen Research (Non-Commercial)` | Official documentation | Licensed under Qwen Research (non-commercial); use Apache-2.0 FLUX.2 Klein for commercial production assets. |
| [Wan 2.2 (5B & A14B Open Video)](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | `mature` | 6-15 GB VRAM via WanGP MMGP v4 | `Apache-2.0` | Official documentation | Newer Wan 3.0 and Wan 2.6 releases remain closed cloud APIs with no published local weights. |

---

**Continue reading:** [Local AI Workstation Guide](../guides/local-ai-workstation.md) · [Harnesses & Inference Runtimes](harnesses-and-runtimes.md)
