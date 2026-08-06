"""验证 diagnosing-bugs 的本地引用、来源登记和触发边界。"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES_ROOT = SKILL_ROOT / "references"


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_json_with_header_comments(path: Path) -> object:
    text = path.read_text(encoding="utf-8-sig")
    payload = "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("//")
    )
    return json.loads(payload)


class DiagnosingIntegrationTests(unittest.TestCase):
    def test_complete_snapshot_and_independent_source_are_registered(self) -> None:
        expected_files = (
            REFERENCES_ROOT / "diagnosing-bugs.md",
            REFERENCES_ROOT / "diagnosing-bugs/scripts/hitl-loop.template.sh",
            REFERENCES_ROOT
            / "upstream-metadata/mattpocock/diagnosing-bugs/openai.yaml",
        )
        for path in expected_files:
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"缺少内置文件: {path}")

        manifest = read_json(REFERENCES_ROOT / "SOURCES.json")
        source = next(
            (
                item
                for item in manifest["sources"]
                if item["id"] == "mattpocock-diagnosing-bugs"
            ),
            None,
        )
        self.assertIsNotNone(source, "缺少独立来源 mattpocock-diagnosing-bugs")
        if source is None:
            return

        self.assertEqual(source["repository"], "mattpocock/skills")
        self.assertEqual(source["branch"], "main")
        self.assertEqual(
            source["commit"], "6acc160e4e0cd062dbbbd7a1b26ae92855edf07e"
        )
        self.assertEqual(
            source["source_tree_sha256"],
            "dff8cc167215259536e5a1828d772e2125c28a1886c9eb3ab826c4312a87a6dd",
        )
        self.assertIn("skills/engineering/diagnosing-bugs", source["source_paths"])
        self.assertIn("diagnosing-bugs.md", source["tracked_local_paths"])
        self.assertTrue(source["local_adaptations"])
        self.assertIn("diagnosing-bugs.md", manifest["runtime_entry_files"])
        self.assertTrue(
            (REFERENCES_ROOT / "licenses/mattpocock-skills-LICENSE.txt").is_file()
        )

    def test_orchestrator_defines_trigger_return_and_non_trigger_boundaries(self) -> None:
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8-sig")
        required = (
            "references/diagnosing-bugs.md",
            "无法由当前证据立即解释",
            "一次针对性修复后仍复现",
            "回到当前 TDD 任务的 VERIFY",
            "正常的 TDD 红灯",
            "不触发",
        )
        for literal in required:
            with self.subTest(literal=literal):
                self.assertIn(literal, skill_text)

        self.assertGreaterEqual(skill_text.count("references/diagnosing-bugs.md"), 2)

    def test_readme_and_behavior_prompts_explain_both_routes(self) -> None:
        readme = (SKILL_ROOT / "README.md").read_text(encoding="utf-8-sig")
        self.assertIn("diagnosing-bugs", readme)
        self.assertIn("不需要另外安装", readme)
        self.assertIn("check_upstream.py", readme)

        prompts = read_json_with_header_comments(SKILL_ROOT / "test-prompts.json")
        texts = [item["prompt"] for item in prompts]
        expectations = [" ".join(item["expected"]) for item in prompts]
        self.assertTrue(any("跨环境" in text and "失败" in text for text in texts))
        self.assertTrue(any("正常 TDD" in text for text in texts))
        self.assertTrue(any("diagnosing-bugs" in text for text in expectations))
        self.assertTrue(any("不得进入" in text for text in expectations))

    def test_source_tracking_does_not_overlap_existing_matt_metadata(self) -> None:
        manifest = read_json(REFERENCES_ROOT / "SOURCES.json")
        matt = next(item for item in manifest["sources"] if item["id"] == "mattpocock-skills")
        self.assertNotIn("upstream-metadata/mattpocock/**", matt["tracked_local_paths"])
        expected = {
            "upstream-metadata/mattpocock/domain-modeling/**",
            "upstream-metadata/mattpocock/grill-me/**",
            "upstream-metadata/mattpocock/grill-with-docs/**",
            "upstream-metadata/mattpocock/grilling/**",
        }
        self.assertTrue(expected.issubset(set(matt["tracked_local_paths"])))

    def test_no_external_skill_path_is_added_to_runtime_entry(self) -> None:
        manifest = read_json(REFERENCES_ROOT / "SOURCES.json")
        external = re.compile(r"(?:\.agents|\.codex|\.claude)[\\/]skills", re.I)
        for relative in manifest["runtime_entry_files"]:
            with self.subTest(relative=relative):
                self.assertIsNone(external.search(relative))


if __name__ == "__main__":
    unittest.main()
