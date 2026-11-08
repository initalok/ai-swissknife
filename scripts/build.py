#!/usr/bin/env python3
"""
AI Swiss Knife Core Engine (v1.0.0)
Implements:
  - `sync`: Pulls upstream GitHub READMEs, filters out Graveyard URLs, writes diff report.
  - `lint`: Enforces relational integrity, 4-column table law, and Graveyard bans.
  - `compile`: Builds high-craft GitHub `README.md` (Human View) & `llms.txt` (Agent View).
  - `forage <intent>`: Autonomous endpoint discovery & key/local/keyless fallback for AI agents.
"""
import json
import os
import sys
import yaml
import requests
from datetime import datetime, timezone

CATALOG_PATH = "data/catalog.yaml"
SOURCES_PATH = "upstream/sources.json"
SNAPSHOT_DIR = "upstream/snapshots"
DIFF_REPORT = "upstream/latest_diff_report.md"


def load_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def cmd_sync():
    print("==> [1/3] SYNC: Pulling upstream snapshots & filtering Graveyard links...")
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    cat = load_catalog()
    graveyard_patterns = [g["match_pattern"].lower() for g in cat.get("graveyard", [])]

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
                old = set(open(snap, encoding="utf-8").read().splitlines()) if os.path.exists(snap) else set()
                new = set(r_raw.text.splitlines())

                raw_added = [l.strip() for l in (new - old) if "http" in l]
                clean_added = [
                    l for l in raw_added
                    if not any(pat in l.lower() for pat in graveyard_patterns)
                ]
                blocked_count = len(raw_added) - len(clean_added)

                with open(snap, "w", encoding="utf-8") as sf:
                    sf.write(r_raw.text)

                prev = repo.get("last_synced_sha")
                repo["last_synced_sha"] = sha
                report.append(f"## {repo['name']} (`{prev}` -> `{sha}`)")
                report.append(f"- **New Candidate Links:** {len(clean_added)} *(Blocked {blocked_count} Graveyard matches)*")
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
    print("==> [2/3] LINT: Auditing relational references, 4-column rule & Graveyard bans...")
    cat = load_catalog()
    provs = cat.get("providers", {})
    graveyard_patterns = [g["match_pattern"].lower() for g in cat.get("graveyard", [])]
    errors = []

    # 1. Provider completeness & Graveyard check
    req_keys = {"name", "url", "base_url", "tier", "default_model", "quota", "bottleneck", "effective_context", "trains_on_data"}
    for pid, p in provs.items():
        missing = req_keys - set(p.keys())
        if missing:
            errors.append(f"Provider '{pid}' missing keys: {missing}")
        for pat in graveyard_patterns:
            if pat in p.get("url", "").lower() or pat in p.get("base_url", "").lower():
                errors.append(f"Provider '{pid}' matches Graveyard pattern '{pat}'")

    # 2. Forage chains relational check
    for intent, route in cat.get("forage_routes", {}).items():
        for ref in route.get("chain", []):
            if ref not in provs:
                errors.append(f"Forage route '{intent}' references unknown provider '{ref}'")

    # 3. 4-Column Law & relational refs in Matrices
    for row in cat.get("text_code_matrix", []):
        for ref in row.get("provider_refs", []):
            if ref not in provs:
                errors.append(f"text_code_matrix references unknown provider '{ref}'")
        if not all(k in row for k in ("col1_task", "col2_winner", "col3_gateway", "col4_gotcha")):
            errors.append("text_code_matrix row violates strict 4-column schema")

    for row in cat.get("multimodal_matrix", []):
        for ref in row.get("provider_refs", []):
            if ref not in provs:
                errors.append(f"multimodal_matrix references unknown provider '{ref}'")
        if not all(k in row for k in ("col1_modality", "col2_models", "col3_cloud", "col4_local_gotcha")):
            errors.append("multimodal_matrix row violates strict 4-column schema")

    for row in cat.get("grounding_matrix", []):
        if not all(k in row for k in ("col1_role", "col2_tool", "col3_quota", "col4_edge")):
            errors.append("grounding_matrix row violates strict 4-column schema")

    if errors:
        print("    [!] LINT FAILED:")
        for e in errors:
            print(f"      - {e}")
        sys.exit(1)
    print(f"    [OK] Lint passed: {len(provs)} providers, {len(cat['forage_routes'])} forage chains, 0 Graveyard leaks.")


