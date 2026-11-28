---
title: "Apple Silicon Mac"
section: worlds
world: mac
summary: "Running a silent ~15W always-on AI control plane with Apple MLX unified-memory inference, native sandboxes, and honest media limits."
order: 2
---

[Home](../README.md) / Compute Worlds / Apple Silicon Mac

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Apple Silicon Mac

Apple Silicon Macs (Mac mini, MacBook Pro, Mac Studio) occupy a unique sweet spot: **unified memory** eliminates the PCIe bottleneck between CPU and GPU, and a Mac mini idles near **~15W**—making it the ideal quiet, always-on **control plane** for `Pi Durable`, Telegram/Tailscale mobile bridges, and Apple/Xcode builds.

## What Apple Silicon Excels At

- **Unified-Memory Local LLMs via `Apple MLX`:** Official WWDC26 benchmarks show `MLX` outperforming `llama.cpp` by **46% to 3×** on Apple GPUs, with 4-bit `Qwen3.8-27B` super-adapter merges reaching ~65 tok/s on 32GB+ Macs.
- **Native Sandboxing Without Docker:** Run untrusted code in [`gondolin`](https://github.com/earendil-works/gondolin) (`libkrun` Linux micro-VMs directly on Apple Silicon) or wrap native `xcodebuild`/`swift` sessions in [`nono`](https://github.com/nolabs-ai/nono) (macOS Seatbelt).
- **24/7 Quiet Operations:** Run `Pi Durable` + `pi-mobile` + `tailscale serve` under `launchd` without a noisy gaming PC humming overnight.

> [!WARNING]
> **Honest Platform Boundary — Avoid Heavy Local Video on Apple MPS:** ComfyUI's own documentation explicitly advises Mac users *against* running heavy modern video models (`MiniMax H3`, `LTX-2.x`) locally on Apple GPUs, and FP8 weights crash macOS MPS (`Float8_e4m3fn` unsupported). Use your Mac as the silent agent controller and send heavy image/video renders over Tailscale to a discrete NVIDIA PC or Comfy Cloud—see [The Personal AI Fabric](personal-ai-fabric.md).

---

## Flagship Mac Launch Recipe (`mlx_lm.server`)

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

## Verified Apple Silicon Stack

<!-- swissknife:begin table world=mac -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | Generating structured, cited background reports over mixed web and local documents. | Apache-2.0 | Official documentation | Audit every cited claim, date, and quantitative metric against primary sources before publishing. |
| [DeerFlow 2.0](https://github.com/bytedance/deer-flow) | Multi-step deep research reports when you want container-isolated execution. | MIT | Official documentation | Requires Docker and careful prompt/token budgeting to avoid runaway web fetches. |
| [Tailscale Serve (Loopback-to-Tailnet HTTPS Mesh)](https://tailscale.com/kb/1312/serve) | Developer standard for connecting Mac mini, NVIDIA GPU PC, and Android/iOS phones without opening router ports. | Encrypted Private Mesh (Dev Standard) | Official documentation | Automatic Let's Encrypt HTTPS certificates log machine.<tailnet>.ts.net hostnames in public CT logs; use neutral box names (e.g., box-a). |
| [LM Link (Tailscale tsnet Zero-VPN GPU Sharing)](https://lmstudio.ai/docs/lmlink) | Newcomers and students wanting to borrow their home desktop GPU from a thin laptop without configuring Tailscale ACLs. | Zero-Config Userspace GPU Bridge | Official documentation | Free during Preview; paid tiers are planned at General Availability (use Tailscale Serve for permanent open control). |
| [pi-mobile (Multi-Box Tailscale HTTPS & Voice Mode)](https://pi.dev/packages/pi-mobile) | Live hands-free HITL steering across a Mac mini, GPU PC, and cloud VM with spoken behavioral summaries and verbal confirmation. | Live Multi-Box Steering & Voice HITL | Official documentation | A paired phone equals shell access on your home machine; keep behind Tailscale ACLs and neutral hostnames. |
| [ayagmar/pi-mobile (Native Android Compose Client)](https://github.com/ayagmar/pi-mobile) | Android developers wanting a dedicated native client with full /tree session branching on macOS or Linux hosts. | Native Android /tree Steering | Official documentation | Requires Tailscale active on both host and Android device plus the Node RPC bridge daemon. |
| [smixs/pi-durable-telegram (Durable Async Telegram Bot)](https://github.com/smixs/pi-durable-telegram) | Zero-extra-app async HITL communication, multimodal mobile capture, and crash-resumable remote jobs. | Async Messaging HITL (Zero Open Ports) | Official documentation | One-command installer configures a Linux systemd user service; run manually or via launchd on macOS, and never run two pollers on one bot token. |
| [dzianisv/opencode-mobile (Android HITL Client)](https://github.com/dzianisv/opencode-mobile) | Mobile approval and monitoring for OpenCode sessions without switching harnesses. | OpenCode Mobile Approvals | Official documentation | Always configure OPENCODE_SERVER_PASSWORD and route over Tailscale rather than unencrypted LAN. |
| [ntfy (One-Way HOOTL Awareness Pings)](https://github.com/binwiederhier/ntfy) | Notifying your phone the moment an unattended build, ComfyUI render, or nightly audit completes or stalls. | One-Way HOOTL Finish/Stall Pings | Official documentation | One-way notification channel; pair with Telegram or pi-mobile when you need interactive multi-turn steering. |
| [Google Antigravity ($0 Individual Tier)](https://antigravity.google/) | Fastest 5-minute guided entry into agentic coding for newcomers and students on any laptop. | $0/mo Individual: unlimited Tab & Command + weekly Work-Done agent quota | Official documentation | Free agent quota resets weekly with no rollover; managed Google Workspace or .edu accounts may hit entitlement walls (use a personal Google account). |
| [OpenCode CLI & Desktop](https://github.com/anomalyco/opencode) | Default local coding harness for newcomers and teams wanting safe out-of-the-box permission prompts. | Mature Newcomer & Team CLI | Primary evaluation | Place baseURL strictly inside options, name the file opencode.json (no leading dot), and never name your custom provider 'openai'. |
| [Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi) | Flagship developer anchor: run naked in 5 minutes, or optionally rice across 6 modular rungs (LoRA, sandbox, smart MCP, durability, mobile HITL, ComfyUI). | Flagship Mod-Able Developer Kernel | Primary evaluation | Intentionally omits built-in per-tool approval prompts; pair with gondolin, nono, or safeagents before autonomous runs. |
| [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness) | Experimenting with custom loop architectures, Creator Mode live UI plugins, or web/desktop sessions. | Swappable-Loop Plugin Platform | Official documentation | Rapidly iterating developer preview; pin plugin peer versions against breaking interface changes. |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Always-on background ops daemons and scheduled digests where you want messaging built in from day one. | Self-Improving Persistent Daemon | Official documentation | Foreground sessions do not auto-compact aggressively like Pi by default (though idle gateway chats now background-compact in v0.23.5); cap context lengths on massive repositories. |
| [llama.cpp (Mainline GGUF Server & Router)](https://github.com/ggml-org/llama.cpp) | Primary local serving engine on NVIDIA workstations and built-in /llama backend for Pi. | MIT | Official documentation | --sleep-idle-seconds leaves ~600 MiB of dormant CUDA context VRAM attached per model (llama.cpp#19379); explicitly Unload via Pi /llama before heavy ComfyUI renders. |
| [Apple MLX (mlx-lm)](https://github.com/ml-explore/mlx-lm) | Primary local LLM serving engine on Apple Silicon Macs (Mac mini, MacBook Pro, Mac Studio). | MIT | Primary evaluation | Prompt prefill lags dedicated NVIDIA Tensor Cores; 32GB+ unified memory is recommended for 27B coding sessions. |
| [Unsloth Runtime & Studio](https://github.com/unslothai/unsloth) | Serving Dynamic v3.1 GGUFs, local Laya decision endpoints, or running local LoRA fine-tunes. | Apache-2.0 | Official documentation | Keep Studio updated alongside mainline llama.cpp when adopting newly released quantization formats. |
| [Comfy-Org Official comfy-mcp (Local & Cloud)](https://github.com/Comfy-Org/comfy-mcp) | Default agent-to-ComfyUI bridge for Pi, OpenCode, and Antigravity across local, Tailscale, or Comfy Cloud backends. | MIT | Official documentation | Local launch/restart requires comfy-cli >= 1.14.0 (>= 1.16.0 for job watching), and v0.11.0 skips local launch/restart whenever COMFYUI_URL is set for remote Tailscale hosts. |
| [artokun/comfyui-mcp (Power-User Control Plane)](https://github.com/artokun/comfyui-mcp) | Power users wanting automated workflow debugging, Mermaid graph conversion, and active VRAM management on 16GB rigs. | MIT | Field observation | Community-maintained; verify compatibility alongside Comfy-Org's first-party comfy-mcp updates. |
| [HeyGen Hyperframes](https://github.com/heygen-com/hyperframes) | Code-driven product demos and technical videos where diffusion flicker is undesirable. | MIT | Official documentation | Designed for structured UI/data motion graphics rather than photorealistic live-action video. |
| [Gradium Phonon 31M WebGPU TTS](https://github.com/blixt/phonon) | Instant zero-install local speech synthesis for students, Mac users, and browser workflows. | 64.5 MB (Browser WebGPU) | Official documentation | Compact English voice model; heavier multilingual dramatic acting requires larger server-side TTS models. |
| [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) | Verifying web applications, forms, and visual regressions directly from Pi, OpenCode, or Antigravity. | Apache-2.0 | Official documentation | Accessibility snapshots cannot inspect inside closed Shadow DOM. |
| [Upstash Context7 (ctx7 & @upstash/context7-pi)](https://github.com/upstash/context7) | Working with fast-moving web, Python, or mobile SDKs. | MIT | Primary evaluation | Pin local Context7 servers to >= 2.1.3 (CVE-2026-75130) and explicitly instruct agents in AGENTS.md to call it. |
| [Sentry MobileBuildMCP](https://github.com/getsentry/MobileBuildMCP) | Native Apple Swift/iOS/macOS development on Apple Silicon Macs. | MIT | Official documentation | Stops at Apple builds and simulators; physical USB Android/iOS UI testing requires separate device tooling. |
| [obra/superpowers (15-Skill Engineering Pack)](https://github.com/obra/superpowers) | Eliminating agent drift during multi-hour autonomous coding sessions across Pi, OpenCode, Antigravity, and Hermes. | MIT | Field observation | On Hermes Agent, use the Hermes-native tool mapping port rather than raw Claude Code tool names. |
| [nicobailon/pi-mcp-adapter (Lazy & Semantic MCP)](https://github.com/nicobailon/pi-mcp-adapter) | Rung 3 of the Pi Ricing Journey once you attach more than 3-4 MCP servers and want zero context bloat. | MIT | Primary evaluation | Automatically replaces Pi's built-in MCP handler upon installation. |
| [Obsidian Official Agent Skills (1.2.3 + defuddle + obsidian-headless)](https://github.com/obsidianmd/obsidian-skills) | Building a human-readable, Git/Obsidian-friendly personal knowledge vault that both you and your agents maintain. | MIT | Official documentation | Treat all web pages clipped through defuddle strictly as untrusted data, never as executable agent instructions. |
| [tobi/qmd (Local BM25 + Vector Markdown Search & MCP)](https://github.com/tobi/qmd) | Searching large local Obsidian/Git knowledge vaults privately with zero cloud vector databases. | MIT | Official documentation | Keep qmd vector index files machine-local; exclude them from Git/Syncthing/Obsidian Sync to avoid corruption. |
| [pi-obsidian-memory (KV-Cache-Stable Vault Memory for Pi)](https://github.com/the-matt-moo/pi-obsidian-memory) | Giving Pi persistent cross-session memory without invalidating local llama.cpp/MLX KV prefix caches every turn. | MIT | Field observation | Keep ambient memory as a session-stable snapshot (refreshing only on deliberate writes) so local KV prefix caches do not thrash. |
| [Qwen3.8-27B (Dense Vision + Text)](https://huggingface.co/Qwen/Qwen3.8-27B) | Daily-driver local coding, strict instruction following, and single-backbone multi-LoRA serving. | 14.5 GB (IQ4_XS, Zone 1 16GB VRAM) / ~16 GB (Mac MLX 4-bit) | Primary evaluation | On 16GB GPUs, keep quantization at IQ4_XS with Q8 KV cache so weights never spill over PCIe. |
| [Qwen3-Coder-Next (80B-A3B Sparse MoE)](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) | Deeper multi-file repository reasoning on 16GB GPU + 64GB RAM workstations or 64GB+ Macs. | 49 GB (UD-Q4_K_XL, Zone 2 16GB VRAM + 64GB RAM) | Official documentation | Keep -ngl 99 so Attention and KV cache stay in GPU VRAM; offload cold experts only via --n-cpu-moe. |
| [Gemma 4 Family (12B Tri-Modal & 26B-A4B Vision)](https://ai.google.dev/gemma) | 8GB-12GB laptops needing local chat/audio, or ultra-fast 16GB vision and general chat. | 8.5 GB (12B) to 14 GB (26B-A4B) | Official documentation | Only E2B, E4B, and 12B process audio; the 26B-A4B MoE checkpoint is Text + Vision only. |
| [NousResearch Hermes 4 (14B / 4.3-36B Neutral)](https://huggingface.co/NousResearch/Hermes-4-14B) | Self-hosted deployments needing predictable operator-controlled behavior rather than abliteration. | 9 GB (14B Q4) / 22 GB (36B Hybrid) | Vendor / lab claim | Always author explicit safety policies in your system prompt if exposing the endpoint beyond solo local use. |
| [Inkling 2 Mini (26.4B Looped Transformer MoE)](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) | Testing high-efficiency looped coding architectures inside 16GB-18GB memory budgets. | 13-18 GB (UD-Q3/Q4) | Vendor / lab claim | Published 79.2% SWE-bench Verified and 48.2% DeepSWE v1.1 figures are lab-reported; trails Qwen3.8-27B on strict chat. |
| [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya) | Fast zero-output-token tool-safety gating, routing, and memory relevance checks without using GPU VRAM. | 678-846 MB (CPU / NPU / WebGPU) | Official documentation | Threshold decisions on calibrated probabilities rather than raw confidence scores; optional vegaml-learn add-on is non-commercial. |
| [Qwen3.8-27B Pi Specialist LoRA (~319 MB)](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted-GGUF) | Rung 1 of the Pi Ricing Journey when running Pi with thinking mode OFF on local Qwen3.8-27B. | +319 MB LoRA on frozen Qwen3.8-27B | Primary evaluation | HF BF16 vLLM evals jumped 39.2% -> 64.7% SWE-Pro and 39% -> 55% TB2.1, but GGUF quants have not been formally re-evaluated in llama.cpp (Q8_0 stays closer to BF16 than Q4). |
| [Qwen3.8-27B Rank-96 Super-Adapter (HF Harness Hub)](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter) | Serving multiple harnesses from one 15 GB base model, or running with thinking mode enabled (xhigh). | +912 MiB LoRA (+304-319 MiB for single-harness specialist) | Primary evaluation | When running a single harness with thinking off, prefer its specialist LoRA (e.g., pi 64.0% vs 46.0% SWE-Pro hard-51). |
| [Qwen3.8-27B 26MB Uncensored LoRA (Rank-3)](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated) | Authorized security testing or unfiltered local experimentation without duplicating 15 GB of base weights. | +26 MB LoRA on frozen Qwen3.8-27B | Field observation | Abliterated adapters cannot refuse destructive tool actions; always isolate behind safeagents and Laya 0.5. |
| [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents) | Auditing autonomous coding harnesses and unfiltered local LoRAs at the tool-call layer. | Apache-2.0 | Primary evaluation | Audits API tool calls rather than isolating local OS binaries; pair with gondolin or nono for filesystem isolation. |
| [earendil-works/gondolin (libkrun Micro-VM + Secret Proxy)](https://github.com/earendil-works/gondolin) | Rung 2 of the Pi Ricing Journey when executing untrusted code or defending against .env secret exfiltration. | ~200 MB Alpine guest image (zero Docker required on Mac) | Official documentation | Cannot run macOS-only host toolchains (xcodebuild/swift); use nono for native macOS builds. |
| [nolabs-ai/nono (macOS Seatbelt & Linux Landlock Sandbox)](https://github.com/nolabs-ai/nono) | Least-privilege local sandboxing when the agent needs native macOS tools (Xcode, Homebrew, local files). | Apache-2.0 | Official documentation | Shares the host kernel; for heavily untrusted code or strict zero-secret isolation, prefer gondolin's micro-VM boundary. |
<!-- swissknife:end -->

---

**Continue reading:** [Discrete GPU PC](gpu-workstation.md) · [The Personal AI Fabric](personal-ai-fabric.md) · [Pi Ricing Workshop](../guides/pi-workshop.md)
