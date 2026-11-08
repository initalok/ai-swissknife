#!/usr/bin/env python3
"""
AI Swiss Knife Core Engine (Karpathy LLM Wiki Triad: ingest -> lint -> compile)
Usage:
  python scripts/engine.py ingest
  python scripts/engine.py lint
  python scripts/engine.py compile
  python scripts/engine.py all
"""
import os
import sys
import json
import yaml
import requests
from datetime import datetime, timezone

SOURCES_FILE = "upstream/sources.json"
SNAPSHOT_DIR = "upstream/snapshots"
DIFF_REPORT = "upstream/latest_diff_report.md"

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def cmd_ingest():
    print("==> [1/3] INGEST: Pulling upstream snapshots & computing link diffs...")
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    report = [f"# Upstream Sync & Diff Report ({datetime.now(timezone.utc).isoformat()})\n"]

    for repo in registry["repositories"]:
        rid = repo["id"]
        api_url = f"https://api.github.com/repos/{repo['name']}/commits/main"
        try:
            r_meta = requests.get(api_url, timeout=15)
            latest_sha = r_meta.json().get("sha", "unknown")[:10] if r_meta.status_code == 200 else "unknown"

            r_raw = requests.get(repo["raw_readme"], timeout=20)
            if r_raw.status_code == 200:
                snap_path = os.path.join(SNAPSHOT_DIR, f"{rid}.md")
                old_lines = set()
                if os.path.exists(snap_path):
                    with open(snap_path, "r", encoding="utf-8") as sf:
                        old_lines = set(sf.read().splitlines())

                new_lines = set(r_raw.text.splitlines())
                added_links = [l.strip() for l in (new_lines - old_lines) if "http" in l]
                removed_links = [l.strip() for l in (old_lines - new_lines) if "http" in l]

                with open(snap_path, "w", encoding="utf-8") as sf:
                    sf.write(r_raw.text)

                prev_sha = repo.get("last_synced_sha")
                repo["last_synced_sha"] = latest_sha

                report.append(f"## {repo['name']} (`{prev_sha}` -> `{latest_sha}`)")
                report.append(f"- **Added Link Lines:** {len(added_links)} | **Removed Link Lines:** {len(removed_links)}")
                for line in added_links[:10]:
                    report.append(f"  + {line}")
                report.append("")
        except Exception as exc:
            report.append(f"## {repo['name']}\n- Sync warning: {exc}\n")

    registry["last_checked"] = datetime.now(timezone.utc).isoformat()
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    with open(DIFF_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"    Upstream sync complete. Diff written to {DIFF_REPORT}")

def cmd_lint():
    print("==> [2/3] LINT: Auditing relational integrity & schema rules...")
    p1 = load_yaml("data/core_01_providers.yaml")
    p2 = load_yaml("data/core_02_text_and_code.yaml")
    p3 = load_yaml("data/core_03_multimodal.yaml")
    p4 = load_yaml("data/core_04_grounding_rag.yaml")

    errors = []
    valid_providers = {p["id"] for p in p1.get("providers", [])}

    # Check required fields in Pillar 1
    required_p1 = {"id", "name", "url", "bottleneck", "effective_free_context", "trains_on_data", "real_world_gotcha"}
    for prov in p1.get("providers", []):
        missing = required_p1 - set(prov.keys())
        if missing:
            errors.append(f"Pillar 1 provider '{prov.get('id')}' missing fields: {missing}")

    # Check relational references in Pillar 2
    for task in p2.get("tasks", []):
        for model in task.get("models", []):
            for ref in model.get("recommended_providers", []):
                if ref not in valid_providers:
                    errors.append(f"Pillar 2 model '{model['name']}' references unknown provider_id '{ref}'")

    # Check relational references in Pillar 3
    for mod in p3.get("modalities", []):
        for ref in mod.get("provider_refs", []):
            if ref not in valid_providers:
                errors.append(f"Pillar 3 modality '{mod['name']}' references unknown provider_id '{ref}'")

    # Check card-free policy in Pillar 4
    for tool in p4.get("tools", []):
        if tool.get("card_required") is True:
            errors.append(f"Pillar 4 tool '{tool['id']}' requires a credit card (violates card-free grounding rule)")

    if errors:
        print("    [!] LINT FAILED:")
        for err in errors:
            print(f"      - {err}")
        sys.exit(1)
    print(f"    [OK] All 4 pillars passed relational & epistemic lint ({len(valid_providers)} verified providers).")

