← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)

# 🎯 Mobile App Development (iOS, Android & Expo) · 🟢 `Fresh`

> [!IMPORTANT]
> **Verdict:** Combine MobileBuildMCP for Apple builds/XCTest/LLDB with Argent for physical USB iOS/Android testing and Expo for unified TypeScript apps.
> **Category:** `engineering` · **Age:** `0d` (TTL `60d`)

## 1. Resolved Stack Components

| Role | Entity & Lifecycle | Live Health | Operational Gotchas |
| :--- | :--- | :--- | :--- |
| **`primary_models`** | [**Qwen3.8-27B Super-Adapter (Rank-96 PEFT Cat)**](https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ If using a single harness with thinking off, prefer its specialist LoRA; mild pre-tool reasoning leakage occurs (arXiv:2610.14270). |
| **`primary_models`** | [**Inkling 2 Mini (26.4B Looped Transformer MoE)**](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF)<br><sub>`experimental`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Stock llama.cpp cannot load looped-layer root GGUFs; requires Unsloth runtime or Basalt.<br>⚠️ Trails Qwen3.8-27B on strict chat (50% MultiChallenge); can enter repetitive debug loops so always cap turns and sandbox file actions. |
| **`harnesses`** | [**Google Antigravity (2.0 Desktop, CLI & SDK)**](https://aistudio.google.com/)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Tied to Google auth/billing for paid frontier nodes; configure local fallback for offline sessions. |
| **`harnesses`** | [**Pi Coding Agent (Building-Block Kernel)**](https://pi.dev/)<br><sub>`mature`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 120d</sub> | ⚠️ Intentionally omits built-in per-tool approval gates; pair with safeagents or OS sandboxes. |
| **`specialist_tools`** | [**Sentry MobileBuildMCP (formerly XcodeBuildMCP)**](https://github.com/getsentry/XcodeBuildMCP)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Stops at Apple builds/simulators (no Android or physical iPhone UI taps); pair with Argent. |
| **`specialist_tools`** | [**Argent Mobile Device & Profiler Bridge**](https://github.com/topics/ios-automation)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Requires local developer provisioning and USB debugging permissions. |
| **`specialist_tools`** | [**Expo (React Native) + Expo MCP**](https://expo.dev/)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Hosted Expo MCP docs search requires a paid Expo plan. |
| **`safety_layer`** | [**Hugging Face safeagents Runtime Proxy**](https://github.com/huggingface/safeagents)<br><sub>`operational`</sub> | 🟢 `Fresh`<br><sub>Age: 0d / 60d</sub> | ⚠️ Configure domain plugins (e.g. hf://harness-hub/qwen-safeagents-plugin) rather than running empty defaults. |

## 2. Recommended Workflow

1. Bootstrap cross-platform TypeScript apps with Expo and its auto-generated AGENTS.md.
2. Run Apple target compilation and XCTest loops via Sentry MobileBuildMCP.
3. Attach Argent over USB to test physical devices, inspect HTTP calls, and catch main-thread hangs.

## 3. Domain Guardrails

- ⚠️ MobileBuildMCP stops at Apple simulators/builds; Expo MCP hosted docs search requires a paid plan.

<details>
<summary>🛠️ <b>Click to expand Resolved Launch Recipes</b></summary>
<br>

```bash
# [qwen38-27b-super-adapter]
llama-server -m Qwen3.8-27B-IQ4_XS.gguf --lora Qwen3.8-27B-super-adapter-F16.gguf -ngl 99 -fa on -c 65536 -ctk q8_0 -ctv q8_0

# [inkling-2-mini]
unsloth run unsloth/Inkling-2-Mini-GGUF:UD-Q4_K_XL --spec-draft-n-max 2
```
</details>

---

← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)
