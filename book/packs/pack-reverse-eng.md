← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)

# 🎯 Reverse Engineering & Binary Triage · 🟢 `Fresh`

> [!IMPORTANT]
> **Verdict:** Run 100% air-gapped local coding weights wired to Ghidra/IDA/JADX/Radare2 MCPs for rapid static triage; keep dynamic debugging human-led.
> **Category:** `engineering` · **Age:** `0d` (TTL `60d`)

## 1. Resolved Stack Components

| Role | Entity & Lifecycle | Live Health | Operational Gotchas |
| :--- | :--- | :--- | :--- |
| **`primary_models`** | [**Qwen3.8-27B (Dense Vision+Text)**](https://huggingface.co/Qwen/Qwen3.8-27B)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Use IQ4_XS + Q8 KV cache on 16GB VRAM so it never spills across PCIe. |
| **`primary_models`** | [**Qwen3-Coder-Next (80B-A3B)**](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Never lower -ngl on MoEs; keep Attention/KV on GPU and sweep --n-cpu-moe. |
| **`harnesses`** | [**Pi Coding Agent (Building-Block Kernel)**](https://pi.dev/)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Intentionally omits built-in per-tool approval gates; pair with safeagents or OS sandboxes. |
| **`specialist_tools`** | [**LLNL OGhidra & GhidraMCP (Ghidra 12.0.3)**](https://github.com/LLNL/OGhidra)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Static decompilation speeds triage/renaming; heavy packing still requires manual dynamic debugging. |
| **`specialist_tools`** | [**Decompiler MCP Suite (IDA / ReVa / JADX / Radare2)**](https://github.com/cyberkaida/reverse-engineering-assistant)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Strictly audit binaries/APKs you own or have explicit legal authorization to analyze. |
| **`safety_layer`** | [**Hugging Face safeagents Runtime Proxy**](https://github.com/huggingface/safeagents)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Configure domain plugins (e.g. hf://harness-hub/qwen-safeagents-plugin) rather than running empty defaults. |

## 2. Recommended Workflow

1. Load binary or APK inside an isolated offline sandbox with outbound cloud endpoints disabled.
2. Attach LLNL OGhidra / GhidraMCP or JADX MCP to bulk-rename functions, trace xrefs, and run MITRE ATT&CK pattern alerts.
3. Switch to manual dynamic debugging for packed, virtualized, or anti-debug control flow.

## 3. Domain Guardrails

- ⚠️ Strictly analyze binaries/APKs you own or have explicit legal authorization to audit.

<details>
<summary>🛠️ <b>Click to expand Resolved Launch Recipes</b></summary>
<br>

```bash
# [qwen3.8-27b]
llama-server -m Qwen3.8-27B-IQ4_XS.gguf -ngl 99 -fa on -c 32768 -ctk q8_0 -ctv q8_0

# [qwen3-coder-next-80b]
GGML_CUDA_GRAPH_OPT=1 llama-server -m Qwen3-Coder-Next-UD-Q4_K_XL.gguf -ngl 99 -fa on -c 120000 --load-mode none --n-cpu-moe 29 -ctk q8_0 -ctv q8_0 --temp 0
```
</details>

---

← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)
