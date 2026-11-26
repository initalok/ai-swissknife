from __future__ import annotations

import os
from typing import Any

STATUS_BADGE = {
    "fresh": "🟢 `Fresh`",
    "aging": "🟡 `Aging`",
    "stale": "🟠 `Needs Re-Verify`",
    "degraded": "🔴 `Degraded`",
    "monitor_only": "🔭 `Monitor-Only`",
    "graveyard": "🪦 `Graveyard`",
}


def _badge(freshness: dict[str, Any]) -> str:
    st = freshness.get("effective_status") or freshness.get("status", "fresh")
    return STATUS_BADGE.get(st, f"`{st}`")


def _link(name: str, urls: dict[str, Any] | None) -> str:
    primary = (urls or {}).get("primary")
    return f"[**{name}**]({primary})" if primary else f"**{name}**"


def _stack_list(items: list[str] | None, prefix: str = "") -> str:
    if not items:
        return "—"
    return "<br>".join(f"{prefix}{x}" for x in items)


def _entity_row(ent: dict[str, Any]) -> str:
    f = ent["freshness"]
    hw = ent.get("hardware", {})
    meta_bits = []
    if ent.get("license"):
        meta_bits.append(f"`{ent['license']}`")
    if hw.get("zone"):
        meta_bits.append(f"<kbd>{hw['zone']}</kbd>")
    if hw.get("vram_gb"):
        meta_bits.append(f"~{hw['vram_gb']} GB")
    if hw.get("vram_delta_mb"):
        meta_bits.append(f"+{hw['vram_delta_mb']} MiB LoRA")
    if ent.get("quota"):
        meta_bits.append(ent["quota"])

    meta_str = " · ".join(meta_bits) or f"`{ent['kind']}`"
    c1 = f"{_link(ent['name'], ent.get('urls'))}<br><sub>`{ent['lifecycle']}` · {_badge(f)}</sub>"
    c2 = _stack_list(ent.get("proof") or [ent.get("summary", ent["kind"])], "🏆 ")
    c3 = f"{meta_str}<br><sub>Verified `{ent['last_verified']}` (TTL {f['ttl_days']}d)</sub>"
    c4 = _stack_list(ent.get("gotchas"), "⚠️ ")
    return f"| {c1} | {c2} | {c3} | {c4} |"


def _render_table(heading: str, headers: list[str], rows: list[str]) -> list[str]:
    if not rows:
        return []
    return [
        f"## {heading}",
        "",
        f"| {headers[0]} | {headers[1]} | {headers[2]} | {headers[3]} |",
        "| :--- | :--- | :--- | :--- |",
        *rows,
        "",
    ]


def _render_book_chapter(
    path: str,
    title: str,
    verdict: str,
    read_if: str,
    sections: list[tuple[str, list[str], list[str]]],
    drawers: list[tuple[str, str]] | None = None,
    monitor_only: bool = False,
) -> None:
    nav = "← [🏠 Field Book Cover](../README.md) &nbsp;|&nbsp; [🎯 Use-Case Packs](packs/README.md) &nbsp;|&nbsp; [🪦 Graveyard](99-graveyard.md)"
    lines = [nav, "", f"# {title}", "", "> [!IMPORTANT]", f"> **Verdict:** {verdict}", f"> **Read this chapter if:** {read_if}", ""]
    if monitor_only:
        lines.extend([
            "> [!NOTE]",
            "> **Monitor-Only Radar:** Strictly tracks apex closed/rack-scale ceilings and trickle-down signals. Excluded from agent auto-foraging (`llms.txt`).",
            "",
        ])
    for heading, headers, rows in sections:
        lines.extend(_render_table(heading, headers, rows))
    for summary, code in (drawers or []):
        if not code.strip():
            continue
        lines.extend([
            "<details>",
            f"<summary>🛠️ <b>{summary}</b></summary>",
            "<br>",
            "",
            "```bash",
            code.rstrip(),
            "```",
            "</details>",
            "",
        ])
    lines.extend(["---", "", nav])
    with open(path, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines) + "\n")


