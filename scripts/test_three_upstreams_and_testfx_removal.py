"""验证三个来源升级、TestFX 移除和本地适配边界。"""

from __future__ import annotations

import json
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES_ROOT = SKILL_ROOT / "references"

EXPECTED_SOURCES = {
    "obra-superpowers": (
        "b36e0829c6d0140e93cfef2ca599b1b07d4a7797",
        "4d0163566c2e1796b1d4d4089eadc4921500df7734a73e237b6ba9708abd95df",
    ),
    "mattpocock-skills": (
        "3cca18b368ae95cdbdebbff572ccafa662551015",
        "e14525bd498884d5cb03326c506766409378cd02b02010a316e3fd787197c0f8",
    ),
    "agent-reach": (
        "da5044d26fc6adddb6554d5679c94ac22e76e428",
        "515c6a093fedb0bc6692eabc52a5f97b3bf8b3a9f8e482c840b98dd4a05b3287",
    ),
}


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


class ThreeUpstreamsAndTestfxRemovalTests(unittest.TestCase):
    def test_three_sources_are_pinned_to_reviewed_commits(self) -> None:
        manifest = read_json(REFERENCES_ROOT / "SOURCES.json")
        sources = {item["id"]: item for item in manifest["sources"]}
        self.assertNotIn("microsoft-testfx", sources)
        self.assertTrue(set(EXPECTED_SOURCES).issubset(sources))
        for source_id, (commit, tree_hash) in EXPECTED_SOURCES.items():
            with self.subTest(source_id=source_id):
                self.assertEqual(sources[source_id]["commit"], commit)
                self.assertEqual(sources[source_id]["source_tree_sha256"], tree_hash)

    def test_testfx_runtime_files_and_references_are_removed(self) -> None:
        forbidden_files = (
            REFERENCES_ROOT / "code-testing-agent.md",
            REFERENCES_ROOT / "code-testing-extensions.md",
            REFERENCES_ROOT / "licenses/testfx-LICENSE.txt",
        )
        for path in forbidden_files:
            with self.subTest(path=path):
                self.assertFalse(path.exists(), f"TestFX 文件仍存在: {path}")
        for directory in (
            REFERENCES_ROOT / "code-testing-agent",
            REFERENCES_ROOT / "code-testing-extensions",
        ):
            with self.subTest(directory=directory):
                self.assertFalse(
                    any(path.is_file() for path in directory.rglob("*")),
                    f"TestFX 目录仍有文件: {directory}",
                )

        texts = (
            (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8-sig"),
            (REFERENCES_ROOT / "DEPENDENCY-MAP.md").read_text(encoding="utf-8-sig"),
            (SKILL_ROOT / "NOTICE").read_text(encoding="utf-8-sig"),
        )
        for text in texts:
            self.assertNotIn("microsoft-testfx", text)
            self.assertNotIn("code-testing-agent", text)
            self.assertNotIn("code-testing-extensions", text)

    def test_grilling_keeps_local_interaction_boundaries(self) -> None:
        grilling = (REFERENCES_ROOT / "grilling.md").read_text(encoding="utf-8-sig")
        self.assertIn("design tree", grilling.lower())
        self.assertIn("one question", grilling.lower())
        self.assertIn("explicitly authorizes", grilling.lower())
        metadata = (
            REFERENCES_ROOT
            / "upstream-metadata/mattpocock/grilling/openai.yaml"
        ).read_text(encoding="utf-8-sig")
        self.assertIn("round of questions", metadata)

    def test_agent_reach_finance_entry_and_local_links_are_present(self) -> None:
        entry = (REFERENCES_ROOT / "agent-reach.md").read_text(encoding="utf-8-sig")
        finance = REFERENCES_ROOT / "agent-reach/finance.md"
        self.assertTrue(finance.is_file())
        self.assertIn("agent-reach/finance.md", entry)
        self.assertNotIn("references/finance.md", entry)
        self.assertIn("不构成投资建议", finance.read_text(encoding="utf-8-sig"))

    def test_runtime_entries_have_no_external_skill_paths(self) -> None:
        manifest = read_json(REFERENCES_ROOT / "SOURCES.json")
        for relative in manifest["runtime_entry_files"]:
            with self.subTest(relative=relative):
                self.assertNotRegex(relative, r"(?:\.agents|\.codex|\.claude)[\\/]skills")


if __name__ == "__main__":
    unittest.main()
