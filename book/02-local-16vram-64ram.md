← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)

# Chapter 02 · Local AI (16GB VRAM + 64GB RAM: Mature vs. Cutting-Edge)

> [!IMPORTANT]
> **Verdict:** Keep battle-tested Mature Riced daily drivers separate from experimental Cutting-Edge architectures so runtime churn never breaks your local workflow.
> **Read this chapter if:** You are deploying local LLMs, Harness LoRAs, Uncensored/Neutral models, or System-1 Decision Models inside 16GB VRAM + 64GB RAM.

## 1. Track A · Mature & Fully Riced

| Model & Health | Proof & Benchmarks | Footprint & TTL | Tuning Gotcha |
| :--- | :--- | :--- | :--- |
| [**Qwen3.8-27B (Dense Vision+Text)**](https://huggingface.co/Qwen/Qwen3.8-27B)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Top 16GB VRAM dense coding & strict-instruction backbone (73.0 Terminal-Bench, 94.9 SWE-Pro Unsloth)<br>🏆 Base model for Hugging Face's official pi/Hermes/OpenCode RL Harness Adapters | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~14.5 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Use IQ4_XS + Q8 KV cache on 16GB VRAM so it never spills across PCIe. |
| [**Qwen3-Coder-Next (80B-A3B)**](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 512-expert sparse MoE activating 3B params/token; mature llama.cpp/ik_llama.cpp daily driver | `Apache-2.0` · <kbd>zone2-64gb-hybrid</kbd> · ~49.0 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Never lower -ngl on MoEs; keep Attention/KV on GPU and sweep --n-cpu-moe. |
| [**North-Mini-Code-1.0 (30B-A3B)**](https://huggingface.co/models)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Multi-harness sparse coding specialist fitting comfortably in 16GB VRAM + minimal RAM spill | `Apache-2.0` · <kbd>zone2-64gb-hybrid</kbd> · ~19.0 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Check exact quant sizing against context window before pinning KV cache. |
| [**Nemotron-Cascade-2 (30B-A3B)**](https://huggingface.co/nvidia)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 90.9% AIME Olympiad reasoning efficiency inside 19 GB sparse MoE footprint | `NVIDIA-Open` · <kbd>zone2-64gb-hybrid</kbd> · ~19.0 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Long reasoning traces consume context fast; cap max tokens on routine tasks. |
| [**Gemma 4 (26B-A4B MoE)**](https://huggingface.co/google)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 3.8B active parameters hitting ~140 tok/s 100% resident in 16GB VRAM | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~14.0 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Text + Vision ONLY; unlike E2B/E4B/12B, the 26B-A4B checkpoint does NOT process audio. |
| [**Gemma 4 (12B Tri-Modal)**](https://huggingface.co/google)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Native Text + Vision + Audio local generalist fitting easily inside 16GB VRAM | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~8.5 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Use this checkpoint (not 26B-A4B) whenever local audio input is required. |
| [**Devstral Small 2 (24B)**](https://huggingface.co/mistralai)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Compact Apache-2.0 agentic software engineering model for 16GB VRAM | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~14.0 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Trails Qwen3.8-27B + Harness Adapters on SWE-bench Pro hard-51. |
| [**NousResearch Hermes 4 (14B / 4.3-36B Neutral)**](https://huggingface.co/NousResearch)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Tops RefusalBench via neutral alignment: uncensored by default while obeying operator system prompts<br>🏆 Hybrid reasoner supporting on/off reasoning tags | `Apache-2.0` · <kbd>zone1-2-hybrid</kbd> · ~9.0 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Always author explicit operator guardrails in the system prompt if deploying beyond solo use. |
| [**Dolphin 3.0 Mistral 24B / Dolphin-R1**](https://huggingface.co/cognitivecomputations)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Deliberate refusal-free finetune with 800K uncensored R1 reasoning traces | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~14.5 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Mature conversational/roleplay feel, but coding benchmarks trail Qwen3.8-27B. |

## 2. Track B · Cutting-Edge & Specialized Local

| Model & Health | Upside & Benchmarks | Footprint & TTL | Early-Adopter Gotcha |
| :--- | :--- | :--- | :--- |
| [**Qwen3.8-27B-Uncensored-GGUF (Abliterated + MTP)**](https://huggingface.co/models)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Orthogonalizes refusal direction (~1-3% weight delta) while retaining MTP head for 1.19-1.28x decode speedup | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~15.0 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Cannot refuse anything ever; strictly isolate behind safeagents/Laya when wired to shell tools.<br>⚠️ Pass --image-min-tokens 1024 for vision; avoid aggressive abliteration builds. |
| [**Gemma-4-26B-MoE-HERETIC**](https://huggingface.co/models)<br><sub>`experimental` · 🟢 `Fresh`</sub> | 🏆 Fast ~140 tok/s Heretic abliterated MoE resident in 16GB VRAM | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~14.0 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Community abliteration checkpoint; verify factual degradation on your domain and never expose to untrusted users. |
| [**Inkling 2 Mini (26.4B Looped Transformer MoE)**](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF)<br><sub>`experimental` · 🟢 `Fresh`</sub> | 🏆 Middle 12 of 24 layers loop 3x (3.4B base / 5.4B eff. active, 1M ctx); 79.2% SWE-bench Verified, 48.2% DeepSWE v1.1, 0.703 Intelligence per Watt<br>🏆 Unsloth provides 1.9x faster decoding; Basalt reaches 60 tok/s on 16GB RTX 5060 Ti | `Apache-2.0 + AUP` · <kbd>zone1-2-hybrid</kbd> · ~17.6 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Stock llama.cpp cannot load looped-layer root GGUFs; requires Unsloth runtime or Basalt.<br>⚠️ Trails Qwen3.8-27B on strict chat (50% MultiChallenge); can enter repetitive debug loops so always cap turns and sandbox file actions. |
| [**Qwen3.8-Flash-Next (180B Dynamic v3.1)**](https://huggingface.co/unsloth)<br><sub>`experimental` · 🟢 `Fresh`</sub> | 🏆 91.9 DeepSWE 1.1; 51B N-gram table prefetches asynchronously from 64GB DDR5 at near-GPU speed | `qwen-community-1.0` · <kbd>zone2-64gb-ceiling</kbd> · ~68.0 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Strictly cap at UD-IQ1_S (66.4 GB), UD-IQ1_M (68 GB), or UD-Q2_0 (70.5 GB) + 2 GB MTP; larger quants overflow 80 GB total pool. |
| [**Recursive Flint (39.8B-A2.5B)**](https://huggingface.co/unsloth)<br><sub>`experimental` · 🟢 `Fresh`</sub> | 🏆 Fast hybrid sparse MoE (2.5B active) with 89.7% vendor-reported SWE-bench Pro v2 | `Apache-2.0` · <kbd>zone2-64gb-hybrid</kbd> · ~25.1 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Scores are vendor-reported and trail Qwen3.8-27B on Unsloth evaluations. |
| [**Meta Muse Glimmer (30B + DFlash)**](https://huggingface.co/models)<br><sub>`experimental` · 🟢 `Fresh`</sub> | 🏆 94.7% AIME, 65.9% OSWorld; DFlash block-diffusion drafter proposes 16 tokens per pass | `OpenMDW` · <kbd>zone2-64gb-hybrid</kbd> · ~20.0 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Requires runtime support for DFlash speculative drafting to hit peak speed. |
| [**DiffusionGemma (26B-A4B)**](https://huggingface.co/models)<br><sub>`experimental` · 🟢 `Fresh`</sub> | 🏆 Non-autoregressive text-diffusion LLM denoising 256-token blocks in parallel | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~15.0 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Early text-diffusion ecosystem; verify tool-calling reliability before replacing autoregressive coders. |

## 3. System-1 Local Decision Models

| Decision Model | Capabilities | Footprint & TTL | Wiring Gotcha |
| :--- | :--- | :--- | :--- |
| [**Laya Local Decision Models (678-846 MB)**](https://huggingface.co/convaiinnovations)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Non-autoregressive System-1 scorer evaluating 64 typed questions in <100-500ms on CPU/NPU/WebGPU | `Apache-2.0` · <kbd>cpu-npu-webgpu</kbd> · ~0.85 GB<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Threshold on probabilities (not confidence); route borderline superseded-vs-contradicted memory cases to review. |
| [**Custom 16K Clef-Head Decision LoRA**](https://github.com/unslothai/unsloth)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 1-epoch 4-bit LoRA via Unsloth DecisionTrainer lifts routing accuracy from ~35% to 78-81% with zero output tokens | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~4.0 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Requires domain-specific labeled classification examples to outperform zero-shot Laya. |

<details>
<summary>🛠️ <b>Local Launch Recipes (`python scripts/cli.py query local`)</b></summary>
<br>

```bash
# [qwen3.8-27b] (mature)
llama-server -m Qwen3.8-27B-IQ4_XS.gguf -ngl 99 -fa on -c 32768 -ctk q8_0 -ctv q8_0

# [qwen3-coder-next-80b] (mature)
GGML_CUDA_GRAPH_OPT=1 llama-server -m Qwen3-Coder-Next-UD-Q4_K_XL.gguf -ngl 99 -fa on -c 120000 --load-mode none --n-cpu-moe 29 -ctk q8_0 -ctv q8_0 --temp 0

# [hermes-4-neutral] (mature)
llama-server -m Hermes-4-14B-Q4_K_M.gguf -ngl 99 -fa on -c 32768

# [dolphin-3-r1-24b] (mature)
llama-server -m Dolphin3.0-R1-Mistral-24B-Q4_K_M.gguf -ngl 99 -fa on -c 32768

# [qwen3.8-27b-uncensored] (operational)
llama-server -m Qwen3.8-27B-Uncensored-IQ4_XS.gguf -ngl 99 -fa on --spec-type draft-mtp --spec-draft-n-max 1 -ctk q8_0 -ctv q8_0

# [inkling-2-mini] (experimental)
unsloth run unsloth/Inkling-2-Mini-GGUF:UD-Q4_K_XL --spec-draft-n-max 2

# [qwen3.8-flash-next] (experimental)
llama-server -m Qwen3.8-Flash-Next-UD-IQ1_M.gguf -ngl 99 -fa on --n-cpu-moe 36 --load-mode none

# [recursive-flint] (experimental)
llama-server -m Recursive-Flint-UD-Q4_K_XL.gguf -ngl 99 -fa on -c 65536 --n-cpu-moe 18

# [laya-decisions] (mature)
unsloth serve-decision convaiinnovations/laya-typed-decisions --port 8888
```
</details>

---

← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)
