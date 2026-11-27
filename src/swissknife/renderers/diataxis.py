from __future__ import annotations

from pathlib import Path
from typing import Any

EVIDENCE_LABELS = {
    "primary-eval": "Primary evaluation",
    "official-docs": "Official documentation",
    "vendor-claim": "Vendor / lab claim",
    "field-note": "Field observation",
}


def _write(path: Path, lines: list[str]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def _link(name: str, url: str | None) -> str:
    return f"[{name}]({url})" if url else name


def _evidence(tier: str) -> str:
    return EVIDENCE_LABELS.get(tier, tier)


def _health_note(freshness: dict[str, Any]) -> str:
    st = freshness.get("effective_status") or freshness.get("status", "fresh")
    if st in ("fresh", "monitor-only"):
        return ""
    if st == "aging":
        return f" *(approaching review: {freshness['age_days']}d / {freshness['ttl_days']}d)*"
    if st == "stale":
        return " *(needs re-verification — excluded from agent routing)*"
    if st == "reverify-upstream":
        return " *(upstream dependency changed — re-verify)*"
    if st == "degraded":
        return " *(degraded — upstream archived or unreachable)*"
    return f" *({st})*"


def _alert_count(digest: dict[str, list[Any]]) -> int:
    return sum(len(digest.get(k, [])) for k in ("stale", "reverify-upstream", "degraded"))


def _page_header(as_of: str, digest: dict[str, list[Any]], section: str, title: str, depth: int = 1) -> list[str]:
    pfx = "../" * depth
    alerts = _alert_count(digest)
    status_text = "All tracked links healthy" if alerts == 0 else f"{alerts} item(s) need review"
    return [
        f"[Home]({pfx}README.md) / {section} / {title}",
        "",
        f"*Last verified: {as_of} · {status_text} ([System Status]({pfx}STATUS.md))*",
        "",
    ]


def _page_footer(links: list[tuple[str, str]]) -> list[str]:
    joined = " · ".join(f"[{label}]({href})" for label, href in links)
    return ["---", "", f"**Continue reading:** {joined}"]


def _details_block(summary: str, code: str, lang: str = "bash") -> list[str]:
    return [
        "<details>",
        f"<summary>{summary}</summary>",
        "",
        f"```{lang}",
        code.rstrip(),
        "```",
        "",
        "</details>",
        "",
    ]


class DiataxisRenderer:
    """Renders the human-first Diataxis handbook and quiet STATUS ledger."""

    def render(self, snapshot: dict[str, Any], root: Path) -> list[Path]:
        written: list[Path] = []
        written.append(self._render_readme(snapshot, root))
        written.append(self._render_status(snapshot, root))
        written.append(self._render_mental_model(snapshot, root))
        written.append(self._render_architecture_doc(snapshot, root))
        written.append(self._render_local_workstation_guide(snapshot, root))
        written.extend(self._render_goal_guides(snapshot, root))
        written.append(self._render_specialist_domains(snapshot, root))
        written.append(self._render_cloud_reference(snapshot, root))
        written.append(self._render_local_models_reference(snapshot, root))
        written.append(self._render_harnesses_runtimes_reference(snapshot, root))
        written.append(self._render_retired_reference(snapshot, root))
        written.append(self._render_harness_adapters_research(snapshot, root))
        written.append(self._render_watch_list(snapshot, root))
        return written

    def _render_readme(self, snap: dict[str, Any], root: Path) -> Path:
        alerts = _alert_count(snap["digest"])
        health_phrase = "All tracked links healthy" if alerts == 0 else f"{alerts} item(s) flagged for review"
        guides = snap["guides"]

        start_rows = [
            "| Use capable AI APIs right now for **$0 (no credit card)** | [Zero-Card Cloud APIs](reference/cloud-free-tiers.md) |",
            "| Run AI privately on a **16GB GPU + 64GB RAM** PC or **Apple Silicon Mac** | [Local AI Workstation Guide](guides/local-ai-workstation.md) |",
        ]
        if "coding-and-apps" in guides:
            start_rows.append("| Build web, CLI, or mobile software with coding agents | [Coding & Apps](guides/coding-and-apps.md) |")
        media_research_links = []
        if "research-and-writing" in guides:
            media_research_links.append("[Research & Writing](guides/research-and-writing.md)")
        if "local-media-studio" in guides:
            media_research_links.append("[Local Media Studio](guides/local-media-studio.md)")
        if media_research_links:
            start_rows.append(
                f"| Synthesize cited research or build a local media studio | {' · '.join(media_research_links)} |"
            )
        start_rows.extend([
            "| Explore specialist domains *(Reverse Engineering, Game Dev, Growth, Unfiltered Local)* | [Specialist Domains](guides/specialist-domains.md) |",
            "| Read primary benchmark evidence or track fast-moving changes | [Harness Adapters Research](research/harness-adapters.md) · [21-Day Watch List](research/watch-list.md) |",
        ])

        guide_toc = [
            "- [Local AI Workstation Guide](guides/local-ai-workstation.md) — Hardware memory zones, mature vs. experimental tracks, Ollama pitfalls, and CUDA/MLX launch commands."
        ]
        for gid, g in guides.items():
            guide_toc.append(f"- [{g['title']}](guides/{gid}.md) — {g['summary']}")
        guide_toc.append(
            "- [Specialist Domains](guides/specialist-domains.md) — Curated starting tools and monitored upstream directories for focused fields."
        )

        lines = [
            "# AI Swiss Knife",
            "",
            "A practical, source-verified field guide to building with zero-cost cloud APIs, local AI hardware, and open agent harnesses—continuously checked against link rot and outdated advice.",
            "",
            f"*Last verified: {snap['as_of']} · {health_phrase} ([System Status](STATUS.md)) · [For AI Agents (`llms.txt`)](llms.txt)*",
            "",
            "**New to local models or agent harnesses?** Start with [How a Modern AI Stack Fits Together](docs/mental-model.md)—a 3-minute plain-English primer explaining models, runtimes, harnesses, and adapters.",
            "",
            "## Start Here",
            "",
            "| If you want to... | Go to |",
            "| :--- | :--- |",
            *start_rows,
            "",
            "## Full Contents",
            "",
            "### Orientation",
            "- [How a Modern AI Stack Fits Together](docs/mental-model.md) — Plain-English concepts and system layers.",
            "- [How This Guide Is Maintained](docs/architecture.md) — For contributors: verification rules, data schema, and live link checks.",
            "",
            "### Practical Guides",
            *guide_toc,
            "",
            "### Reference",
            "- [Zero-Card Cloud Free Tiers](reference/cloud-free-tiers.md) — Verified card-free gateways, coding-agent token math, quotas, and fallback order.",
            "- [Local Models](reference/local-models.md) — Mature daily drivers, experimental architectures, and non-autoregressive decision models.",
            "- [Harnesses & Inference Runtimes](reference/harnesses-and-runtimes.md) — Agent harnesses, safety proxies, and serving engines.",
            "- [Retired & Disqualified Tools](reference/retired.md) — What stopped working, why it was cut, and what replaced it.",
            "",
            "### Research & Horizon",
            "- [Harness Adapters & In-Harness RL](research/harness-adapters.md) — Primary evidence for lightweight per-harness LoRAs, difficulty filtering, and out-of-distribution controls.",
            "- [21-Day Watch List](research/watch-list.md) — Strictly capped radar of frontier ceilings (monitor-only) and community field observations.",
            "",
            "## Editorial Standards",
            "",
            "1. **Every claim names its evidence:** Entries distinguish between *Primary evaluation*, *Official documentation*, *Vendor / lab claim*, and *Field observation*.",
            "2. **Every tool states its limits:** Nothing is listed without explicit boundary conditions explaining when *not* to use it.",
            "3. **Stale advice is automatically hidden from agents:** Automated link and review-window checks gate expired entries out of [`llms.txt`](llms.txt) until re-verified. See [System Status](STATUS.md).",
        ]
        return _write(root / "README.md", lines)

    def _render_status(self, snap: dict[str, Any], root: Path) -> Path:
        c = snap["counts"]
        dig = snap["digest"]
        lines = [
            "[Home](README.md) / System Status",
            "",
            "# System Status & Live Link Health",
            "",
            f"Snapshot date: **{snap['as_of']}** · Catalog entries: **{c['entries']}** ({c['agent_eligible']} eligible for `llms.txt`) · Supporting tool & directory links: **{c['external_links']}**.",
            "",
            "This ledger is updated automatically by the rolling link and freshness verifier. Healthy pages stay quiet; items requiring review are collected here.",
            "",
            "## Summary",
            "",
            "| Category | Count | Meaning |",
            "| :--- | :---: | :--- |",
            f"| Approaching review window | {len(dig['aging'])} | Past 75% of scheduled review interval; still active. |",
            f"| Needs re-verification | {len(dig['stale'])} | Past review window; automatically excluded from `llms.txt`. |",
            f"| Upstream dependency alert | {len(dig['reverify-upstream'])} | A base model or harness this item adapts has aged or degraded. |",
            f"| Degraded | {len(dig['degraded'])} | Upstream repository archived or unreachable for 3+ checks. |",
            f"| Retirement candidates | {len(dig['retirement_candidates'])} | Queued for removal into `reference/retired.md`. |",
            "",
            "## Core Catalog Entries",
            "",
            "| Entry | Category | Status | Verified | Review Window | Upstream Activity |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for entry in snap["entries"].values():
            f = entry["freshness"]
            pushed = f.get("upstream_pushed_at")
            pushed_str = pushed[:10] if pushed else "Not yet probed"
            lines.append(
                f"| {_link(entry['name'], entry['url'])} | `{entry['category']}` | `{f['effective_status']}` | {entry['last_verified']} | {f['ttl_days']}d | {pushed_str} |"
            )

        if snap.get("external_links"):
            lines.extend([
                "",
                "## Supporting Tools & Upstream Directories",
                "",
                "| Resource | Scope | Status | Verified | Upstream Activity |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ])
            for ext in snap["external_links"]:
                ef = ext["freshness"]
                pushed = ef.get("upstream_pushed_at")
                pushed_str = pushed[:10] if pushed else "Not yet probed"
                lines.append(
                    f"| {_link(ext['name'], ext['url'])} | `{ext['scope']}` | `{ef['effective_status']}` | {ext['last_verified']} | {pushed_str} |"
                )

        return _write(root / "STATUS.md", lines)

    def _render_mental_model(self, snap: dict[str, Any], root: Path) -> Path:
        lines = [
            *_page_header(snap["as_of"], snap["digest"], "Orientation", "How a Modern AI Stack Fits Together"),
            "# How a Modern AI Stack Fits Together",
            "",
            "If you are new to running open-weight models or coding agents, the vocabulary can blur together quickly. A practical AI setup is not one monolithic program—it is five replaceable layers working in sequence.",
            "",
            "```mermaid",
            "flowchart TB",
            '    L1["1. Interface — Terminal, IDE (Zed), or Messaging App"]',
            '    L2["2. Agent Harness — Manages tool calls, context, and loops (Pi, Hermes, DeepSeek Harness)"]',
            '    L3["3. Safety Boundary — Inspects or blocks risky tool calls (safeagents, Laya)"]',
            '    L4["4. Inference Runtime — Loads weights onto GPU/RAM (llama.cpp, Unsloth, MLX)"]',
            '    L5["5. Weights + Optional LoRA Adapter — Frozen base model + small task/harness adapter"]',
            "    L1 --> L2 --> L3 --> L4 --> L5",
            "```",
            "",
            "## What Each Layer Does",
            "",
            "1. **Base Model (Weights):** The trained neural network (for example, `Qwen3.8-27B` or `Inkling 2 Mini`). You can access capable models through a [zero-card cloud API](../reference/cloud-free-tiers.md) or run open weights privately on your own hardware.",
            "2. **Adapter (Optional LoRA):** A small add-on file (26 MB to 912 MB) loaded alongside a frozen base model to specialize it for a specific agent harness or policy without duplicating the 15 GB base file. See [Harness Adapters Research](../research/harness-adapters.md).",
            "3. **Inference Runtime:** The serving engine (`llama.cpp`, `Unsloth`, or Apple `MLX`) that loads model files into GPU VRAM or unified memory and exposes an OpenAI- or Anthropic-compatible HTTP endpoint.",
            "4. **Safety Boundary:** An optional proxy (`safeagents`) or lightweight non-autoregressive decision model (`Laya`) sitting between the harness and your shell/files so autonomous tool calls are audited before execution.",
            "5. **Agent Harness:** The control loop (`Pi`, `DeepSeek Harness`, `Hermes Agent`, `OpenCode`) that sends prompts, executes file edits or shell commands, compacts long context, and feeds results back to the model.",
            "",
            *_page_footer([
                ("Zero-Card Cloud APIs", "../reference/cloud-free-tiers.md"),
                ("Local AI Workstation Guide", "../guides/local-ai-workstation.md"),
            ]),
        ]
        return _write(root / "docs/mental-model.md", lines)

    def _render_architecture_doc(self, snap: dict[str, Any], root: Path) -> Path:
        lines = [
            *_page_header(snap["as_of"], snap["digest"], "Orientation", "How This Guide Is Maintained"),
            "# How This Guide Is Maintained",
            "",
            "This page is for maintainers and contributors. Readers do not need to understand these internals to use the guide.",
            "",
            "## Design Principles",
            "",
            "- **Headless data, declarative views:** All factual entries live in seven plain-data YAML files under `catalog/`. Markdown pages and `llms.txt` are compiled from a single typed JSON snapshot (`dist/catalog.json`) and are never hand-edited.",
            "- **Canonical URL Law:** Automated validation rejects uncheckable placeholder URLs (such as GitHub `/topics/` pages, generic model directories, or subreddit homepages) so every link can be verified programmatically.",
            "- **Review Windows & Freshness Gating:** Each entry carries a decay class (`volatile`: 21 days, `operational`: 60 days, `stable`: 120 days). When an entry passes its review window or fails 3 consecutive health checks, it is automatically omitted from `llms.txt` until re-verified.",
            "- **Relational Compatibility:** Entries declare three lightweight relationships (`runs_on`, `adapts`, `guards`). When a base model or harness degrades, adapters referencing it automatically raise an upstream review alert.",
            "",
            "## Local Maintainer Workflow",
            "",
            "```bash",
            "pip install -e .",
            "python -m unittest discover -s tests -t . -v",
            "swissknife validate",
            "swissknife build",
            "```",
            "",
            *_page_footer([
                ("Contributing Guidelines", "../CONTRIBUTING.md"),
                ("System Status", "../STATUS.md"),
            ]),
        ]
        return _write(root / "docs/architecture.md", lines)

    def _render_local_workstation_guide(self, snap: dict[str, Any], root: Path) -> Path:
        entries = snap["entries"]
        adapters_for = snap["indices"].get("adapters_for", {})
        local_models = [
            e for e in entries.values()
            if e["kind"] == "model" and e["category"] in ("local-mature", "local-experimental", "local-decision")
        ]

        lines = [
            *_page_header(snap["as_of"], snap["digest"], "Guides", "Local AI Workstation Guide"),
            "# Local AI Workstation Guide",
            "",
            "Running capable AI models locally comes down to one physical constraint: **memory bandwidth**. Models that fit inside GPU VRAM run fast; dense models that spill into system RAM slow to a crawl—unless they use a sparse Mixture-of-Experts (MoE) architecture.",
            "",
            "## How the 16GB VRAM + 64GB RAM Memory Split Works",
            "",
            "```mermaid",
            "flowchart LR",
            '    subgraph Z1 ["Zone 1: Pure 16GB VRAM (Fastest)"]',
            '        D["Dense 12B–27B Model + Optional LoRA + Q8 KV Cache<br/>100% resident in GPU VRAM (Zero PCIe bottleneck)"]',
            "    end",
            '    subgraph Z2 ["Zone 2: 16GB VRAM + 64GB DDR5 Hybrid (Sparse MoE Only)"]',
            '        GPU["16GB GPU VRAM: Attention Layers + KV Cache + Hot Experts"]',
            '        RAM["64GB System RAM: Cold Sparse MoE Experts (--n-cpu-moe)"]',
            "        GPU <--> RAM",
            "    end",
            "```",
            "",
            "- **Apple Silicon Macs (Unified Memory):** CPU and GPU share one memory pool, eliminating the PCIe split. Use `mlx-lm` or `llama.cpp` Metal; 32GB+ unified memory is comfortable for 27B models.",
            "- **Why dense 70B models are excluded:** Offloading a dense 70B model onto 64GB system RAM forces every token through CPU memory bandwidth (~2–4 tok/s). Sparse MoEs (`Qwen3-Coder-Next`, `Inkling 2 Mini`) activate only 3B–5.4B parameters per token, staying responsive in hybrid mode.",
            "",
            "> [!WARNING]",
            "> **Common Local Pitfall — Ollama's 4K Default Context Trap:** Below 24 GiB VRAM, Ollama defaults to a **4,096-token context window** (32K on 24–48 GiB, 256K only on 48 GiB+), which silently causes coding agents to drop system instructions and break tool loops. In addition, Ollama's OpenAI-compatible `/v1/chat/completions` endpoint has a reported hang issue on `qwen3.8:27b`. For agentic coding, prefer `llama-server` (with explicit `-c 32768` or `-c 65536`) or `mlx_lm.server` on Apple Silicon.",
            "",
            "## Two Local Tracks: Keep Them Separate",
            "",
            "1. **Mature Daily Drivers:** Battle-tested models with predictable runtime flags and verified LoRA adapters. Use these for daily work.",
            "2. **Experimental Architectures:** Newer looped-layer or extreme-quant models with high upside but rougher edges (such as debug-loop sensitivity). Test these in a sandbox before relying on them.",
            "",
            "## Recommended Starter Setups",
            "",
        ]

        for cat, heading in (
            ("local-mature", "### Mature Daily Drivers"),
            ("local-experimental", "### Experimental Local Architectures"),
            ("local-decision", "### Lightweight Decision & Safety Models (CPU / NPU)"),
        ):
            group = [m for m in local_models if m["category"] == cat]
            if not group:
                continue
            lines.extend([heading, ""])
            for m in group:
                note = _health_note(m["freshness"])
                lines.append(f"#### {_link(m['name'], m['url'])}{note}")
                lines.append("")
                lines.append(m["summary"])
                lines.append("")
                lines.append(f"- **When to use:** {m['when_to_use']}")
                if m.get("footprint"):
                    lines.append(f"- **Memory footprint:** {m['footprint']}")
                if m.get("license"):
                    lines.append(f"- **License:** {m['license']}")
                lines.append(f"- **Evidence:** {_evidence(m['evidence_tier'])}")
                compat = adapters_for.get(m["id"], [])
                if compat:
                    links = ", ".join(_link(entries[a]["name"], entries[a]["url"]) for a in compat if a in entries)
                    lines.append(f"- **Compatible hot-swappable adapters:** {links}")
                for lim in m["limitations"]:
                    lines.append(f"- **Limitation:** {lim}")
                lines.append("")
                if m.get("launch_recipe"):
                    lines.extend(_details_block("Launch command (16GB VRAM / CUDA / llama-server)", m["launch_recipe"]))
                if m.get("mac_launch_recipe"):
                    lines.extend(_details_block("Launch command (Apple Silicon Mac / MLX)", m["mac_launch_recipe"]))

        lines.extend(_page_footer([
            ("Local Models Reference", "../reference/local-models.md"),
            ("Harnesses & Inference Runtimes", "../reference/harnesses-and-runtimes.md"),
            ("Harness Adapters Research", "../research/harness-adapters.md"),
        ]))
        return _write(root / "guides/local-ai-workstation.md", lines)

    def _render_goal_guides(self, snap: dict[str, Any], root: Path) -> list[Path]:
        written: list[Path] = []
        entries = snap["entries"]

        for gid, guide in snap["guides"].items():
            res = guide["resolved"]
            lines = [
                *_page_header(snap["as_of"], snap["digest"], "Guides", guide["title"]),
                f"# {guide['title']}",
                "",
                guide["summary"],
                "",
                "## Recommended Stack",
                "",
                "The components below are selected for this workflow based on verified compatibility and current link health.",
                "",
            ]

            for label, bucket in (
                ("Models & Cloud Gateways", res["models_and_gateways"]),
                ("Agent Harnesses", res["harnesses"]),
                ("Inference & Media Runtimes", res["runtimes"]),
                ("Compatible LoRA Adapters", res["adapters"]),
                ("Safety Boundaries", res["guards"]),
            ):
                if not bucket:
                    continue
                lines.append(f"### {label}")
                lines.append("")
                for item in bucket:
                    note = _health_note(item["freshness"])
                    full = entries.get(item["id"], {})
                    desc = full.get("when_to_use") or full.get("summary") or ""
                    ev = f" *({_evidence(item['evidence_tier'])})*" if item.get("evidence_tier") else ""
                    lines.append(f"- **{_link(item['name'], item['url'])}**{note} — {desc}{ev}")
                lines.append("")

            if guide.get("tools"):
                lines.extend(["## Supporting Domain Tools", ""])
                for tool in guide["tools"]:
                    note = _health_note(tool["freshness"])
                    desc = f" — {tool['summary']}" if tool.get("summary") else ""
                    lines.append(f"- **{_link(tool['name'], tool['url'])}**{note}{desc}")
                lines.append("")

            lines.extend(["## Step-by-Step Workflow", ""])
            for idx, step in enumerate(guide.get("steps", []), 1):
                lines.append(f"{idx}. {step}")
            lines.append("")

            if guide.get("limitations"):
                lines.extend(["## Limitations & Trade-Offs", ""])
                for lim in guide["limitations"]:
                    lines.append(f"- {lim}")
                lines.append("")

            lines.extend(_page_footer([
                ("Local AI Workstation Guide", "local-ai-workstation.md"),
                ("Specialist Domains", "specialist-domains.md"),
            ]))
            written.append(_write(root / "guides" / f"{gid}.md", lines))
        return written

    def _render_specialist_domains(self, snap: dict[str, Any], root: Path) -> Path:
        lines = [
            *_page_header(snap["as_of"], snap["digest"], "Guides", "Specialist Domains"),
            "# Specialist Domains",
            "",
            "Rather than duplicating fast-moving niche tool catalogs, each domain below pairs your verified local or cloud stack with at most two direct starting tools and a monitored upstream directory for deeper exploration.",
            "",
        ]
        for spec in snap["specialists"].values():
            res = spec["resolved"]
            hub = spec["upstream_directory"]
            pushed = hub["freshness"].get("upstream_pushed_at")
            pushed_note = f" *(upstream last updated {pushed[:10]})*" if pushed else ""

            models = ", ".join(_link(m["name"], m["url"]) for m in res["models_and_gateways"]) or "See Local Models Reference"
            adapters = ", ".join(_link(a["name"], a["url"]) for a in res["adapters"])
            guards = ", ".join(_link(g["name"], g["url"]) for g in res["guards"])

            lines.extend([
                f"## {spec['title']}",
                "",
                spec["summary"],
                "",
                f"- **Recommended base stack:** {models}",
            ])
            if adapters:
                lines.append(f"- **Compatible adapters:** {adapters}")
            if guards:
                lines.append(f"- **Recommended safety layer:** {guards}")

            lines.append("- **Direct starting tools:**")
            for pick in spec.get("direct_picks", []):
                note = _health_note(pick["freshness"])
                desc = f" — {pick['summary']}" if pick.get("summary") else ""
                lines.append(f"  - **{_link(pick['name'], pick['url'])}**{note}{desc}")

            lines.append(f"- **Broader upstream directory:** **{_link(hub['name'], hub['url'])}**{_health_note(hub['freshness'])}{pushed_note}")
            for g in spec.get("limitations", []):
                lines.append(f"- **Guardrail:** {g}")
            lines.append("")

        lines.extend(_page_footer([
            ("Local Models Reference", "../reference/local-models.md"),
            ("21-Day Watch List", "../research/watch-list.md"),
        ]))
        return _write(root / "guides/specialist-domains.md", lines)

    def _render_cloud_reference(self, snap: dict[str, Any], root: Path) -> Path:
        entries = list(snap["entries"].values())
        gateways = [e for e in entries if e["kind"] == "gateway"]
        grounding = [e for e in entries if e["category"] == "grounding"]

        lines = [
            *_page_header(snap["as_of"], snap["digest"], "Reference", "Zero-Card Cloud Free Tiers"),
            "# Zero-Card Cloud Free Tiers",
            "",
            "Every API listed here has been verified to work without a credit card on file. Because free quotas change frequently, entries carry a 21-day review window and are automatically removed from `llms.txt` if they expire.",
            "",
            "## Coding Agent Token Math (Why Most Free Tiers Fail)",
            "",
            "A real autonomous coding agent (`Pi`, `Hermes Agent`, `OpenCode`, or `DeepSeek Harness`) sends roughly **20,000 input tokens per step** and takes **~15 steps per bug fix (~300,000 tokens per task)**.",
            "",
            "- **Groq's 8,000 TPM free limit** hits HTTP 429 on Step 1 of a coding loop—reserve Groq for fast `<6K`-token classifiers and free Whisper audio transcription.",
            "- **Unverified OpenRouter (`50 RPD`)** exhausts a day's allowance in roughly three multi-step coding tasks.",
            "- **Google AI Studio (`gemini-4-hydrogen` / `3.8 Flash`)** and **Z.ai (`glm-4.7-flash`)** are the primary card-free cloud gateways that can sustain multi-step repository loops.",
            "",
            "## Language & Decision Gateways",
            "",
            "| Provider | Default Model | Free Quota | Key Limitation |",
            "| :--- | :--- | :--- | :--- |",
        ]
        for g in gateways:
            note = _health_note(g["freshness"])
            lim = g["limitations"][0] if g["limitations"] else "—"
            lines.append(
                f"| {_link(g['name'], g['url'])}{note} | `{g.get('default_model') or '—'}` | {g.get('quota') or 'See docs'} | {lim} |"
            )

        lines.extend(["", "## Gateway Details", ""])
        for g in gateways:
            note = _health_note(g["freshness"])
            lines.append(f"### {_link(g['name'], g['url'])}{note}")
            lines.append("")
            lines.append(g["summary"])
            lines.append("")
            lines.append(f"- **When to use:** {g['when_to_use']}")
            if g.get("base_url"):
                lines.append(f"- **OpenAI-compatible endpoint:** `{g['base_url']}` (env: `{g.get('env_key') or 'Keyless'}`)")
            lines.append(f"- **Evidence:** {_evidence(g['evidence_tier'])} · verified {g['last_verified']}")
            for lim in g["limitations"]:
                lines.append(f"- **Limitation:** {lim}")
            lines.append("")

        if grounding:
            lines.extend([
                "## Search, Scraping & Academic Grounding",
                "",
                "| Service | Free Allocation | Best Used For | Limitation |",
                "| :--- | :--- | :--- | :--- |",
            ])
            for t in grounding:
                note = _health_note(t["freshness"])
                lim = t["limitations"][0] if t["limitations"] else "—"
                lines.append(
                    f"| {_link(t['name'], t['url'])}{note} | {t.get('quota') or '—'} | {t['when_to_use']} | {lim} |"
                )
            lines.append("")

        if snap.get("routing_chains"):
            lines.extend(["## Suggested Fallback Order by Task", ""])
            for intent, chain in snap["routing_chains"].items():
                names = " -> ".join(snap["entries"][cid]["name"] for cid in chain if cid in snap["entries"])
                lines.append(f"- **`{intent}`:** {names}")
            lines.append("")

        lines.extend(_page_footer([
            ("Local AI Workstation Guide", "../guides/local-ai-workstation.md"),
            ("Retired & Disqualified Tools", "retired.md"),
        ]))
        return _write(root / "reference/cloud-free-tiers.md", lines)

    def _render_local_models_reference(self, snap: dict[str, Any], root: Path) -> Path:
        models = [e for e in snap["entries"].values() if e["kind"] == "model"]
        lines = [
            *_page_header(snap["as_of"], snap["digest"], "Reference", "Local Models"),
            "# Local Models Reference",
            "",
            "Factual index of verified open-weight models fitting within the starter hardware envelopes (`16GB VRAM + 64GB RAM` or `Apple Silicon Mac`). For memory-layout concepts and setup walkthroughs, see the [Local AI Workstation Guide](../guides/local-ai-workstation.md).",
            "",
            "| Model | Track | Footprint | License | Evidence | Primary Limitation |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for m in models:
            note = _health_note(m["freshness"])
            lim = m["limitations"][0] if m["limitations"] else "—"
            lines.append(
                f"| {_link(m['name'], m['url'])}{note} | `{m['lifecycle']}` | {m.get('footprint') or '—'} | `{m.get('license') or '—'}` | {_evidence(m['evidence_tier'])} | {lim} |"
            )
        lines.append("")
        lines.extend(_page_footer([
            ("Local AI Workstation Guide", "../guides/local-ai-workstation.md"),
            ("Harnesses & Inference Runtimes", "harnesses-and-runtimes.md"),
        ]))
        return _write(root / "reference/local-models.md", lines)

    def _render_harnesses_runtimes_reference(self, snap: dict[str, Any], root: Path) -> Path:
        entries = list(snap["entries"].values())
        harnesses = [e for e in entries if e["kind"] == "harness"]
        safety = [e for e in entries if e["category"] == "safety"]
        runtimes = [e for e in entries if e["kind"] == "runtime"]

        lines = [
            *_page_header(snap["as_of"], snap["digest"], "Reference", "Harnesses & Runtimes"),
            "# Harnesses, Safety Proxies & Inference Runtimes",
            "",
            "Practical reference for the control loops that execute agent workflows, the safety proxies that audit tool calls, and the engines that serve local weights.",
            "",
            "## Agent Harnesses",
            "",
        ]
        for h in harnesses:
            note = _health_note(h["freshness"])
            role = f" — *{h['role']}*" if h.get("role") else ""
            lines.append(f"### {_link(h['name'], h['url'])}{role}{note}")
            lines.append("")
            lines.append(h["summary"])
            lines.append("")
            lines.append(f"- **When to use:** {h['when_to_use']}")
            lines.append(f"- **License:** `{h.get('license') or '—'}` · **Evidence:** {_evidence(h['evidence_tier'])}")
            for lim in h["limitations"]:
                lines.append(f"- **Limitation:** {lim}")
            lines.append("")
            if h.get("launch_recipe"):
                lines.extend(_details_block("Show quickstart command", h["launch_recipe"]))

        if safety:
            lines.extend(["## Safety Boundaries", ""])
            for s in safety:
                note = _health_note(s["freshness"])
                lines.append(f"### {_link(s['name'], s['url'])}{note}")
                lines.append("")
                lines.append(s["summary"])
                lines.append("")
                lines.append(f"- **When to use:** {s['when_to_use']}")
                for lim in s["limitations"]:
                    lines.append(f"- **Limitation:** {lim}")
                lines.append("")
                if s.get("launch_recipe"):
                    lines.extend(_details_block("Show proxy command", s["launch_recipe"]))

        if runtimes:
            lines.extend([
                "## Inference & Media Runtimes",
                "",
                "| Runtime | Best Used For | License | Key Limitation |",
                "| :--- | :--- | :--- | :--- |",
            ])
            for r in runtimes:
                note = _health_note(r["freshness"])
                lim = r["limitations"][0] if r["limitations"] else "—"
                lines.append(
                    f"| {_link(r['name'], r['url'])}{note} | {r['when_to_use']} | `{r.get('license') or '—'}` | {lim} |"
                )
            lines.append("")

        lines.extend(_page_footer([
            ("Harness Adapters Research", "../research/harness-adapters.md"),
            ("Local Models Reference", "local-models.md"),
        ]))
        return _write(root / "reference/harnesses-and-runtimes.md", lines)

    def _render_retired_reference(self, snap: dict[str, Any], root: Path) -> Path:
        entries = snap["entries"]
        lines = [
            *_page_header(snap["as_of"], snap["digest"], "Reference", "Retired & Disqualified Tools"),
            "# Retired & Disqualified Tools",
            "",
            "Free tiers close, endpoints deprecate, and some open models exceed consumer workstation memory. Items below are blocked by automated validation across core entries, guides, specialist directories, and community notes so outdated advice cannot creep back into the guide.",
            "",
            "| Area | Item | Retired / Verified | Why Disqualified | Active Alternative |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
        for r in snap["retired"]:
            rep_id = r.get("replaced_by")
            rep = _link(entries[rep_id]["name"], entries[rep_id]["url"]) if rep_id and rep_id in entries else "—"
            lines.append(f"| {r['category'].title()} | {r['name']} | {r['retired_on'] or '—'} | {r['reason']} | {rep} |")
        lines.append("")
        lines.extend(_page_footer([
            ("Zero-Card Cloud Free Tiers", "cloud-free-tiers.md"),
            ("System Status", "../STATUS.md"),
        ]))
        return _write(root / "reference/retired.md", lines)

    def _render_harness_adapters_research(self, snap: dict[str, Any], root: Path) -> Path:
        items = [e for e in snap["entries"].values() if e["kind"] == "adapter" or e["category"] == "rl-research"]
        lines = [
            *_page_header(snap["as_of"], snap["digest"], "Research", "Harness Adapters & In-Harness RL"),
            "# Harness Adapters & In-Harness Reinforcement Learning",
            "",
            "A central empirical finding in 2026 agent engineering is that **adapting a frozen mid-sized model to a specific harness** often delivers larger accuracy gains and far lower token cost than moving to a heavier unadapted model.",
            "",
            "> **Note on benchmark comparability:** Vendor-reported scores for `Qwen3.8-27B` are measured on Qwen's own internal harness. In Hugging Face's independent reproduction using the `pi` harness with thinking off, base `Qwen3.8-27B` scored **39% pass@1** on Terminal-Bench 2.1 using **2.9K tokens/task**—and adding an RL-trained LoRA lifted it to **55% pass@1** while cutting usage to **1.5K tokens/task**.",
            "",
            "## Choosing the Right Adapter",
            "",
            "```mermaid",
            "flowchart TD",
            '    Q1{"Running a single harness<br/>with thinking mode OFF?"}',
            '    Q1 -- "Yes" --> A1["Use the single-harness Specialist LoRA<br/>(Highest pass@1 on that harness, ~304 MiB)"]',
            '    Q1 -- "No (Thinking ON or multiple harnesses)" --> A2["Use the Rank-96 Merged Super-Adapter<br/>(One adapter across Pi, Hermes, & OpenCode, ~912 MiB)"]',
            "```",
            "",
            "## Verified Adapters & Methodology",
            "",
        ]
        for item in items:
            note = _health_note(item["freshness"])
            lines.append(f"### {_link(item['name'], item['url'])}{note}")
            lines.append("")
            lines.append(item["summary"])
            lines.append("")
            lines.append(f"- **When to use:** {item['when_to_use']}")
            lines.append(f"- **Evidence tier:** {_evidence(item['evidence_tier'])} · verified {item['last_verified']}")
            for ev in item.get("evidence_notes", []):
                lines.append(f"- **Observation:** {ev}")
            for lim in item["limitations"]:
                lines.append(f"- **Caveat / boundary:** {lim}")
            for tbl in item.get("eval_tables", []):
                hdrs = tbl["headers"]
                lines.extend([
                    "",
                    f"**{tbl['title']}**",
                    "",
                    "| " + " | ".join(hdrs) + " |",
                    "| " + " | ".join(":---" for _ in hdrs) + " |",
                ])
                for row in tbl["rows"]:
                    lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
            lines.append("")
            if item.get("launch_recipe"):
                lines.extend(_details_block("Show serving command (llama-server / vLLM)", item["launch_recipe"]))
            if item.get("mac_launch_recipe"):
                lines.extend(_details_block("Show serving command (Apple Silicon Mac / MLX)", item["mac_launch_recipe"]))

        lines.extend(_page_footer([
            ("Local AI Workstation Guide", "../guides/local-ai-workstation.md"),
            ("21-Day Watch List", "watch-list.md"),
        ]))
        return _write(root / "research/harness-adapters.md", lines)

    def _render_watch_list(self, snap: dict[str, Any], root: Path) -> Path:
        lines = [
            *_page_header(snap["as_of"], snap["digest"], "Research", "21-Day Watch List"),
            "# 21-Day Watch List",
            "",
            "Fast-moving developments are tracked here under strict size limits (maximum 5 frontier items and 5 community field notes) and a 21-day review window. Frontier items are strictly **monitor-only** and are excluded from automated agent routing (`llms.txt`).",
            "",
            "## Frontier Ceiling (Monitor-Only)",
            "",
            "Tracked to observe capability ceilings, caching/harness innovations, and signals of what will trickle down to free or local tiers next.",
            "",
        ]
        for item in snap["watch"]["frontier"]:
            f = item["freshness"]
            left = max(0, f["ttl_days"] - f["age_days"])
            lines.append(f"### {_link(item['name'], item['url'])}")
            lines.append("")
            lines.append(item["summary"])
            lines.append("")
            lines.append(f"- **Evidence:** {_evidence(item['evidence_tier'])} · **Review window:** {left} days remaining")
            for lim in item["limitations"]:
                lines.append(f"- **Boundary:** {lim}")
            lines.append("")

        lines.extend([
            "## Community Field Observations",
            "",
            "Reproducible workflows, runtime breakthroughs, and community tooling observed in real use.",
            "",
        ])
        for item in snap["watch"]["community"]:
            f = item["freshness"]
            left = max(0, f["ttl_days"] - f["age_days"])
            note = _health_note(f)
            lines.append(f"### {_link(item['name'], item['url'])}{note}")
            lines.append("")
            lines.append(item["summary"])
            lines.append("")
            lines.append(f"- **Evidence:** {_evidence(item['evidence_tier'])} · **Review window:** {left} days remaining")
            for lim in item["limitations"]:
                lines.append(f"- **Boundary:** {lim}")
            lines.append("")

        lines.extend(_page_footer([
            ("Home", "../README.md"),
            ("System Status", "../STATUS.md"),
        ]))
        return _write(root / "research/watch-list.md", lines)
