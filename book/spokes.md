[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; [🖥️ Local](../book/local.md) &nbsp;·&nbsp; [⚙️ Harnesses & RL](../book/harnesses-and-rl.md) &nbsp;·&nbsp; [📘 Playbooks](../book/playbooks.md) &nbsp;·&nbsp; **🧭 Spokes** &nbsp;·&nbsp; [📡 Radar](../book/radar.md) &nbsp;·&nbsp; [🪦 Graveyard](../book/graveyard.md)

# 🧭 Horizon Spoke Directory (Upstream-Federated)

> [!IMPORTANT]
> Spokes keep `ai-swissknife` multi-horizon without spreading thin: each spoke plugs into your implicit Core, lists **at most 2 canonical entry points** (enforced by CI), and delegates the long tail to a **live-monitored Upstream Hub**.

## 🧭 Game Development & Local 16GB 3D Assets (`game-dev-3d`)
> Plug local sparse coding MoEs into Unity or Blender MCPs, backed by MIT-licensed 16GB TRELLIS v1 for rapid 3D blockouts.

- **Implicit Core Plug-In:** Models `qwen3-coder-next`, `inkling-2-mini` · Auto-Adapters None · Guards `laya-05`, `safeagents`
- **Canonical Entry Points (Max 2):**
  - [**CoplayDev Unity MCP (16.2K stars, MIT)**](https://github.com/CoplayDev/unity-mcp) · 🟢 `Fresh`
  - [**ahujasid Blender MCP (34.9K stars, MIT)**](https://github.com/ahujasid/blender-mcp) · 🟢 `Fresh`
- **Upstream Hub (Long Tail):** [**Microsoft TRELLIS v1 (MIT 16GB 3D Asset Generator)**](https://github.com/microsoft/TRELLIS) · 🟢 `Fresh`
- ⚠️ Commit binary scenes before automated MCP edits; TRELLIS.2 requires 24GB VRAM officially (stick to v1 on 16GB).

## 🧭 Social Media, Launch Promotion & Growth (`growth-and-social`)
> Run persistent Hermes or Pi agents feeding Postiz's 30+ network approval calendar and blader/humanizer, backed by upstream marketing skill packs.

- **Implicit Core Plug-In:** Models `google-ai-studio`, `qwen3.8-27b` · Auto-Adapters None · Guards `laya-05`, `safeagents`
- **Canonical Entry Points (Max 2):**
  - [**Postiz (Open-Source 30+ Network Scheduler)**](https://github.com/gitroomhq/postiz-app) · 🟢 `Fresh`
  - [**blader/humanizer (Strips AI Copy Tells)**](https://github.com/blader/humanizer) · 🟢 `Fresh`
- **Upstream Hub (Long Tail):** [**ericosiu/ai-marketing-skills (SEO/AEO, CRO, Launch & Outbound Skills)**](https://github.com/ericosiu/ai-marketing-skills) · 🟢 `Fresh`
- ⚠️ Always route agent drafts through Postiz's human approval calendar; audit outbound skills for CAN-SPAM/GDPR compliance.

## 🧭 Reverse Engineering & Binary Triage (`reverse-engineering`)
> Air-gapped local coding weights wired to GhidraMCP / LLNL OGhidra for rapid static renaming and triage; delegate the 122-repo long tail upstream.

- **Implicit Core Plug-In:** Models `qwen3.8-27b`, `qwen3-coder-next` · Auto-Adapters `qwen38-super-adapter` · Guards `laya-05`, `safeagents`
- **Canonical Entry Points (Max 2):**
  - [**LaurieWired GhidraMCP (12K+ stars)**](https://github.com/LaurieWired/GhidraMCP) · 🟢 `Fresh`
  - [**LLNL OGhidra (Adaptive Loop + MITRE ATT&CK)**](https://github.com/LLNL/OGhidra) · 🟢 `Fresh`
- **Upstream Hub (Long Tail):** [**zhuyansen/awesome-ai-reverse-engineering (122 security-graded repos)**](https://github.com/zhuyansen/awesome-ai-reverse-engineering) · 🟢 `Fresh`
- ⚠️ Strictly audit binaries/APKs you own or have explicit legal authorization to analyze; keep outbound cloud APIs disabled.

## 🧭 Unfiltered & Operator-Aligned Local Stacks (`unfiltered-sovereign`)
> Skip brittle jailbreaks: pick neutral-aligned Hermes 4 or hot-swap Securelayer7's 26 MB LoRA over frozen Qwen3.8-27B behind safeagents + Laya 0.5.

- **Implicit Core Plug-In:** Models `qwen3.8-27b`, `hermes-4` · Auto-Adapters `qwen38-abliterated-lora` · Guards `laya-05`, `safeagents`
- **Canonical Entry Points (Max 2):**
  - [**NousResearch Hermes 4 (Neutral Operator Alignment)**](https://huggingface.co/NousResearch/Hermes-4-14B) · 🟢 `Fresh`
  - [**Securelayer7 Qwen3.8-27B 26MB Uncensored LoRA**](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated) · 🟢 `Fresh`
- **Upstream Hub (Long Tail):** [**huihui-ai/Huihui-Qwen3.8-27B-abliterated (Full Abliterated Weights + MTP)**](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated) · 🟢 `Fresh`
- ⚠️ Abliterated weights cannot refuse anything ever; strictly isolate behind safeagents + Laya 0.5 whenever shell tools are attached.

---

[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; [🖥️ Local](../book/local.md) &nbsp;·&nbsp; [⚙️ Harnesses & RL](../book/harnesses-and-rl.md) &nbsp;·&nbsp; [📘 Playbooks](../book/playbooks.md) &nbsp;·&nbsp; **🧭 Spokes** &nbsp;·&nbsp; [📡 Radar](../book/radar.md) &nbsp;·&nbsp; [🪦 Graveyard](../book/graveyard.md)