def _render_pack_page(pack: dict[str, Any], out_dir: str) -> str:
    pid = pack["pack_id"]
    fname = f"{pid}.md"
    f = pack["freshness"]
    nav = "← [🎯 All Use-Case Packs](README.md) &nbsp;|&nbsp; [🏠 Field Book Cover](../../README.md)"
    lines = [
        nav,
        "",
        f"# 🎯 {pack['title']} · {_badge(f)}",
        "",
        "> [!IMPORTANT]",
        f"> **Verdict:** {pack['verdict']}",
        f"> **Category:** `{pack['category']}` · **Age:** `{f['age_days']}d` (TTL `{f['ttl_days']}d`)",
        "",
    ]

    dep_issues = f.get("degraded_dependencies", [])
    if dep_issues:
        warn = ", ".join(f"`{d['entity_id']}` ({d['status']})" for d in dep_issues)
        lines.extend([
            "> [!WARNING]",
            f"> **Partial Degradation:** Referenced entities needing re-verification ({warn}) are automatically gated out of `llms.txt`. Healthy stack members remain active.",
            "",
        ])

    rows = []
    launch_cmds = []
    for role, items in pack.get("stack", {}).items():
        for item in items:
            if item.get("launch_recipe"):
                launch_cmds.append(f"# [{item['id']}]\n{item['launch_recipe']}")
            rows.append(
                f"| **`{role}`** | {_link(item['name'], item.get('urls'))}<br><sub>`{item['lifecycle']}`</sub> | "
                f"{_badge(item['freshness'])}<br><sub>Age: {item['freshness']['age_days']}d / {item['freshness']['ttl_days']}d</sub> | "
                f"{_stack_list(item.get('gotchas'), '⚠️ ')} |"
            )

    lines.extend(_render_table("1. Resolved Stack Components", ["Role", "Entity & Lifecycle", "Live Health", "Operational Gotchas"], rows))

    if pack.get("workflow_steps"):
        lines.append("## 2. Recommended Workflow")
        lines.append("")
        for i, step in enumerate(pack["workflow_steps"], 1):
            lines.append(f"{i}. {step}")
        lines.append("")

    if pack.get("gotchas"):
        lines.append("## 3. Domain Guardrails")
        lines.append("")
        for g in pack["gotchas"]:
            lines.append(f"- ⚠️ {g}")
        lines.append("")

    if launch_cmds:
        lines.extend([
            "<details>",
            "<summary>🛠️ <b>Click to expand Resolved Launch Recipes</b></summary>",
            "<br>",
            "",
            "```bash",
            "\n\n".join(launch_cmds),
            "```",
            "</details>",
            "",
        ])

    lines.extend(["---", "", nav])
    with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines) + "\n")
    return fname


