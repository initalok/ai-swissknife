---
title: "Mobile as Human Communicator (HITL)"
section: worlds
world: mobile-hitl
summary: "Using your phone strictly as a Human-in-the-Loop approval gate, voice steering surface, and capture bridge—never as a brute-force LLM runner."
order: 4
---

[Home](../README.md) / Compute Worlds / Mobile as Human Communicator (HITL)

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Mobile as Human Communicator (HITL)

Phones are terrible at brute-forcing 27B coding models on battery—and brilliant at **human presence**. This guide treats your Android or iOS device strictly as a **communicator, approval gate, multimodal capture tool (voice/camera/share-sheet), and zero-port remote steering surface** while heavy compute stays on your Mac mini, GPU PC, or Cloud.

## HITL vs. HOOTL (Why Mobile Matters)

- **HOOTL (Human-Out-of-the-Loop):** Unattended scheduled jobs (nightly research digests, health checks, read-only repo audits). Default to **read-only** and send a one-way ping to your phone when complete.
- **HITL (Human-in-the-Loop):** Any live session writing code, executing shell commands, or pushing branches. Instead of babysitting your desk terminal—or walking away while your agent stalls on one approval prompt—your phone brings human judgment into the loop from anywhere.

---

## Four Mobile Communication Modes

| Mode | Job It Solves | Verified Tools | Key Boundary |
| :--- | :--- | :--- | :--- |
| **1. One-Way Pings** | Know immediately when a long build, ComfyUI render, or scheduled audit finishes or stalls. | `ntfy` (self-hostable or 250 free msgs/day) | Fires after completion; cannot steer mid-loop. |
| **2. Messaging-App Async HITL** | Chat, drop whiteboard photos/PDFs, send voice notes, and tap Approve/Deny with **zero open ports** (outbound long-polling). | `smixs/pi-durable-telegram`, Hermes native Telegram, `@grinev/opencode-telegram-bot` | Never run two pollers on one Telegram bot token; Antigravity currently lacks an official mobile app. |
| **3. Live Multi-Box Steering** | Actively steer running agents across multiple computers, answer extension dialogs, fork `/tree` branches, or use **Voice Mode** (spoken behavioral summaries + explicit verbal confirmation). | `pi-mobile` (`pi-mobile-voice`), `ayagmar/pi-mobile` (Android Compose), `dzianisv/opencode-mobile` (F-Droid) | **A paired mobile client equals shell access on your home machine.** Keep strictly behind Tailscale HTTPS. |
| **4. Out-of-Band Secret Approval** | Keep API keys out of `.env` files visible to agents; tap Approve on your phone when a credential is requested. | Watch-listed pattern: `loonshoot/agent_vault` (POC) | Prototype-grade today, but the cleanest direction for high-stakes secret gating. |

---

## Active Mobile HITL Slot & Tools

<!-- swissknife:begin slot id=mobile-hitl-primary -->
**Active Anchor — [pi-mobile (Multi-Box Tailscale HTTPS & Voice Mode)](https://pi.dev/packages/pi-mobile)**

E2E-encrypted Pi package uniting multiple computers (/remote add box) into one phone queue sorted by 'who needs you', answering any extension dialog with Voice Mode and 2-min desk-idle mute.

- **When to use:** Live hands-free HITL steering across a Mac mini, GPU PC, and cloud VM with spoken behavioral summaries and verbal confirmation.
- **Evidence:** Official documentation · verified 2026-11-28
- **Why this pick:** [Treat Mobile Strictly as Human Communicator & HITL Steering Surface](../docs/why-this-stack.md#adr-why-mobile-hitl)
- **Limitation:** A paired phone equals shell access on your home machine; keep behind Tailscale ACLs and neutral hostnames.
<!-- swissknife:end -->

<!-- swissknife:begin table world=mobile-hitl -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Tailscale Serve (Loopback-to-Tailnet HTTPS Mesh)](https://tailscale.com/kb/1312/serve) | Developer standard for connecting Mac mini, NVIDIA GPU PC, and Android/iOS phones without opening router ports. | Encrypted Private Mesh (Dev Standard) | Official documentation | Automatic Let's Encrypt HTTPS certificates log machine.<tailnet>.ts.net hostnames in public CT logs; use neutral box names (e.g., box-a). |
| [pi-mobile (Multi-Box Tailscale HTTPS & Voice Mode)](https://pi.dev/packages/pi-mobile) | Live hands-free HITL steering across a Mac mini, GPU PC, and cloud VM with spoken behavioral summaries and verbal confirmation. | Live Multi-Box Steering & Voice HITL | Official documentation | A paired phone equals shell access on your home machine; keep behind Tailscale ACLs and neutral hostnames. |
| [ayagmar/pi-mobile (Native Android Compose Client)](https://github.com/ayagmar/pi-mobile) | Android developers wanting a dedicated native client with full /tree session branching on macOS or Linux hosts. | Native Android /tree Steering | Official documentation | Requires Tailscale active on both host and Android device plus the Node RPC bridge daemon. |
| [smixs/pi-durable-telegram (Durable Async Telegram Bot)](https://github.com/smixs/pi-durable-telegram) | Zero-extra-app async HITL communication, multimodal mobile capture, and crash-resumable remote jobs. | Async Messaging HITL (Zero Open Ports) | Official documentation | One-command installer configures a Linux systemd user service; run manually or via launchd on macOS, and never run two pollers on one bot token. |
| [dzianisv/opencode-mobile (Android HITL Client)](https://github.com/dzianisv/opencode-mobile) | Mobile approval and monitoring for OpenCode sessions without switching harnesses. | OpenCode Mobile Approvals | Official documentation | Always configure OPENCODE_SERVER_PASSWORD and route over Tailscale rather than unencrypted LAN. |
| [ntfy (One-Way HOOTL Awareness Pings)](https://github.com/binwiederhier/ntfy) | Notifying your phone the moment an unattended build, ComfyUI render, or nightly audit completes or stalls. | One-Way HOOTL Finish/Stall Pings | Official documentation | One-way notification channel; pair with Telegram or pi-mobile when you need interactive multi-turn steering. |
<!-- swissknife:end -->

**Ergonomics tip:** Typing long coding prompts on glass is frustrating. Lean on **spoken intent** (Voice Mode / voice notes) and **camera or OS share-sheet capture** (snapping error screens, hardware boards, or sharing PDFs straight into a durable home session).

---

**Continue reading:** [The Personal AI Fabric](personal-ai-fabric.md) · [Security & Trust Boundaries](../docs/security-and-trust.md)
