← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)

# 🎯 Uncensored & Operator-Aligned Local Stacks · 🟢 `Fresh`

> [!IMPORTANT]
> **Verdict:** Skip brittle jailbreak prompts; pick neutral-aligned Hermes 4 for operator-controlled rules, or abliterated Qwen3.8-27B + MTP behind safeagents.
> **Category:** `specialized` · **Age:** `0d` (TTL `60d`)

## 1. Resolved Stack Components

| Role | Entity & Lifecycle | Live Health | Operational Gotchas |
| :--- | :--- | :--- | :--- |
| **`primary_models`** | [**NousResearch Hermes 4 (14B / 4.3-36B Neutral)**](https://huggingface.co/NousResearch)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Always author explicit operator guardrails in the system prompt if deploying beyond solo use. |
| **`primary_models`** | [**Qwen3.8-27B-Uncensored-GGUF (Abliterated + MTP)**](https://huggingface.co/models)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Cannot refuse anything ever; strictly isolate behind safeagents/Laya when wired to shell tools.<br>⚠️ Pass --image-min-tokens 1024 for vision; avoid aggressive abliteration builds. |
| **`primary_models`** | [**Gemma-4-26B-MoE-HERETIC**](https://huggingface.co/models)<br><sub>`experimental`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Community abliteration checkpoint; verify factual degradation on your domain and never expose to untrusted users. |
| **`primary_models`** | [**Dolphin 3.0 Mistral 24B / Dolphin-R1**](https://huggingface.co/cognitivecomputations)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Mature conversational/roleplay feel, but coding benchmarks trail Qwen3.8-27B. |
| **`harnesses`** | [**Pi Coding Agent (Building-Block Kernel)**](https://pi.dev/)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Intentionally omits built-in per-tool approval gates; pair with safeagents or OS sandboxes. |
| **`harnesses`** | [**OpenCode CLI**](https://github.com/anomalyco/opencode)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Does not auto-compact as aggressively as Pi; watch context length on multi-hour repos. |
| **`safety_layer`** | [**Hugging Face safeagents Runtime Proxy**](https://github.com/huggingface/safeagents)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Configure domain plugins (e.g. hf://harness-hub/qwen-safeagents-plugin) rather than running empty defaults. |
| **`safety_layer`** | [**Laya Local Decision Models (678-846 MB)**](https://huggingface.co/convaiinnovations)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Threshold on probabilities (not confidence); route borderline superseded-vs-contradicted memory cases to review. |

## 2. Recommended Workflow

1. Choose Hermes 4 when you want neutral compliance with custom operator system-prompt policies.
2. Choose abliterated Qwen3.8-27B (with --spec-type draft-mtp) when you need zero built-in refusals at high coding strength.
3. Always place safeagents + Laya between unfiltered models and local bash/filesystem tools.

## 3. Domain Guardrails

- ⚠️ Abliterated checkpoints cannot refuse anything ever; never expose directly to public users or unguarded shells.

<details>
<summary>🛠️ <b>Click to expand Resolved Launch Recipes</b></summary>
<br>

```bash
# [hermes-4-neutral]
llama-server -m Hermes-4-14B-Q4_K_M.gguf -ngl 99 -fa on -c 32768

# [qwen3.8-27b-uncensored]
llama-server -m Qwen3.8-27B-Uncensored-IQ4_XS.gguf -ngl 99 -fa on --spec-type draft-mtp --spec-draft-n-max 1 -ctk q8_0 -ctv q8_0

# [dolphin-3-r1-24b]
llama-server -m Dolphin3.0-R1-Mistral-24B-Q4_K_M.gguf -ngl 99 -fa on -c 32768

# [laya-decisions]
unsloth serve-decision convaiinnovations/laya-typed-decisions --port 8888
```
</details>

---

← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)
