---
title: "Newcomer & Student Onboarding"
section: docs
track: newcomer
summary: "Six essential terms, a 30-second hardware check, and three zero-paralysis first wins ($0 Cloud, Local Coding, or Local Media)."
order: 1
---

[Home](../README.md) / Orientation / Newcomer & Student Onboarding

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Newcomer & Student Onboarding

Welcome. AI tooling moves fast and throws jargon at you from day one. You do not need to learn everything at once—this page gives you the **six concepts** that actually matter here, checks what your computer can run, and walks you through **one clean first win**.

---

## 1. Six Terms You Actually Need

1. **Cloud API vs. Local Model:** A *cloud API* sends your prompt to remote servers (zero hardware needed, fast start). A *local model* downloads the model file ("weights") onto your own computer so everything stays private and offline.
2. **Parameters, Quantization (`Q4`/`IQ4`), & VRAM:** A model's size is measured in billions of parameters (for example, `27B`). *Quantization* compresses those weights so a 27B model shrinks to ~14.5 GB. **GPU VRAM** (or Apple Silicon Unified Memory) is the fast memory that holds the model—if it fits inside VRAM, it runs fast; if it spills out, it slows down sharply.
3. **Tokens & Context Window:** Models read text in chunks called *tokens* (~3–4 characters each). The *context window* is the model's working memory. Autonomous coding tools send far more tokens per turn than simple chat.
4. **Inference Runtime:** The engine (`llama.cpp` or Apple `MLX`) that loads a model file onto your GPU or Mac and serves it locally on `http://127.0.0.1:8080`.
5. **Agent Harness:** The control loop (`Antigravity`, `OpenCode`, or `Pi`) that connects a model to your files and terminal so it can read code, suggest edits, and run commands with your approval.
6. **Skills & MCP:** *Skills* (`SKILL.md`) are small instruction files teaching an agent good habits; *MCP* (Model Context Protocol) lets an agent plug into external tools like live documentation or a browser.

Want a visual map of how these layers connect? Read [How a Modern AI Stack Fits Together](mental-model.md).

---

## 2. The 30-Second Hardware Check

Before installing local models, match your actual machine so you do not hit an out-of-memory wall:

| Your Machine | Best Starting Path |
| :--- | :--- |
| **Any laptop (8GB–16GB RAM, no dedicated GPU, or Chromebook)** | Start with **Path A ($0 Cloud)**. If you want offline local chat/audio on an 8GB–12GB laptop, use [`Gemma 4 12B`](../reference/models-and-harnesses.md) (~8.5 GB) instead of a 27B model. |
| **PC with 16GB NVIDIA GPU (or Apple Silicon Mac with 32GB+ memory)** | Try **Path A ($0 Cloud)** first if you want a 5-minute win, or jump straight to **Path B (Private Local Coding)**. |
| **PC with 6GB–16GB NVIDIA GPU wanting Images, Video, or Audio** | Jump to **Path C (Turnkey Local Media Studio)**. |

---

## 3. Choose One First Path

### Path A · Learn & Build in 5 Minutes ($0 Cloud, No Credit Card)

Start in the browser with **Google AI Studio** to experiment with prompts, PDFs, images, and thinking levels, then install **Google Antigravity** ($0 Individual tier) for your first guided agentic coding session.

<!-- swissknife:begin slot id=cloud-flagship -->
**Active Anchor — [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/)**

Google's primary card-free developer API gateway serving Gemini 4 Hydrogen with a 1,048,576-token unified context window, multimodal inputs, and four thinking levels alongside Gemini Decision 1.

