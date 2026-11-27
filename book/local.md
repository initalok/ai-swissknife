[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; **🖥️ Local** &nbsp;·&nbsp; [⚙️ Harnesses & RL](../book/harnesses-and-rl.md) &nbsp;·&nbsp; [📘 Playbooks](../book/playbooks.md) &nbsp;·&nbsp; [🧭 Spokes](../book/spokes.md) &nbsp;·&nbsp; [📡 Radar](../book/radar.md) &nbsp;·&nbsp; [🪦 Graveyard](../book/graveyard.md)

# 🖥️ Local AI Hardware Blueprints

> [!IMPORTANT]
> Built around your starter hardware profiles (`16vram-64ram` and `mac-apple-silicon`). Daily-driver **Track A (Mature & Riced)** models stay strictly isolated from **Track B (Cutting-Edge)** experimental architectures.

## 1. Track A · Mature & Fully Riced (Daily Drivers)
*Predictable runtimes, verified LoRA adapters, zero kernel drama.*

### [**Qwen3.8-27B (Dense Vision+Text Backbone)**](https://huggingface.co/Qwen/Qwen3.8-27B) · 🟢 `Fresh`
**Profiles:** `16vram-64ram`, `mac-apple-silicon` · **Footprint:** `14.5 GB (IQ4_XS · Zone 1 16GB VRAM)` · **License:** `Apache-2.0` · *Verified `2026-11-27`*

- 🏆 Top 16GB VRAM dense coding & strict-instruction backbone (73.0 Terminal-Bench, 94.9 SWE-Pro Unsloth)
- 🏆 Single frozen backbone hosting both HF Harness RL Adapters and Securelayer7 26 MB uncensored LoRA
- ⚡ **Hot-Swappable Adapters (Implicit `adapts` Edges):** [**Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)**](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter), [**Qwen3.8-27B 26MB Uncensored LoRA (Rank-3)**](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated)
- ⚠️ Use IQ4_XS + Q8 KV cache on 16GB VRAM so weights never spill across PCIe.

```bash
llama-server -m Qwen3.8-27B-IQ4_XS.gguf -ngl 99 -fa on -c 32768 -ctk q8_0 -ctv q8_0
```

### [**Qwen3-Coder-Next (80B-A3B Sparse MoE)**](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) · 🟢 `Fresh`
**Profiles:** `16vram-64ram`, `mac-apple-silicon` · **Footprint:** `49 GB (UD-Q4_K_XL · Zone 2 16GB+64GB Hybrid)` · **License:** `Apache-2.0` · *Verified `2026-11-27`*

- 🏆 512-expert sparse MoE activating 3B params/token; battle-tested daily driver in llama.cpp & ik_llama.cpp
- ⚠️ Never lower -ngl on MoEs; keep Attention/KV on GPU and sweep --n-cpu-moe.

```bash
GGML_CUDA_GRAPH_OPT=1 llama-server -m Qwen3-Coder-Next-UD-Q4_K_XL.gguf -ngl 99 -fa on -c 120000 --load-mode none --n-cpu-moe 29 -ctk q8_0 -ctv q8_0 --temp 0
```

### [**Gemma 4 Family (26B-A4B Vision & 12B Tri-Modal)**](https://ai.google.dev/gemma) · 🟢 `Fresh`
**Profiles:** `16vram-64ram`, `mac-apple-silicon` · **Footprint:** `8.5-14 GB (Zone 1 16GB VRAM)` · **License:** `Apache-2.0` · *Verified `2026-11-27`*

- 🏆 26B-A4B runs ~140 tok/s 100% resident in 16GB VRAM; 12B adds native local audio input
- ⚠️ Gemma 4 Audio Trap: only E2B/E4B/12B process audio; 26B-A4B is Text + Vision only.

### [**NousResearch Hermes 4 (14B / 4.3-36B Neutral)**](https://huggingface.co/NousResearch/Hermes-4-14B) · 🟢 `Fresh`
**Profiles:** `16vram-64ram`, `mac-apple-silicon` · **Footprint:** `9 GB (14B) / 22 GB (36B Hybrid)` · **License:** `Apache-2.0` · *Verified `2026-11-27`*

