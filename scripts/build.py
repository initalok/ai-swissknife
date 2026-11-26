#!/usr/bin/env python3
"""
AI Swiss Knife Field Book Engine (v2.0.0-beta.1)
Commands:
  python scripts/build.py lint                      # Enforce 5-beat schema, 4-col law & scoped Graveyards
  python scripts/build.py compile                   # Build README.md, book/*.md, llms.txt, llms-full.txt
  python scripts/build.py sync                      # Pull upstream repos & filter Graveyard URLs
  python scripts/build.py forage <intent>           # Cloud/local/keyless auto-foraging
  python scripts/build.py forage <profile> --local  # Local 16GB+64GB launch command
  python scripts/build.py all [--sync]              # Run [optional sync ->] lint -> compile
"""
import json
import os
import sys
import yaml
import requests
from datetime import datetime, timezone

META_PATH = "data/meta.yaml"
CLOUD_PATH = "data/01_cloud.yaml"
LOCAL_PATH = "data/02_local.yaml"
SOURCES_PATH = "upstream/sources.json"
SNAPSHOT_DIR = "upstream/snapshots"
DIFF_REPORT = "upstream/latest_diff_report.md"


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_book():
    meta = load_yaml(META_PATH)
    chapters = [load_yaml(p) for p in meta["chapters"]]
    graveyard = load_yaml(meta["graveyard_file"])
    return meta, chapters, graveyard


