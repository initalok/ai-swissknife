from __future__ import annotations

import os
from typing import Any

BADGES = {
    "fresh": "🟢 `Fresh`",
    "aging": "🟡 `Aging`",
    "stale": "🟠 `Stale`",
    "reverify_upstream": "🟣 `Re-Verify Upstream`",
    "degraded": "🔴 `Degraded`",
    "monitor_only": "🔭 `Monitor-Only`",
    "graveyard": "🪦 `Graveyard`",
}


def _badge(f: dict[str, Any]) -> str:
    st = f.get("effective_status") or f.get("status", "fresh")
    return BADGES.get(st, f"`{st}`")


def _link(name: str, url: str | None) -> str:
    return f"[**{name}**]({url})" if url else f"**{name}**"


def _write(path: str, lines: list[str]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines) + "\n")


def _render_nav(active: str, depth: int = 1) -> str:
    pfx = "../" if depth == 1 else ""
    items = [
        ("🏠 Hub", f"{pfx}README.md"),
        ("☁️ Cloud", f"{pfx}book/cloud.md"),
        ("🖥️ Local", f"{pfx}book/local.md"),
        ("⚙️ Harnesses & RL", f"{pfx}book/harnesses-and-rl.md"),
        ("📘 Playbooks", f"{pfx}book/playbooks.md"),
        ("🧭 Spokes", f"{pfx}book/spokes.md"),
        ("📡 Radar", f"{pfx}book/radar.md"),
        ("🪦 Graveyard", f"{pfx}book/graveyard.md"),
    ]
    return " &nbsp;·&nbsp; ".join(f"**{lbl}**" if lbl == active else f"[{lbl}]({href})" for lbl, href in items)


def _render_dashboard(snap: dict[str, Any], root: str) -> None:
    c = snap["counts"]
    dig = snap["digest"]
    by_prof = snap.get("by_profile", {})

    lines = [
        f"# ⚡ AI Swiss Knife (`v{snap['schema_version']}`)",
        "> A lean, Hub-and-Spoke, self-policing AI Field Book with built-in live health, implicit graph state, and freshness-gated agent manifests.",
        "",
        _render_nav("🏠 Hub", depth=0),
        "",
        f"**Live Pulse (`{snap['as_of']}`):** `{c['core_nodes']}` Core Nodes (`{c['agent_eligible_nodes']}` agent-eligible) · `{c['playbooks']}` Deep Playbooks · `{c['spokes']}` Upstreamed Spokes · Alerts: `{len(dig['aging'])}` Aging / `{len(dig['stale'])}` Stale / `{len(dig['reverify_upstream'])}` Upstream / `{len(dig['degraded'])}` Degraded",
        "",
        "**Agent Surface (Freshness-Gated):** [`llms.txt`](llms.txt) · [`llms-full.txt`](llms-full.txt) · [`dist/graph.json`](dist/graph.json)",
        "",
        "## 🖥️ Start From Your Hardware Profile",
        "> Entry points below are data-driven (`graph/profiles.yaml`) and expandable without code changes.",
        "",
        "| Profile | Hardware Envelope | Active Core Nodes | Jump In |",
        "| :--- | :--- | :---: | :--- |",
    ]
    for pid, prof in snap["profiles"].items():
        node_count = len(by_prof.get(pid, []))
        target = "book/cloud.md" if pid == "zero-card-cloud" else "book/local.md"
        lines.append(f"| **{prof['name']}** (`{pid}`) | {prof['summary']} | `{node_count}` | [**Open Blueprint →**]({target}) |")

    lines.extend([
        "",
        "## 🧭 Hub-and-Spoke Topology",
        "",
        "```mermaid",
        "flowchart LR",
        '    HUB["⚡ OWNED CORE (Canonical Nodes)<br/>Cloud · Local (Mature vs Edge) · Harnesses · RL Adapters"]',
        '    PB["📘 3 DEEP PLAYBOOKS<br/>Coding & Apps · Research · Local Media Studio"]',
        '    SP["🧭 4 UPSTREAMED SPOKES<br/>Reverse Eng · Game Dev · Growth & Social · Unfiltered"]',
        '    RAD["📡 CAPPED 21d RADAR<br/>Monitor-Only Frontier (<=5) · Community IRL (<=5)"]',
        "    HUB --> PB & SP",
        "    RAD -.-> HUB",
        "```",
        "",
        "## 🗺️ Directory Map",
        "",
        "### Owned Core (Domain-Native Blueprints)",
        "- **☁️ [Cloud Gateways & Grounding](book/cloud.md)** — Verified zero-card APIs, Gemini 4 Hydrogen, System-1 Decisions & RAG routing circuit.",
        "- **🖥️ [Local AI Blueprints](book/local.md)** — Track A (*Mature Riced*) vs. Track B (*Cutting-Edge*), hot-swappable LoRAs, & System-1 `Laya 0.5`.",
        "- **⚙️ [Harnesses, Backends & RL Lab Dossier](book/harnesses-and-rl.md)** — `Pi` Kernel, `DeepSeek Harness`, `Hermes Agent`, `safeagents`, & HF Harness Adapters lab tables.",
        "",
        "### Horizons & Monitoring",
        "- **📘 [3 Deep Owned Playbooks](book/playbooks.md)** — End-to-end runbooks for *Coding & Apps*, *Research & Grounding*, and *Local Media Studio*.",
        "- **🧭 [4 Upstreamed Horizon Spokes](book/spokes.md)** — Lean, live-monitored entry points into *Reverse Engineering*, *Game Dev & 3D*, *Growth & Social*, and *Unfiltered Sovereign*.",
        "- **📡 [Capped 21-Day Radar](book/radar.md)** — Monitor-Only Frontier Watch & Community IRL Field Log.",
        "- **🪦 [The Graveyard](book/graveyard.md)** — CI-enforced cut list with live replacement pointers.",
        "",
        "## 🤖 Implicit State CLI",
        "```bash",
        "python scripts/cli.py validate                                   # Canonical URL Law + Budgets + 4-Edge check",
        "python scripts/cli.py resolve coding-and-apps --profile 16vram-64ram",
        "python scripts/cli.py resolve reverse-engineering --profile 16vram-64ram",
        "python scripts/cli.py build                                      # Compile GitHub Views, llms*.txt & graph.json",
        "```",
    ])
    _write(os.path.join(root, "README.md"), lines)