- 🏆 Tops RefusalBench via neutral alignment: uncensored by default while obeying operator system-prompt policies
- ⚠️ Author explicit operator rules in the system prompt if deploying beyond solo use.

```bash
llama-server -m Hermes-4-14B-Q4_K_M.gguf -ngl 99 -fa on -c 32768
```

## 2. Track B · Cutting-Edge Local (High Upside / Faster Churn)
*Looped MoEs, N-gram prefetch ceilings, and emerging architectures.*

### [**Inkling 2 Mini (26.4B Looped Transformer MoE)**](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) · 🟢 `Fresh`
**Profiles:** `16vram-64ram`, `mac-apple-silicon` · **Footprint:** `13-18 GB (UD-Q3/Q4 + DSpark · Zone 1/2)` · **License:** `Apache-2.0 + AUP` · *Verified `2026-11-27`*

- 🏆 Middle 12 of 24 layers loop 3x (3.4B base / 5.4B eff. active, 1M ctx); 79.2% SWE-bench Verified, 48.2% DeepSWE v1.1
- 🏆 Mainline llama.cpp (#32218, Nov 23) now supports looped layers & DSpark natively alongside Unsloth
- ⚠️ Trails Qwen3.8-27B on strict chat (50% MultiChallenge); cap turns/tokens to avoid repetitive debug loops and sandbox file edits.

```bash
llama-server -hf unsloth/Inkling-2-Mini-GGUF:UD-Q4_K_M
```

## 3. System-1 Local Decision Models (Non-Autoregressive)
*Zero-output-token safety gates, routers, and multimodal classifiers.*

### [**Laya 0.5 (Multimodal System-1 Decision Model)**](https://github.com/NandhaKishorM/laya) · 🟢 `Fresh`
**Profiles:** `16vram-64ram`, `mac-apple-silicon` · **Footprint:** `678-846 MB (CPU / NPU / WebGPU)` · **License:** `Apache-2.0` · *Verified `2026-11-27`*

- 🏆 Evaluates 64 typed decisions per pass in <100-500ms; v0.5 reads text, images, audio & video up to 73,728 tokens
- 🏆 Installs cleanly via pip install -U laya; serves via Unsloth Decision API (localhost:8888)
- ⚠️ Threshold on probabilities (not confidence); vegaml-learn continuous learning add-on is non-commercial.

```bash
unsloth serve-decision convaiinnovations/laya-typed-decisions --port 8888
```

## 4. Local Media & Voice Anchors
*Core open-weight creative models fitting inside 16GB VRAM + 64GB RAM.*

### [**Qwen-Image-2.1 (7B DiT Native RGBA)**](https://huggingface.co/Qwen/Qwen-Image-2.1) · 🟢 `Fresh`
**Profiles:** `16vram-64ram`, `mac-apple-silicon` · **Footprint:** `9.1 GB VRAM (Q4_K_M)` · **License:** `Qwen Research (Non-Commercial)` · *Verified `2026-11-27`*

- 🏆 #1 VDEBench; native RGBA layer output and 2048px typography inside 16GB VRAM
- ⚠️ Non-commercial Qwen Research license; use FLUX.2 Klein (Apache-2.0) for commercial graphics.

### [**Wan 2.2 (5B & A14B Open Video)**](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) · 🟢 `Fresh`
**Profiles:** `16vram-64ram` · **Footprint:** `6-15 GB VRAM via WanGP MMGP v4` · **License:** `Apache-2.0` · *Verified `2026-11-27`*

- 🏆 Top permissive Apache-2.0 local video checkpoint accelerated by WanGP v20.12
- ⚠️ Wan 3.0 and Wan 2.6 remain closed APIs with no published weights.

---

[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; **🖥️ Local** &nbsp;·&nbsp; [⚙️ Harnesses & RL](../book/harnesses-and-rl.md) &nbsp;·&nbsp; [📘 Playbooks](../book/playbooks.md) &nbsp;·&nbsp; [🧭 Spokes](../book/spokes.md) &nbsp;·&nbsp; [📡 Radar](../book/radar.md) &nbsp;·&nbsp; [🪦 Graveyard](../book/graveyard.md)
