from __future__ import annotations

import re
import tempfile
import unittest
from datetime import date
from pathlib import Path

from swissknife.renderers.agent import AgentRenderer
from swissknife.renderers.diataxis import DiataxisRenderer
from swissknife.resolver import build_snapshot
from tests.test_core import _sample_catalog

MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")


class TestRenderers(unittest.TestCase):
    def test_full_repo_internal_link_integrity_and_zero_jargon(self) -> None:
        cat = _sample_catalog()
        for extra_id, title in (
            ("research-and-writing", "Research & Writing"),
            ("local-media-studio", "Local Media Studio"),
        ):
            base = cat.guides["coding-and-apps"]
            cat.guides[extra_id] = type(base)(**{**base.__dict__, "id": extra_id, "title": title})

        snap = build_snapshot(cat, as_of=date(2026, 11, 27))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONTRIBUTING.md").write_text("# Contributing\n", encoding="utf-8")
            DiataxisRenderer().render(snap, root)
            AgentRenderer().render(snap, root)

            readme = (root / "README.md").read_text(encoding="utf-8")
            for forbidden in ("Hub-and-Spoke", "Core Nodes", "Upstreamed Spokes", "implicit graph"):
                self.assertNotIn(forbidden.lower(), readme.lower())

            # Crawl EVERY generated Markdown file for broken relative internal links
            for md_file in root.rglob("*.md"):
                content = md_file.read_text(encoding="utf-8")
                for target in MD_LINK_RE.findall(content):
                    if target.startswith(("http://", "https://", "mailto:")):
                        continue
                    resolved = (md_file.parent / target).resolve()
                    self.assertTrue(resolved.exists(), f"Broken link in {md_file.relative_to(root)}: '{target}'")

            # Verify Mac MLX recipe & Coding Agent Token Math rendered
            local_guide = (root / "guides/local-ai-workstation.md").read_text(encoding="utf-8")
            self.assertIn("mlx_lm.server", local_guide)
            self.assertIn("4,096-token context window", local_guide)

            cloud_ref = (root / "reference/cloud-free-tiers.md").read_text(encoding="utf-8")
            self.assertIn("300,000 tokens per task", cloud_ref)

    def test_stale_entry_gated_from_llms_and_flagged_in_status(self) -> None:
        cat = _sample_catalog()
        cat.health_state["specialist:reverse-engineering:upstream"] = {"upstream_archived": True, "consecutive_fails": 0}
        snap = build_snapshot(cat, as_of=date(2026, 12, 27))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            DiataxisRenderer().render(snap, root)
            AgentRenderer().render(snap, root)

            llms = (root / "llms.txt").read_text(encoding="utf-8")
            cloud_md = (root / "reference/cloud-free-tiers.md").read_text(encoding="utf-8")
            status_md = (root / "STATUS.md").read_text(encoding="utf-8")

            self.assertNotIn("[google-ai-studio]", llms)
            self.assertIn("needs re-verification", cloud_md)
            self.assertIn("`stale`", status_md)
            self.assertIn("Supporting Tools & Upstream Directories", status_md)
            self.assertIn("`degraded`", status_md)


if __name__ == "__main__":
    unittest.main()