def _render_cloud(snap: dict[str, Any], root: str) -> None:
    nodes = list(snap["nodes"].values())
    gateways = [n for n in nodes if n["kind"] == "gateway"]
    grounding = [n for n in nodes if n.get("domain") == "grounding"]
    nav = _render_nav("☁️ Cloud")

    lines = [
        nav,
        "",
        "# ☁️ Zero-Card Cloud Gateways & Grounding",
        "",
        "> [!IMPORTANT]",
        "> Every gateway below is verified card-free and carries a `volatile` 21-day TTL. Expired gateways are automatically gated out of `llms.txt` until re-verified.",
        "",
        "```mermaid",
        "flowchart LR",
        '    W1["Coding / 1M Ctx"] --> G1["Google AI Studio (4 Hydrogen / 3.8 Flash)"]',
        '    W1 -.-> G2["Z.ai BigModel (GLM-4.7-Flash 200K)"]',
        '    W2["500B+ MoE Reasoning"] --> G3["NVIDIA NIM / OpenRouter :free"]',
        '    W3["System-1 Decisions ($0 Out)"] --> G4["Gemini Decision 1 / Cloudflare Clef"]',
        '    W4["<6K Fast JSON / Whisper STT"] --> G5["Groq Cloud (8K TPM Wall)"]',
        "```",
        "",
        "## 1. Verified Gateways (Quota Cards)",
        "",
    ]
    for g in gateways:
        f = g["freshness"]
        env_key = g.get("env_key") or "Keyless"
        lines.append(f"### {_link(g['name'], g['url'])} · {_badge(f)}")
        lines.append(f"- **Quota:** {g.get('quota', 'See provider docs')} · **Default Model:** `{g.get('default_model', '—')}` · **Env Key:** `{env_key}`")
        if g.get("base_url"):
            lines.append(f"- **Endpoint:** `{g['base_url']}`")
        for p in g.get("proof", []):
            lines.append(f"- 🏆 {p}")
        for gt in g.get("gotchas", []):
            lines.append(f"- ⚠️ {gt}")
        lines.append(f"- *Verified `{g['last_verified']}` (TTL `{f['ttl_days']}d`)*")
        lines.append("")

    if grounding:
        lines.extend([
            "## 2. Grounding, Search & Academic RAG",
            "",
            "| Tool & Health | Quota & Capability | Key Gotcha |",
            "| :--- | :--- | :--- |",
        ])
        for t in grounding:
            f = t["freshness"]
            proof = "; ".join(t.get("proof", [])) or t.get("quota", "—")
            gotcha = "; ".join(t.get("gotchas", []))
            lines.append(f"| {_link(t['name'], t['url'])} · {_badge(f)} | **{t.get('quota', '')}** — {proof} | ⚠️ {gotcha} |")
        lines.append("")

    if snap.get("forage_routes"):
        lines.extend(["## 3. Cloud Fallback Chains", ""])
        for intent, route in snap["forage_routes"].items():
            chain = " → ".join(f"`{cid}`" for cid in route.get("chain", []))
            lines.append(f"- **`{intent}`:** {chain}")
        lines.append("")

    lines.extend(["---", "", nav])
    _write(os.path.join(root, "book/cloud.md"), lines)


