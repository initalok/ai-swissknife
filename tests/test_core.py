from __future__ import annotations

import unittest
from datetime import date

from swissknife.models import (
    Catalog,
    Edges,
    Entry,
    ExternalLink,
    GuideSpec,
    HardwareProfile,
    RetiredItem,
    SpecialistSpec,
    WatchItem,
)
from swissknife.resolver import build_snapshot, evaluate_state, resolve_target
from swissknife.validate import validate_catalog


def _sample_catalog() -> Catalog:
    profiles = {
        "zero-card-cloud": HardwareProfile("zero-card-cloud", "Zero-Card Cloud", "Free cloud APIs."),
        "16vram-64ram": HardwareProfile("16vram-64ram", "16GB VRAM + 64GB RAM", "Hybrid local workstation."),
        "mac-apple-silicon": HardwareProfile("mac-apple-silicon", "Apple Silicon Mac", "Unified memory via MLX."),
    }
    entries = {
        "google-ai-studio": Entry(
            id="google-ai-studio",
            kind="gateway",
            category="cloud",
            name="Google AI Studio",
            summary="Card-free cloud API gateway hosting Gemini 4 Hydrogen.",
            when_to_use="Zero-cost cloud coding and long-context runs.",
            limitations=["Free tier prompts may be logged outside EU/UK/CH."],
            evidence_tier="official-docs",
            lifecycle="operational",
            decay_class="volatile",
            last_verified="2026-11-27",
            url="https://aistudio.google.com/",
            default_model="gemini-4-hydrogen",
            capabilities=["coding"],
            edges=Edges(runs_on=["zero-card-cloud"]),
        ),
        "qwen3.8-27b": Entry(
            id="qwen3.8-27b",
            kind="model",
            category="local-mature",
            name="Qwen3.8-27B",
            summary="Dense 27B coding and vision model.",
            when_to_use="Primary 16GB VRAM daily driver.",
            limitations=["Use IQ4_XS + Q8 KV cache to stay resident in 16GB VRAM."],
            evidence_tier="primary-eval",
            lifecycle="mature",
            decay_class="stable",
            last_verified="2026-11-27",
            url="https://huggingface.co/Qwen/Qwen3.8-27B",
            capabilities=["coding", "reverse-eng"],
            edges=Edges(runs_on=["16vram-64ram", "mac-apple-silicon"]),
            launch_recipe="llama-server -m Qwen3.8-27B-IQ4_XS.gguf -ngl 99 -fa on -c 32768",
            mac_launch_recipe="mlx_lm.server --model mlx-community/Qwen3.8-27B-4bit --port 8000",
        ),
        "pi": Entry(
            id="pi",
            kind="harness",
            category="harness",
            name="Pi Coding Agent",
            summary="Minimal hackable agent kernel.",
            when_to_use="Transparent context assembly and DAG branching.",
            limitations=["Omits built-in approval prompts; pair with safeagents."],
            evidence_tier="official-docs",
            lifecycle="mature",
            decay_class="stable",
            last_verified="2026-11-27",
            url="https://github.com/earendil-works/pi",
            capabilities=["coding", "reverse-eng"],
            edges=Edges(runs_on=["zero-card-cloud", "16vram-64ram", "mac-apple-silicon"]),
        ),
        "qwen38-super-adapter": Entry(
            id="qwen38-super-adapter",
            kind="adapter",
            category="rl-adapter",
            name="Qwen3.8-27B Super-Adapter",
            summary="Rank-96 merged harness LoRA adapter.",
            when_to_use="Multi-harness fleets or thinking-on runs.",
            limitations=["Prefer single-harness specialist LoRA when thinking is off."],
            evidence_tier="primary-eval",
            lifecycle="mature",
            decay_class="stable",
            last_verified="2026-11-27",
            url="https://huggingface.co/harness-hub/Qwen3.8-27B-super-adapter",
            capabilities=["coding", "reverse-eng"],
            edges=Edges(adapts=["qwen3.8-27b", "pi"], runs_on=["16vram-64ram", "mac-apple-silicon"]),
        ),
        "safeagents": Entry(
            id="safeagents",
            kind="tool",
            category="safety",
            name="safeagents Proxy",
            summary="Transparent runtime safety proxy.",
            when_to_use="Guarding autonomous tool calls.",
            limitations=["Requires configuring a domain plugin."],
            evidence_tier="primary-eval",
            lifecycle="operational",
            decay_class="operational",
            last_verified="2026-11-27",
            url="https://github.com/huggingface/safeagents",
            capabilities=["safety"],
            edges=Edges(guards=["*"]),
        ),
    }
    guides = {
        "coding-and-apps": GuideSpec(
            id="coding-and-apps",
            title="Coding & Apps",
            summary="End-to-end engineering workflow.",
            last_verified="2026-11-27",
            decay_class="operational",
            capabilities=["coding"],
            privacy="any",
            require_guard=True,
            pin_entries=[],
            tools=[ExternalLink("playwright", "Playwright MCP", "https://github.com/microsoft/playwright-mcp")],
            steps=["Verify docs with Context7.", "Run Playwright end-to-end tests."],
            limitations=["Accessibility snapshots skip closed Shadow DOM."],
        )
    }
    specialists = {
        "reverse-engineering": SpecialistSpec(
            id="reverse-engineering",
            title="Reverse Engineering",
            summary="Air-gapped static triage.",
            last_verified="2026-11-27",
            capabilities=["reverse-eng"],
            privacy="local-only",
            require_guard=True,
            direct_picks=[ExternalLink("ghidra-mcp", "GhidraMCP", "https://github.com/LaurieWired/GhidraMCP")],
            upstream_directory=ExternalLink("reveng-hub", "Awesome AI RevEng", "https://github.com/zhuyansen/awesome-ai-reverse-engineering"),
            guardrails=["Only audit authorized binaries."],
        )
    }
    watch_frontier = [
        WatchItem("f1", "frontier", "Frontier Alpha", "https://www.anthropic.com/", "2026-11-27", "vendor-claim", "Ceiling.", ["Paid only."])
    ]
    retired = [
        RetiredItem("cloud", "Cerebras Legacy Free", "cerebras.ai", "2026-11-18", "Requires payment method.", "google-ai-studio")
    ]
    return Catalog(profiles, entries, {"coding": ["google-ai-studio"]}, guides, specialists, watch_frontier, [], retired, {})


