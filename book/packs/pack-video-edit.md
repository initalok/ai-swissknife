← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)

# 🎯 Video Editing, Motion Graphics & Local AI Footage · 🟢 `Fresh`

> [!IMPORTANT]
> **Verdict:** Use DaVinci Resolve MCP for Studio NLE cuts, Hyperframes/Remotion for code-driven motion graphics, and WanGP v20.12 for 5.9 GB local footage.
> **Category:** `creative` · **Age:** `0d` (TTL `60d`)

## 1. Resolved Stack Components

| Role | Entity & Lifecycle | Live Health | Operational Gotchas |
| :--- | :--- | :--- | :--- |
| **`primary_models`** | [**Google AI Studio (Gemini 4 Hydrogen & 3.8 Flash)**](https://aistudio.google.com/)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 21d</sub> | ⚠️ Gemini 2.5 retires Dec 1, 2026; 4 Argon/Carbon/Neon, Batch, and Search Grounding are paid-only.<br>⚠️ Free tier prompts may be logged outside EU/UK/CH; redact sensitive PII. |
| **`primary_models`** | [**Qwen3.8-27B (Dense Vision+Text)**](https://huggingface.co/Qwen/Qwen3.8-27B)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Use IQ4_XS + Q8 KV cache on 16GB VRAM so it never spills across PCIe. |
| **`primary_models`** | [**Wan 2.2 (5B & A14B Video)**](https://huggingface.co/Wan-AI)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Wan 3.0 and Wan 2.6 remain closed APIs with no published weights. |
| **`primary_models`** | [**LTX-2.5 (22B Video + Sync Audio)**](https://huggingface.co/Lightricks)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Requires 64GB RAM block-swapping on 16GB GPUs; verify LTX Community commercial thresholds. |
| **`harnesses`** | [**Pi Coding Agent (Building-Block Kernel)**](https://pi.dev/)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Intentionally omits built-in per-tool approval gates; pair with safeagents or OS sandboxes. |
| **`harnesses`** | [**DeepSeek Harness (dsh / Cordis Platform)**](https://github.com/deepseek-ai/deepseek-harness)<br><sub>`experimental`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 21d</sub> | ⚠️ Rapidly iterating developer preview (0.2.3-alpha.2); pin plugin versions against breaking API changes. |
| **`specialist_tools`** | [**DaVinci Resolve MCP (27 Compound NLE Tools)**](https://github.com/topics/davinci-resolve-mcp)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ External scripting/MCP strictly requires paid DaVinci Resolve Studio 20.x; the free edition blocks scripting APIs. |
| **`specialist_tools`** | [**HeyGen Hyperframes & Remotion Skills**](https://github.com/remotion-dev/remotion)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Excels at code-driven motion graphics, not organic live-action B-roll. |
| **`specialist_tools`** | [**OpenMontage & OpenMotion (Motion.md)**](https://github.com/topics/remotion)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 21d</sub> | ⚠️ Fast-moving indie repos; pin releases before committing commercial deliverables. |
| **`specialist_tools`** | [**WanGP v20.12 + MMGP v4 + SageGP 1.0.2**](https://github.com/deepbeepmeep/WanGP)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 21d</sub> | ⚠️ Install WGPKernels 1.5.0 and SageGP 1.0.2 (PyTorch 2.10; Triton 3.6+ for RTX 50xx adaptive Sage2/3). |

## 2. Recommended Workflow

1. Generate motion graphics and product explainers programmatically with Hyperframes or Remotion Skills.
2. Synthesize consistent multi-shot AI footage locally via WanGP v20.12 Extreme Chunker + Wan 2.2 / LTX-2.5.
3. Automate final timeline assembly, color, and Fairlight audio through DaVinci Resolve MCP.

## 3. Domain Guardrails

- ⚠️ DaVinci Resolve external scripting/MCP strictly requires paid Resolve Studio 20.x.

<details>
<summary>🛠️ <b>Click to expand Resolved Launch Recipes</b></summary>
<br>

```bash
# [qwen3.8-27b]
llama-server -m Qwen3.8-27B-IQ4_XS.gguf -ngl 99 -fa on -c 32768 -ctk q8_0 -ctv q8_0
```
</details>

---

← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)