def _render_local(snap: dict[str, Any], root: str) -> None:
    nodes_map = snap["nodes"]
    adapters_for = snap.get("adapters_for", {})
    local_models = [n for n in nodes_map.values() if n["kind"] == "model"]

    mature = [n for n in local_models if n["lifecycle"] == "mature" and n.get("domain") not in ("local-decision", "multimodal")]
    edge = [n for n in local_models if n["lifecycle"] in ("experimental", "operational") and n.get("domain") not in ("local-decision", "multimodal")]
    sys1 = [n for n in local_models if n.get("domain") == "local-decision"]
    media = [n for n in local_models if n.get("domain") == "multimodal"]
    nav = _render_nav("🖥️ Local")

    lines = [
        nav,
        "",
        "# 🖥️ Local AI Hardware Blueprints",
        "",
        "> [!IMPORTANT]",
        "> Built around your starter hardware profiles (`16vram-64ram` and `mac-apple-silicon`). Daily-driver **Track A (Mature & Riced)** models stay strictly isolated from **Track B (Cutting-Edge)** experimental architectures.",
        "",
    ]

    def _emit_track(heading: str, subtitle: str, items: list[dict[str, Any]]) -> None:
        if not items:
            return
        lines.extend([f"## {heading}", f"*{subtitle}*", ""])
        for m in items:
            f = m["freshness"]
            profs = ", ".join(f"`{p}`" for p in m.get("edges", {}).get("runs_on", [])) or "—"
            hw = m.get("hardware", {})
            mem = f"`{hw['footprint']}`" if hw.get("footprint") else "—"
            lic = f"`{m['license']}`" if m.get("license") else "—"
            lines.append(f"### {_link(m['name'], m['url'])} · {_badge(f)}")
            lines.append(f"**Profiles:** {profs} · **Footprint:** {mem} · **License:** {lic} · *Verified `{m['last_verified']}`*")
            lines.append("")
            for p in m.get("proof", []):
                lines.append(f"- 🏆 {p}")
            compat_loras = adapters_for.get(m["id"], [])
            if compat_loras:
                lora_links = ", ".join(_link(nodes_map[aid]["name"], nodes_map[aid]["url"]) for aid in compat_loras if aid in nodes_map)
                lines.append(f"- ⚡ **Hot-Swappable Adapters (Implicit `adapts` Edges):** {lora_links}")
            for gt in m.get("gotchas", []):
                lines.append(f"- ⚠️ {gt}")
            if m.get("launch_recipe"):
                lines.extend(["", "```bash", m["launch_recipe"].rstrip(), "```"])
            lines.append("")

    _emit_track("1. Track A · Mature & Fully Riced (Daily Drivers)", "Predictable runtimes, verified LoRA adapters, zero kernel drama.", mature)
    _emit_track("2. Track B · Cutting-Edge Local (High Upside / Faster Churn)", "Looped MoEs, N-gram prefetch ceilings, and emerging architectures.", edge)
    _emit_track("3. System-1 Local Decision Models (Non-Autoregressive)", "Zero-output-token safety gates, routers, and multimodal classifiers.", sys1)
    _emit_track("4. Local Media & Voice Anchors", "Core open-weight creative models fitting inside 16GB VRAM + 64GB RAM.", media)

    lines.extend(["---", "", nav])
    _write(os.path.join(root, "book/local.md"), lines)