class TestSwissKnifeCore(unittest.TestCase):
    def test_valid_catalog_passes(self) -> None:
        self.assertEqual(validate_catalog(_sample_catalog()), [])

    def test_canonical_url_law_blocks_placeholders(self) -> None:
        cat = _sample_catalog()
        cat.watch_community.append(
            WatchItem("bad", "community", "Subreddit", "https://www.reddit.com/r/LocalLLaMA/", "2026-11-27", "field-note", "Noise.", ["Uncheckable."])
        )
        errs = validate_catalog(cat)
        self.assertTrue(any("Canonical URL Law" in e for e in errs))

    def test_retired_patterns_blocked_in_guides_and_specialists(self) -> None:
        cat = _sample_catalog()
        cat.guides["coding-and-apps"].tools.append(ExternalLink("c-old", "Cerebras", "https://inference.cerebras.ai/v1"))
        errs = validate_catalog(cat)
        self.assertTrue(any("matches retired pattern 'cerebras.ai'" in e for e in errs))

    def test_reserved_guide_slug_rejected(self) -> None:
        cat = _sample_catalog()
        base = cat.guides["coding-and-apps"]
        cat.guides["local-ai-workstation"] = GuideSpec(**{**base.__dict__, "id": "local-ai-workstation"})
        errs = validate_catalog(cat)
        self.assertTrue(any("reserved built-in guide slug" in e for e in errs))

    def test_external_links_tracked_in_health_digest(self) -> None:
        cat = _sample_catalog()
        cat.health_state["specialist:reverse-engineering:upstream"] = {"upstream_archived": True, "consecutive_fails": 0}
        st = evaluate_state(cat, as_of=date(2026, 11, 27))
        self.assertTrue(any(x["id"] == "specialist:reverse-engineering:upstream" for x in st["digest"]["degraded"]))

    def test_privacy_isolation_keeps_multi_profile_harness_and_blocks_cloud_gateway(self) -> None:
        cat = _sample_catalog()
        res = resolve_target(cat, "reverse-engineering", profile_id="16vram-64ram", as_of=date(2026, 11, 27))
        model_ids = [m["id"] for m in res["resolved"]["models_and_gateways"]]
        harness_ids = [h["id"] for h in res["resolved"]["harnesses"]]
        adapter_ids = [a["id"] for a in res["resolved"]["adapters"]]
        guard_ids = [g["id"] for g in res["resolved"]["guards"]]

        self.assertIn("qwen3.8-27b", model_ids)
        self.assertNotIn("google-ai-studio", model_ids)
        self.assertIn("pi", harness_ids)
        self.assertIn("qwen38-super-adapter", adapter_ids)
        self.assertIn("safeagents", guard_ids)

    def test_ttl_gating_and_transitive_upstream_alert(self) -> None:
        cat = _sample_catalog()
        res_30 = resolve_target(cat, "coding-and-apps", profile_id="zero-card-cloud", as_of=date(2026, 12, 27))
        self.assertEqual(res_30["resolved"]["models_and_gateways"], [])
        self.assertTrue(any(x["id"] == "google-ai-studio" for x in res_30["excluded_stale"]))

        cat.health_state["entry:qwen3.8-27b"] = {"upstream_archived": True, "consecutive_fails": 0}
        st = evaluate_state(cat, as_of=date(2026, 11, 27))
        self.assertEqual(st["freshness"]["qwen3.8-27b"].status, "degraded")
        self.assertEqual(st["freshness"]["qwen38-super-adapter"].effective_status, "reverify-upstream")

    def test_snapshot_counts(self) -> None:
        snap = build_snapshot(_sample_catalog(), as_of=date(2026, 11, 27))
        self.assertEqual(snap["counts"]["entries"], 5)
        self.assertEqual(snap["counts"]["external_links"], 3)


if __name__ == "__main__":
    unittest.main()
