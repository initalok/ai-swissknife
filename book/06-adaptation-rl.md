← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)

# Chapter 06 · Harness Adapters, In-Harness RL & Frontier Research

> [!IMPORTANT]
> **Verdict:** Adapting a frozen 27B model inside its unmodified shipping harness via AsyncGRPO + OpenEnv yields double-digit pass@1 lifts while cutting tool calls 53–73%.
> **Read this chapter if:** You want to serve hot-swappable per-harness LoRAs, reproduce in-harness RL, or track self-improvement research.

## 1. Harness Adapters, RL Stack & Research Leads

| Artifact & Health | Verified Results | License, Footprint & TTL | Rule & Caveat |
| :--- | :--- | :--- | :--- |
| [**Qwen3.8-27B Super-Adapter (Rank-96 PEFT Cat)**](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Zero-retraining orthogonal rank-96 merge (wt 0.5) of pi, Hermes, and OpenCode LoRAs<br>🏆 Thinking Off: beats base 6/6 pairs (39.5% -> 49.0%, 53-73% fewer calls); Thinking On: wins 5/6 & ties 1 (55.5% -> 63.5%) | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · +912 MiB LoRA<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ If using a single harness with thinking off, prefer its specialist LoRA; mild pre-tool reasoning leakage occurs (arXiv:2610.14270). |
| [**Qwen3.8-27B-pi-adapted (Specialist LoRA)**](https://huggingface.co/collections/harness-hub/qwen38-27b-harness-adapters)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Lifts SWE-bench Pro hard-51 from 39.2% -> 64.7% and Terminal-Bench 2.1 by +16.3 pts with 56-72% fewer tool calls<br>🏆 Transfers cleanly across harnesses to OpenCode (44.8% -> 54.0%) and Hermes (46.3% -> 56.1%) | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · +304 MiB LoRA<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Trained on BF16 weights with thinking off; validate GGUF quant fidelity locally. |
| [**Qwen3.8-27B-hermes-adapted (Specialist LoRA)**](https://huggingface.co/collections/harness-hub/qwen38-27b-harness-adapters)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Lifts Hermes SWE-Pro hard-51 from 29.4% -> 43.1% and Terminal-Bench 2.1 by +14.1 pts with 56-70% fewer calls | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · +304 MiB LoRA<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Shows slight OOD dip on AutomationBench (17.7% vs 23.0% base); use super-adapter for general tasks. |
| [**Qwen3.8-27B-opencode-adapted (Specialist LoRA)**](https://huggingface.co/harness-hub/Qwen3.8-27B-opencode-adapted-GGUF)<br><sub>`mature` · 🟢 `Fresh`</sub> | 🏆 Lifts OpenCode SWE-Pro hard-51 from 35.3% -> 51.0% and held-out TB2.1 by +13.6 pts with 53-72% fewer calls | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · +304 MiB LoRA<br><sub>Verified `2026-11-26` (TTL 120d)</sub> | ⚠️ Community confirmed cross-derivative transfer onto Qwen3.8 fine-tunes like Swift-1.5. |
| [**OpenEnv + Harbor + TRL AsyncGRPOTrainer**](https://huggingface.co/blog/harness-adapters-at-scale)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Proxy-based in-harness RL inside unmodified shipping harnesses (2xB200; 1.2x-2.3x more task groups/step as trajectories shrink)<br>🏆 openenv validate passed 858/1,127 tasks; base-model difficulty filter lifted step-50 reward to 0.81 vs 0.63 | `Apache-2.0`<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Use all-linear LoRA, LR 2e-5 (1e-4 collapses rollouts), tool bonus 0.1, and never train GRPO on all-pass/all-fail tasks. |
| [**Repo2RLEnv (Tasksmith) Pipeline**](https://github.com/huggingface/Repo2RLEnv)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 Converts merged GitHub PRs into verified Harbor RL tasks targeting specific capability gaps (22/24 qualified rate) | `Apache-2.0`<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Always re-run openenv validate wrong-answer controls to catch permissive test verifiers. |
| [**TML-d24-varloop-research (Variable-Loop Compute)**](https://huggingface.co/thinkingmachines)<br><sub>`experimental` · 🟢 `Fresh`</sub> | 🏆 Companion checkpoint to Inkling 2 Mini dialing loop_num_passes dynamically at inference time | `Apache-2.0`<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Research checkpoint; pair with a Laya complexity router for experimental test-time compute routing. |
| [**Gradient-Free Self-Rewriting LLMs (arXiv:2611.21885)**](https://arxiv.org/abs/2611.21885)<br><sub>`monitor-only` · 🔭 `Monitor-Only`</sub> | 🏆 UIUC paper demonstrating LLMs diagnosing failures via pure reasoning and rewriting their own weights with zero gradients | `Research`<br><sub>Verified `2026-11-26` (TTL 21d)</sub> | ⚠️ Early academic milestone; monitor for future persistent local self-healing agents. |
| [**Custom 16K Clef-Head Decision LoRA**](https://github.com/unslothai/unsloth)<br><sub>`operational` · 🟢 `Fresh`</sub> | 🏆 1-epoch 4-bit LoRA via Unsloth DecisionTrainer lifts routing accuracy from ~35% to 78-81% with zero output tokens | `Apache-2.0` · <kbd>zone1-16gb-vram</kbd> · ~4.0 GB<br><sub>Verified `2026-11-26` (TTL 60d)</sub> | ⚠️ Requires domain-specific labeled classification examples to outperform zero-shot Laya. |

<details>
<summary>🛠️ <b>OpenEnv Validation & Multi-LoRA Serving</b></summary>
<br>

```bash
openenv validate path/to/task --sandbox hf-sandbox
vllm serve Qwen/Qwen3.8-27B --enable-lora --max-lora-rank 128 --lora-modules pi=harness-hub/Qwen3.8-27B-pi-adapted super=harness-hub/Qwen3.8-27B-super-adapter
```
</details>

---

← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)