def _render_harnesses_and_rl(snap: dict[str, Any], root: str) -> None:
    nodes_map = snap["nodes"]
    adapters_for = snap.get("adapters_for", {})
    harnesses = [n for n in nodes_map.values() if n["kind"] == "harness"]
    adapters_rl = [n for n in nodes_map.values() if n["kind"] == "adapter" or n.get("domain") == "adaptation"]
    backends = [n for n in nodes_map.values() if n["kind"] == "backend"]
    guards = [n for n in nodes_map.values() if n.get("edges", {}).get("guards")]
    nav = _render_nav("⚙️ Harnesses & RL")

    lines = [
        nav,
        "",
        "# ⚙️ Harnesses, Backends & RL Adapters Lab Dossier",
        "",
        "> [!IMPORTANT]",
        "> Treat **`Pi` / `Pi Durable`** as your building-block kernel, **`DeepSeek Harness` (`dsh`)** as your Cordis plugin platform, and **`Hermes Agent`** as your persistent self-improving daemon—paired with hot-swappable RL LoRA adapters and `safeagents`.",
        "",
        "## 1. Harness Architecture Dossiers",
        "",
    ]
    for h in harnesses:
        f = h["freshness"]
        role = h.get("role", h["lifecycle"])
        lines.append(f"### {_link(h['name'], h['url'])} · `{role}` · {_badge(f)}")
        for p in h.get("proof", []):
            lines.append(f"- 🏆 {p}")
        compat = adapters_for.get(h["id"], [])
        if compat:
            links = ", ".join(_link(nodes_map[aid]["name"], nodes_map[aid]["url"]) for aid in compat if aid in nodes_map)
            lines.append(f"- ⚡ **Official Harness Adapters:** {links}")
        for gt in h.get("gotchas", []):
            lines.append(f"- ⚠️ {gt}")
        if h.get("launch_recipe"):
            lines.extend(["", "```bash", h["launch_recipe"].rstrip(), "```"])
        lines.append("")

    if guards:
        lines.extend(["## 2. Runtime Safety Proxies (`guards` Edges)", ""])
        for g in guards:
            f = g["freshness"]
            summary = "; ".join(g.get("proof", []))
            lines.append(f"- {_link(g['name'], g['url'])} · {_badge(f)} — {summary}")
            for gt in g.get("gotchas", []):
                lines.append(f"  - ⚠️ {gt}")
        lines.append("")

    if adapters_rl:
        lines.extend(["## 3. Harness Adapters & In-Harness RL Lab Notebook", ""])
        for a in adapters_rl:
            f = a["freshness"]
            targets = ", ".join(f"`{t}`" for t in a.get("edges", {}).get("adapts", [])) or "Core RL Pipeline"
            lines.append(f"### {_link(a['name'], a['url'])} · {_badge(f)}")
            lines.append(f"**Targets:** {targets} · **License:** `{a.get('license', '—')}` · *Verified `{a['last_verified']}`*")
            lines.append("")
            for p in a.get("proof", []):
                lines.append(f"- 🏆 {p}")
            for gt in a.get("gotchas", []):
                lines.append(f"- ⚠️ {gt}")
            for tbl in a.get("eval_tables", []):
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
            if a.get("launch_recipe"):
                lines.extend(["", "```bash", a["launch_recipe"].rstrip(), "```"])
            lines.append("")

    if backends:
        lines.extend([
            "## 4. Inference Backends & 2026 Flag Reference",
            "",
            "| Backend & Health | Breakthroughs & Target | Critical Gotcha |",
            "| :--- | :--- | :--- |",
        ])
        for b in backends:
            proof_s = "; ".join(b.get("proof", []))
            gotcha_s = "; ".join(b.get("gotchas", []))
            lines.append(f"| {_link(b['name'], b['url'])} · {_badge(b['freshness'])} | {proof_s} | ⚠️ {gotcha_s} |")
        lines.append("")

    lines.extend(["---", "", nav])
    _write(os.path.join(root, "book/harnesses-and-rl.md"), lines)