def build_readme(cat):
    m = cat["meta"]
    lines = [
        f"# {m['title']} (`v{m['version']}`)",
        f"> {m['tagline']}\n",
        "> [!IMPORTANT]",
        f"> **Editorial Standard:** {m['editorial_note']}\n",
        "---",
        "",
        "## 🧭 1. The Routing Circuit: Where Should Your Workload Go?",
        "*Visualizing why thin TPM pipes (like Groq's 8K cap) choke on 20K-token coding agent turns, while wide pipelines (Google 1M TPM, Z.ai Unlimited Flash, Mistral 1B/mo) sustain autonomous loops.*\n",
        "```mermaid",
        "flowchart LR",
        '    subgraph INTENT ["1. YOUR WORKLOAD"]',
        '        A["🤖 Coding Agent<br/>(20K tok/step)"]',
        '        B["📚 Full Repo / PDF<br/>(100K–1M tok)"]',
        '        C["🔬 PhD Logic / Math<br/>(Deep CoT)"]',
        '        D["⚡ Fast JSON / Router<br/>(<200ms TTFT)"]',
        "    end",
        "",
        '    subgraph PIPE ["2. FREE QUOTA PIPE"]',
        '        P1["🟢 Z.ai BigModel<br/>Unlimited Flash / 5-10 Conc."]',
        '        P2["🔵 Google AI Studio<br/>1,000,000 TPM / 1.5K RPD"]',
        '        P3["🟣 NVIDIA NIM / OpenRouter<br/>40 RPM / 1K RPD ($10 bal)"]',
        '        P4["🟠 Cerebras Wafer-Scale<br/>1M Tok/Day @ 2,000 tok/s"]',
        '        TRAP["🔴 Groq Cloud<br/>❌ 8K TPM Wall (Chokes on 20K)"]',
        "    end",
        "",
        '    A ==>|"Primary (84.3% Term-Bench)"| P1',
        '    A -.->|"Fallback"| P2',
        '    A x--x|"429 Error on Step 1"| TRAP',
        '    B ==>|"Only True 1M Free Pipe"| P2',
        '    C ==>|"Kimi K3 (93.5% GPQA)"| P3',
        '    D ==>|"Qwen3-32B"| P4',
        "```",
        "",
        "<br>",
        "",
        "## ⚡ 2. Task-Routed Intelligence Matrix (Text & Code)",
        "",
        "| Task & Workload | Primary Winner & Proof | Free Gateway & Quota Pipe | The Catch (`Gotcha` & Privacy) |",
        "| :--- | :--- | :--- | :--- |"
    ]

    for r in cat["text_code_matrix"]:
        lines.append(f"| {r['col1_task']} | {r['col2_winner']} | {r['col3_gateway']} | {r['col4_gotcha']} |")

    lines.extend([
        "",
        "<details>",
        "<summary>🛠️ <b>Click to expand Ready-to-Use <code>.env</code> Endpoints & Autonomous Agent Foraging Commands</b></summary>",
        "<br>\n",
        "```bash",
        "# Let the repo automatically probe your environment keys, local Unsloth server, or keyless fallbacks:",
        "python scripts/build.py forage coding-agent",
        "python scripts/build.py forage repo-1m",
        "",
        "# Manual Primary (Z.ai) + Fallback (Google 1M TPM) + Emergency Keyless (Pollinations)",
        'export OPENAI_API_BASE="https://open.bigmodel.cn/api/paas/v4/"',
        'export OPENAI_MODEL="glm-5.3-flash"',
        'export FALLBACK_API_BASE="https://generativelanguage.googleapis.com/v1beta/openai/"',
        'export FALLBACK_MODEL="gemini-3.8-flash"',
        'export KEYLESS_API_BASE="https://text.pollinations.ai/openai"',
        "```",
        "</details>",
        "",
        "---",
        "",
        "## 🎨 3. Multimodal & Sensory Stack (Cloud Free vs. Open-Weights)",
        "",
        "> [!TIP]",
        "> **Why Empty Space Matters Here:** Free cloud GPUs for heavy Video and Music generation rarely exist without watermarks or tiny credit caps. The matrix below explicitly maps **when to use a free cloud API** (Voice STT/TTS, OCR, Flux Images) vs. **when to pivot immediately to Apache-2.0 Open Weights** (`Wan 3.0`, `Kyutai Moshi`, `Stable Audio`) on local or free Colab/Kaggle GPUs.\n",
        "```mermaid",
        "flowchart TD",
        '    M["🎨 Multimodal Workload"] --> A["🎙️ Voice & Duplex Speech"]',
        '    M --> B["📄 Document Vision & OCR"]',
        '    M --> C["🖼️ Image & In-Context Edit"]',
        '    M --> D["🎬 Video & Music Generation"]',
        '    A -->|"Free Cloud API"| A1["Groq: Whisper-Large-v3 (2K RPD)<br/>Fish Audio: S2.1 Pro (Fair-Use Free)"]',
        '    A -->|"Local <200ms Duplex"| A2["Kyutai Moshi / Hibiki & Voxtral (Apache-2.0)"]',
        '    B -->|"Free Cloud API"| B1["Mistral OCR 4 (1B tok/mo)<br/>Gemini 3.8 Flash Vision (1M TPM)"]',
        '    C -->|"Keyless Cloud API"| C1["Pollinations: FLUX Endpoint (0-Auth)"]',
        '    C -->|"Local / Weights"| C2["FLUX.2 Klein & Qwen Image 3 (Apache-2.0)"]',
        '    D -->|"Trial Credits Only"| D1["MiniMax Hailuo H3 ($5) / fal.ai (FLUX 3 Max)"]',
        '    D -->|"True Free Route"| D2["Wan 3.0 & Stable Audio Open (Colab / Local)"]',
        "```",
        "",
        "<br>",
        "",
        "| Modality & Job | Top Verified Models | Free Cloud Route & Quota | Open-Weight / Local Alternative & Gotcha |",
        "| :--- | :--- | :--- | :--- |"
    ])

    for r in cat["multimodal_matrix"]:
        lines.append(f"| {r['col1_modality']} | {r['col2_models']} | {r['col3_cloud']} | {r['col4_local_gotcha']} |")

    lines.extend([
        "",
        "<details>",
        "<summary>🛠️ <b>Click to expand Multimodal Quick-Call Snippets (Zero-Auth FLUX Image & Groq Whisper STT)</b></summary>",
        "<br>\n",
        "```bash",
        "# 1. Zero-Auth Keyless FLUX Image Generation (Pollinations - No API Key Needed)",
        'curl -L "https://image.pollinations.ai/prompt/minimalist_swiss_grid_architecture_diagram?width=1024&height=1024&model=flux&nologo=true" -o diagram.jpg',
        "",
        "# 2. Free Whisper-Large-v3 Audio Transcription (Groq Cloud - 2,000 RPD Free)",
        'curl "https://api.groq.com/openai/v1/audio/transcriptions" \\',
        '  -H "Authorization: Bearer $GROQ_API_KEY" \\',
        '  -F "model=whisper-large-v3" \\',
        '  -F "file=@audio.mp3"',
        "```",
        "</details>",
        "",
        "---",
        "",
        "## 🔍 4. Grounding, Search, Scraping & RAG Stack (100% Card-Free)",
        "",
        "| Grounding Role | Tool & Endpoint | Verified Free Quota | Why It Wins & Technical Gotcha |",
        "| :--- | :--- | :--- | :--- |"
    ])

    for r in cat["grounding_matrix"]:
        lines.append(f"| {r['col1_role']} | {r['col2_tool']} | {r['col3_quota']} | {r['col4_edge']} |")

    lines.extend([
        "",
        "<details>",
        "<summary>🛠️ <b>Click to expand Zero-Auth Foraging Snippets (Jina URL-to-Markdown & OpenAlex Paper Graph)</b></summary>",
        "<br>\n",
        "```bash",
        "# 1. Convert any live webpage or PDF into clean LLM Markdown (Zero Auth, Zero SDK)",
        'curl -s "https://r.jina.ai/https://example.com"',
        "",
        "# 2. Query OpenAlex for latest Open-Access papers (100,000 req/day Free Polite Pool)",
        'curl -s "https://api.openalex.org/works?search=autonomous+coding+agents&filter=is_oa:true&per-page=3&mailto=agent@localhost"',
        "```",
        "</details>",
        "",
        "---",
        "",
        "## 🪦 5. The Graveyard (What We Cut & Why)",
        "",
        "> [!WARNING]",
        "> Most `awesome-*` repositories rot because they never delete dead or bait-and-switch endpoints. These entries are tracked in `data/catalog.yaml` so our upstream sync linter **blocks them from ever being re-added**.\n"
    ])

    for g in cat["graveyard"]:
        lines.append(f"* ❌ **{g['name']}:** {g['reason']}")

    lines.extend([
        "",
        "---",
        "",
        "## 🤖 6. Dual-Interface CLI & Agent Self-Foraging (`llms.txt`)",
        "Point any coding or research agent to [`llms.txt`](llms.txt) or run the built-in CLI:",
        "```bash",
        "python scripts/build.py forage coding-agent   # Auto-detects working env key, local Unsloth, or keyless fallback",
        "python scripts/build.py sync                  # Pulls upstream GitHub commits & strips Graveyard links",
        "python scripts/build.py lint                  # Enforces 4-column layout & relational integrity",
        "python scripts/build.py compile               # Rebuilds README.md and llms.txt from data/catalog.yaml",
        "python scripts/build.py all                   # Runs sync -> lint -> compile",
        "```"
    ])

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def build_llms_txt(cat):
    lines = [
        "# AI Swiss Knife — Agent Foraging Manifest (llms.txt)",
        f"> Version: {cat['meta']['version']} | Machine-readable index of verified zero-cost and keyless AI endpoints.\n",
        "## Tier 0: Immediate Keyless Endpoints (100% Autonomous / No API Key Needed)",
        "- LLM Chat (OpenAI-compat): POST https://text.pollinations.ai/openai/chat/completions (model: 'openai')",
        "- Image Gen (FLUX): GET https://image.pollinations.ai/prompt/{url_encoded_prompt}?model=flux&nologo=true",
        "- Web/PDF to Clean Markdown: GET https://r.jina.ai/{target_url}",
        "- Keyless Web Search (Markdown): GET https://s.jina.ai/?q={query}",
        "- Academic Papers (100K/day Free): GET https://api.openalex.org/works?search={query}&filter=is_oa:true&mailto=agent@localhost\n",
        "## Tier 1: Local Open-Weight Runtime (Check if localhost:8000 is reachable)",
        "- Unsloth Dynamic 3.0 GGUF: http://localhost:8000/v1 (Speaks OpenAI /v1/chat/completions & Anthropic /v1/messages)\n",
        "## Tier 2: Verified No-Card Cloud Free Gateways (Inspect Env Vars Before Calling)"
    ]
    for pid, p in cat["providers"].items():
        if p["tier"] == "tier2-cloud-free":
            lines.append(
                f"- [{pid}] env:{p['env_key']} | base_url:{p['base_url']} | default_model:{p['default_model']} | quota:{p['quota']} | bottleneck:{p['bottleneck']}"
            )

    lines.append("\n## Opinionated Foraging Chains (Run `python scripts/build.py forage <intent>`)")
    for intent, r in cat["forage_routes"].items():
        chain_str = " -> ".join(r["chain"])
        lines.append(f"- {intent} ({r['description']}): {chain_str}")

    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def cmd_compile():
    print("==> [3/3] COMPILE: Generating README.md (Human View) and llms.txt (Agent View)...")
    cat = load_catalog()
    build_readme(cat)
    build_llms_txt(cat)
    print("    [OK] Compiled README.md and llms.txt successfully.")


