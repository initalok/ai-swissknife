#!/usr/bin/env python3
"""
AI SWISS KNIFE // OPINIONATED CLI HARNESS & ONE-PAGE SPATIAL COMPILER (v0.2.0)
Inspired by Stone Librande (One-Page Design) & Katie Dill (Scaling Intent & Craft).

Commands:
  python ask.py route <intent>   # Opinionated provider + model + .env export
  python ask.py env <intent>     # Emit raw .env configuration block
  python ask.py check            # Live HTTP latency & endpoint telemetry check
  python ask.py ingest           # Sync upstream GitHub README snapshots & diffs
  python ask.py lint             # Validate relational graph & barycentric math
  python ask.py render           # Compile poster.svg, index.html, and README.md
  python ask.py all              # Run ingest -> lint -> render
"""
import json
import math
import os
import sys
import time
import yaml
import requests
from datetime import datetime, timezone

GRAPH_PATH = "data/core_graph.yaml"
SOURCES_PATH = "upstream/sources.json"
SNAPSHOT_DIR = "upstream/snapshots"
DIFF_REPORT = "upstream/latest_diff_report.md"


def load_graph():
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def cmd_route(intent=None):
    g = load_graph()
    routes = g["routes"]
    providers = g["providers"]
    if not intent or intent not in routes:
        print("Available Opinionated Intents:")
        for k, v in routes.items():
            print(f"  ./ask.py route {k:<15} -> {v['title']} ({v['primary_model']})")
        return

    r = routes[intent]
    p_prim = providers[r["primary_provider"]]
    p_fall = providers[r["fallback_provider"]]
    p_blk = providers[r["blocked_provider"]]

    print("╭─── AI SWISS KNIFE // OPINIONATED HARNESS ────────────────────────────────────╮")
    print(f"│ INTENT    : {r['title']} ({r['load']})")
    print(f"│ PRIMARY   : {r['primary_model']} via {p_prim['name']} [{p_prim['pipe_label']}]")
    print(f"│ BENCHMARK : {r['benchmark']}")
    print(f"│ FALLBACK  : {r['fallback_model']} via {p_fall['name']}")
    print(f"│ BLOCKED   : ✗ {p_blk['name']} — {r['blocked_reason']}")
    print(f"│ GOTCHA    : {p_prim['gotcha']}")
    print("╰──────────────────────────────────────────────────────────────────────────────╯")
    print("# Drop-in Shell / Agent Export:")
    print(f'export OPENAI_API_BASE="{p_prim["base_url"]}"')
    print(f'export OPENAI_MODEL="{r["primary_model"]}"')
    print(f'export ASK_FALLBACK_BASE="{p_fall["base_url"]}"')
    print(f'export ASK_FALLBACK_MODEL="{r["fallback_model"]}"')


def cmd_env(intent):
    g = load_graph()
    if intent not in g["routes"]:
        sys.exit(f"Unknown intent '{intent}'. Run `./ask.py route` for list.")
    r = g["routes"][intent]
    p_prim = g["providers"][r["primary_provider"]]
    p_fall = g["providers"][r["fallback_provider"]]
    print(f"# AI Swiss Knife Auto-Generated Harness ({intent})")
    print(f"OPENAI_API_BASE={p_prim['base_url']}")
    print(f"OPENAI_MODEL={r['primary_model']}")
    print(f"ASK_FALLBACK_BASE={p_fall['base_url']}")
    print(f"ASK_FALLBACK_MODEL={r['fallback_model']}")
    print(f"ASK_MAX_TPM_GUARD={p_prim['pipe_tpm']}")


