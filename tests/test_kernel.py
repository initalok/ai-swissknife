from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from swissknife.engine import build_snapshot, evaluate_workspace, query_entries, resolve_slot, resolve_specialist
from swissknife.probes import BREAKING_KEYWORDS_RE, HF_COLLECTION_RE, SEMVER_TAG_RE
from swissknife.store import load_workspace
from swissknife.validate import validate_workspace

SAMPLE_TAXONOMY = """
allowed_kinds: [gateway, model, adapter, harness, runtime, tool, mcp, memory, fabric, mobile]
tracks:
  - { id: newcomer, name: "Newcomer & Student", summary: "Guided first wins." }
  - { id: developer, name: "Seasoned Developer", summary: "Physics, Pi ricing, and automation." }
worlds:
  - { id: cloud, name: "Zero-Card Cloud", summary: "$0 card-free cloud APIs." }
  - { id: mac, name: "Apple Silicon Mac", summary: "Silent always-on control plane + MLX." }
  - { id: gpu-pc, name: "Discrete GPU PC", summary: "16GB VRAM + 64GB RAM workstation." }
  - { id: mobile-hitl, name: "Mobile (Human Communicator)", summary: "HITL approvals, voice steering, and remote pings." }
sections:
  - { id: docs, name: "Orientation & Philosophy", summary: "Onboarding, mental models, security, and ADRs." }
  - { id: guides, name: "Guides", summary: "Goal-driven workflows." }
non_goals:
  - "Brute-force LLM inference on phone batteries."
  - "Custom benchmarking or smoke-test frameworks."
"""

SAMPLE_CORE_REGISTRY = """
entries:
  - id: google-ai-studio
    kind: gateway
    name: "Google AI Studio (Gemini 4 Hydrogen)"
    summary: "Card-free developer API with 1M context."
    when_to_use: "Zero-install cloud coding and long-context runs."
    limitations: ["Free-tier prompts may be logged outside EU/UK/CH."]
    evidence_tier: official-docs
    lifecycle: operational
    decay_class: volatile
    last_verified: "2026-11-27"
    url: "https://aistudio.google.com/"
    capabilities: [coding]
    relations: { runs_on: [cloud] }
    meta: { default_model: gemini-4-hydrogen }

  - id: qwen3.8-27b
    kind: model
    name: "Qwen3.8-27B"
    summary: "Dense 27B coding backbone fitting inside 16GB VRAM."
    when_to_use: "Primary local daily driver."
    limitations: ["Requires IQ4_XS + Q8 KV cache on 16GB VRAM."]
    evidence_tier: primary-eval
    lifecycle: mature
    decay_class: stable
    last_verified: "2026-11-27"
    url: "https://huggingface.co/Qwen/Qwen3.8-27B"
    capabilities: [coding, reverse-eng]
    relations: { runs_on: [gpu-pc, mac] }

  - id: pi
    kind: harness
    name: "Pi Coding Agent"
    summary: "Minimal, hackable agent kernel."
    when_to_use: "Developer anchor with optional 6-rung ricing ladder."
    limitations: ["Omits built-in approval prompts; pair with gondolin/nono/safeagents."]
    evidence_tier: primary-eval
    lifecycle: mature
    decay_class: stable
    last_verified: "2026-11-27"
    url: "https://github.com/earendil-works/pi"
    capabilities: [coding, reverse-eng]
    relations: { runs_on: [cloud, mac, gpu-pc] }
    meta: { last_reviewed_release: "v1.6.1" }

  - id: opencode
    kind: harness
    name: "OpenCode CLI"
    summary: "Mature terminal harness with built-in approval prompts."
    when_to_use: "Newcomer local coding onboarding."
    limitations: ["Less aggressive context compaction than Pi."]
    evidence_tier: official-docs
    lifecycle: mature
    decay_class: stable
    last_verified: "2026-11-27"
    url: "https://github.com/anomalyco/opencode"
    capabilities: [coding]
    relations: { runs_on: [cloud, mac, gpu-pc] }

  - id: qwen38-pi-lora
    kind: adapter
    name: "Qwen3.8-27B Pi Specialist LoRA"
    summary: "RL-trained LoRA tailored to Pi."
    when_to_use: "Single-harness local coding with thinking off."
    limitations: ["GGUF quants not formally re-evaluated in llama.cpp."]
    evidence_tier: primary-eval
    lifecycle: mature
    decay_class: stable
    last_verified: "2026-11-27"
    url: "https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted-GGUF"
    capabilities: [coding, reverse-eng]
    relations: { adapts: [qwen3.8-27b, pi], runs_on: [gpu-pc, mac] }

  - id: safeagents
    kind: tool
    name: "Hugging Face safeagents Proxy"
    summary: "Transparent tool-call auditing proxy."
    when_to_use: "Runtime safety gate for shell-capable agents."
    limitations: ["Configure a domain plugin before running."]
    evidence_tier: primary-eval
    lifecycle: operational
    decay_class: operational
    last_verified: "2026-11-27"
    url: "https://github.com/huggingface/safeagents"
    capabilities: [safety]
    relations: { guards: ["*"], runs_on: [mac, gpu-pc] }

slots:
  - id: dev-harness
    title: "Developer Coding Harness"
    role: "Flagship mod-able agent loop for developers."
    primary: pi
    fallbacks: [opencode]
    decision_id: adr-why-pi

specialists:
  - id: reverse-engineering
    title: "Reverse Engineering & Binary Triage"
    summary: "Air-gapped local coding stack wired to decompiler MCPs."
    last_verified: "2026-11-27"
    constraints: { capabilities: [reverse-eng], privacy: local-only, require_guard: true }
    direct_picks:
      - { id: ghidra-mcp, name: "GhidraMCP", url: "https://github.com/LaurieWired/GhidraMCP", summary: "Ghidra MCP server." }
    upstream_hub:
      id: awesome-ai-reveng
      name: "awesome-ai-reverse-engineering"
      url: "https://github.com/zhuyansen/awesome-ai-reverse-engineering"
      summary: "122 graded tools."
    guardrails: ["Audit only authorized binaries."]

watch:
  frontier:
    - id: qwen4-max
      name: "Qwen4-Max (2.4T)"
      url: "https://qwenlm.github.io/"
      last_verified: "2026-11-27"
      evidence_tier: official-docs
      summary: "Signals smaller open Qwen4 checkpoints ahead."
      limitations: ["Cloud API only."]

retired:
  - area: pi-extension
    name: "huggingface/pi-llama"
    match_pattern: "huggingface/pi-llama"
    retired_on: "2026-11-09"
    reason: "Absorbed directly into Pi core (/llama)."
    replaced_by: pi
"""

