---
title: "Persistent Context, Memory & Knowledge Loops"
section: guides
summary: "Four clean layers for durable agent and personal memory using AGENTS.md/SKILL.md, Pi Durable, plain-Markdown Obsidian vaults, local qmd hybrid search, and KV-cache-stable injection."
order: 4
---

[Home](../README.md) / Guides / Persistent Context, Memory & Knowledge Loops

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Persistent Context, Memory & Knowledge Loops

Most agent memory systems break in one of two ways: dumping giant files into every turn (destroying local KV caches) or trapping notes inside opaque vector databases humans cannot inspect or fix. Organize memory into **four clean layers** instead:

| Layer | Lifespan | What Lives Here | Anchor Standard |
| :--- | :--- | :--- | :--- |
| **1. Repo Rules & Skills** | Versioned in Git | Project conventions and progressive-disclosure workflows (~100 tokens at startup; full `SKILL.md` loads only when triggered). | `AGENTS.md` + `SKILL.md` (supported across 46+ agents) |
| **2. Session Working-Set** | Multi-hour task | Active transcripts, task state, and background compaction backed by searchable disk history. | `@earendil-works/pi-durable` (SQLite/JSONL + `search_history`) |
| **3. Personal Knowledge Vault** | Years (Human + Agent) | Cross-project notes, architecture decisions, and clipped web research stored as plain readable `.md` files. | `obsidianmd/obsidian-skills` (`v1.2.3`) + `defuddle` + `tobi/qmd` + `pi-obsidian-memory` |
| **4. Multi-Device Sync** | Across your Fabric | Sync **only plain `.md` files** (Git, Syncthing, or `obsidian-headless`); keep local vector indexes (`qmd`) strictly machine-local. | Plain-text sync + local index exclusion |

---

## Active Knowledge-Loop Slot & Tools

<!-- swissknife:begin slot id=knowledge-vault -->
**Active Anchor — [Obsidian Official Agent Skills (1.2.3 + defuddle + obsidian-headless)](https://github.com/obsidianmd/obsidian-skills)**

Official Obsidian skill pack working across Antigravity, Hermes, OpenCode, and Pi, bundling Markdown/Bases/Canvas rules, headless CLI sync, and kepano/defuddle web clipping.

- **When to use:** Building a human-readable, Git/Obsidian-friendly personal knowledge vault that both you and your agents maintain.
- **Evidence:** Official documentation · verified 2026-11-28
- **Why this pick:** [Keep Long-Term Agent Memory in Plain Markdown Vaults with KV-Cache-Stable Injection](../docs/why-this-stack.md#adr-why-markdown-memory)
- **Limitation:** Treat all web pages clipped through defuddle strictly as untrusted data, never as executable agent instructions.
<!-- swissknife:end -->

<!-- swissknife:begin table kind=memory -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Obsidian Official Agent Skills (1.2.3 + defuddle + obsidian-headless)](https://github.com/obsidianmd/obsidian-skills) | Building a human-readable, Git/Obsidian-friendly personal knowledge vault that both you and your agents maintain. | MIT | Official documentation | Treat all web pages clipped through defuddle strictly as untrusted data, never as executable agent instructions. |
| [tobi/qmd (Local BM25 + Vector Markdown Search & MCP)](https://github.com/tobi/qmd) | Searching large local Obsidian/Git knowledge vaults privately with zero cloud vector databases. | MIT | Official documentation | Keep qmd vector index files machine-local; exclude them from Git/Syncthing/Obsidian Sync to avoid corruption. |
| [pi-obsidian-memory (KV-Cache-Stable Vault Memory for Pi)](https://github.com/the-matt-moo/pi-obsidian-memory) | Giving Pi persistent cross-session memory without invalidating local llama.cpp/MLX KV prefix caches every turn. | MIT | Field observation | Keep ambient memory as a session-stable snapshot (refreshing only on deliberate writes) so local KV prefix caches do not thrash. |
<!-- swissknife:end -->

## Two Critical Local Physics & Security Rules

1. **Protect Your Local KV Prefix Cache (`llama.cpp` / `MLX` / `vLLM`):** Prefix caching invalidates from the *first modified token onward*. If a memory plugin rewrites your system prompt on every single turn, your GPU or Mac re-prefills the entire conversation every turn. Keep ambient vault memory as a **session-stable snapshot** (refreshing only on deliberate long-term writes or day rollover) and inject dynamic search hits *after* the cached prefix.
2. **Clipped Web Pages Are Untrusted Data:** When clipping documentation or articles with `kepano/defuddle`, explicitly treat extracted content as data—never as executable agent instructions.

---

**Continue reading:** [Pi Ricing Workshop](pi-workshop.md) · [Security & Trust Boundaries](../docs/security-and-trust.md)
