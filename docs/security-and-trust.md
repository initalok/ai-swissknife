---
title: "Security & Trust Boundaries"
section: docs
summary: "Three calm safety habits for newcomers and a six-boundary threat model for connecting Cloud, Mac, GPU PC, Mobile HITL, and Knowledge Vaults."
order: 5
---

[Home](../README.md) / Orientation / Security & Trust Boundaries

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Security & Trust Boundaries

Security matters most the moment you move from chatting in a browser to giving agents shell access, connecting a Mac mini to a GPU PC, or approving actions from your phone. Keep this model calm, practical, and layered.

## Three Habits for Newcomers

1. **Never send secrets to free cloud tiers:** Zero-card cloud gateways (like Google AI Studio Free Tier) may log prompts for product improvement outside the EU/UK/CH. Keep API keys, passwords, and private code on local hardware.
2. **Keep approval prompts turned on:** Use `OpenCode`'s default per-action confirmation prompts or `Antigravity`'s review gates until you deliberately configure an OS/VM sandbox.
3. **Treat clipped web pages and external skills as untrusted data:** Web scrapers (`defuddle`, `Firecrawl`) and third-party skills can carry hidden prompt injections—never grant blind shell execution on freshly clipped external content.

---

## Six Trust Boundaries Across a Connected Personal AI Fabric

| Surface / Connection | Real-World Failure Mode | Required Boundary |
| :--- | :--- | :--- |
| **Local Servers & Bridges** | Binding `llama-server`, `ComfyUI`, or `opencode serve` to `0.0.0.0` exposes unauthenticated API or shell access across shared Wi-Fi. | Bind strictly to **`127.0.0.1`**; set `OPENCODE_SERVER_PASSWORD`; never forward router ports. |
| **Private Mesh (`Tailscale` / `LM Link`)** | Over-broad tailnet access or leaking sensitive project names into public Let's Encrypt CT logs (`*.ts.net`). | Enforce Tailscale ACL tags (`tag:ai-node`, `tag:admin-devices`) and assign neutral hostnames (`box-a`, `gpu-1`). |
| **Autonomous Code Execution (`Pi`)** | `Pi` intentionally omits built-in approval prompts; untrusted scripts can read `.env` credentials. | Run untrusted code inside **`gondolin`** (`libkrun` micro-VM with host placeholder secret injection) or use **`nono`** (macOS Seatbelt / Linux Landlock) for native host builds. |
| **Tool Auditing & Unfiltered LoRAs** | Abliterated LoRAs cannot refuse destructive shell actions; prompt injection can hijack tool calls. | Wrap shell-capable harnesses behind **`safeagents`** (`atif-scan` + plugin) and/or **`Laya 0.5`** (`localhost:8888`). |
| **Mobile HITL Steering** | A paired mobile client equals remote shell access on your home machine. | Use E2E Tailscale HTTPS (`pi-mobile`) or outbound Telegram long-polling with strict user allow-lists; never use unencrypted LAN token modes on shared networks. |
| **Personal Knowledge Vaults** | Prompt injection hidden in clipped web pages; binary vector DB corruption across multi-device sync. | Treat clipped Markdown as untrusted data; sync **only `.md` files** and keep local search indexes (`tobi/qmd`) machine-local. |

---

## Verified Security & Isolation Tools