SAMPLE_DECISION = """
decisions:
  - id: adr-why-pi
    title: "Choose Pi as Flagship Developer Harness"
    status: accepted
    date: "2026-11-27"
    job: "Provide a transparent, mod-able local/cloud agent kernel."
    anchor_ids: [pi]
    slot_ids: [dev-harness]
    alternatives: ["OpenCode", "Hermes Agent", "DeepSeek Harness"]
    rationale: "Minimal loop you own, built-in /llama router, /tree branching, and highest HF RL LoRA lift."
    exceptions: ["Beginners should start with OpenCode for built-in approval prompts."]
    reversal_trigger: "Another MIT harness surpasses Pi's transparency and local adapter ecosystem with lower friction."
"""


def _build_fixture_repo(root: Path) -> None:
    (root / "catalog" / "registry").mkdir(parents=True)
    (root / "catalog" / "decisions").mkdir(parents=True)
    (root / "catalog" / "taxonomy.yaml").write_text(SAMPLE_TAXONOMY, encoding="utf-8")
    (root / "catalog" / "registry" / "core.yaml").write_text(SAMPLE_CORE_REGISTRY, encoding="utf-8")
    (root / "catalog" / "decisions" / "adr-why-pi.yaml").write_text(SAMPLE_DECISION, encoding="utf-8")