def render(snapshot: dict[str, Any], root: str = ".") -> None:
    book_dir = os.path.join(root, "book")
    packs_dir = os.path.join(book_dir, "packs")
    os.makedirs(packs_dir, exist_ok=True)

    ents = list(snapshot["entities"].values())
    by_domain = lambda d: [e for e in ents if e.get("domain") == d]

    _render_book_chapter(
        os.path.join(book_dir, "01-cloud-apis.md"),
        "Chapter 01 · Zero-Card Cloud APIs, Decisions & Grounding",
        "Only verified card-free gateways and zero-auth grounding tools enter this chapter; stale volatile tiers are automatically gated from agents.",
        "You need $0 cloud LLMs, Gemini 4 Hydrogen, System-1 decision endpoints, or keyless RAG/search APIs.",
        [
            ("1. Verified No-Card Cloud Gateways", ["Gateway & Health", "Capabilities & Proof", "Quota & TTL", "The Catch (`⚠️ Gotcha`)"], [_entity_row(e) for e in ents if e["kind"] == "gateway"]),
            ("2. Grounding, Search & RAG Tools", ["Tool & Health", "Capabilities & Proof", "Quota & TTL", "The Catch (`⚠️ Gotcha`)"], [_entity_row(e) for e in by_domain("grounding")]),
        ],
        drawers=[("Cloud Foraging CLI", "python scripts/cli.py query cloud coding-agent\npython scripts/cli.py query cloud decision-gate")],
    )

    mature_local = [e for e in ents if e.get("domain") == "local-llm" and e["lifecycle"] == "mature"]
    edge_local = [e for e in ents if e.get("domain") == "local-llm" and e["lifecycle"] in ("experimental", "operational")]
    sys1_local = [e for e in ents if e.get("domain") == "local-decision"]
    local_recipes = "\n\n".join(f"# [{e['id']}] ({e['lifecycle']})\n{e['launch_recipe']}" for e in (mature_local + edge_local + sys1_local) if e.get("launch_recipe"))

    _render_book_chapter(
        os.path.join(book_dir, "02-local-16vram-64ram.md"),
        "Chapter 02 · Local AI (16GB VRAM + 64GB RAM: Mature vs. Cutting-Edge)",
        "Keep battle-tested Mature Riced daily drivers separate from experimental Cutting-Edge architectures so runtime churn never breaks your local workflow.",
        "You are deploying local LLMs, Harness LoRAs, Uncensored/Neutral models, or System-1 Decision Models inside 16GB VRAM + 64GB RAM.",
        [
            ("1. Track A · Mature & Fully Riced", ["Model & Health", "Proof & Benchmarks", "Footprint & TTL", "Tuning Gotcha"], [_entity_row(e) for e in mature_local]),
            ("2. Track B · Cutting-Edge & Specialized Local", ["Model & Health", "Upside & Benchmarks", "Footprint & TTL", "Early-Adopter Gotcha"], [_entity_row(e) for e in edge_local]),
            ("3. System-1 Local Decision Models", ["Decision Model", "Capabilities", "Footprint & TTL", "Wiring Gotcha"], [_entity_row(e) for e in sys1_local]),
        ],
        drawers=[("Local Launch Recipes (`python scripts/cli.py query local`)", local_recipes)],
    )

    _render_book_chapter(
        os.path.join(book_dir, "03-multimodal-sensory.md"),
        "Chapter 03 · Multimodal, Voice, Video, 3D & World Models",
        "Use free cloud STT/vision where fast, and pivot locally for RGBA editing, directed multi-speaker TTS, 3D meshes, and 5.9 GB 1080p video.",
        "You are building image, video, audio, OCR, 3D asset, or interactive world pipelines.",
        [("1. Verified Multimodal & 3D Stack", ["Model & Health", "Strengths & Proof", "License, Footprint & TTL", "Hardware / License Gotcha"], [_entity_row(e) for e in by_domain("multimodal")])],
    )

    _render_book_chapter(
        os.path.join(book_dir, "04-harnesses-protocols.md"),
        "Chapter 04 · Agent Harnesses, Protocols & Safety",
        "Use Pi / Pi Durable as your minimal building-block kernel, DeepSeek Harness (dsh) for Cordis plugin composability, and Hermes Agent for self-improving persistence—shielded by safeagents.",
        "You are choosing an agent harness, wiring Skills/MCP, or sandboxing autonomous tool calls.",
        [
            ("1. Agent Harnesses by Architectural Role", ["Harness & Health", "Architecture & Capabilities", "License & TTL", "Pairing & Gotcha"], [_entity_row(e) for e in ents if e["kind"] == "harness"]),
            ("2. Safety Proxies & Core Protocols", ["Tool / Pattern", "What It Solves", "License & TTL", "Production Guardrail"], [_entity_row(e) for e in by_domain("safety-protocol")]),
        ],
        drawers=[("DeepSeek Harness & safeagents Quickstart", "npx @deepseek-ai/dsh web\nsafeagents start http://localhost:8000 --plugin hf://harness-hub/qwen-safeagents-plugin")],
    )

    _render_book_chapter(
        os.path.join(book_dir, "05-backends-flags-silicon.md"),
        "Chapter 05 · Backends, Quantization & OS/Silicon",
        "Serving kernels and hybrid MoE memory flags (`--n-cpu-moe`, `--load-mode`, `WanGP v20.12`) unlock 2x–5x speedups on 16GB cards and Apple Silicon.",
        "You are tuning local inference servers, CUDA/AVX-512 offload sweeps, or Mac MLX stacks.",
        [("1. Verified Backends & Silicon Engines", ["Backend & Health", "Breakthroughs", "Target & TTL", "Compatibility Gotcha"], [_entity_row(e) for e in by_domain("backend")])],
        drawers=[("2026 Zone-2 MoE Sweep Flag Reference", "GGML_CUDA_GRAPH_OPT=1 llama-server -m Qwen3-Coder-Next-UD-Q4_K_XL.gguf -ngl 99 -fa on -c 120000 --load-mode none --n-cpu-moe 29 -ctk q8_0 -ctv q8_0 --temp 0")],
    )

    _render_book_chapter(
        os.path.join(book_dir, "06-adaptation-rl.md"),
        "Chapter 06 · Harness Adapters, In-Harness RL & Frontier Research",
        "Adapting a frozen 27B model inside its unmodified shipping harness via AsyncGRPO + OpenEnv yields double-digit pass@1 lifts while cutting tool calls 53–73%.",
        "You want to serve hot-swappable per-harness LoRAs, reproduce in-harness RL, or track self-improvement research.",
        [("1. Harness Adapters, RL Stack & Research Leads", ["Artifact & Health", "Verified Results", "License, Footprint & TTL", "Rule & Caveat"], [_entity_row(e) for e in ents if e["kind"] == "adapter" or e.get("domain") == "adaptation"])],
        drawers=[("OpenEnv Validation & Multi-LoRA Serving", "openenv validate path/to/task --sandbox hf-sandbox\nvllm serve Qwen/Qwen3.8-27B --enable-lora --max-lora-rank 128 --lora-modules pi=harness-hub/Qwen3.8-27B-pi-adapted super=harness-hub/Qwen3.8-27B-super-adapter")],
    )

    for fid, out_name in (("community-irl", "07-community-irl.md"), ("frontier-watch", "08-frontier-watch.md")):
        feed = snapshot["feeds"].get(fid)
        if not feed:
            continue
        rows = []
        for item in feed.get("items", []):
            f = item["freshness"]
            c1 = f"{_link(item['name'], item.get('urls'))}<br><sub>`{item.get('group', fid)}` · {_badge(f)}</sub>"
            c2 = _stack_list(item.get("proof") or [item.get("summary", "")], "🏆 ")
            c3 = f"{item.get('stack_label', '—')}<br><sub>Verified `{item['last_verified']}` (TTL {f['ttl_days']}d)</sub>"
            c4 = _stack_list(item.get("gotchas"), "⚠️ ")
            rows.append(f"| {c1} | {c2} | {c3} | {c4} |")
        _render_book_chapter(
            os.path.join(book_dir, out_name),
            feed["title"],
            feed["verdict"],
            feed["read_if"],
            [("Tracked Entries (Volatile Feed)", ["Project / Model", "Verified Signal", "Stack & TTL", "Caveat / Trickle-Down"], rows)],
            monitor_only=bool(feed.get("monitor_only")),
        )

    g = snapshot["graveyard"]
    g_lines = [
        "← [🏠 Field Book Cover](../README.md)",
        "",
        "# 🪦 Appendix · The Graveyard (CI-Enforced Cut List)",
        "",
        "> [!WARNING]",
        "> Any active entity or Use-Case Pack referencing these patterns fails `python scripts/cli.py validate`.",
        "",
        "## 🌐 Cloud API Graveyard",
        *[f"- ❌ **{x['name']}:** {x['reason']}" for x in g.get("cloud", [])],
        "",
        "## 🖥️ Local Hardware Wall Graveyard (`16GB VRAM + 64GB RAM`)",
        *[f"- ❌ **{x['name']}:** {x['reason']}" for x in g.get("local", [])],
    ]
    with open(os.path.join(book_dir, "99-graveyard.md"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(g_lines) + "\n")

    pack_index_rows = []
    for pid, pack in snapshot["packs"].items():
        fname = _render_pack_page(pack, packs_dir)
        f = pack["freshness"]
        dep_note = f" ({len(f['degraded_dependencies'])} dep stale)" if f.get("degraded_dependencies") else ""
        pack_index_rows.append(
            f"| **{pack['title']}** | `{pack['category']}` | {_badge(f)}{dep_note} | [**Open Playbook →**]({fname}) |"
        )

    idx_lines = [
        "← [🏠 Field Book Cover](../../README.md)",
        "",
        "# 🎯 Use-Case & Application Specialist Packs",
        "",
        "> [!IMPORTANT]",
        "> Each pack is an independently maintained manifest (`packs/*.yaml`) composed from atomic entities (`entities/*.yaml`). A stale tool degrades only its own pack—never the rest of the book.",
        "",
        *_render_table("Available Specialist Playbooks", ["Domain Pack", "Category", "Live Health", "Playbook"], pack_index_rows),
    ]
    with open(os.path.join(packs_dir, "README.md"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(idx_lines) + "\n")

    counts = snapshot["counts"]
    dig = snapshot["digest"]
    cover = [
        f"# ⚡ AI Swiss Knife — Modular Field Book (`v{snapshot['schema_version']}`)",
        "> A pace-layered, headless-first, self-policing AI Field Book for humans and autonomous agents.",
        "",
        f"**Snapshot Date:** `{snapshot['as_of']}` · **Entities:** `{counts['entities']}` (`{counts['agent_eligible_entities']}` agent-eligible) · **Use-Case Packs:** `{counts['packs']}` · **Aging/Stale/Degraded:** `{len(dig['aging'])} / {len(dig['stale'])} / {len(dig['degraded'])}`",
        "",
        "**Agent Manifests (Freshness-Gated):** [`llms.txt`](llms.txt) · [`llms-full.txt`](llms-full.txt) · [`dist/registry.json`](dist/registry.json)",
        "",
        "## 🧭 The 3-Second Universal Compass",
        "",
        "```mermaid",
        "flowchart LR",
        '    NEED["🎯 YOUR GOAL"] --> P1["PART I: MODELS & ACCESS<br/>Ch 01 Cloud · Ch 02 Local · Ch 03 Media"]',
        '    NEED --> P2["PART II: ENGINE ROOM<br/>Ch 04 Harnesses · Ch 05 Backends · Ch 06 RL Adapters"]',
        '    NEED --> PACKS["🎯 9 USE-CASE SPECIALIST PACKS<br/>Web · App · Game · RevEng · Research · Video · Social · Promo · Uncensored"]',
        '    NEED --> P3["PART III: VOLATILE RADAR<br/>Ch 07 Community IRL · Ch 08 Frontier Watch"]',
        "```",
        "",
        "## 📖 Core Field Book Chapters",
        "",
        "| Chapter | Part | Focus | Direct Link |",
        "| :--- | :--- | :--- | :--- |",
        "| **01 · Cloud APIs & Grounding** | `PART I` | Verified no-card gateways, Gemini 4 Hydrogen, System-1 Decisions & RAG | [**Open →**](book/01-cloud-apis.md) |",
        "| **02 · Local AI (16GB+64GB)** | `PART I` | **Track A:** Mature Riced (`Qwen3.8+LoRA`) vs **Track B:** Cutting-Edge (`Inkling 2 Mini`) | [**Open →**](book/02-local-16vram-64ram.md) |",
        "| **03 · Multimodal, 3D & Worlds** | `PART I` | Cloud-free vs local pivot for Image, Video (`WanGP`), Voice (`Drama 3`/`Phonon`) & 3D | [**Open →**](book/03-multimodal-sensory.md) |",
        "| **04 · Harnesses & Safety** | `PART II` | `Pi` Kernel, `DeepSeek Harness (dsh)`, `Hermes Agent`, `Antigravity` & `safeagents` | [**Open →**](book/04-harnesses-protocols.md) |",
        "| **05 · Backends & 2026 Flags** | `PART II` | `Unsloth`, `llama/ik_llama`, `WanGP v20.12`, `--n-cpu-moe` & OS/Silicon | [**Open →**](book/05-backends-flags-silicon.md) |",
        "| **06 · Harness Adapters & RL** | `PART II` | In-Harness `AsyncGRPO`, `OpenEnv`, Rank-96 Super-Adapter & Frontier RL | [**Open →**](book/06-adaptation-rl.md) |",
        "| **07 · Community IRL Builds** | `PART III` | Consumer 12–16GB engine hacks, `obra/superpowers`, & indie pipelines (`TTL 21d`) | [**Open →**](book/07-community-irl.md) |",
        "| **08 · Frontier Watch** | `PART III` | `MONITOR-ONLY` apex radar (`Claude Fable/Mythos`, `GPT-6.2`, `Gemini 4 Carbon`, `Qwen4-Max`) | [**Open →**](book/08-frontier-watch.md) |",
        "| **99 · The Graveyard** | `APPENDIX` | Machine-enforced cut list of dead cloud tiers & >80 GB local walls | [**Inspect →**](book/99-graveyard.md) |",
        "",
        "## 🎯 Independent Use-Case Specialist Packs (`packs/*.yaml`)",
        "",
        "| Domain Pack | Category | Live Health | Playbook |",
        "| :--- | :--- | :--- | :--- |",
        *[row.replace("](", "](book/packs/") for row in pack_index_rows],
        "",
        "## 🤖 Freshness-Gated CLI",
        "```bash",
        "python scripts/cli.py validate                       # Zero-HTML-leak, ref integrity & Graveyard check",
        "python scripts/cli.py query pack pack-reverse-eng    # Resolve fresh specialist stack as JSON",
        "python scripts/cli.py query local --lifecycle mature # Mature Riced local profiles only",
        "python scripts/cli.py build                          # Validate + compile Book, Packs & llms*.txt",
        "```",
    ]
    with open(os.path.join(root, "README.md"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(cover) + "\n")