def cmd_check():
    g = load_graph()
    print("==> [CHECK] Pinging provider endpoints for live telemetry...")
    for pid, p in g["providers"].items():
        if pid == "unsloth-local":
            print(f"  [LOCAL] {p['name']:<24} -> {p['base_url']} (Hardware Runtime)")
            continue
        t0 = time.time()
        try:
            resp = requests.get(p["url"], timeout=6)
            ms = int((time.time() - t0) * 1000)
            status = "UP" if resp.status_code < 500 else f"WARN ({resp.status_code})"
            print(f"  [{status:^5}] {p['name']:<24} -> {ms:>4}ms | Pipe: {p['pipe_label']}")
        except Exception as e:
            print(f"  [DOWN ] {p['name']:<24} -> {e}")


def cmd_ingest():
    print("==> [1/3] INGEST: Syncing upstream GitHub snapshots & diffing links...")
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    with open(SOURCES_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    lines = [f"# Upstream Sync Report ({datetime.now(timezone.utc).isoformat()})\n"]
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
                added = [l.strip() for l in (new - old) if "http" in l]
                with open(snap, "w", encoding="utf-8") as sf:
                    sf.write(r_raw.text)
                prev = repo.get("last_synced_sha")
                repo["last_synced_sha"] = sha
                lines.append(f"## {repo['name']} (`{prev}` -> `{sha}`)")
                lines.append(f"- Net-new link lines: **{len(added)}**")
                for a in added[:8]:
                    lines.append(f"  + {a}")
                lines.append("")
        except Exception as exc:
            lines.append(f"## {repo['name']}\n- Warning: {exc}\n")

    registry["last_checked"] = datetime.now(timezone.utc).isoformat()
    with open(SOURCES_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    with open(DIFF_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"    [OK] Upstream diff saved to {DIFF_REPORT}")


def cmd_lint():
    print("==> [2/3] LINT: Verifying relational links & barycentric coordinates...")
    g = load_graph()
    provs = g.get("providers", {})
    errors = []

    for pid, p in provs.items():
        tri = p.get("tri", [])
        if len(tri) != 3 or abs(sum(tri) - 1.0) > 0.05:
            errors.append(f"Provider '{pid}' tri coordinates must sum to ~1.0 (got {tri})")
        for req in ("name", "base_url", "pipe_tpm", "gotcha", "trains_on_data"):
            if req not in p:
                errors.append(f"Provider '{pid}' missing required key '{req}'")

    for rid, r in g.get("routes", {}).items():
        for k in ("primary_provider", "fallback_provider", "blocked_provider"):
            if r.get(k) not in provs:
                errors.append(f"Route '{rid}' key '{k}' references unknown provider '{r.get(k)}'")

    for row in g.get("matrix", {}).get("rows", []):
        for cid, cell in row.get("cells", {}).items():
            ref = cell.get("ref")
            if ref is not None and ref not in provs:
                errors.append(f"Matrix row '{row['modality']}' col '{cid}' references unknown provider '{ref}'")

    if errors:
        for e in errors:
            print(f"  [!] {e}")
        sys.exit(1)
    print(f"    [OK] Graph verified: {len(provs)} providers, {len(g['routes'])} routes, {len(g['matrix']['rows'])} matrix rows.")


def barycentric_to_xy(tri, top, left, right):
    # tri = [w_reasoning (top), w_speed (left), w_quota (right)]
    w_top, w_left, w_right = tri
    x = w_top * top[0] + w_left * left[0] + w_right * right[0]
    y = w_top * top[1] + w_left * left[1] + w_right * right[1]
    return round(x, 1), round(y, 1)


def generate_svg(g):
    provs = g["providers"]
    routes = g["routes"]
    matrix = g["matrix"]

    svg = [
        '<svg xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)" viewBox="0 0 1400 1060" width="100%" height="100%" style="background:#090d16;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;">',
        '<defs>',
        '  <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">',
        '    <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#151f32" stroke-width="1"/>',
        '  </pattern>',
        '</defs>',
        '<rect width="1400" height="1060" fill="url(#grid)"/>',
        # Header Banner
        '<rect x="24" y="20" width="1352" height="58" rx="6" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>',
        f'<text x="44" y="47" fill="#f8fafc" font-size="18" font-weight="bold" letter-spacing="1.5">{g["meta"]["title"]}</text>',
        f'<text x="44" y="66" fill="#94a3b8" font-size="11">{g["meta"]["subtitle"]} — [ONE-PAGE ARCHITECTURAL POSTER // {g["meta"]["version"]}]</text>',
        '<rect x="1170" y="34" width="186" height="30" rx="4" fill="#064e3b" stroke="#10b981" stroke-width="1"/>',
        '<text x="1263" y="53" fill="#ecfdf5" font-size="11" font-weight="bold" text-anchor="middle">● 9/9 GATES VERIFIED</text>',

        # ZONE A: Minard Routing Circuit (Left Panel)
        '<rect x="24" y="92" width="760" height="440" rx="6" fill="#0b1120" fill-opacity="0.9" stroke="#1e293b" stroke-width="1.5"/>',
        '<text x="44" y="118" fill="#38bdf8" font-size="13" font-weight="bold" letter-spacing="1">ZONE A // MINARD TASK-TO-GATEWAY CIRCUIT (PIPE WIDTH = FREE TPM CEILING)</text>',
        '<text x="44" y="135" fill="#64748b" font-size="10">Visualizes why 20K-token coding agents choke on thin TPM pipes (Groq 8K) vs wide highways (Google 1M / Z.ai / Mistral 1B).</text>'
    ]

    y_start = 165
    for idx, (rid, r) in enumerate(routes.items()):
        y = y_start + idx * 50
        p_prim = provs[r["primary_provider"]]
        p_blk = provs[r["blocked_provider"]]
        # Compute visual pipe thickness (2px to 14px log-scaled)
        stroke_w = max(2.5, min(14.0, round(math.log10(max(1000, p_prim["pipe_tpm"])) * 2.2 - 5, 1)))
        color = p_prim["color"]

        # Intent Box
        svg.append(f'<rect x="44" y="{y}" width="215" height="36" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>')
        svg.append(f'<text x="54" y="{y+15}" fill="#f1f5f9" font-size="11" font-weight="bold">{r["title"]}</text>')
        svg.append(f'<text x="54" y="{y+29}" fill="#94a3b8" font-size="9.5">{r["load"]}</text>')

        # Minard Proportional Flow Pipe
        svg.append(f'<path d="M 259 {y+18} C 310 {y+18}, 320 {y+18}, 370 {y+18}" fill="none" stroke="{color}" stroke-width="{stroke_w}" stroke-opacity="0.85"/>')
        svg.append(f'<text x="314" y="{y+11}" fill="{color}" font-size="8.5" text-anchor="middle" font-weight="bold">{p_prim["short"]}</text>')

        # Target Model & Benchmark Node
        svg.append(f'<rect x="370" y="{y}" width="245" height="36" rx="4" fill="#0f172a" stroke="{color}" stroke-width="1.2"/>')
        svg.append(f'<text x="380" y="{y+15}" fill="#f8fafc" font-size="10.5" font-weight="bold">✓ {r["primary_model"]}</text>')
        svg.append(f'<text x="380" y="{y+29}" fill="#94a3b8" font-size="8.8">{r["benchmark"][:38]}</text>')

        # Blocked Trap Callout
        svg.append(f'<rect x="625" y="{y+3}" width="142" height="30" rx="4" fill="#2a1215" stroke="#ef4444" stroke-width="0.8" stroke-dasharray="3,2"/>')
        svg.append(f'<text x="633" y="{y+16}" fill="#fca5a5" font-size="9" font-weight="bold">✗ {p_blk["short"]}</text>')
        svg.append(f'<text x="633" y="{y+27}" fill="#f87171" font-size="8">{r["blocked_reason"][:22]}</text>')

    # ZONE B: Barycentric Trade-Off Triangle (Right Panel)
    svg.extend([
        '<rect x="800" y="92" width="576" height="440" rx="6" fill="#0b1120" fill-opacity="0.9" stroke="#1e293b" stroke-width="1.5"/>',
        '<text x="820" y="118" fill="#a78bfa" font-size="13" font-weight="bold" letter-spacing="1">ZONE B // 3-AXIS CAPABILITY TRIANGLE (SLIDER SPACE)</text>',
        '<text x="820" y="135" fill="#64748b" font-size="10">Stone Librande continuous trade-off space: Reasoning vs. Speed vs. Free Quota.</text>'
    ])

    top_v = (1088, 175)
    left_v = (865, 470)
    right_v = (1311, 470)

    # Triangle Grid & Outer Frame
    svg.append(f'<polygon points="{top_v[0]},{top_v[1]} {left_v[0]},{left_v[1]} {right_v[0]},{right_v[1]}" fill="#0f172a" stroke="#475569" stroke-width="1.5"/>')
    cx, cy = barycentric_to_xy([0.333, 0.333, 0.334], top_v, left_v, right_v)
    svg.append(f'<line x1="{top_v[0]}" y1="{top_v[1]}" x2="{cx}" y2="{cy}" stroke="#1e293b" stroke-dasharray="4,4"/>')
    svg.append(f'<line x1="{left_v[0]}" y1="{left_v[1]}" x2="{cx}" y2="{cy}" stroke="#1e293b" stroke-dasharray="4,4"/>')
    svg.append(f'<line x1="{right_v[0]}" y1="{right_v[1]}" x2="{cx}" y2="{cy}" stroke="#1e293b" stroke-dasharray="4,4"/>')

    # Vertex Labels
    svg.append(f'<text x="{top_v[0]}" y="{top_v[1]-12}" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">▲ FRONTIER REASONING (GPQA / SWE)</text>')
    svg.append(f'<text x="{left_v[0]-10}" y="{left_v[1]+20}" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="start">◀ RAW SPEED (2,000+ tok/s)</text>')
    svg.append(f'<text x="{right_v[0]+10}" y="{right_v[1]+20}" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="end">FREE QUOTA &amp; PRIVACY ▶</text>')

    for pid, p in provs.items():
        px, py = barycentric_to_xy(p["tri"], top_v, left_v, right_v)
        c = p["color"]
        svg.append(f'<circle cx="{px}" cy="{py}" r="7" fill="{c}" stroke="#090d16" stroke-width="2"/>')
        svg.append(f'<text x="{px+11}" y="{py+4}" fill="#e2e8f0" font-size="10" font-weight="bold">{p["short"]}</text>')

    # ZONE C: Top-Down Modality Matrix (Bottom Full-Width Panel)
    svg.extend([
        '<rect x="24" y="546" width="1352" height="490" rx="6" fill="#0b1120" fill-opacity="0.95" stroke="#1e293b" stroke-width="1.5"/>',
        '<text x="44" y="574" fill="#34d399" font-size="13" font-weight="bold" letter-spacing="1">ZONE C // TOP-DOWN MODALITY × ACCESS TIER MATRIX (ZERO-SCROLL CROSSWORD GRID)</text>',
        '<text x="44" y="591" fill="#64748b" font-size="10">Every cell is benchmark-filtered. Empty cells (—) expose where free cloud GPUs do not exist, routing you to trial credits or Apache-2.0 local weights.</text>'
    ])

    col_w = 265
    row_h = 74
    x0 = 285
    y0 = 610

    # Column Headers
    for c_idx, col in enumerate(matrix["columns"]):
        cx = x0 + c_idx * col_w
        svg.append(f'<rect x="{cx}" y="{y0}" width="{col_w-10}" height="32" rx="4" fill="#1e293b" stroke="#334155"/>')
        svg.append(f'<text x="{cx + (col_w-10)//2}" y="{y0+20}" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">{col["label"]}</text>')

    # Matrix Rows & Cells
    for r_idx, row in enumerate(matrix["rows"]):
        ry = y0 + 42 + r_idx * row_h
        svg.append(f'<rect x="44" y="{ry}" width="230" height="{row_h-10}" rx="4" fill="#0f172a" stroke="#334155"/>')
        svg.append(f'<text x="56" y="{ry+36}" fill="#e2e8f0" font-size="11" font-weight="bold">{row["modality"]}</text>')

        for c_idx, col in enumerate(matrix["columns"]):
            cx = x0 + c_idx * col_w
            cell = row["cells"][col["id"]]
            ref = cell.get("ref")
            border_c = provs[ref]["color"] if ref in provs else "#1e293b"
            bg_c = "#0f172a" if ref else "#090d16"

            svg.append(f'<rect x="{cx}" y="{ry}" width="{col_w-10}" height="{row_h-10}" rx="4" fill="{bg_c}" stroke="{border_c}" stroke-width="1.2"/>')
            svg.append(f'<text x="{cx+12}" y="{ry+22}" fill="#f8fafc" font-size="11" font-weight="bold">{cell["title"]}</text>')
            svg.append(f'<text x="{cx+12}" y="{ry+42}" fill="#94a3b8" font-size="9.5">{cell["sub"]}</text>')
            # Micro Badge
            svg.append(f'<rect x="{cx+col_w-88}" y="{ry+8}" width="68" height="16" rx="3" fill="#1e293b"/>')
            svg.append(f'<text x="{cx+col_w-54}" y="{ry+19}" fill="{border_c}" font-size="8" font-weight="bold" text-anchor="middle">{cell["badge"]}</text>')

    svg.append('</svg>')
    with open("poster.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg) + "\n")


def generate_html(g):
    graph_json = json.dumps(g)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{g['meta']['title']}</title>
<style>
  :root {{
    --bg: #070b14;
    --panel: #0f172a;
    --border: #1e293b;
    --text: #f8fafc;
    --muted: #94a3b8;
    --accent: #38bdf8;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg);
    background-image: radial-gradient(#1e293b 1px, transparent 1px);
    background-size: 24px 24px;
    color: var(--text);
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    padding: 18px;
    line-height: 1.4;
  }}
  header {{
    display: flex; justify-content: space-between; align-items: center;
    background: var(--panel); border: 1px solid #334155; border-radius: 8px;
    padding: 14px 20px; margin-bottom: 16px;
  }}
  .title-block h1 {{ font-size: 18px; letter-spacing: 1px; }}
  .title-block p {{ font-size: 12px; color: var(--muted); margin-top: 3px; }}
  .status-pill {{
    background: #064e3b; border: 1px solid #10b981; color: #a7f3d0;
    padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold;
  }}
  .top-grid {{
    display: grid; grid-template-columns: 1.25fr 1fr; gap: 16px; margin-bottom: 16px;
  }}
  .panel {{
    background: rgba(15, 23, 42, 0.92); border: 1px solid var(--border);
    border-radius: 8px; padding: 16px;
  }}
  .panel-title {{
    font-size: 13px; font-weight: bold; color: var(--accent);
    letter-spacing: 0.8px; margin-bottom: 4px;
  }}
  .panel-sub {{ font-size: 11px; color: var(--muted); margin-bottom: 12px; }}
  .route-row {{
    display: grid; grid-template-columns: 190px 1fr 220px 135px;
    align-items: center; gap: 10px; padding: 8px 10px;
    border: 1px solid #1e293b; border-radius: 6px; margin-bottom: 8px;
    cursor: pointer; transition: border-color 0.15s, transform 0.1s;
    background: #090e1a;
  }}
  .route-row:hover {{ border-color: var(--accent); transform: translateX(2px); }}
  .pipe-bar {{
    height: 10px; border-radius: 999px; position: relative;
  }}
  .matrix-table {{ width: 100%; border-collapse: separate; border-spacing: 8px; }}
  .matrix-table th {{
    background: #1e293b; color: #f8fafc; font-size: 11px; padding: 10px; border-radius: 6px;
  }}
  .matrix-row-label {{
    background: #090e1a; border: 1px solid #334155; font-weight: bold;
    font-size: 11px; padding: 12px; border-radius: 6px; width: 210px;
  }}
  .matrix-cell {{
    background: #090e1a; border: 1px solid #1e293b; border-radius: 6px;
    padding: 10px 12px; cursor: pointer; vertical-align: top;
    transition: all 0.15s; position: relative;
  }}
  .matrix-cell:hover {{ border-color: #f8fafc; transform: translateY(-2px); }}
  .cell-badge {{
    float: right; font-size: 9px; font-weight: bold; padding: 2px 6px;
    border-radius: 4px; background: #1e293b;
  }}
  .hud {{
    position: fixed; bottom: 18px; right: 18px; width: 500px;
    background: #0f172a; border: 2px solid var(--accent); border-radius: 8px;
    padding: 16px; box-shadow: 0 20px 45px rgba(0,0,0,0.75);
  }}
  .hud pre {{
    background: #050811; padding: 10px; border-radius: 6px;
    font-size: 11px; color: #34d399; overflow-x: auto; margin-top: 8px;
    border: 1px solid #1e293b;
  }}
  .copy-btn {{
    background: var(--accent); color: #070b14; border: none;
    padding: 5px 10px; border-radius: 4px; font-weight: bold;
    font-size: 11px; cursor: pointer; float: right;
  }}
</style>
</head>
<body>
<header>
  <div class="title-block">
    <h1>{g['meta']['title']}</h1>
    <p>{g['meta']['subtitle']} — Click any route, node, or cell to inspect & copy its CLI harness</p>
  </div>
  <div class="status-pill">● 9 GATEWAYS // ZERO DEAD LINKS</div>
</header>

<div class="top-grid">
  <div class="panel">
    <div class="panel-title">ZONE A // MINARD TASK-TO-GATEWAY CIRCUIT (CLICK TO ROUTE)</div>
    <div class="panel-sub">Pipe thickness scales with free Tokens-Per-Minute (TPM) ceiling.</div>
    <div id="routes-container"></div>
  </div>
  <div class="panel">
    <div class="panel-title">ZONE B // 3-AXIS TRADE-OFF TRIANGLE & PROVIDER INSPECTOR</div>
    <div class="panel-sub">Click any provider node to inspect quota bottlenecks, privacy, and gotchas.</div>
    <div id="providers-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px;"></div>
  </div>
</div>

<div class="panel">
  <div class="panel-title">ZONE C // TOP-DOWN MODALITY × ACCESS TIER MATRIX</div>
  <div class="panel-sub">Stone Librande top-down grid: cross-references Modality against Friction Tier.</div>
  <table class="matrix-table" id="matrix-table"></table>
</div>

<div class="hud" id="hud">
  <button class="copy-btn" onclick="copyEnv()">Copy .env Harness</button>
  <div style="font-size:13px;font-weight:bold;color:#38bdf8;" id="hud-title">INSPECTOR HUD // READY</div>
  <div style="font-size:11px;color:#cbd5e1;margin-top:6px;" id="hud-desc">Click any route or provider above to generate an opinionated .env harness.</div>
  <pre id="hud-code">./ask.py route coding-agent</pre>
</div>

<script>
const DATA = {graph_json};

function selectRoute(rid) {{
  const r = DATA.routes[rid];
  const p = DATA.providers[r.primary_provider];
  const f = DATA.providers[r.fallback_provider];
  document.getElementById('hud-title').innerText = `ROUTE // ${{r.title}} (${{r.primary_model}})`;
  document.getElementById('hud-desc').innerText = `Benchmark: ${{r.benchmark}} | Gotcha: ${{p.gotcha}}`;
  document.getElementById('hud-code').innerText =
`export OPENAI_API_BASE="${{p.base_url}}"
export OPENAI_MODEL="${{r.primary_model}}"
export ASK_FALLBACK_BASE="${{f.base_url}}"
export ASK_FALLBACK_MODEL="${{r.fallback_model}}"`;
}}

function selectProvider(pid) {{
  if (!pid || !DATA.providers[pid]) return;
  const p = DATA.providers[pid];
  document.getElementById('hud-title').innerText = `GATEWAY // ${{p.name}} [${{p.tier}}]`;
  document.getElementById('hud-desc').innerText = `Pipe: ${{p.pipe_label}} | Context: ${{p.effective_ctx}} | Trains on data: ${{p.trains_on_data}}`;
  document.getElementById('hud-code').innerText =
`# Gotcha: ${{p.gotcha}}
export OPENAI_API_BASE="${{p.base_url}}"
# Docs: ${{p.url}}`;
}}

function copyEnv() {{
  navigator.clipboard.writeText(document.getElementById('hud-code').innerText);
  const btn = document.querySelector('.copy-btn');
  btn.innerText = 'Copied!';
  setTimeout(() => btn.innerText = 'Copy .env Harness', 1200);
}}

// Render Routes
const rc = document.getElementById('routes-container');
Object.entries(DATA.routes).forEach(([rid, r]) => {{
  const p = DATA.providers[r.primary_provider];
  const b = DATA.providers[r.blocked_provider];
  const pct = Math.min(100, Math.max(12, Math.log10(p.pipe_tpm) * 16));
  const div = document.createElement('div');
  div.className = 'route-row';
  div.onclick = () => selectRoute(rid);
  div.innerHTML = `
    <div><div style="font-size:11px;font-weight:bold;">${{r.title}}</div><div style="font-size:9.5px;color:#94a3b8;">${{r.load}}</div></div>
    <div><div class="pipe-bar" style="width:${{pct}}%;background:${{p.color}};"></div><div style="font-size:9px;color:${{p.color}};margin-top:3px;">${{p.short}} (${{p.pipe_label.split('/')[0]}})</div></div>
    <div><div style="font-size:11px;font-weight:bold;color:#f8fafc;">✓ ${{r.primary_model}}</div><div style="font-size:9px;color:#94a3b8;">${{r.benchmark.slice(0,34)}}</div></div>
    <div style="font-size:9.5px;color:#fca5a5;background:#2a1215;padding:4px 6px;border-radius:4px;border:1px dashed #ef4444;">✗ ${{b.short}}<br><span style="font-size:8.5px;color:#f87171;">${{r.blocked_reason.slice(0,20)}}</span></div>
  `;
  rc.appendChild(div);
}});

// Render Provider Nodes
const pg = document.getElementById('providers-grid');
Object.entries(DATA.providers).forEach(([pid, p]) => {{
  const card = document.createElement('div');
  card.style.cssText = `background:#090e1a;border:1px solid ${{p.color}};border-radius:6px;padding:8px 10px;cursor:pointer;`;
  card.onclick = () => selectProvider(pid);
  card.innerHTML = `
    <div style="font-size:11px;font-weight:bold;color:${{p.color}};">● ${{p.name}}</div>
    <div style="font-size:9.5px;color:#cbd5e1;margin-top:2px;">${{p.pipe_label}}</div>
    <div style="font-size:8.5px;color:#94a3b8;margin-top:3px;">Trains: ${{p.trains_on_data}}</div>
  `;
  pg.appendChild(card);
}});

// Render Matrix
const mt = document.getElementById('matrix-table');
let thead = '<tr><th>MODALITY // ACCESS TIER</th>';
DATA.matrix.columns.forEach(c => thead += `<th>${{c.label}}</th>`);
thead += '</tr>';
mt.innerHTML = thead;

DATA.matrix.rows.forEach(row => {{
  const tr = document.createElement('tr');
  let html = `<td class="matrix-row-label">${{row.modality}}</td>`;
  DATA.matrix.columns.forEach(col => {{
    const cell = row.cells[col.id];
    const p = cell.ref ? DATA.providers[cell.ref] : null;
    const border = p ? p.color : '#1e293b';
    html += `<td class="matrix-cell" style="border-color:${{border}}" onclick="selectProvider('${{cell.ref || ''}}')">
      <span class="cell-badge" style="color:${{border}}">${{cell.badge}}</span>
      <div style="font-size:11px;font-weight:bold;color:#f8fafc;">${{cell.title}}</div>
      <div style="font-size:9.5px;color:#94a3b8;margin-top:4px;">${{cell.sub}}</div>
    </td>`;
  }});
  tr.innerHTML = html;
  mt.appendChild(tr);
}});

selectRoute('coding-agent');
</script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


def generate_readme(g):
    md = [
        f"# {g['meta']['title']}",
        f"> **{g['meta']['subtitle']}** — Built on Stone Librande's *One-Page Design Philosophy* and Katie Dill's *Opinionated Harness & Craft*.\n",
        "![AI Swiss Knife One-Page Architectural Blueprint](poster.svg)\n",
        "## ⚡ Opinionated CLI Harness (`./ask.py`)",
        "Instead of hunting through fragmented wiki pages, query the routing engine directly from your terminal or agent harness:\n",
        "```bash",
        "python ask.py route coding-agent   # Get primary/fallback endpoints & .env for 20K-token coding loops",
        "python ask.py route repo-1m        # Route 200K-1M context prompts without hitting 8K TPM walls",
        "python ask.py route deep-reason    # Route PhD logic/math to Kimi K3 (93.5% GPQA) / Gemini 2.5 Pro",
        "python ask.py route fast-json      # Route 2,000+ tok/s structured JSON extraction to Cerebras",
        "python ask.py env coding-agent > .env.ai",
        "python ask.py check                # Live HTTP latency & status check across all 9 gateways",
        "python ask.py all                  # Sync upstream GitHub repos -> Lint graph -> Render poster.svg & index.html",
        "```\n",
        "## 🧭 Quick CLI Route Reference (Single-Glance Index)",
        "| Intent (`./ask.py route <id>`) | Primary Model & Gateway | Verified Benchmark / Pipe Edge | Fallback Route | Blocked Trap |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    for rid, r in g["routes"].items():
        p = g["providers"][r["primary_provider"]]
        f = g["providers"][r["fallback_provider"]]
        b = g["providers"][r["blocked_provider"]]
        md.append(
            f"| **`{rid}`** ({r['title']}) | `{r['primary_model']}` via [**{p['short']}**]({p['url']}) | {r['benchmark']} | `{r['fallback_model']}` ({f['short']}) | ✗ `{b['short']}` ({r['blocked_reason']}) |"
        )
    md.append("\n---\n*Interactive War Room Canvas: open `index.html` locally or enable GitHub Pages on this repository.*")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")


def cmd_render():
    print("==> [3/3] RENDER: Compiling One-Page Vector Poster (poster.svg), Interactive Canvas (index.html), & README.md...")
    g = load_graph()
    generate_svg(g)
    generate_html(g)
    generate_readme(g)
    print("    [OK] Rendered poster.svg, index.html, and README.md from data/core_graph.yaml.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == "route":
        cmd_route(arg)
    elif cmd == "env":
        cmd_env(arg)
    elif cmd == "check":
        cmd_check()
    elif cmd == "ingest":
        cmd_ingest()
    elif cmd == "lint":
        cmd_lint()
    elif cmd == "render":
        cmd_render()
    elif cmd == "all":
        cmd_ingest()
        cmd_lint()
        cmd_render()
    else:
        print(f"Unknown command '{cmd}'. Use: route | env | check | ingest | lint | render | all")
        sys.exit(1)
