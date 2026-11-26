← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)

# Chapter 07 · Community Field Notes (IRL Builds & Workflows)

> [!IMPORTANT]
> **Verdict:** The biggest real-world gains come from community 12-16GB alt-engines, discipline skill packs (obra/superpowers), two-pass audit loops, and chained indie media pipelines.
> **Read this chapter if:** You want to see what builders are actually shipping IRL right now on consumer GPUs and self-hosted harnesses.

## Tracked Entries (Volatile Feed)

| Project / Model | Verified Signal | Stack & TTL | Caveat / Trickle-Down |
| :--- | :--- | :--- | :--- |
| [**Basalt (0.5.5+) & RustingStrata Alt-Engines**](https://www.reddit.com/r/LocalLLaMA/)<br><sub>`consumer-gpu-hacks` · 🟢 `Fresh`</sub> | 🏆 Basalt hits up to 60 tok/s on 16GB RTX 5060 Ti (NVFP4 + DSpark); RustingStrata hits 31 tok/s on RTX 3060 12GB (3x stock llama.cpp) | RTX 3060 12GB / 5060 Ti 16GB + Inkling 2 Mini<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Fast-moving single-GPU community engines; pin working git commits. |
| [**pecera-engine + Hermes 2-Pass Audit Loop**](https://www.reddit.com/r/LocalLLaMA/)<br><sub>`consumer-gpu-hacks` · 🟢 `Fresh`</sub> | 🏆 Fused CUDA glue-op kernels hit 76-80 tok/s; 3,000-tok thinking cap + 5 self-check skills + 2nd audit session scored 47/89 (52.8%) on TB2.0 | RTX 4070 Ti 12GB + Inkling 2 Mini + Hermes<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Reusable IRL takeaway: capping thinking tokens + forcing a fresh 2nd audit session cures small-model debug loops. |
| [**obra/superpowers (+ Hermes Port)**](https://github.com/obra/superpowers)<br><sub>`harness-extensions` · 🟢 `Fresh`</sub> | 🏆 15 discipline skills enforcing Brainstorm -> Spec -> Red/Green TDD -> Fresh Subagent -> Verification for 2+ hour autonomous runs | Pi · Antigravity · Hermes · OpenCode · Claude Code<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ On Hermes, use the Hermes-native port (hermes-tools.md) rather than raw Claude Code tool names. |
| [**pi-subagents-community**](https://pi.dev/)<br><sub>`harness-extensions` · 🟢 `Fresh`</sub> | 🏆 Adds parallel sub-agents, fleet widget, mid-run steering, and JS orchestration without bloating Pi's minimal core | Pi v1.0+ (npm:pi-subagents-community)<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Keep concurrency bounded when pointing parallel sub-agents at a single local 16GB GPU. |
| [**wanbinyu-harness-toolbox (dsh)**](https://github.com/deepseek-ai/deepseek-harness)<br><sub>`harness-extensions` · 🟢 `Fresh`</sub> | 🏆 Bilingual Cordis plugin catalog with SHA-256 verified assets, Windows updater preserving .dsh data, and LAN Android client | DeepSeek Harness (dsh)<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Independent community repo; verify peer compatibility after dsh alpha releases. |
| [**Hermes SRE, Obsidian LLM Wiki & Digest Pipelines**](https://github.com/NousResearch/hermes-agent)<br><sub>`production-ops` · 🟢 `Fresh`</sub> | 🏆 IRL teams run Incident Commander SRE triage, PR review (~30% faster cycles), Obsidian+Defuddle wikis, and 200-500 source cron digests | Hermes Agent · OpenClaw · Pi Durable · Obsidian<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Never jump to 100% autonomy on day 1; graduate from agent-drafts/human-approves to weekly 10-20% spot audits. |
| [**WanGP Showrunner & Hy-Nomas + LTX-2.5 + CADMAGEDDON**](https://github.com/deepbeepmeep/WanGP)<br><sub>`indie-media` · 🟢 `Fresh`</sub> | 🏆 Recurring location Sets + Deep Review continuity audits for indie films; Hy-Nomas+LTX-2.5 worlds; CADMAGEDDON local mesh-to-CAD | WanGP v20.12 · Hy-Nomas · LTX-2.5 · CADMAGEDDON<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Hy-Nomas uses NVIDIA PixelUMM (non-commercial previs only); community Showrunner forks track specific WanGP commits. |

---

← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)