def _render_playbooks(snap: dict[str, Any], root: str) -> None:
    nav = _render_nav("📘 Playbooks")
    lines = [
        nav,
        "",
        "# 📘 Core Playbooks (3 Deep Owned Runbooks)",
        "",
        "> [!IMPORTANT]",
        "> Core models, harnesses, backends, hot-swappable LoRAs, and mandatory guards below are **resolved implicitly** from the headless graph. Only flagship domain tools are declared per playbook.",
        "",
    ]
    for pid, pb in snap["playbooks"].items():
        core = pb["implicit_core"]
        lines.extend([
            f"## 📘 {pb['title']} (`{pid}`)",
            "",
            f"> **Verdict:** {pb['verdict']}",
            "",
        ])
        if pb.get("degraded_dependency_count", 0) > 0:
            lines.extend([
                "> [!WARNING]",
                f"> `{pb['degraded_dependency_count']}` upstream dependencies are currently stale/degraded and gated out of `llms.txt`.",
                "",
            ])

        models = ", ".join(f"`{m['id']}` ({_badge(m['freshness'])})" for m in core["models_and_gateways"]) or "—"
        harnesses = ", ".join(f"`{h['id']}` ({_badge(h['freshness'])})" for h in core["harnesses"]) or "—"
        backends = ", ".join(f"`{b['id']}` ({_badge(b['freshness'])})" for b in core.get("backends", []))
        adapters = ", ".join(f"`{a['id']}`" for a in core["discovered_adapters"]) or "None"
        guards = ", ".join(_link(g["name"], g["url"]) for g in core["guards"]) or "None"

        lines.extend([
            "### Implicitly Resolved Core Stack",
            f"- **Brains / Gateways:** {models}",
            f"- **Harnesses:** {harnesses}",
        ])
        if backends:
            lines.append(f"- **Core Backends:** {backends}")
        lines.extend([
            f"- **Auto-Discovered Adapters (`adapts`):** {adapters}",
            f"- **Attached Safety Layer (`guards`):** {guards}",
            "",
            "### Verified Flagship Domain Tools",
            "",
            "| Tool | Health | Canonical Repo |",
            "| :--- | :--- | :--- |",
        ])
        for tool in pb.get("domain_tools", []):
            lines.append(f"| **{tool['name']}** | {_badge(tool['freshness'])} | `{tool['url']}` |")

        lines.extend(["", "### Execution Workflow", ""])
        for idx, step in enumerate(pb.get("workflow", []), 1):
            lines.append(f"{idx}. {step}")

        lines.extend(["", "### Guardrails", ""])
        for g in pb.get("guardrails", []):
            lines.append(f"- ⚠️ {g}")
        lines.extend(["", "---", ""])

    lines.append(nav)
    _write(os.path.join(root, "book/playbooks.md"), lines)


