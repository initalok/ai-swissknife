[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; [🖥️ Local](../book/local.md) &nbsp;·&nbsp; [⚙️ Harnesses & RL](../book/harnesses-and-rl.md) &nbsp;·&nbsp; [📘 Playbooks](../book/playbooks.md) &nbsp;·&nbsp; [🧭 Spokes](../book/spokes.md) &nbsp;·&nbsp; **📡 Radar** &nbsp;·&nbsp; [🪦 Graveyard](../book/graveyard.md)

# 📡 Capped 21-Day Radar (Frontier Watch & Community IRL)

> [!NOTE]
> Hard-capped by CI (`<=5` Frontier, `<=5` Community, **21-day TTL**). Adding a new entry requires consciously retiring an older one. Frontier items are strictly `Monitor-Only` and excluded from `llms.txt`.

## 🔭 Frontier Watch (Monitor-Only Apex Ceiling)

- [**Claude Fable 5.2 & Mythos 5.2**](https://www.anthropic.com/) · 🔭 `Monitor-Only` (`21d` left) — 1M ctx / 128K out; 10-12 hr autonomous audits, 89.3% OSWorld 2.1, 69.9% FrontierSWE v2, & 1,000-agent Lean proofs.
  - ⚠️ Paid API / Enterprise only; monitor-only ceiling tracker.
- [**GPT-6.2 Astra & GPT-6.2 Sol**](https://openai.com/) · 🔭 `Monitor-Only` (`21d` left) — API caching breakthrough: adjust reasoning effort & toggle tools mid-conversation without breaking prompt cache.
  - ⚠️ Track cache-preserving effort/tool switching as a future local vLLM/llama.cpp harness pattern.
- [**Gemini 4 Carbon & 4 Argon**](https://deepmind.google/) · 🔭 `Monitor-Only` (`21d` left) — 53.9% AutomationBench autonomous workflow ceiling powering Spark Task mode; Gemini 4 Hydrogen already trickled down to Free Tier.
  - ⚠️ Pro/Ultra and paid API only.
- [**Qwen4-Max (2.4T)**](https://qwenlm.github.io/) · 🔭 `Monitor-Only` (`21d` left) — 2.4T params, 1M ctx, 262K CoT; Alibaba explicitly confirmed smaller open-weight Qwen4 models are coming next.
  - ⚠️ #1 local watchlist signal to potentially supersede Qwen3.8-27B.
- [**DeepSeek-V4.1-Flash (552B) & Pending V4.1-Pro**](https://www.deepseek.com/) · 🔭 `Monitor-Only` (`21d` left) — Asymmetric Causal Encoder-Decoder (8B active in / 16B out) achieving 1/4 HBM KV cache footprint.
  - ⚠️ Exceeds 16GB+64GB local memory; watch for smaller asymmetric KV-compressed open checkpoints.

## 🛠️ Community IRL Field Log (Consumer Hardware & Extensions)

- [**obra/superpowers (+ Hermes Port)**](https://github.com/obra/superpowers) · 🟢 `Fresh` (`21d` left) — 15 discipline skills enforcing Brainstorm -> Spec -> Red/Green TDD -> Fresh Subagent -> Verification for 2+ hr runs.
  - ⚠️ Use Hermes-native tool mapping when running on Hermes Agent.
- [**disler/durable-pi (Multi-Device Durable Agent Showcase)**](https://github.com/disler/durable-pi) · 🟢 `Fresh` (`21d` left) — Crash-resumable SQLite agent network over Pi with atomic shared state and live tool hot-swapping.
  - ⚠️ First-party @earendil-works/pi-durable also ships inside the main Pi monorepo.
- [**hiteshK03/davinci-resolve-mcp (Free Resolve Internal Bridge)**](https://github.com/hiteshK03/davinci-resolve-mcp) · 🟢 `Fresh` (`21d` left) — Unlocks 155/162 DaVinci Resolve MCP tools even on the Free edition via internal script bridging.
  - ⚠️ External official API remains Studio-only; verify bridge compatibility across Resolve updates.
- [**Tencent-Hunyuan/Hy-Nomas (Interactive Walkable Worlds)**](https://github.com/Tencent-Hunyuan/Hy-Nomas) · 🟢 `Fresh` (`21d` left) — Single-GPU WASD-navigable world generator chained by indie creators with LTX-2.5 for video-conditioned audio.
  - ⚠️ Uses NVIDIA PixelUMM decoder (non-commercial previs/pitch use only).
- [**Gradium Phonon 31M (Browser WebGPU TTS)**](https://github.com/blixt/phonon) · 🟢 `Fresh` (`21d` left) — 64.5 MB Apache-2.0 GGUF hitting 115-130x real-time (4.9ms latency) directly in browser WebGPU at 0 GPU server cost.
  - ⚠️ English-only; larger 5-language Phonon 40M checkpoints are CC BY-NC 4.0.

---

[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; [🖥️ Local](../book/local.md) &nbsp;·&nbsp; [⚙️ Harnesses & RL](../book/harnesses-and-rl.md) &nbsp;·&nbsp; [📘 Playbooks](../book/playbooks.md) &nbsp;·&nbsp; [🧭 Spokes](../book/spokes.md) &nbsp;·&nbsp; **📡 Radar** &nbsp;·&nbsp; [🪦 Graveyard](../book/graveyard.md)
