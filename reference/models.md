---
title: "Models Reference (Across Hardware Tiers & Special Use Cases)"
section: reference
summary: "Core model fundamentals spanning Edge/16GB M4 Mac, 16-24GB GPUs, Hybrid/80GB servers, research-leading open frontier weights, and specialized OCR/speech/video/diffusion checkpoints."
order: 1
---

[Home](../README.md) / Reference / Models Reference

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Models Reference (Core Fundamentals)

Models are the load-bearing foundation of every stack in this handbook. Rather than limiting coverage strictly to one rig, this page organizes verified open-weight models by **physical hardware tier** and **special use cases**—including research-leading frontier open weights whose architectural breakthroughs (KV compression, Attention Residuals, DFlash/DSpark drafters, native MXFP4) trickle down into consumer hardware within quarters.

*(Looking for agent harnesses and inference runtimes? Those now live together in [Seasoned Developer Fast-Track](../docs/start-here-developer.md).)*

## Tier 1 · Edge, Laptop & 16GB M4 Mac mini (`<= 10 GB` Active Memory)

Fits cleanly inside a base 16GB M4 Mac mini's ~10.7 GB wired GPU budget or an 8GB-12GB laptop without swapping.

<!-- swissknife:begin table tag=tier-edge-mac -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Gemma 4 Family (12B Tri-Modal & 26B-A4B Vision)](https://ai.google.dev/gemma) | 8GB-12GB laptops needing local chat/audio, or ultra-fast 16GB vision and general chat. | 8.5 GB (12B) to 14 GB (26B-A4B) | Official documentation | Only E2B, E4B, and 12B process audio; the 26B-A4B MoE checkpoint is Text + Vision only. |
| [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya) | Fast zero-output-token tool-safety gating, routing, and memory relevance checks without using GPU VRAM. | 678-846 MB (CPU / NPU / WebGPU) | Official documentation | Threshold decisions on calibrated probabilities rather than raw confidence scores; optional vegaml-learn add-on is non-commercial. |
| [Qwen3.5-9B (Multimodal Hybrid DeltaNet)](https://huggingface.co/Qwen/Qwen3.5-9B) | Fast local helper, screenshot triage, and offline coding/edits on a base 16GB M4 Mac mini or 8GB-12GB GPU laptop. | ~5.6 GB (4-bit MLX / Q4 GGUF, 262K native ctx) | Official documentation | Trails 27B+ backbones on complex multi-file refactors; route heavy coding tasks to GPU PC or $0 Cloud. |
| [DeepSeek-OCR-2 (3B Visual Causal Flow)](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2) | Local private PDF/scan-to-Markdown ingestion into Obsidian knowledge vaults on any 6GB-16GB GPU or Mac. | ~2-6 GB (GGUF / vLLM) | Primary evaluation | Specialized for document layout and OCR rather than general multi-turn chat. |
<!-- swissknife:end -->

## Tier 2 · Consumer 16GB–24GB GPUs (`12–20 GB` VRAM)

Daily-driver coding backbones, looped-layer MoEs, block-diffusion LLMs, and DFlash-accelerated local agents.

<!-- swissknife:begin table tag=tier-16-24gb -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B) | Daily-driver local coding, strict instruction following, and single-backbone multi-LoRA serving. | 14.5 GB (IQ4_XS, Zone 1 16GB VRAM) / ~16 GB (Mac MLX 4-bit) | Primary evaluation | On 16GB GPUs, keep quantization at IQ4_XS with Q8 KV cache so weights never spill over PCIe. |
| [Gemma 4 Family (12B Tri-Modal & 26B-A4B Vision)](https://ai.google.dev/gemma) | 8GB-12GB laptops needing local chat/audio, or ultra-fast 16GB vision and general chat. | 8.5 GB (12B) to 14 GB (26B-A4B) | Official documentation | Only E2B, E4B, and 12B process audio; the 26B-A4B MoE checkpoint is Text + Vision only. |
| [NousResearch Hermes 4 (14B / 4.3-36B Neutral)](https://huggingface.co/NousResearch/Hermes-4-14B) | Self-hosted deployments needing predictable operator-controlled behavior rather than abliteration. | 9 GB (14B Q4) / 22 GB (36B Hybrid) | Vendor / lab claim | Always author explicit safety policies in your system prompt if exposing the endpoint beyond solo local use. |
| [Inkling 2 Mini (26.4B Looped Transformer MoE)](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) | Testing high-efficiency looped coding architectures inside 16GB-18GB memory budgets. | 13-18 GB (UD-Q3/Q4) | Vendor / lab claim | Published 79.2% SWE-bench Verified and 48.2% DeepSWE v1.1 figures are lab-reported; trails Qwen3.8-27B on strict chat. |
| [OpenAI gpt-oss-20b (Native MXFP4 MoE)](https://huggingface.co/openai/gpt-oss-20b) | Fast 16GB GPU reasoning, function calling, and browser/agent workflows with generous 32K-64K context headroom. | ~12.8 GB (Native MXFP4; 16GB GPU or Mac w/ wired_limit_mb tuning) | Official documentation | Requires the Harmony response format (handled automatically by modern llama.cpp/vLLM chat templates); text-only. |
| [Meta Muse Glimmer 30B (+ DFlash 16-Token Drafter)](https://huggingface.co/meta-models/Muse-Glimmer-30B) | 24GB-32GB VRAM workstations or 32GB+ Macs wanting high-speed local multimodal agents with controllable reasoning strength. | <20 GB (4-bit K-Quant + Perception Encoder + DFlash; 24GB-32GB envelope) | Vendor / lab claim | Needs a 24GB-32GB VRAM or unified-memory envelope alongside KV cache and DFlash; exceeds a single 16GB card without RAM spill. |
| [Google DiffusionGemma 26B-A4B (Block-Diffusion LLM)](https://huggingface.co/google/diffusiongemma-26B-A4B-it) | 24GB+ GPUs researching non-autoregressive parallel code/layout generation and fast canvas infilling. | ~18 GB quantized (24GB+ VRAM recommended) | Official documentation | Requires diffusion-aware sampling (entropy-bounded denoising) and works best on well-structured tasks rather than open-ended prose. |
<!-- swissknife:end -->

## Tier 3 · Hybrid Workstations (`16GB+64GB`) & Single-80GB Servers

Sparse MoEs, RAM-prefetchable N-gram hybrids (`Qwen3.8-Flash-Next`), and single-H100 / DGX Spark open checkpoints.

<!-- swissknife:begin table tag=tier-hybrid-80gb -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) | Deeper multi-file repository reasoning on 16GB GPU + 64GB RAM workstations or 64GB+ Macs. | 49 GB (UD-Q4_K_XL, Zone 2 16GB VRAM + 64GB RAM) | Official documentation | Keep -ngl 99 so Attention and KV cache stay in GPU VRAM; offload cold experts only via --n-cpu-moe. |
| [Qwen3.8-Flash-Next (180B / 6B Active + 51B N-Gram)](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | High-memory workstations (64GB-128GB RAM + 16GB+ VRAM via Unsloth Dynamic v3.1 UD-IQ1_M/UD-Q2_0) or SGLang/vLLM servers. | 66-70 GB (Unsloth Dynamic v3.1 UD-IQ1_M / UD-Q2_0) or multi-GPU BF16 | Official documentation | Custom qwen-community-1.0 license; avoid the oversized 79.6 GB UD-Q2_K_XL quant on 16GB+64GB systems. |
| [OpenAI gpt-oss-120b (Single-80GB MXFP4 Reasoning)](https://huggingface.co/openai/gpt-oss-120b) | Single-80GB server deployments wanting strong Apache-2.0 reasoning and tool calling without multi-GPU tensor parallelism. | ~65-80 GB (Single 80GB H100/MI300X or 96GB+ Unified RAM) | Official documentation | Exceeds 16GB+64GB consumer rigs; requires Harmony prompt formatting. |
| [NVIDIA Nemotron 3.5 Super VL (120B-A12B Mamba-2 Hybrid)](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-BF16) | Video/document understanding and long-context multimodal agents on DGX Spark or multi-GPU servers. | NVFP4 on DGX Spark / 4xH100 (BF16) | Official documentation | Datacenter / DGX Spark class footprint; prototype card-free via NVIDIA NIM if you lack server GPUs. |
<!-- swissknife:end -->

## Tier 4 · Research-Leading Open Frontier (`500B–2.8T`)

Cluster-scale open weights tracked for capability ceilings, cloud prototyping (NVIDIA NIM), and architectural trickle-down.

<!-- swissknife:begin table tag=tier-frontier-open -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [DeepSeek-V4.1-Flash-1017 (552B · 4x KV Compression)](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) | Cluster hosting, NVIDIA NIM cloud prototyping, and tracking KV-compression breakthroughs trickling down to smaller local models. | Multi-GPU FP8/INT4 cluster (prototype free via NVIDIA NIM) | Vendor / lab claim | No Jinja chat template (uses encoding.py or Rust deepseek-recipe); far beyond single-workstation memory. |
| [Mistral Large 4 (1T-A52B + Embedded DSpark Drafter)](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) | Cluster/512GB-Ultra deployments and tracking embedded DSpark speculative decoding for future smaller Mistral releases. | 8x GPU NVFP4 or 512GB Mac Ultra (Q2_K) | Vendor / lab claim | Reasoning cannot be disabled (defaults to high); custom license restricts commercial Model-as-a-Service hosting. |
| [Moonshot Kimi-K3 (2.8T-A104B · First Open 3T-Class)](https://huggingface.co/moonshotai/Kimi-K3) | Research reference for frontier architectures (AttnRes already trickled down into Inkling 2 Mini) and multi-node deployments. | Multi-node cluster (native MXFP4/MXFP8) | Vendor / lab claim | Research/cluster scale only; tracked for architectural trickle-down. |
<!-- swissknife:end -->

## Special Use Cases (OCR, Expressive Speech, Video & Text Diffusion)

<!-- swissknife:begin table tag=tier-special-model -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Google DiffusionGemma 26B-A4B (Block-Diffusion LLM)](https://huggingface.co/google/diffusiongemma-26B-A4B-it) | 24GB+ GPUs researching non-autoregressive parallel code/layout generation and fast canvas infilling. | ~18 GB quantized (24GB+ VRAM recommended) | Official documentation | Requires diffusion-aware sampling (entropy-bounded denoising) and works best on well-structured tasks rather than open-ended prose. |
| [DeepSeek-OCR-2 (3B Visual Causal Flow)](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2) | Local private PDF/scan-to-Markdown ingestion into Obsidian knowledge vaults on any 6GB-16GB GPU or Mac. | ~2-6 GB (GGUF / vLLM) | Primary evaluation | Specialized for document layout and OCR rather than general multi-turn chat. |
| [Fish Audio Drama 3 (35B-A3B Multi-Speaker TTS)](https://huggingface.co/fishaudio/drama-3) | Studio-grade local multi-speaker narration and expressive TTS on 32GB-80GB GPUs (or Hybrid RAM). | 32-80 GB GPU (SGLang-Omni / vLLM-Omni) | Official documentation | Too heavy for a 16GB GPU alongside an LLM; use Phonon 31M for zero-GPU/laptop speech. |
| [Lightricks LTX-2.5 (22B Distilled Video + Synchronized Audio)](https://huggingface.co/Lightricks/LTX-2.5) | Local video generation with synchronized audio on 8GB-24GB NVIDIA GPUs. | 5.9-8.1 GiB (WanGP) / 16-24 GiB (ComfyUI) | Official documentation | Gated Hugging Face license acceptance required; use Wan 2.2 when strict Apache-2.0 licensing is mandatory. |
<!-- swissknife:end -->

---

**Track fast-moving releases:** [Model News & Development Radar (21-Day Watch List)](../research/watch-list.md) · [Harness Adapters Research](../research/harness-adapters.md) · [Retired Models](retired.md)