def _render_spokes(snap: dict[str, Any], root: str) -> None:
    nav = _render_nav("🧭 Spokes")
    lines = [
        nav,
        "",
        "# 🧭 Horizon Spoke Directory (Upstream-Federated)",
        "",
        "> [!IMPORTANT]",
        "> Spokes keep `ai-swissknife` multi-horizon without spreading thin: each spoke plugs into your implicit Core, lists **at most 2 canonical entry points** (enforced by CI), and delegates the long tail to a **live-monitored Upstream Hub**.",
        "",
    ]
    for sid, sp in snap["spokes"].items():
        core = sp["implicit_core"]
        hub = sp["upstream_hub"]
        pushed = hub["freshness"].get("upstream_pushed_at")
        pushed_str = f" · Last Upstream Push: `{pushed[:10]}`" if pushed else ""

        models = ", ".join(f"`{m['id']}`" for m in core["models_and_gateways"]) or "—"
        adapters = ", ".join(f"`{a['id']}`" for a in core["discovered_adapters"]) or "None"
        guards = ", ".join(f"`{g['id']}`" for g in core["guards"]) or "None"

        lines.extend([
            f"## 🧭 {sp['title']} (`{sid}`)",
            f"> {sp['verdict']}",
            "",
            f"- **Implicit Core Plug-In:** Models {models} · Auto-Adapters {adapters} · Guards {guards}",
            "- **Canonical Entry Points (Max 2):**",
        ])
        for ep in sp.get("entry_points", []):
            lines.append(f"  - {_link(ep['name'], ep['url'])} · {_badge(ep['freshness'])}")
        lines.append(f"- **Upstream Hub (Long Tail):** {_link(hub['name'], hub['url'])} · {_badge(hub['freshness'])}{pushed_str}")
        for g in sp.get("guardrails", []):
            lines.append(f"- ⚠️ {g}")
        lines.append("")

    lines.extend(["---", "", nav])
    _write(os.path.join(root, "book/spokes.md"), lines)


def _render_radar_and_graveyard(snap: dict[str, Any], root: str) -> None:
    nav_r = _render_nav("📡 Radar")
    r_lines = [
        nav_r,
        "",
        "# 📡 Capped 21-Day Radar (Frontier Watch & Community IRL)",
        "",
        "> [!NOTE]",
        "> Hard-capped by CI (`<=5` Frontier, `<=5` Community, **21-day TTL**). Adding a new entry requires consciously retiring an older one. Frontier items are strictly `Monitor-Only` and excluded from `llms.txt`.",
        "",
        "## 🔭 Frontier Watch (Monitor-Only Apex Ceiling)",
        "",
    ]
    for item in snap["radar"]["frontier"]:
        f = item["freshness"]
        left = max(0, f["ttl_days"] - f["age_days"])
        r_lines.append(f"- {_link(item['name'], item['url'])} · {_badge(f)} (`{left}d` left) — {item.get('signal', '')}")
        for gt in item.get("gotchas", []):
            r_lines.append(f"  - ⚠️ {gt}")

    r_lines.extend(["", "## 🛠️ Community IRL Field Log (Consumer Hardware & Extensions)", ""])
    for item in snap["radar"]["community"]:
        f = item["freshness"]
        left = max(0, f["ttl_days"] - f["age_days"])
        r_lines.append(f"- {_link(item['name'], item['url'])} · {_badge(f)} (`{left}d` left) — {item.get('signal', '')}")
        for gt in item.get("gotchas", []):
            r_lines.append(f"  - ⚠️ {gt}")

    r_lines.extend(["", "---", "", nav_r])
    _write(os.path.join(root, "book/radar.md"), r_lines)

    nav_g = _render_nav("🪦 Graveyard")
    nodes_map = snap["nodes"]
    g_lines = [
        nav_g,
        "",
        "# 🪦 The Graveyard (CI-Enforced Cut Ledger)",
        "",
        "> [!WARNING]",
        "> Any active node matching a pattern below fails `python scripts/cli.py validate`.",
        "",
        "| Category | Retired / Blocked Item | Why Cut | Active Replacement |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for bucket, label in (("cloud", "☁️ Cloud"), ("local", "🖥️ Local")):
        for entry in snap["graveyard"].get(bucket, []):
            rep_id = entry.get("replaced_by")
            rep_str = _link(nodes_map[rep_id]["name"], nodes_map[rep_id]["url"]) if rep_id in nodes_map else "—"
            g_lines.append(f"| {label} | ❌ **{entry['name']}** | {entry['reason']} | {rep_str} |")

    g_lines.extend(["", "---", "", nav_g])
    _write(os.path.join(root, "book/graveyard.md"), g_lines)


def render(snapshot: dict[str, Any], root: str = ".") -> None:
    _render_dashboard(snapshot, root)
    _render_cloud(snapshot, root)
    _render_local(snapshot, root)
    _render_harnesses_and_rl(snapshot, root)
    _render_playbooks(snapshot, root)
    _render_spokes(snapshot, root)
    _render_radar_and_graveyard(snapshot, root)