def cmd_sync():
    print("==> [SYNC] Pulling upstream snapshots & filtering Cloud + Local Graveyards...")
    if not os.path.exists(SOURCES_PATH):
        print(f"    [WARN] {SOURCES_PATH} not found; skipping upstream sync.")
        return

    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    _, _, graveyard = load_book()
    patterns = [
        g["match_pattern"].lower()
        for bucket in ("cloud_graveyard", "local_graveyard")
        for g in graveyard.get(bucket, [])
        if g.get("match_pattern")
    ]

    with open(SOURCES_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    report = [f"# Upstream Sync & Diff Report ({datetime.now(timezone.utc).isoformat()})\n"]
    for repo in registry.get("repositories", []):
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
    print("==> [LINT] Auditing 5-beat schema, 4-column law, forage chains, & scoped Graveyards...")
    meta, chapters, graveyard = load_book()
    errors = []

    cloud_bans = [g["match_pattern"].lower() for g in graveyard.get("cloud_graveyard", [])]
    local_bans = [g["match_pattern"].lower() for g in graveyard.get("local_graveyard", [])]

    for ch in chapters:
        cid = ch.get("id", "unknown")
        for req in ("number", "title", "short_title", "output_file", "part", "verdict", "read_if", "sections"):
            if req not in ch:
                errors.append(f"[{cid}] Missing required 5-beat field '{req}'")

        # Scoped provider & forage validation for Ch 01 Cloud
        if cid == "01-cloud":
            provs = ch.get("providers", {})
            req_p = {"name", "url", "base_url", "tier", "default_model", "quota", "bottleneck", "effective_context", "trains_on_data"}
            for pid, p in provs.items():
                missing = req_p - set(p.keys())
                if missing:
                    errors.append(f"[01-cloud] Provider '{pid}' missing keys: {missing}")
                blob = f"{p.get('url', '')} {p.get('base_url', '')} {p.get('default_model', '')}".lower()
                for pat in cloud_bans:
                    if pat in blob:
                        errors.append(f"[01-cloud] Provider '{pid}' matches Cloud Graveyard ban '{pat}'")
            for intent, r in ch.get("forage_routes", {}).items():
                for ref in r.get("chain", []):
                    if ref not in provs:
                        errors.append(f"[01-cloud] Forage route '{intent}' references unknown provider '{ref}'")

        # Scoped local profile validation for Ch 02 Local
        if cid == "02-local":
            for pid, p in ch.get("forage_local_profiles", {}).items():
                blob = f"{p.get('model', '')} {p.get('launch', '')}".lower()
                for pat in local_bans:
                    if pat in blob:
                        errors.append(f"[02-local] Local profile '{pid}' matches Local Graveyard ban '{pat}'")

        # Enforce 4-column law & scoped Graveyard bans on recommended columns (c1..c3)
        active_bans = cloud_bans if cid == "01-cloud" else (local_bans if cid in ("02-local", "03-multimodal") else [])
        for sec in ch.get("sections", []):
            if len(sec.get("headers", [])) != 4:
                errors.append(f"[{cid}] Section '{sec.get('heading')}' violates strict 4-column law")
            for idx, row in enumerate(sec.get("rows", []), 1):
                if not all(k in row for k in ("c1", "c2", "c3", "c4")):
                    errors.append(f"[{cid}] Row {idx} in '{sec.get('heading')}' missing c1..c4")
                rec_blob = " ".join(str(row.get(k, "")) for k in ("c1", "c2", "c3")).lower()
                for pat in active_bans:
                    if pat in rec_blob:
                        errors.append(f"[{cid}] Row {idx} in '{sec.get('heading')}' recommends banned '{pat}'")

    if errors:
        print("    [!] BOOK LINT FAILED:")
        for e in errors:
            print(f"      - {e}")
        sys.exit(1)
    print(f"    [OK] Lint passed: {len(chapters)} chapters verified, {len(cloud_bans)} cloud + {len(local_bans)} local Graveyard bans enforced.")


def render_breadcrumb(chapters, idx):
    prev_link = (
        f"← [{chapters[idx - 1]['short_title']}]({os.path.basename(chapters[idx - 1]['output_file'])})"
        if idx > 0
        else "← [🏠 Field Book Cover](../README.md)"
    )
    next_link = (
        f"[{chapters[idx + 1]['short_title']}]({os.path.basename(chapters[idx + 1]['output_file'])}) →"
        if idx + 1 < len(chapters)
        else "[🪦 Appendix: Graveyard](99-graveyard.md) →"
    )
    return f"{prev_link} &nbsp;|&nbsp; [🏠 Cover](../README.md) &nbsp;|&nbsp; {next_link}"


def render_chapter(ch, breadcrumb):
    lines = [
        breadcrumb,
        "",
        f"# {ch['title']}",
        "",
        "> [!IMPORTANT]",
        f"> **Verdict:** {ch['verdict']}",
        f"> **Read this chapter if:** {ch['read_if']}",
        "",
    ]
    if ch.get("mermaid"):
        lines.extend(["```mermaid", ch["mermaid"].rstrip(), "```", "", "<br>", ""])

    for sec in ch.get("sections", []):
        h = sec["headers"]
        lines.extend([
            f"## {sec['heading']}",
            "",
            f"| {h[0]} | {h[1]} | {h[2]} | {h[3]} |",
            "| :--- | :--- | :--- | :--- |",
        ])
        for r in sec.get("rows", []):
            lines.append(f"| {r['c1']} | {r['c2']} | {r['c3']} | {r['c4']} |")
        lines.append("")

    for d in ch.get("drawers", []):
        lines.extend([
            "<details>",
            f"<summary>🛠️ <b>{d['summary']}</b></summary>",
            "<br>",
            "",
            f"```{d.get('lang', 'bash')}",
            d["code"].rstrip(),
            "```",
            "</details>",
            "",
        ])

    lines.extend(["---", "", breadcrumb])
    return "\n".join(lines) + "\n"


def render_cover(meta, chapters):
    lines = [
        f"# {meta['title']} (`v{meta['version']}`)",
        f"> {meta['tagline']}",
        "",
        f"**Hardware Local Envelope:** `{meta['hardware_envelope']}` · **Design Rules:** [`DESIGN_SYSTEM.md`](docs/DESIGN_SYSTEM.md) · **Agent Manifests:** [`llms.txt`](llms.txt) · [`llms-full.txt`](llms-full.txt)",
        "",
        "> [!IMPORTANT]",
        f"> **Editorial Constitution:** {meta['editorial_constitution']}",
        "",
        "## 🧭 The 3-Second Universal Compass",
        "",
        "```mermaid",
        meta["compass_mermaid"].rstrip(),
        "```",
        "",
        "## 📖 Field Book Contents",
        "",
        "| Chapter | Part | Scope & Core Verdict | Direct Link |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for ch in chapters:
        clean_name = ch["short_title"].split(": ")[-1]
        lines.append(
            f"| **{ch['number']} · {clean_name}** | `{ch['part']}` | {ch['verdict']} | [**Open Chapter →**]({ch['output_file']}) |"
        )
    lines.append(
        "| **99 · The Graveyard** | `APPENDIX` | Machine-enforced cut list of dead cloud tiers & >80 GB local walls. | [**Inspect Cuts →**](book/99-graveyard.md) |"
    )
    lines.extend([
        "",
        "## 🤖 Dual-Interface CLI & Agent Self-Foraging",
        "```bash",
        "python scripts/build.py forage coding-agent             # Cloud/local/keyless auto-foraging",
        "python scripts/build.py forage inkling-coding --local   # Local 16GB+64GB launch profile",
        "python scripts/build.py forage qwen-27b-super-adapter --local",
        "python scripts/build.py all                             # Lint + compile Cover, Book, & llms*.txt",
        "```",
        "",
        "---",
        "*Built from `data/*.yaml` via `scripts/build.py`. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CHANGELOG.md`](CHANGELOG.md).*",
    ])
    return "\n".join(lines) + "\n"


def render_graveyard(chapters, graveyard):
    last_ch = chapters[-1]
    nav = f"← [{last_ch['short_title']}]({os.path.basename(last_ch['output_file'])}) &nbsp;|&nbsp; [🏠 Cover](../README.md)"
    lines = [
        nav,
        "",
        "# 🪦 Appendix · The Graveyard (Machine-Enforced Cut List)",
        "",
        "> [!WARNING]",
        "> Every pattern below is automatically blocked by `scripts/build.py lint` and `.github/workflows/ci_lint.yml`.",
        "",
        "## 🌐 Cloud API Graveyard",
    ]
    for g in graveyard.get("cloud_graveyard", []):
        lines.append(f"- ❌ **{g['name']}:** {g['reason']}")
    lines.append("\n## 🖥️ Local Hardware Wall Graveyard (`16GB VRAM + 64GB RAM`)")
    for g in graveyard.get("local_graveyard", []):
        lines.append(f"- ❌ **{g['name']}:** {g['reason']}")
    lines.extend(["", "---", "", nav])
    return "\n".join(lines) + "\n"


def render_llms(meta, chapters):
    cloud = load_yaml(CLOUD_PATH)
    local = load_yaml(LOCAL_PATH)

    compact = [
        f"# AI Swiss Knife — Compact Agent Router (v{meta['version']})",
        f"> Local Hardware Envelope: {meta['hardware_envelope']}",
        "> Fetch `llms-full.txt` for complete tables or open individual `book/*.md` chapters.\n",
        "## Tier 0: Immediate Keyless Endpoints (No API Key Required)",
        "- LLM Chat (OpenAI-compat): POST https://text.pollinations.ai/openai/chat/completions (model: 'openai')",
        "- Image Gen (FLUX): GET https://image.pollinations.ai/prompt/{prompt}?model=flux&nologo=true",
        "- Web/PDF to Markdown: GET https://r.jina.ai/{target_url}",
        "- Keyless Search: GET https://s.jina.ai/?q={query}",
        "- Firecrawl Keyless Skill: GET https://www.firecrawl.dev/agent-onboarding/SKILL.md",
        "- Academic Papers (100K/day): GET https://api.openalex.org/works?search={query}&filter=is_oa:true&mailto=agent@localhost\n",
        "## Tier 1: Local Runtime (`python scripts/build.py forage <id> --local`)",
        "- Unsloth / llama-server: http://localhost:8000/v1 | Local Laya Decisions: http://localhost:8888",
    ]
    for pid, p in local.get("forage_local_profiles", {}).items():
        compact.append(f"- [{pid}] ({p['zone']}) -> `{p['launch']}`")

    compact.append("\n## Tier 2: Verified No-Card Cloud Gateways (`python scripts/build.py forage <intent>`)")
    for pid, p in cloud.get("providers", {}).items():
        if p.get("tier") == "tier2-cloud-free":
            compact.append(f"- [{pid}] env:{p['env_key']} | base_url:{p['base_url']} | model:{p['default_model']}")

    compact.append("\n## Field Book Chapters")
    full = [f"# AI Swiss Knife — Full Machine-Readable Index (v{meta['version']})\n"]
    for ch in chapters:
        compact.append(f"- [{ch['short_title']}]({ch['output_file']}): {ch['verdict']}")
        full.append(f"## {ch['title']}\nVerdict: {ch['verdict']}\n")
        for sec in ch.get("sections", []):
            full.append(f"### {sec['heading']}")
            for r in sec.get("rows", []):
                full.append(f"- {r['c1']} | {r['c2']} | {r['c3']} | {r['c4']}")
            full.append("")
    return "\n".join(compact) + "\n", "\n".join(full) + "\n"


def cmd_compile():
    print("==> [COMPILE] Generating README.md, book/01..06 + 99-graveyard, llms.txt, & llms-full.txt...")
    meta, chapters, graveyard = load_book()
    os.makedirs("book", exist_ok=True)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(render_cover(meta, chapters))

    for idx, ch in enumerate(chapters):
        with open(ch["output_file"], "w", encoding="utf-8") as f:
            f.write(render_chapter(ch, render_breadcrumb(chapters, idx)))

    with open("book/99-graveyard.md", "w", encoding="utf-8") as f:
        f.write(render_graveyard(chapters, graveyard))

    compact, full = render_llms(meta, chapters)
    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write(compact)
    with open("llms-full.txt", "w", encoding="utf-8") as f:
        f.write(full)
    print(f"    [OK] Compiled README.md, {len(chapters)} chapters, 99-graveyard.md, llms.txt, & llms-full.txt.")


def cmd_forage(intent=None, local_mode=False):
    if local_mode:
        loc = load_yaml(LOCAL_PATH)
        profiles = loc.get("forage_local_profiles", {})
        if not intent or intent not in profiles:
            print("Available Local 16GB+64GB Profiles (`--local`):")
            for k, v in profiles.items():
                print(f"  python scripts/build.py forage {k:<24} --local  # {v['zone']}")
            return
        p = profiles[intent]
        print(f"# [LOCAL FORAGER] {intent} | {p['zone']} | Runtime: {p['runtime']}")
        print(p["launch"])
        return

    cloud = load_yaml(CLOUD_PATH)
    routes = cloud.get("forage_routes", {})
    provs = cloud.get("providers", {})
    if not intent or intent not in routes:
        print("Available Cloud Foraging Intents:")
        for k, v in routes.items():
            print(f"  python scripts/build.py forage {k:<16} # {v['description']}")
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
    sync_flag = "--sync" in args
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
        if sync_flag:
            cmd_sync()
        cmd_lint()
        cmd_compile()
    else:
        print("Usage: python scripts/build.py [sync|lint|compile|forage <id> [--local]|all [--sync]]")
        sys.exit(1)
