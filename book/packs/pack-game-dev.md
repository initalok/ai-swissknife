← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)

# 🎯 Game Development & Local 16GB 3D Assets · 🟢 `Fresh`

> [!IMPORTANT]
> **Verdict:** Wire sparse coding MoEs directly into Blender, Unity, Godot, Unreal 5.8, or Aseprite MCPs, backed by local 16GB MIT TRELLIS v1 meshes.
> **Category:** `engineering` · **Age:** `0d` (TTL `60d`)

## 1. Resolved Stack Components

| Role | Entity & Lifecycle | Live Health | Operational Gotchas |
| :--- | :--- | :--- | :--- |
| **`primary_models`** | [**Qwen3-Coder-Next (80B-A3B)**](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Never lower -ngl on MoEs; keep Attention/KV on GPU and sweep --n-cpu-moe. |
| **`primary_models`** | [**Inkling 2 Mini (26.4B Looped Transformer MoE)**](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF)<br><sub>`experimental`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Stock llama.cpp cannot load looped-layer root GGUFs; requires Unsloth runtime or Basalt.<br>⚠️ Trails Qwen3.8-27B on strict chat (50% MultiChallenge); can enter repetitive debug loops so always cap turns and sandbox file actions. |
| **`primary_models`** | [**Microsoft TRELLIS v1 (3D Asset Gen)**](https://github.com/microsoft/TRELLIS)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ TRELLIS.2 officially demands 24GB VRAM; stick to TRELLIS v1 or quantized ComfyUI builds on 16GB. |
| **`primary_models`** | [**Hunyuan3D 2.0 / 2mini (PBR 3D)**](https://github.com/Tencent/Hunyuan3D-2)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Tencent Community License is invalid in EU, UK, and South Korea; HY 3D 3.0/3.1 are closed API-only. |
| **`harnesses`** | [**Pi Coding Agent (Building-Block Kernel)**](https://pi.dev/)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Intentionally omits built-in per-tool approval gates; pair with safeagents or OS sandboxes. |
| **`harnesses`** | [**Zed Editor + ACP Registry**](https://zed.dev/)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Requires ACP-compatible agent binary installed locally. |
| **`specialist_tools`** | [**MCP for Blender**](https://github.com/ahujasid/blender-mcp)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Checkpoint .blend files frequently before running destructive mesh-modifier scripts. |
| **`specialist_tools`** | [**Game Engine MCP Suite (Coplay Unity / Godot MCP / Unreal 5.8)**](https://github.com/CoplayDev/unity-mcp)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Engine scene-graph APIs change across minor versions; pin MCP plugin versions per project. |
| **`specialist_tools`** | [**Aseprite MCP (123 Pixel-Art Tools)**](https://github.com/topics/aseprite-mcp)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Requires local Aseprite binary compiled or licensed on host machine. |
| **`safety_layer`** | [**Hugging Face safeagents Runtime Proxy**](https://github.com/huggingface/safeagents)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Configure domain plugins (e.g. hf://harness-hub/qwen-safeagents-plugin) rather than running empty defaults. |

## 2. Recommended Workflow

1. Generate rapid 3D blockouts locally with MIT TRELLIS v1 (16GB VRAM) or sprites with Aseprite MCP.
2. Connect Blender/Unity/Godot/Unreal MCPs to iterate scene hierarchies and gameplay scripts.
3. Commit scene binaries before letting agents run bulk mesh or prefab mutations.

## 3. Domain Guardrails

- ⚠️ Hunyuan3D 2.x license is invalid in EU, UK, and South Korea; TRELLIS.2 requires 24GB VRAM officially.

<details>
<summary>🛠️ <b>Click to expand Resolved Launch Recipes</b></summary>
<br>

```bash
# [qwen3-coder-next-80b]
GGML_CUDA_GRAPH_OPT=1 llama-server -m Qwen3-Coder-Next-UD-Q4_K_XL.gguf -ngl 99 -fa on -c 120000 --load-mode none --n-cpu-moe 29 -ctk q8_0 -ctv q8_0 --temp 0

# [inkling-2-mini]
unsloth run unsloth/Inkling-2-Mini-GGUF:UD-Q4_K_XL --spec-draft-n-max 2
```
</details>

---

← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)