def cmd_forage(intent=None):
    cat = load_catalog()
    routes = cat["forage_routes"]
    provs = cat["providers"]
    if not intent or intent not in routes:
        print("Available Foraging Intents:")
        for k, v in routes.items():
            print(f"  python scripts/build.py forage {k:<14} # {v['description']}")
        return

    chain = routes[intent]["chain"]
    selected = None
    reason = ""

    for pid in chain:
        p = provs[pid]
        tier = p["tier"]
        env_key = p.get("env_key")

        if tier == "tier2-cloud-free" and env_key and os.environ.get(env_key):
            selected = p
            reason = f"Found active env key ${env_key}"
            break
        elif tier == "tier1-local":
            try:
                r = requests.get(f"{p['base_url']}/models", timeout=1.2)
                if r.status_code == 200:
                    selected = p
                    reason = "Local Unsloth server online at localhost:8000"
                    break
            except Exception:
                continue
        elif tier == "tier0-keyless":
            selected = p
            reason = "Zero-auth keyless fallback (no env keys or local server detected)"
            break

    if not selected:
        selected = provs[chain[0]]
        reason = f"Default primary selected (set ${selected.get('env_key')} to authenticate)"

    print(f"# [AI SWISS KNIFE FORAGER] Intent: {intent} -> Selected: {selected['name']} ({reason})")
    print(f'export OPENAI_API_BASE="{selected["base_url"]}"')
    print(f'export OPENAI_MODEL="{selected["default_model"]}"')
    if selected.get("env_key"):
        k = selected["env_key"]
        print(f'export OPENAI_API_KEY="${{{k}:-sk-none}}"')
    else:
        print('export OPENAI_API_KEY="sk-keyless"')


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == "sync":
        cmd_sync()
    elif cmd == "lint":
        cmd_lint()
    elif cmd == "compile":
        cmd_compile()
    elif cmd == "forage":
        cmd_forage(arg)
    elif cmd == "all":
        cmd_sync()
        cmd_lint()
        cmd_compile()
    else:
        print("Usage: python scripts/build.py [sync|lint|compile|forage <intent>|all]")
        sys.exit(1)
