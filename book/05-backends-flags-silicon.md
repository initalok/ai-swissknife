← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)

# Chapter 05 · Backends, Quantization & OS/Silicon

> [!IMPORTANT]
> **Verdict:** Serving kernels and hybrid MoE memory flags (`--n-cpu-moe`, `--load-mode`, `WanGP v20.12`) unlock 2x–5x speedups on 16GB cards and Apple Silicon.
> **Read this chapter if:** You are tuning local inference servers, CUDA/AVX-512 offload sweeps, or Mac MLX stacks.

## 1. Verified Backends & Silicon Engines

| Backend & Health | Breakthroughs | Target & TTL | Compatibility Gotcha |
| :--- | :--- | :--- | :--- |
| [**Unsloth Runtime & Studio (v0.1.923-beta)**](https://github.com/unslothai/unsloth)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 1.9x faster Inkling 2 Mini, 3x faster VRAM-exceeding MoE GGUFs, 4.1x faster Laya, AMD NPU, Bwrap/Seatbelt/MXC sandboxes | `Apache-2.0`<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Mandatory runtime for Unsloth's looped-layer Inkling 2 Mini GGUFs and Anthropic-endpoint local Claude Code routing. |
| [**llama.cpp (Mainline GGUF Engine)**](https://github.com/ggml-org/llama.cpp)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Universal CUDA/Metal/Vulkan/ROCm engine with --n-cpu-moe hybrid offload, --lora hot-loading, and --load-mode | `MIT`<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ --no-mmap is deprecated (migrate to --load-mode none); add -cuda graphs=0 if partial MoE offload outputs gibberish. |
| [**ik_llama.cpp (High-Perf CUDA/AVX-512 Fork)**](https://github.com/ikawrakow/ik_llama.cpp)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Leads bleeding-edge kernels: FlashMLA, IQK AVX-512 (HAVE_FANCY_SIMD), Trellis IQ2_KS/IQ3_KT quants | `MIT`<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ CPU + NVIDIA CUDA only; avoid -rtr on k-quants with MoE offload. |
| [**WanGP v20.12 + MMGP v4 + SageGP 1.0.2**](https://github.com/deepbeepmeep/WanGP)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Extreme Chunker fits 15s of 1080p Hailuo H3 video into 5.9 GB VRAM; pi-H3 DWD (2-4 steps), Infinite Sliding Windows, Deepy MCP | `Apache-2.0`<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Install WGPKernels 1.5.0 and SageGP 1.0.2 (PyTorch 2.10; Triton 3.6+ for RTX 50xx adaptive Sage2/3). |
| [**ComfyUI (v0.46+)**](https://github.com/comfyanonymous/ComfyUI)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Modular visual node engine with SenseNova, RMBG 3.0, RAFT Video Deflicker, and KJNodes block-swap | `GPL-3.0`<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Heavy custom node graphs break across updates; pin venv snapshots for production pipelines. |
| [**Apple MLX (mlx-lm / mlx-vlm)**](https://github.com/ml-explore/mlx-lm)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Zero PCIe copy bottleneck on Mac mini/Studio unified memory; runs Qwen3.8-27B-super-adapter-MLX at ~65 tok/s (4-bit) | `MIT`<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Prompt prefill lags dedicated NVIDIA Tensor Cores; 32GB+ unified memory recommended for 27B MLX. |

<details>
<summary>🛠️ <b>2026 Zone-2 MoE Sweep Flag Reference</b></summary>
<br>

```bash
GGML_CUDA_GRAPH_OPT=1 llama-server -m Qwen3-Coder-Next-UD-Q4_K_XL.gguf -ngl 99 -fa on -c 120000 --load-mode none --n-cpu-moe 29 -ctk q8_0 -ctv q8_0 --temp 0
```
</details>

---

← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)
