[Home](README.md) / System Status

# System Status & Upstream Momentum Ledger

Snapshot date: **2026-11-28** · Tracked entries: **57** (57 eligible for `llms.txt`) · Workflow slots: **12** · Active decisions: **10**.

This ledger is maintained automatically by the rolling link and upstream release verifier. Healthy handbook pages stay quiet; release updates, stale links, and flagged decisions collect here.

## Health & Momentum Summary

| Signal | Count | Meaning |
| :--- | :---: | :--- |
| Upstream release updates | 0 | Tracked anchor shipped a newer GitHub release than last reviewed. |
| Decision records to review | 0 | An accepted ADR's anchor degraded, went stale, or had a breaking release. |
| Upstream dependency alerts | 0 | A base model or harness adapted by a LoRA has changed or degraded. |
| Needs re-verification | 0 | Past review window; automatically omitted from `llms.txt`. |
| Approaching review window | 0 | Past 75% of scheduled review interval; still active. |
| Degraded / retirement queue | 0 | Upstream archived or unreachable for 3+ checks. |

## Core Registry Entries

| Entry | Kind | Status | Verified | Window | Upstream Activity / Release |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)](https://aistudio.google.com/) | `gateway` | `fresh` | 2026-11-28 | 21d | Not yet probed |
| [Z.ai BigModel (GLM-4.7-Flash)](https://open.bigmodel.cn/) | `gateway` | `fresh` | 2026-11-28 | 21d | Not yet probed |
| [NVIDIA NIM Developer Catalog](https://docs.api.nvidia.com/nim/docs/introduction) | `gateway` | `fresh` | 2026-11-28 | 21d | Not yet probed |
| [OpenRouter (:free Routes)](https://openrouter.ai/) | `gateway` | `fresh` | 2026-11-28 | 21d | Not yet probed |
| [Groq Cloud LPU](https://console.groq.com/) | `gateway` | `fresh` | 2026-11-28 | 21d | Not yet probed |
| [Cloudflare Workers AI (Clef & Clairic)](https://developers.cloudflare.com/workers-ai/) | `gateway` | `fresh` | 2026-11-28 | 21d | Not yet probed |
| [Pollinations AI](https://pollinations.ai/) | `gateway` | `fresh` | 2026-11-28 | 120d | Not yet probed |
| [Firecrawl](https://www.firecrawl.dev/) | `tool` | `fresh` | 2026-11-28 | 60d | Not yet probed |
| [Jina Reader (r.jina.ai / s.jina.ai)](https://jina.ai/reader/) | `tool` | `fresh` | 2026-11-28 | 120d | Not yet probed |
| [Exa 3.0 Neural Search](https://exa.ai/) | `tool` | `fresh` | 2026-11-28 | 21d | Not yet probed |
| [OpenAlex Academic Graph](https://docs.openalex.org/) | `tool` | `fresh` | 2026-11-28 | 120d | Not yet probed |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | `tool` | `fresh` | 2026-11-28 | 60d | 2026-11-23 |
| [DeerFlow 2.0](https://github.com/bytedance/deer-flow) | `tool` | `fresh` | 2026-11-28 | 60d | 2026-11-28 |
| [Tailscale Serve (Loopback-to-Tailnet HTTPS Mesh)](https://tailscale.com/kb/1312/serve) | `fabric` | `fresh` | 2026-11-28 | 120d | Not yet probed |
| [LM Link (Tailscale tsnet Zero-VPN GPU Sharing)](https://lmstudio.ai/docs/lmlink) | `fabric` | `fresh` | 2026-11-28 | 21d | Not yet probed |
| [pi-mobile (Multi-Box Tailscale HTTPS & Voice Mode)](https://pi.dev/packages/pi-mobile) | `mobile` | `fresh` | 2026-11-28 | 21d | Not yet probed |
| [ayagmar/pi-mobile (Native Android Compose Client)](https://github.com/ayagmar/pi-mobile) | `mobile` | `fresh` | 2026-11-28 | 60d | 2026-10-03 |
| [smixs/pi-durable-telegram (Durable Async Telegram Bot)](https://github.com/smixs/pi-durable-telegram) | `mobile` | `fresh` | 2026-11-28 | 60d | 2026-11-25 |
| [dzianisv/opencode-mobile (Android HITL Client)](https://github.com/dzianisv/opencode-mobile) | `mobile` | `fresh` | 2026-11-28 | 60d | 2026-11-26 |
| [ntfy (One-Way HOOTL Awareness Pings)](https://github.com/binwiederhier/ntfy) | `mobile` | `fresh` | 2026-11-28 | 120d | 2026-11-27 |
| [Google Antigravity ($0 Individual Tier)](https://antigravity.google/) | `harness` | `fresh` | 2026-11-28 | 21d | Not yet probed |
| [OpenCode CLI & Desktop](https://github.com/anomalyco/opencode) | `harness` | `fresh` | 2026-11-28 | 120d | `v2.4.2` |
| [Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi) | `harness` | `fresh` | 2026-11-28 | 120d | `v1.7.0` |
| [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness) | `harness` | `fresh` | 2026-11-28 | 21d | 2026-11-22 |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | `harness` | `fresh` | 2026-11-28 | 60d | `v0.23.5` |
| [llama.cpp (Mainline GGUF Server & Router)](https://github.com/ggml-org/llama.cpp) | `runtime` | `fresh` | 2026-11-28 | 120d | `v1.1.0` |
| [Apple MLX (mlx-lm)](https://github.com/ml-explore/mlx-lm) | `runtime` | `fresh` | 2026-11-28 | 120d | `v0.32.2` |
| [Unsloth Runtime & Studio](https://github.com/unslothai/unsloth) | `runtime` | `fresh` | 2026-11-28 | 60d | 2026-11-28 |
| [WanGP v20.21 (One-Stop Low-VRAM Media Studio)](https://github.com/deepbeepmeep/WanGP) | `runtime` | `fresh` | 2026-11-28 | 21d | `manager-v0.1.21` |
| [ComfyUI (Comfy-Org Programmable Node Graph)](https://github.com/Comfy-Org/ComfyUI) | `runtime` | `fresh` | 2026-11-28 | 60d | `v0.46.0` |
| [Comfy-Org Official comfy-mcp (Local & Cloud)](https://github.com/Comfy-Org/comfy-mcp) | `mcp` | `fresh` | 2026-11-28 | 21d | `v0.11.0` |
| [artokun/comfyui-mcp (Power-User Control Plane)](https://github.com/artokun/comfyui-mcp) | `mcp` | `fresh` | 2026-11-28 | 21d | 2026-11-23 |
| [Wan 2.2 (5B & A14B Apache-2.0 Video)](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | `model` | `fresh` | 2026-11-28 | 120d | 2025-08-07 |
| [Qwen-Image-2.1 (7B DiT Native RGBA)](https://huggingface.co/Qwen/Qwen-Image-2.1) | `model` | `fresh` | 2026-11-28 | 120d | 2026-09-30 |
| [HeyGen Hyperframes](https://github.com/heygen-com/hyperframes) | `tool` | `fresh` | 2026-11-28 | 60d | 2026-11-28 |
| [Gradium Phonon 31M WebGPU TTS](https://github.com/blixt/phonon) | `tool` | `fresh` | 2026-11-28 | 120d | 2026-11-04 |
| [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) | `mcp` | `fresh` | 2026-11-28 | 60d | 2026-11-27 |
| [Upstash Context7 (ctx7 & @upstash/context7-pi)](https://github.com/upstash/context7) | `mcp` | `fresh` | 2026-11-28 | 60d | 2026-11-28 |
| [Sentry MobileBuildMCP](https://github.com/getsentry/MobileBuildMCP) | `mcp` | `fresh` | 2026-11-28 | 60d | 2026-11-19 |
| [obra/superpowers (15-Skill Engineering Pack)](https://github.com/obra/superpowers) | `tool` | `fresh` | 2026-11-28 | 60d | 2026-11-28 |
| [nicobailon/pi-mcp-adapter (Lazy & Semantic MCP)](https://github.com/nicobailon/pi-mcp-adapter) | `mcp` | `fresh` | 2026-11-28 | 60d | 2026-11-21 |
| [Obsidian Official Agent Skills (1.2.3 + defuddle + obsidian-headless)](https://github.com/obsidianmd/obsidian-skills) | `memory` | `fresh` | 2026-11-28 | 60d | `1.2.3` |
| [tobi/qmd (Local BM25 + Vector Markdown Search & MCP)](https://github.com/tobi/qmd) | `memory` | `fresh` | 2026-11-28 | 60d | 2026-11-20 |
| [pi-obsidian-memory (KV-Cache-Stable Vault Memory for Pi)](https://github.com/the-matt-moo/pi-obsidian-memory) | `memory` | `fresh` | 2026-11-28 | 21d | 2026-09-20 |
| [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B) | `model` | `fresh` | 2026-11-28 | 120d | 2026-11-07 |
| [Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) | `model` | `fresh` | 2026-11-28 | 120d | 2026-03-06 |
| [Gemma 4 Family (12B Tri-Modal & 26B-A4B Vision)](https://ai.google.dev/gemma) | `model` | `fresh` | 2026-11-28 | 120d | Not yet probed |
| [NousResearch Hermes 4 (14B / 4.3-36B Neutral)](https://huggingface.co/NousResearch/Hermes-4-14B) | `model` | `fresh` | 2026-11-28 | 120d | 2026-01-09 |
| [Inkling 2 Mini (26.4B Looped Transformer MoE)](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) | `model` | `fresh` | 2026-11-28 | 60d | 2026-11-23 |
| [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya) | `model` | `fresh` | 2026-11-28 | 120d | `v0.5.6` |
| [Qwen3.8-27B Pi Specialist LoRA (~319 MB)](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted-GGUF) | `adapter` | `fresh` | 2026-11-28 | 120d | 2026-11-27 |
| [Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter) | `adapter` | `fresh` | 2026-11-28 | 120d | 2026-11-27 |
| [Qwen3.8-27B 26MB Uncensored LoRA (Rank-3)](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated) | `adapter` | `fresh` | 2026-11-28 | 60d | 2026-08-21 |
| [In-Harness RL Recipe & HF Collection (OpenEnv + Harbor + TRL AsyncGRPO)](https://huggingface.co/collections/harness-hub/qwen38-27b-harness-adapters) | `tool` | `fresh` | 2026-11-28 | 60d | `items:11` |
| [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents) | `tool` | `fresh` | 2026-11-28 | 60d | 2026-11-27 |
| [earendil-works/gondolin (libkrun Micro-VM + Secret Proxy)](https://github.com/earendil-works/gondolin) | `tool` | `fresh` | 2026-11-28 | 21d | 2026-11-27 |
| [nolabs-ai/nono (macOS Seatbelt & Linux Landlock Sandbox)](https://github.com/nolabs-ai/nono) | `tool` | `fresh` | 2026-11-28 | 60d | 2026-11-27 |

## Specialist Tools & Upstream Directories

| Resource | Scope | Status | Verified | Upstream Activity |
| :--- | :--- | :--- | :--- | :--- |
| [LaurieWired GhidraMCP](https://github.com/LaurieWired/GhidraMCP) | `specialist:reverse-engineering` | `fresh` | 2026-11-28 | 2026-10-10 |
| [LLNL OGhidra](https://github.com/LLNL/OGhidra) | `specialist:reverse-engineering` | `fresh` | 2026-11-28 | 2026-11-23 |
| [zhuyansen/awesome-ai-reverse-engineering](https://github.com/zhuyansen/awesome-ai-reverse-engineering) | `specialist:reverse-engineering:upstream` | `fresh` | 2026-11-28 | 2026-11-27 |
| [CoplayDev Unity MCP](https://github.com/CoplayDev/unity-mcp) | `specialist:game-dev-3d` | `fresh` | 2026-11-28 | 2026-11-17 |
| [ahujasid Blender MCP](https://github.com/ahujasid/blender-mcp) | `specialist:game-dev-3d` | `fresh` | 2026-11-28 | 2026-11-26 |
| [Microsoft TRELLIS v1 (MIT 16GB 3D)](https://github.com/microsoft/TRELLIS) | `specialist:game-dev-3d:upstream` | `fresh` | 2026-11-28 | 2026-10-27 |
| [Postiz](https://github.com/gitroomhq/postiz-app) | `specialist:growth-and-social` | `fresh` | 2026-11-28 | 2026-11-27 |
| [blader/humanizer](https://github.com/blader/humanizer) | `specialist:growth-and-social` | `fresh` | 2026-11-28 | 2026-11-19 |
| [ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills) | `specialist:growth-and-social:upstream` | `fresh` | 2026-11-28 | 2026-11-26 |
| [NousResearch Hermes 4 (Neutral Alignment)](https://huggingface.co/NousResearch/Hermes-4-14B) | `specialist:unfiltered-sovereign` | `fresh` | 2026-11-28 | 2026-01-09 |
| [Securelayer7 Qwen3.8-27B 26MB Uncensored LoRA](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated) | `specialist:unfiltered-sovereign` | `fresh` | 2026-11-28 | 2026-08-21 |
| [huihui-ai/Huihui-Qwen3.8-27B-abliterated](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated) | `specialist:unfiltered-sovereign:upstream` | `fresh` | 2026-11-28 | 2026-08-24 |