class TestOpenClosedKernel(unittest.TestCase):
    def test_recursive_discovery_accepts_new_domain_with_zero_code_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_fixture_repo(root)
            (root / "catalog" / "registry" / "memory.yaml").write_text(
                """
entries:
  - id: obsidian-skills
    kind: memory
    name: "Obsidian Official Agent Skills"
    summary: "Plain-Markdown vault skills and defuddle web clipper."
    when_to_use: "Human-editable long-term knowledge loop."
    limitations: ["Treat clipped pages as untrusted data, not instructions."]
    evidence_tier: official-docs
    lifecycle: operational
    decay_class: operational
    last_verified: "2026-11-27"
    url: "https://github.com/obsidianmd/obsidian-skills"
    tags: [knowledge-loop]
    relations: { runs_on: [mac, gpu-pc] }
""",
                encoding="utf-8",
            )
            ws = load_workspace(root)
            self.assertEqual(validate_workspace(ws), [])
            res = query_entries(ws, kind="memory", as_of=date(2026, 11, 27))
            self.assertEqual(res["count"], 1)
            self.assertEqual(res["entries"][0]["id"], "obsidian-skills")

    def test_slot_world_filter_excludes_local_adapter_and_snapshot_exposes_failover(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_fixture_repo(root)
            ws = load_workspace(root)

            cloud_res = resolve_slot(ws, "dev-harness", world="cloud", as_of=date(2026, 11, 27))
            self.assertEqual(cloud_res["active"]["id"], "pi")
            self.assertEqual(cloud_res["discovered_adapters"], [])

            gpu_res = resolve_slot(ws, "dev-harness", world="gpu-pc", as_of=date(2026, 11, 27))
            self.assertEqual([a["id"] for a in gpu_res["discovered_adapters"]], ["qwen38-pi-lora"])

            ws.health_state["entry:pi"] = {"upstream_archived": True, "consecutive_fails": 0}
            snap = build_snapshot(ws, as_of=date(2026, 11, 27))
            sl = snap["slots"]["dev-harness"]
            self.assertEqual(sl["configured_primary"]["id"], "pi")
            self.assertEqual(sl["active"]["id"], "opencode")
            self.assertTrue(sl["fallback_used"])

    def test_resolve_specialist_enforces_local_only_and_hydrates_hub_health(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_fixture_repo(root)
            ws = load_workspace(root)
            ws.health_state["specialist:reverse-engineering:upstream"] = {
                "upstream_pushed_at": "2026-11-26T10:00:00Z",
                "consecutive_fails": 0,
            }
            sp = resolve_specialist(ws, "reverse-engineering", world="gpu-pc", as_of=date(2026, 11, 27))
            self.assertEqual([m["id"] for m in sp["resolved"]["models_and_gateways"]], ["qwen3.8-27b"])
            self.assertEqual([h["id"] for h in sp["resolved"]["harnesses"]], ["pi"])
            self.assertEqual([a["id"] for a in sp["resolved"]["adapters"]], ["qwen38-pi-lora"])
            self.assertEqual([g["id"] for g in sp["resolved"]["guards"]], ["safeagents"])
            self.assertEqual(sp["upstream_hub"]["freshness"]["upstream_pushed_at"], "2026-11-26T10:00:00Z")

    def test_release_momentum_and_breaking_change_triggers_adr_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_fixture_repo(root)
            ws = load_workspace(root)
            ws.health_state["entry:pi"] = {
                "latest_release_tag": "v2.0.0",
                "release_breaking_signal": True,
                "consecutive_fails": 0,
            }
            st = evaluate_workspace(ws, as_of=date(2026, 11, 27))
            self.assertEqual(len(st["deltas"]["release_updates"]), 1)
            self.assertEqual(st["deltas"]["decision_reviews"][0]["decision_id"], "adr-why-pi")

    def test_watch_auto_expiry_and_hf_collection_regex(self) -> None:
        self.assertIsNotNone(HF_COLLECTION_RE.match("https://huggingface.co/collections/harness-hub/qwen38-27b-harness-adapters"))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_fixture_repo(root)
            ws = load_workspace(root)
            snap = build_snapshot(ws, as_of=date(2026, 12, 27))
            self.assertEqual(snap["counts"]["watch_active"], 0)
            self.assertEqual(snap["counts"]["watch_expired"], 1)

    def test_validation_hardening_catches_retired_duplicates_and_bad_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_fixture_repo(root)
            (root / "docs").mkdir()
            (root / "docs" / "bad.md").write_text(
                "---\ntitle: Bad\nsection: docs\nsummary: Bad block.\n---\n"
                "<!-- swissknife:begin slot id=nonexistent -->\n<!-- swissknife:end -->\n",
                encoding="utf-8",
            )
            ws = load_workspace(root)
            errs = validate_workspace(ws)
            self.assertTrue(any("unknown slot id 'nonexistent'" in e for e in errs))

    def test_semver_and_breaking_regex(self) -> None:
        m = SEMVER_TAG_RE.match("v2.4.2")
        self.assertIsNotNone(m)
        self.assertEqual(tuple(int(g) for g in m.groups()), (2, 4, 2))
        self.assertIsNotNone(SEMVER_TAG_RE.match("1.2.3"))
        self.assertIsNone(SEMVER_TAG_RE.match("manager-v0.1.21"))
        self.assertIsNone(SEMVER_TAG_RE.match("v2.0.0-alpha.1"))

        self.assertIsNotNone(BREAKING_KEYWORDS_RE.search("Breaking Change: removed telemetry"))
        self.assertIsNone(BREAKING_KEYWORDS_RE.search("when a profile is renamed, moved or removed"))


if __name__ == "__main__":
    unittest.main()
