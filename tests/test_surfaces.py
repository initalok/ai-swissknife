from __future__ import annotations

import re
import tempfile
import unittest
from datetime import date
from pathlib import Path

from swissknife.engine import build_snapshot
from swissknife.store import load_workspace
from swissknife.surfaces.agent import StatusAndAgentSurface
from swissknife.surfaces.blocks import ManagedBlockSyncer
from swissknife.validate import validate_workspace
from tests.test_kernel import _build_fixture_repo

MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")


class TestManagedBlockSurfaces(unittest.TestCase):
    def _seed_pages(self, root: Path) -> None:
        (root / "docs").mkdir(parents=True, exist_ok=True)
        (root / "guides").mkdir(parents=True, exist_ok=True)

        (root / "README.md").write_text(
            "# AI Swiss Knife\n\n"
            "Human intro stays untouched forever.\n\n"
            "<!-- swissknife:begin status-banner -->\n"
            "stale placeholder\n"
            "<!-- swissknife:end -->\n\n"
            "## Guides\n\n"
            "<!-- swissknife:begin nav section=guides -->\n"
            "<!-- swissknife:end -->\n\n"
            "## Non-Goals\n\n"
            "<!-- swissknife:begin non-goals -->\n"
            "<!-- swissknife:end -->\n",
            encoding="utf-8",
        )
        (root / "docs" / "why-this-stack.md").write_text(
            "---\n"
            "title: Why This Stack\n"
            "section: docs\n"
            "summary: Architectural decisions and reversal triggers.\n"
            "order: 2\n"
            "---\n\n"
            "# Why This Stack\n\n"
            "<!-- swissknife:begin decisions-index -->\n"
            "<!-- swissknife:end -->\n\n"
            "Example syntax inside a code fence must NEVER be mutated:\n\n"
            "```markdown\n"
            "<!-- swissknife:begin slot id=dev-harness -->\n"
            "DO NOT TOUCH THIS EXAMPLE\n"
            "<!-- swissknife:end -->\n"
            "```\n",
            encoding="utf-8",
        )
        (root / "guides" / "dev-setup.md").write_text(
            "---\n"
            "title: Developer Setup\n"
            "section: guides\n"
            "summary: Mod-able local and cloud coding harness.\n"
            "order: 1\n"
            "---\n\n"
            "# Developer Setup\n\n"
            "<!-- swissknife:begin status-banner -->\n"
            "<!-- swissknife:end -->\n\n"
            "<!-- swissknife:begin slot id=dev-harness -->\n"
            "<!-- swissknife:end -->\n",
            encoding="utf-8",
        )

    def test_in_place_sync_preserves_prose_code_fences_idempotency_and_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_fixture_repo(root)
            self._seed_pages(root)

            ws = load_workspace(root)
            self.assertEqual(validate_workspace(ws), [])
            snap = build_snapshot(ws, as_of=date(2026, 11, 27))

            syncer = ManagedBlockSyncer()
            agent = StatusAndAgentSurface()
            changed_first = syncer.sync(snap, root)
            agent.sync(snap, root)
            self.assertEqual(len(changed_first), 3)

            # Strict idempotency: second run mutates ZERO Markdown files
            changed_second = syncer.sync(snap, root)
            self.assertEqual(changed_second, [])

            readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("Human intro stays untouched forever.", readme)
            self.assertIn("[Developer Setup](guides/dev-setup.md)", readme)
            self.assertIn("Brute-force LLM inference on phone batteries.", readme)

            why = (root / "docs" / "why-this-stack.md").read_text(encoding="utf-8")
            self.assertIn("DO NOT TOUCH THIS EXAMPLE", why)
            self.assertIn("Choose Pi as Flagship Developer Harness", why)

            for md_file in root.rglob("*.md"):
                content = md_file.read_text(encoding="utf-8")
                for target in MD_LINK_RE.findall(content):
                    if target.startswith(("http://", "https://", "mailto:")):
                        continue
                    resolved = (md_file.parent / target).resolve()
                    self.assertTrue(resolved.exists(), f"Broken link in {md_file.relative_to(root)}: '{target}'")

    def test_slot_failover_updates_managed_block_and_llms_txt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_fixture_repo(root)
            self._seed_pages(root)

            ws = load_workspace(root)
            ws.health_state["entry:pi"] = {"upstream_archived": True, "consecutive_fails": 0}
            snap = build_snapshot(ws, as_of=date(2026, 11, 27))

            ManagedBlockSyncer().sync(snap, root)
            StatusAndAgentSurface().sync(snap, root)

            guide = (root / "guides" / "dev-setup.md").read_text(encoding="utf-8")
            llms = (root / "llms.txt").read_text(encoding="utf-8")
            status = (root / "STATUS.md").read_text(encoding="utf-8")

            self.assertIn("automatically failing over to **OpenCode CLI**", guide)
            self.assertIn("[dev-harness] [FAILOVER] -> opencode", llms)
            self.assertIn("Decision Records Flagged for Review", status)


if __name__ == "__main__":
    unittest.main()