def cmd_compile():
    print("==> [3/3] COMPILE: Building modular Markdown views & master README...")
    os.makedirs("modules", exist_ok=True)
    p1 = load_yaml("data/core_01_providers.yaml")
    p2 = load_yaml("data/core_02_text_and_code.yaml")
    p3 = load_yaml("data/core_03_multimodal.yaml")
    p4 = load_yaml("data/core_04_grounding_rag.yaml")

    # 1. Compile Pillar 1
    m1 = [f"# {p1['title']}\n> {p1['description']}\n",
          "| Provider | Access Type | Free Quota Summary | Bottleneck | Effective Context | Trains on Data? | Real-World Gotcha |",
          "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"]
    for p in p1["providers"]:
        m1.append(f"| [**{p['name']}**]({p['url']}) (`{p['id']}`) | `{p['access_type']}` | {p['quota_summary']} | {p['bottleneck']} | {p['effective_free_context']} | {p['trains_on_data']} | {p['real_world_gotcha']} |")
    with open("modules/01-providers.md", "w", encoding="utf-8") as f:
        f.write("\n".join(m1) + "\n")

    # 2. Compile Pillar 2
    m2 = [f"# {p2['title']}\n> {p2['description']}\n"]
    for t in p2["tasks"]:
        m2.append(f"## Role: `{t['primary_role']}`\n*{t['job_description']}*\n")
        m2.append("| Model | Origin / License | Benchmark Proof | Optimal Free Upstreams | Agent-Loop Ready |")
        m2.append("| :--- | :--- | :--- | :--- | :--- |")
        for m in t["models"]:
            upstreams = ", ".join(f"`{u}`" for u in m["recommended_providers"])
            ready = "Yes" if m.get("agent_ready") else "Router/Edge Only"
            m2.append(f"| **{m['name']}** | `{m['origin_region']}` / `{m['license']}` | {m['benchmark_proof']} | {upstreams} | {ready} |")
        m2.append("")
    with open("modules/02-text-and-code.md", "w", encoding="utf-8") as f:
        f.write("\n".join(m2) + "\n")

    # 3. Compile Pillar 3
    m3 = [f"# {p3['title']}\n> {p3['description']}\n",
          "| Category | Top Verified Models / APIs | Region | Access Route | Linked Gateways | Benchmark / Niche Edge |",
          "| :--- | :--- | :--- | :--- | :--- | :--- |"]
    for mod in p3["modalities"]:
        refs = ", ".join(f"`{r}`" for r in mod.get("provider_refs", []))
        m3.append(f"| `{mod['category']}` | [**{mod['name']}**]({mod['external_url']}) | `{mod['origin_region']}` | `{mod['access_route']}` | {refs} | {mod['benchmark_edge']} |")
    with open("modules/03-multimodal.md", "w", encoding="utf-8") as f:
        f.write("\n".join(m3) + "\n")

    # 4. Compile Pillar 4
    m4 = [f"# {p4['title']}\n> {p4['description']}\n",
          "| Role | Tool / Endpoint | Free Quota (No Card) | Technical Edge |",
          "| :--- | :--- | :--- | :--- |"]
    for tool in p4["tools"]:
        m4.append(f"| **{tool['role']}** | [**{tool['name']}**]({tool['url']}) | {tool['free_quota']} | {tool['technical_edge']} |")
    with open("modules/04-grounding-rag.md", "w", encoding="utf-8") as f:
        f.write("\n".join(m4) + "\n")

    # 5. Compile Master README
    readme = [
        "# AI Swiss Knife Knowledge Base (`v0.1.0-core`)",
        "> A lean, modular, benchmark-filtered, and upstream-synced AI resource database.\n",
        "## Core Architecture (4-Pillar Relational Database)",
        "- **[Pillar 1: Verified API Gateways & Runtimes](modules/01-providers.md)** — Cloud gateways + Unsloth local runtime with rate-limit bottlenecks, effective context caps, and privacy audits.",
        "- **[Pillar 2: Task-Routed Text & Coding Models](modules/02-text-and-code.md)** — Benchmark-verified frontier generalists & niche specialists (SWE-bench, Terminal-Bench 2.1, GPQA Diamond).",
        "- **[Pillar 3: Multimodal Specialty APIs & Open Weights](modules/03-multimodal.md)** — Audio (STT/TTS/Duplex), Document OCR, Image (`FLUX.2`/`Kontext`), Video (`FLUX 3 Max`/`Seedance 2.5`/`Wan 3.0`), & Music.",
        "- **[Pillar 4: Search, Scraping, Reranking & Academic Grounding](modules/04-grounding-rag.md)** — Card-free agent grounding (`Firecrawl Keyless`, `Jina Reader`, `Exa 3.0`, `Tavily`, `Cohere Embed/Rerank 5`, `OpenAlex`).\n",
        "## Engine CLI (`Ingest -> Lint -> Compile`)",
        "```bash",
        "python scripts/engine.py ingest   # Pull latest upstream READMEs & generate diff report",
        "python scripts/engine.py lint     # Audit relational integrity & schema rules",
        "python scripts/engine.py compile  # Auto-generate modules/*.md and README.md",
        "python scripts/engine.py all      # Run full pipeline",
        "```"
    ]
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(readme) + "\n")
    print("    [OK] Compiled modules/01..04.md and README.md successfully.")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "ingest":
        cmd_ingest()
    elif cmd == "lint":
        cmd_lint()
    elif cmd == "compile":
        cmd_compile()
    elif cmd == "all":
        cmd_ingest()
        cmd_lint()
        cmd_compile()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