- **When to use:** Default zero-card cloud gateway for multi-step coding agents, full-repository ingestion, and multimodal reasoning.
- **Free quota:** No card: Free Tier (gemini-4-hydrogen 1M unified ctx, implicit caching) + Decision 1 (200 RPM / 10K RPD)
- **Upstream docs:** [Official setup & reference](https://ai.google.dev/gemini-api/docs)
- **Evidence:** Official documentation · verified 2026-11-28
- **Why this pick:** [Anchor Zero-Card Cloud on Google AI Studio (Gemini 4 Hydrogen) & Antigravity](why-this-stack.md#adr-why-google-cloud)
- **Limitation:** Free Tier prompts are used to improve products outside EU/UK/CH; never paste secrets or proprietary source code.
- **Limitation:** Search Grounding, Maps Grounding, Batch API, and explicit context caching are paid-tier only on Gemini 4 Hydrogen.
- **Limitation:** Passing thinking_level=minimal or out-of-range temperature/top_p/top_k returns HTTP 400 on gemini-4-hydrogen.
<!-- swissknife:end -->

<!-- swissknife:begin slot id=newcomer-cloud-ide -->
**Active Anchor — [Google Antigravity ($0 Individual Tier)](https://antigravity.google/)**

Zero-install agentic coding suite spanning native desktop App, IDE extensions, and agy CLI with unlimited Tab/Command completions and weekly free agent quota.

- **When to use:** Fastest 5-minute guided entry into agentic coding for newcomers and students on any laptop.
- **Free quota:** $0/mo Individual: unlimited Tab & Command + weekly Work-Done agent quota
- **Evidence:** Official documentation · verified 2026-11-28
- **Why this pick:** [Anchor Zero-Card Cloud on Google AI Studio (Gemini 4 Hydrogen) & Antigravity](why-this-stack.md#adr-why-google-cloud)
- **Limitation:** Free agent quota resets weekly with no rollover; managed Google Workspace or .edu accounts may hit entitlement walls (use a personal Google account).
- **Limitation:** No official first-party mobile companion app as of Nov 2026.
<!-- swissknife:end -->

**Quick starter checklist:**
1. Sign into Google AI Studio with a **personal Google account** (school/work Google Workspace accounts sometimes restrict free AI entitlements).
2. Test a real prompt (drop in a textbook PDF or small code file) using `gemini-4-hydrogen`.
3. Install Antigravity, select your focus area during onboarding, and try one small task inside a scratch folder.

---

### Path B · Your First Private Local Coding Agent

Once you have a **16GB GPU** or **32GB+ Apple Silicon Mac**, pair one mature open-weight model (`Qwen3.8-27B`) with `llama.cpp` (or `MLX` on Mac) and **OpenCode**—chosen specifically for beginners because it asks your permission before editing files or running shell commands.

<!-- swissknife:begin slot id=local-mature-coder -->
**Active Anchor — [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B)**

Apache-2.0 27B dense model serving as the primary 16GB VRAM and Apple Silicon coding backbone, hosting both Hugging Face's RL harness adapters and compact uncensored LoRAs on one frozen file.

- **When to use:** Daily-driver local coding, strict instruction following, and single-backbone multi-LoRA serving.
- **Footprint:** 14.5 GB (IQ4_XS, Zone 1 16GB VRAM) / ~16 GB (Mac MLX 4-bit)
- **Evidence:** Primary evaluation · verified 2026-11-28
- **Compatible adapters:** [Qwen3.8-27B Pi Specialist LoRA (~319 MB)](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted-GGUF), [Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter), [Qwen3.8-27B 26MB Uncensored LoRA (Rank-3)](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated)
- **Experimental challenger:** [Inkling 2 Mini (26.4B Looped Transformer MoE)](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) — Testing high-efficiency looped coding architectures inside 16GB-18GB memory budgets.
- **Why this pick:** [Standardize Local Coding on Frozen Qwen3.8-27B + Hot-Swappable LoRAs](why-this-stack.md#adr-why-qwen38-27b)
- **Limitation:** On 16GB GPUs, keep quantization at IQ4_XS with Q8 KV cache so weights never spill over PCIe.
- **Limitation:** Avoid Ollama's /v1/chat/completions endpoint with qwen3.8:27b due to reported hangs; use llama-server or mlx_lm.server.
- **Limitation:** Not suited for 8GB-12GB student laptops; use $0 Cloud or Gemma 4 12B on smaller hardware.
<!-- swissknife:end -->

<!-- swissknife:begin slot id=newcomer-local-harness -->
**Active Anchor — [OpenCode CLI & Desktop](https://github.com/anomalyco/opencode)**

Mature, vendor-agnostic coding harness with 1-line install, built-in per-action approval prompts, offline share-disabled mode, and an official HF Qwen3.8-27B adapter.

- **When to use:** Default local coding harness for newcomers and teams wanting safe out-of-the-box permission prompts.
- **Upstream docs:** [Official setup & reference](https://opencode.ai/docs/providers)
- **Evidence:** Primary evaluation · verified 2026-11-28
- **Compatible adapters:** [Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)
- **Why this pick:** [Pair OpenCode (Newcomer Anchor) with Pi (Flagship Developer Kernel)](why-this-stack.md#adr-why-pi-and-opencode)
- **Limitation:** Place baseURL strictly inside options, name the file opencode.json (no leading dot), and never name your custom provider 'openai'.
- **Limitation:** opencode serve starts without a password by default; set OPENCODE_SERVER_PASSWORD before exposing beyond 127.0.0.1.
<!-- swissknife:end -->

**Step 1 — Start your local model server (loopback only):**

<!-- swissknife:begin recipe id=qwen3.8-27b -->
<details>
<summary>Launch command — Qwen3.8-27B (Dense Vision + Text) (CUDA / llama.cpp / CLI)</summary>

```bash
llama-server -m Qwen3.8-27B-IQ4_XS.gguf -ngl 99 -fa on -c 32768 -ctk q8_0 -ctv q8_0 --host 127.0.0.1 --port 8080
```

</details>

<details>
<summary>Launch command — Qwen3.8-27B (Dense Vision + Text) (Apple Silicon / MLX)</summary>

```bash
mlx_lm.server --model netprojects/Qwen3.8-27B-super-adapter-MLX-6bit --host 127.0.0.1 --port 8080
```

</details>

Built-in upstream check: `curl -s http://127.0.0.1:8080/health`
<!-- swissknife:end -->

**Step 2 — Connect OpenCode cleanly (avoiding the 4 beginner config traps):**

<!-- swissknife:begin recipe id=opencode -->
<details>
<summary>Working opencode.json for local llama-server (avoids the 4 beginner traps)</summary>

```json
{
  "$schema": "https://opencode.ai/config.json",
  "share": "disabled",
  "provider": {
    "local": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Local llama.cpp",
      "options": {
        "baseURL": "http://127.0.0.1:8080/v1",
        "apiKey": "sk-local"
      },
      "models": {
        "qwen3.8-27b": {
          "name": "Qwen3.8-27B Local",
          "limit": { "context": 32768, "output": 8192 }
        }
      }
    }
  },
  "model": "local/qwen3.8-27b"
}
```

</details>

Built-in upstream check: `opencode debug config && opencode models local`
<!-- swissknife:end -->

*(On an 8GB–12GB laptop? Skip `Qwen3.8-27B` for now—use Path A or run `Gemma 4 12B` locally without fighting memory limits.)*

---

### Path C · Your First Local Media Studio (Image, Video & Audio)

Most beginners burn out on local media by juggling four conflicting Python installs. Start with **one guided app** on NVIDIA GPUs (`WanGP`, starting at 6 GB VRAM), or run instant browser speech synthesis (`Phonon 31M`) with zero GPU setup.

<!-- swissknife:begin slot id=turnkey-media -->
**Active Anchor — [WanGP v20.21 (One-Stop Low-VRAM Media Studio)](https://github.com/deepbeepmeep/WanGP)**

Guided-installer local studio covering Video (Wan 2.2, H3), Images (Qwen-Image-2.1, FLUX.2), Music, Speech, and 3D inside one browser UI starting at 6 GB VRAM, plus native MCP.

- **When to use:** Default turnkey local media setup for newcomers and 6GB-16GB NVIDIA workstations (5.9-14.3 GiB video VRAM vs ComfyUI's 22.7-23.5 GiB).
- **Footprint:** 6-15 GB NVIDIA VRAM (MMGP v4 + Extreme Chunker)
- **Evidence:** Primary evaluation · verified 2026-11-28
- **Why this pick:** [Split Local Media Into Turnkey Low-VRAM (WanGP) vs. Programmable Agent Engine (ComfyUI + MCP)](why-this-stack.md#adr-why-wangp-and-comfyui)
- **Limitation:** Install WGPKernels 1.5.0 and SageGP 1.0.2 (PyTorch 2.10; Triton 3.6+ required for RTX 50-series adaptive Sage2/3).
- **Limitation:** Heavy local video synthesis targets NVIDIA GPUs; Mac users should route heavy video to a remote GPU PC or Comfy Cloud.
- **Limitation:** GitHub /releases/latest tracks WanGP Manager (manager-v0.1.21) while core studio wgp.py ships on main at v20.21.
<!-- swissknife:end -->

- **No NVIDIA GPU (or on a Mac/student laptop)?** Try [Gradium Phonon 31M](https://github.com/blixt/phonon) right in your browser (64.5 MB WebGPU English speech), or read [Local Media Studio](../guides/media-studio.md) for code-driven videos (`Hyperframes`) and remote rendering options.

---

## 4. Three Safety Habits From Day One

1. **Keep secrets off free cloud tiers:** Free cloud APIs may log prompts outside the EU/UK/CH—never paste `.env` keys, passwords, or private coursework/company data.
2. **Keep approval prompts enabled:** Always review file edits and terminal commands while learning (`OpenCode` and `Antigravity` prompt you by default).
3. **Treat web pages and third-party skills as untrusted data:** Read [Security & Trust Boundaries](security-and-trust.md) before connecting multiple devices.

---

**Where to go next:** [How a Modern AI Stack Fits Together](mental-model.md) · [Why This Stack](why-this-stack.md) · [Seasoned Developer Fast-Track](start-here-developer.md)
