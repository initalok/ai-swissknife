#!/usr/bin/env python3
"""
AI Swiss Knife Unified Engine (v1.1.0 Cloud + v2.0.0 Local + v3.0.0 Ecosystem)
Commands:
  python scripts/build.py sync                    # Sync upstream repos & filter Graveyard links
  python scripts/build.py lint                    # Lint all 3 YAML catalogs (4-col law + dual graveyards)
  python scripts/build.py compile                 # Build README.md, llms.txt, LOCAL_AI.md, llms-local.txt, ECOSYSTEM.md
  python scripts/build.py forage <intent>         # Cloud/local/keyless auto-foraging
  python scripts/build.py forage <id> --local     # Local 16GB VRAM + 64GB RAM launch config
  python scripts/build.py all                     # Run sync -> lint -> compile
"""
import json
import os
import sys
import yaml
import requests
from datetime import datetime, timezone

CLOUD_YAML = "data/catalog.yaml"
LOCAL_YAML = "data/local_catalog.yaml"
ECO_YAML = "data/ecosystem.yaml"
SOURCES_PATH = "upstream/sources.json"
SNAPSHOT_DIR = "upstream/snapshots"
DIFF_REPORT = "upstream/latest_diff_report.md"


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def cmd_sync():
    print("==> [1/3] SYNC: Pulling upstream snapshots & filtering Cloud + Local Graveyards...")
    if not os.path.exists(SOURCES_PATH):
        print(f"    [WARN] {SOURCES_PATH} not found; skipping upstream sync.")
        return

    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    cloud = load_yaml(CLOUD_YAML)
    local = load_yaml(LOCAL_YAML)
    patterns = [g["match_pattern"].lower() for g in cloud.get("graveyard", [])] + [
        g["match_pattern"].lower() for g in local.get("local_graveyard", [])
    ]

    with open(SOURCES_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    report = [f"# Upstream Sync & Diff Report ({datetime.now(timezone.utc).isoformat()})\n"]
    for repo in registry["repositories"]:
        rid = repo["id"]
        api_url = f"https://api.github.com/repos/{repo['name']}/commits/main"
        try:
            r_meta = requests.get(api_url, timeout=12)
            sha = r_meta.json().get("sha", "unknown")[:10] if r_meta.status_code == 200 else "unknown"
            r_raw = requests.get(repo["raw_readme"], timeout=15)
            if r_raw.status_code == 200:
                snap = os.path.join(SNAPSHOT_DIR, f"{rid}.md")
                old = set()
                if os.path.exists(snap):
                    with open(snap, "r", encoding="utf-8") as sf:
                        old = set(sf.read().splitlines())
                new = set(r_raw.text.splitlines())
                raw_added = [l.strip() for l in (new - old) if "http" in l]
                clean_added = [l for l in raw_added if not any(p in l.lower() for p in patterns)]
                blocked = len(raw_added) - len(clean_added)
                with open(snap, "w", encoding="utf-8") as sf:
                    sf.write(r_raw.text)
                prev = repo.get("last_synced_sha")
                repo["last_synced_sha"] = sha
                report.append(f"## {repo['name']} (`{prev}` -> `{sha}`)")
                report.append(f"- **New Candidate Links:** {len(clean_added)} *(Blocked {blocked} Graveyard matches)*")
                for line in clean_added[:10]:
                    report.append(f"  + {line}")
                report.append("")
        except Exception as exc:
            report.append(f"## {repo['name']}\n- Sync warning: {exc}\n")

    registry["last_checked"] = datetime.now(timezone.utc).isoformat()
    with open(SOURCES_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    with open(DIFF_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"    [OK] Upstream diff saved to {DIFF_REPORT}")


def cmd_lint():
    print("==> [2/3] LINT: Auditing v1 Cloud, v2 Local, and v3 Ecosystem schemas...")
    cloud = load_yaml(CLOUD_YAML)
    local = load_yaml(LOCAL_YAML)
    eco = load_yaml(ECO_YAML)
    errors = []

    provs = cloud.get("providers", {})
    c_grave = [g["match_pattern"].lower() for g in cloud.get("graveyard", [])]
    req_p = {"name", "url", "base_url", "tier", "default_model", "quota", "bottleneck", "effective_context", "trains_on_data"}
    for pid, p in provs.items():
        missing = req_p - set(p.keys())
        if missing:
            errors.append(f"[v1] Provider '{pid}' missing keys: {missing}")
        for pat in c_grave:
            if pat in p.get("url", "").lower() or pat in p.get("base_url", "").lower() or pat in p.get("default_model", "").lower():
                errors.append(f"[v1] Provider '{pid}' matches Graveyard ban '{pat}'")

    for intent, r in cloud.get("forage_routes", {}).items():
        for ref in r.get("chain", []):
            if ref not in provs:
                errors.append(f"[v1] Forage route '{intent}' references unknown provider '{ref}'")

    for row in cloud.get("text_code_matrix", []):
        for ref in row.get("provider_refs", []):
            if ref not in provs:
                errors.append(f"[v1] text_code_matrix references unknown provider '{ref}'")
        if not all(k in row for k in ("col1_task", "col2_winner", "col3_gateway", "col4_gotcha")):
            errors.append("[v1] text_code_matrix violates 4-column law")

    for row in cloud.get("multimodal_matrix", []):
        for ref in row.get("provider_refs", []):
            if ref not in provs:
                errors.append(f"[v1] multimodal_matrix references unknown provider '{ref}'")
        if not all(k in row for k in ("col1_modality", "col2_models", "col3_cloud", "col4_local_gotcha")):
            errors.append("[v1] multimodal_matrix violates 4-column law")

    for row in cloud.get("grounding_matrix", []):
        if not all(k in row for k in ("col1_role", "col2_tool", "col3_quota", "col4_edge")):
            errors.append("[v1] grounding_matrix violates 4-column law")

    l_grave = [g["match_pattern"].lower() for g in local.get("local_graveyard", [])]
    for sec, keys in (
        ("local_text_code_matrix", ("col1_role", "col2_models", "col3_license_mem", "col4_proof_gotcha")),
        ("local_decision_matrix", ("col1_role", "col2_models", "col3_mem_latency", "col4_wiring_gotcha")),
        ("local_multimodal_matrix", ("col1_modality", "col2_models", "col3_license_mem", "col4_proof_gotcha")),
    ):
        for row in local.get(sec, []):
            if not all(k in row for k in keys):
                errors.append(f"[v2] {sec} violates 4-column law")
            blob = " ".join(str(row[k]) for k in keys).lower()
            for pat in l_grave:
                if pat in blob:
                    errors.append(f"[v2] {sec} contains banned pattern '{pat}'")

    for dom in eco.get("domains", []):
        if len(dom.get("headers", [])) != 4:
            errors.append(f"[v3] Domain '{dom.get('id')}' header count != 4")
        for row in dom.get("rows", []):
            if not all(k in row for k in ("col1", "col2", "col3", "col4")):
                errors.append(f"[v3] Domain '{dom.get('id')}' row violates 4-column law")

    if errors:
        print("    [!] LINT FAILED:")
        for e in errors:
            print(f"      - {e}")
        sys.exit(1)
    print(f"    [OK] All 3 dimensions verified: {len(provs)} cloud gateways, {len(local['forage_local_profiles'])} local profiles, {len(eco['domains'])} ecosystem domains.")


def build_v1_readme(cat):
    m = cat["meta"]
    lines = [
        f"# {m['title']} (`v{m['version']}`)",
        f"> {m['tagline']}\n",
        "**Dimensions:** 🌐 **Cloud APIs (`README.md`)** · 🖥️ [**Local AI: 16GB VRAM + 64GB RAM (`LOCAL_AI.md`)**](LOCAL_AI.md) · 🛠️ [**Harnesses, Backends & Flags (`ECOSYSTEM.md`)**](ECOSYSTEM.md) · 🤖 [**Agent Manifest (`llms.txt`)**](llms.txt)\n",
        "> [!IMPORTANT]",
        f"> **Editorial Standard:** {m['editorial_note']}\n",
        "---\n",
        "## 🧭 1. The Cloud Routing Circuit (Verified Card-Free Survivors)",
        "*Only **6 gateways** remain genuinely card-free (`Google AI Studio`, `Z.ai BigModel`, `OpenRouter :free`, `Groq`, `NVIDIA NIM`, `Cloudflare Workers AI`).*\n",
        "```mermaid",
        "flowchart LR",
        '    subgraph INTENT ["1. CLOUD WORKLOAD"]',
        '        A["🤖 Coding Agent<br/>(20K tok/step)"]',
        '        B["🔬 500B+ Reasoning<br/>(DeepSeek / Nemotron)"]',
        '        C["⚖️ System-1 Decisions<br/>($0 Output Tokens)"]',
        '        D["⚡ Fast Micro-Route<br/>(<6K tok / Whisper)"]',
        "    end",
        '    subgraph PIPE ["2. VERIFIED NO-CARD GATEWAY"]',
        '        P1["🔵 Google AI Studio<br/>Gemini 3.8 Flash (1M ctx)"]',
        '        P2["🟢 Z.ai BigModel<br/>GLM-4.7-Flash (200K Free)"]',
        '        P3["🟣 NVIDIA NIM / OpenRouter<br/>40 RPM / 1K RPD (10 Cr)"]',
        '        P4["🟠 Cloudflare / Decision 1<br/>Clef · Clairic · 10K RPD"]',
        '        TRAP["🔴 Groq Cloud<br/>8K TPM Wall (STT / <6K only)"]',
        "    end",
        '    A ==>|"Primary"| P1',
        '    A -.->|"Free 200K Fallback"| P2',
        '    A x--x|"429 on 20K Prompts"| TRAP',
        '    B ==>|"DeepSeek-V4.1-Flash"| P3',
        '    C ==>|"Single-Pass Probs"| P4',
        '    D ==>|"Qwen3.8-27B / Whisper"| TRAP',
        "```\n<br>\n",
        "## ⚡ 2. Task-Routed Cloud Intelligence & Decision Matrix",
        "",
        "| Task & Workload | Primary Winner & Proof | Free Gateway & Quota Pipe | The Catch (`Gotcha` & Privacy) |",
        "| :--- | :--- | :--- | :--- |"
    ]
    for r in cat["text_code_matrix"]:
        lines.append(f"| {r['col1_task']} | {r['col2_winner']} | {r['col3_gateway']} | {r['col4_gotcha']} |")

    lines.extend([
        "",
        "<details>",
        "<summary>🛠️ <b>Click to expand Ready-to-Use <code>.env</code> Endpoints & Agent Foraging Commands</b></summary>",
        "<br>\n",
        "```bash",
        "python scripts/build.py forage coding-agent",
        "python scripts/build.py forage decision-gate",
        "",
        'export OPENAI_API_BASE="https://generativelanguage.googleapis.com/v1beta/openai/"',
        'export OPENAI_MODEL="gemini-3.8-flash"',
        'export FALLBACK_API_BASE="https://open.bigmodel.cn/api/paas/v4/"',
        'export FALLBACK_MODEL="glm-4.7-flash"',
        'export KEYLESS_API_BASE="https://text.pollinations.ai/openai"',
        "```",
        "</details>\n\n---\n",
        "## 🎨 3. Multimodal & Sensory Stack (Cloud Free vs. Local Pivot)",
        "",
        "| Modality & Job | Top Verified Models | Free Cloud Route & Quota | Local Pivot (`LOCAL_AI.md`) & Gotcha |",
        "| :--- | :--- | :--- | :--- |"
    ])
    for r in cat["multimodal_matrix"]:
        lines.append(f"| {r['col1_modality']} | {r['col2_models']} | {r['col3_cloud']} | {r['col4_local_gotcha']} |")

    lines.extend([
        "\n---\n",
        "## 🔍 4. Grounding, Search, Scraping & RAG Stack (100% Card-Free)",
        "",
        "| Grounding Role | Tool & Endpoint | Verified Free Quota | Why It Wins & Technical Gotcha |",
        "| :--- | :--- | :--- | :--- |"
    ])
    for r in cat["grounding_matrix"]:
        lines.append(f"| {r['col1_role']} | {r['col2_tool']} | {r['col3_quota']} | {r['col4_edge']} |")

    lines.extend([
        "\n---\n",
        "## 🪦 5. The Graveyard (What We Cut & Why)",
        "",
        "> [!WARNING]",
        "> Enforced by `scripts/build.py lint` & `sync` so dead or card-gated tiers can never creep back in.\n"
    ])
    for g in cat["graveyard"]:
        lines.append(f"* ❌ **{g['name']}:** {g['reason']}")

    lines.extend([
        "\n---\n",
        "## 🤖 6. Unified CLI & Dual-Interface Agent Foraging",
        "```bash",
        "python scripts/build.py forage coding-agent             # Cloud/local/keyless auto-foraging",
        "python scripts/build.py forage inkling-coding --local   # Local 16GB+64GB launch command",
        "python scripts/build.py all                             # Sync -> Lint (v1+v2+v3) -> Compile all 5 views",
        "```"
    ])
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def build_v1_llms_txt(cat):
    lines = [
        "# AI Swiss Knife — Cloud Agent Foraging Manifest (llms.txt)",
        f"> Version: {cat['meta']['version']} | See `llms-local.txt` for 16GB VRAM + 64GB RAM local models.\n",
        "## Tier 0: Immediate Keyless Endpoints (Zero Auth / No API Key Needed)",
        "- LLM Chat (OpenAI-compat): POST https://text.pollinations.ai/openai/chat/completions (model: 'openai')",
        "- Image Gen (FLUX): GET https://image.pollinations.ai/prompt/{prompt}?model=flux&nologo=true",
        "- Web/PDF to Markdown: GET https://r.jina.ai/{target_url}",
        "- Keyless Web Search: GET https://s.jina.ai/?q={query}",
        "- Firecrawl Keyless Skill: GET https://www.firecrawl.dev/agent-onboarding/SKILL.md",
        "- Academic Papers (100K/day): GET https://api.openalex.org/works?search={query}&filter=is_oa:true&mailto=agent@localhost\n",
        "## Tier 1: Local Hardware Runtime (See llms-local.txt)",
        "- Unsloth / llama-server: http://localhost:8000/v1 | Local Decision API (Laya): http://localhost:8888\n",
        "## Tier 2: Verified No-Card Cloud Gateways (Check Env Vars First)"
    ]
    for pid, p in cat["providers"].items():
        if p["tier"] == "tier2-cloud-free":
            lines.append(f"- [{pid}] env:{p['env_key']} | base_url:{p['base_url']} | default_model:{p['default_model']} | quota:{p['quota']} | bottleneck:{p['bottleneck']}")
    lines.append("\n## Foraging Chains (`python scripts/build.py forage <intent>`)")
    for intent, r in cat["forage_routes"].items():
        lines.append(f"- {intent} ({r['description']}): {' -> '.join(r['chain'])}")
    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def build_v2_local(loc):
    m = loc["meta"]
    lines = [
        f"# {m['title']} (`v{m['version']}`)",
        f"> **Hardware Envelope:** `{m['hardware_envelope']}` — {m['tagline']}\n",
        "**Navigation:** 🌐 [**Cloud APIs (`README.md`)**](README.md) · 🖥️ **Local Models (`LOCAL_AI.md`)** · 🛠️ [**Backends & Flags (`ECOSYSTEM.md`)**](ECOSYSTEM.md) · 🤖 [**Local Manifest (`llms-local.txt`)**](llms-local.txt)\n",
        "> [!IMPORTANT]",
        f"> **Curation Policy:** {m['editorial_note']}\n",
        "---\n",
        "## 🧭 1. The Two-Zone Physics Map (`16GB VRAM + 64GB RAM`)\n",
        "```mermaid",
        "flowchart LR",
        '    subgraph Z1 ["⚡ ZONE 1: 100% IN 16GB VRAM (<= 15 GB)"]',
        '        Z1A["💻 Coding & Vision<br/>Inkling 2 Mini (UD-Q3) · Qwen3.8-27B<br/>Gemma 4 (26B-A4B Text+Vis) · Devstral 2"]',
        '        Z1B["⚖️ System-1 & Sensory<br/>Laya (678MB) · Qwen-Image-2.1 (9.1GB)<br/>DeepSeek-OCR 2 · Phonon 31M · Hy-Nomas"]',
        "    end",
        '    subgraph Z2 ["🚀 ZONE 2: 16GB VRAM + 64GB RAM HYBRID (18–73 GB)"]',
        '        Z2A["🔥 Frontier MoE Coding<br/>Qwen3.8-Flash-Next (180B: IQ1_M/Q2_0)<br/>Qwen3-Coder-Next (80B) · Inkling 2 Mini (Q4)"]',
        '        Z2B["🧠 Agents, Logic & Heavy Media<br/>Recursive Flint · Muse Glimmer (DFlash)<br/>Nemotron-Cascade-2 · Fish Drama 3 · Wan 2.2"]',
        "    end",
        "```\n<br>\n",
        "## 🧠 2. Local Text, Coding & Reasoning Roster",
        "",
        "| Role & Memory Zone | Verified Local Models | Origin, License & Footprint | Benchmark Proof & Hardware Gotcha |",
        "| :--- | :--- | :--- | :--- |"
    ]
    for r in loc["local_text_code_matrix"]:
        lines.append(f"| {r['col1_role']} | {r['col2_models']} | {r['col3_license_mem']} | {r['col4_proof_gotcha']} |")

    lines.extend([
        "\n---\n",
        "## ⚖️ 3. System-1 Local Decision Models (Non-Autoregressive)",
        "",
        "| Role & Job | Verified Local Models | Memory & Latency | Wiring & Calibration Gotcha |",
        "| :--- | :--- | :--- | :--- |"
    ])
    for r in loc["local_decision_matrix"]:
        lines.append(f"| {r['col1_role']} | {r['col2_models']} | {r['col3_mem_latency']} | {r['col4_wiring_gotcha']} |")

    lines.extend([
        "\n---\n",
        "## 🎨 4. Local Multimodal, World, Voice & Retrieval Roster",
        "",
        "| Modality & Niche | Verified Local Models | License & Memory Profile | Why It Wins & Hardware Gotcha |",
        "| :--- | :--- | :--- | :--- |"
    ])
    for r in loc["local_multimodal_matrix"]:
        lines.append(f"| {r['col1_modality']} | {r['col2_models']} | {r['col3_license_mem']} | {r['col4_proof_gotcha']} |")

    lines.extend([
        "",
        "<details>",
        "<summary>🛠️ <b>Click to expand Verified Local Launch Profiles (<code>python scripts/build.py forage &lt;id&gt; --local</code>)</b></summary>",
        "<br>\n",
        "```bash"
    ])
    for pid, p in loc["forage_local_profiles"].items():
        lines.append(f"# [{pid}] {p['zone']} — {p['model']}")
        lines.append(p["launch"])
        lines.append("")
    lines.extend([
        "```",
        "</details>\n\n---\n",
        "## 🪦 5. The Local Hardware Wall Graveyard",
        "",
        "> [!WARNING]",
        "> Models below either have no published weights or physically overflow `16GB VRAM + 64GB RAM` (~80 GB).\n"
    ])
    for g in loc["local_graveyard"]:
        lines.append(f"* ❌ **{g['name']}:** {g['reason']}")

    with open("LOCAL_AI.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    ll = [
        "# AI Swiss Knife — Local AI Manifest (16GB VRAM + 64GB RAM)",
        f"> Version: {m['version']} | Run `python scripts/build.py forage <profile> --local`\n",
        "## Ready-to-Run Local Profiles"
    ]
    for pid, p in loc["forage_local_profiles"].items():
        ll.append(f"- [{pid}] zone:{p['zone']} | model:{p['model']} | runtime:{p['runtime']} | cmd: `{p['launch']}`")
    with open("llms-local.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(ll) + "\n")


def build_v3_ecosystem(eco):
    m = eco["meta"]
    lines = [
        f"# {m['title']} (`v{m['version']}`)",
        f"> {m['tagline']}\n",
        "**Navigation:** 🌐 [**Cloud APIs (`README.md`)**](README.md) · 🖥️ [**Local Models (`LOCAL_AI.md`)**](LOCAL_AI.md) · 🛠️ **Ecosystem Atlas (`ECOSYSTEM.md`)**\n",
        "> [!IMPORTANT]",
        f"> **Scope:** {m['editorial_note']}\n",
        "---\n",
        "```mermaid",
        "flowchart TB",
        '    subgraph V3 ["🛠️ v3 OPERATIONAL STACK"]',
        '        D1["1. Harnesses<br/>Antigravity 2.0 · Pi/Durable Pi · Zed ACP"]',
        '        D2["2. Backends<br/>Unsloth · llama/ik_llama · WanGP v20.12"]',
        '        D3["3. Flags & Quants<br/>--n-cpu-moe · --load-mode · DFlash/DSpark"]',
        '        D4["4. Protocols<br/>SKILL.md · AGENTS.md · Context Archival"]',
        '        D5["5. OS & Silicon<br/>Linux AVX-512 · NVFP4 · MLX · WebGPU"]',
        '        D6["6. Frontier Leads<br/>arXiv:2611.21885 · varloop · Hy-Nomas"]',
        "    end",
        "    D1 --> D4 --> D2 --> D3 --> D5",
        "    D6 -.-> D1 & D2 & D3",
        "```\n"
    ]
    for dom in eco["domains"]:
        lines.append(f"---\n\n## {dom['title']}")
        lines.append(f"*{dom['subtitle']}*\n")
        h = dom["headers"]
        lines.append(f"| {h[0]} | {h[1]} | {h[2]} | {h[3]} |")
        lines.append("| :--- | :--- | :--- | :--- |")
        for r in dom["rows"]:
            lines.append(f"| {r['col1']} | {r['col2']} | {r['col3']} | {r['col4']} |")
        if dom.get("drawer_code"):
            lines.extend([
                "",
                "<details>",
                f"<summary>🛠️ <b>{dom['drawer_title']}</b></summary>",
                "<br>\n",
                "```bash",
                dom["drawer_code"].rstrip(),
                "```",
                "</details>"
            ])
        lines.append("")

    with open("ECOSYSTEM.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def cmd_compile():
    print("==> [3/3] COMPILE: Generating README.md, llms.txt, LOCAL_AI.md, llms-local.txt, & ECOSYSTEM.md...")
    build_v1_readme(load_yaml(CLOUD_YAML))
    build_v1_llms_txt(load_yaml(CLOUD_YAML))
    build_v2_local(load_yaml(LOCAL_YAML))
    build_v3_ecosystem(load_yaml(ECO_YAML))
    print("    [OK] Compiled all 5 dual-interface artifacts cleanly.")


def cmd_forage(intent=None, local_mode=False):
    if local_mode:
        loc = load_yaml(LOCAL_YAML)
        profiles = loc["forage_local_profiles"]
        if not intent or intent not in profiles:
            print("Available Local 16GB+64GB Profiles (`--local`):")
            for k, v in profiles.items():
                print(f"  python scripts/build.py forage {k:<16} --local  # {v['zone']} ({v['model']})")
            return
        p = profiles[intent]
        print(f"# [LOCAL FORAGER] {intent} | {p['zone']} | Runtime: {p['runtime']}")
        print(p["launch"])
        return

    cat = load_yaml(CLOUD_YAML)
    routes = cat["forage_routes"]
    provs = cat["providers"]
    if not intent or intent not in routes:
        print("Available Cloud Foraging Intents:")
        for k, v in routes.items():
            print(f"  python scripts/build.py forage {k:<15} # {v['description']}")
        return

    selected, reason = None, ""
    for pid in routes[intent]["chain"]:
        p = provs[pid]
        env_key = p.get("env_key")
        if p["tier"] == "tier2-cloud-free" and env_key and os.environ.get(env_key):
            selected, reason = p, f"Found active env key ${env_key}"
            break
        elif p["tier"] == "tier1-local":
            try:
                if requests.get(f"{p['base_url']}/models", timeout=1.2).status_code == 200:
                    selected, reason = p, "Local Unsloth/llama server online at localhost:8000"
                    break
            except Exception:
                continue
        elif p["tier"] == "tier0-keyless":
            selected, reason = p, "Zero-auth keyless fallback (no env keys or local server detected)"
            break

    if not selected:
        selected = provs[routes[intent]["chain"][0]]
        reason = f"Default primary selected (set ${selected.get('env_key')} to authenticate)"

    env_k = selected.get("env_key")
    print(f"# [CLOUD FORAGER] Intent: {intent} -> {selected['name']} ({reason})")
    print(f'export OPENAI_API_BASE="{selected["base_url"]}"')
    print(f'export OPENAI_MODEL="{selected["default_model"]}"')
    if env_k:
        print(f'export OPENAI_API_KEY="${{{env_k}:-sk-none}}"')
    else:
        print('export OPENAI_API_KEY="sk-keyless"')


if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = args[0] if args else "all"
    local_flag = "--local" in args
    pos = [a for a in args[1:] if not a.startswith("--")]
    arg = pos[0] if pos else None

    if cmd == "sync":
        cmd_sync()
    elif cmd == "lint":
        cmd_lint()
    elif cmd == "compile":
        cmd_compile()
    elif cmd == "forage":
        cmd_forage(arg, local_mode=local_flag)
    elif cmd == "all":
        cmd_sync()
        cmd_lint()
        cmd_compile()
    else:
        print("Usage: python scripts/build.py [sync|lint|compile|forage <intent> [--local]|all]")
        sys.exit(1)