<!-- swissknife:begin table tag=security -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Tailscale Serve (Loopback-to-Tailnet HTTPS Mesh)](https://tailscale.com/kb/1312/serve) | Developer standard for connecting Mac mini, NVIDIA GPU PC, and Android/iOS phones without opening router ports. | Encrypted Private Mesh (Dev Standard) | Official documentation | Automatic Let's Encrypt HTTPS certificates log machine.<tailnet>.ts.net hostnames in public CT logs; use neutral box names (e.g., box-a). |
| [pi-mobile (Multi-Box Tailscale HTTPS & Voice Mode)](https://pi.dev/packages/pi-mobile) | Live hands-free HITL steering across a Mac mini, GPU PC, and cloud VM with spoken behavioral summaries and verbal confirmation. | Live Multi-Box Steering & Voice HITL | Official documentation | A paired phone equals shell access on your home machine; keep behind Tailscale ACLs and neutral hostnames. |
| [Obsidian Official Agent Skills (1.2.3 + defuddle + obsidian-headless)](https://github.com/obsidianmd/obsidian-skills) | Building a human-readable, Git/Obsidian-friendly personal knowledge vault that both you and your agents maintain. | MIT | Official documentation | Treat all web pages clipped through defuddle strictly as untrusted data, never as executable agent instructions. |
| [Laya 0.5 (Multimodal System-1 Decision Model)](https://github.com/NandhaKishorM/laya) | Fast zero-output-token tool-safety gating, routing, and memory relevance checks without using GPU VRAM. | 678-846 MB (CPU / NPU / WebGPU) | Official documentation | Threshold decisions on calibrated probabilities rather than raw confidence scores; optional vegaml-learn add-on is non-commercial. |
| [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents) | Auditing autonomous coding harnesses and unfiltered local LoRAs at the tool-call layer. | Apache-2.0 | Primary evaluation | Audits API tool calls rather than isolating local OS binaries; pair with gondolin or nono for filesystem isolation. |
| [earendil-works/gondolin (libkrun Micro-VM + Secret Proxy)](https://github.com/earendil-works/gondolin) | Rung 2 of the Pi Ricing Journey when executing untrusted code or defending against .env secret exfiltration. | ~200 MB Alpine guest image (zero Docker required on Mac) | Official documentation | Cannot run macOS-only host toolchains (xcodebuild/swift); use nono for native macOS builds. |
| [nolabs-ai/nono v0.82 (macOS Seatbelt & Linux Landlock Sandbox)](https://github.com/nolabs-ai/nono) | Production-grade least-privilege sandboxing for 24/7 Mac mini servers and native macOS/Linux host toolchains. | Apache-2.0 | Official documentation | Shares the host kernel; for heavily untrusted code execution or strict zero-secret micro-VM isolation, pair with gondolin. |
<!-- swissknife:end -->

## 5-Point Production-Ready Environment Checklist

1. **Loopback Only (`127.0.0.1`):** Bind every inference engine, MCP server, and UI bridge strictly to `127.0.0.1`—publish across devices only via `tailscale serve` or `rex server tailscale on`.
2. **OS or Micro-VM Sandbox:** Wrap host-native Mac/Linux builds (`Pi`, `OpenCode`, `xcodebuild`) in `nono v0.82` (`nolabs-ai/pi` / `nolabs-ai/opencode`) or run untrusted dependencies inside a `gondolin` micro-VM.
3. **Never Expose Raw `.env` Secrets:** Inject credentials through `nono --credential` (macOS Keychain) or `gondolin`'s host placeholder HTTP proxy so runaway agent shells never read plaintext API tokens.
4. **Runtime Tool-Call Auditing:** Route autonomous or abliterated tool calls through `safeagents` and/or `Laya 0.5` (`localhost:8888`).
5. **Reboot-Safe Durability & Rollback:** Run `Pi Durable` inside `Rex` on 24/7 hosts and enable `nono --rollback` before unsupervised file-mutating loops.

<!-- swissknife:begin recipe id=nono -->
<details>
<summary>Launch command — nolabs-ai/nono v0.82 (macOS Seatbelt & Linux Landlock Sandbox) (CUDA / llama.cpp / CLI)</summary>

```bash
nono pull nolabs-ai/pi && nono run --profile nolabs-ai/pi -- pi
```

</details>

Built-in upstream check: `nono why --path ~/.ssh/id_rsa --op read`
<!-- swissknife:end -->

<!-- swissknife:begin recipe id=safeagents -->
<details>
<summary>Launch command — Hugging Face safeagents Proxy (CUDA / llama.cpp / CLI)</summary>

```bash
safeagents start http://127.0.0.1:8080 --plugin hf://harness-hub/qwen-safeagents-plugin
```

</details>
<!-- swissknife:end -->

<!-- swissknife:begin recipe id=laya-05 -->
<details>
<summary>Launch command — Laya 0.5 (Multimodal System-1 Decision Model) (CUDA / llama.cpp / CLI)</summary>

```bash
pip install -U laya && unsloth serve-decision convaiinnovations/laya-typed-decisions --port 8888
```

</details>
<!-- swissknife:end -->

---

**Continue reading:** [The Personal AI Fabric](../worlds/personal-ai-fabric.md) · [Pi Ricing Workshop](../guides/pi-workshop.md)
