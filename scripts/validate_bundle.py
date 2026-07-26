# requirement-workflow — 需求先行六阶段开发工作流
# Copyright (C) 2026 quanfanpro-code
#
# 本文件是 requirement-workflow 的原创编排层,采用 GNU Affero General Public
# License v3.0 (AGPL-3.0) 发布。
# 完整协议见项目根目录 LICENSE 文件(AGPL-3.0)。
##!/usr/bin/env python3
"""校验 requirement-workflow 的自包含性、引用闭包和文本编码。"""

from __future__ import annotations

import fnmatch
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES_ROOT = SKILL_ROOT / "references"
MANIFEST_PATH = REFERENCES_ROOT / "SOURCES.json"

TEXT_SUFFIXES = {
    ".md",
    ".json",
    ".txt",
    ".py",
    ".js",
    ".cjs",
    ".sh",
    ".yaml",
    ".yml",
    ".dot",
    ".html",
}

EXTERNAL_RUNTIME_PATTERNS = (
    re.compile(r"(?:^|[\\/])\.agents?[\\/]skills(?:[\\/]|$)", re.IGNORECASE),
    re.compile(r"(?:^|[\\/])\.codex[\\/]skills(?:[\\/]|$)", re.IGNORECASE),
    re.compile(r"(?:^|[\\/])\.claude[\\/]skills(?:[\\/]|$)", re.IGNORECASE),
    re.compile(r"\bsuperpowers:[a-z0-9-]+\b", re.IGNORECASE),
    re.compile(r"\belements-of-style:[a-z0-9-]+\b", re.IGNORECASE),
    re.compile(r"(?<!https:)(?<!http:)/grilling\b", re.IGNORECASE),
    re.compile(r"(?<!https:)(?<!http:)/domain-modeling\b", re.IGNORECASE),
    re.compile(r"\.\.[\\/]using-superpowers[\\/]references", re.IGNORECASE),
)

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def read_utf8(path: Path) -> str:
    """严格按 UTF-8 读取，同时兼容 BOM。"""

    return path.read_text(encoding="utf-8-sig")


def load_manifest() -> dict:
    return json.loads(read_utf8(MANIFEST_PATH))


def iter_text_files() -> list[Path]:
    return sorted(
        path
        for path in SKILL_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
    )


def check_external_runtime_dependencies(manifest: dict) -> list[str]:
    issues: list[str] = []
    for relative in manifest["runtime_entry_files"]:
        path = REFERENCES_ROOT / relative
        if not path.is_file():
            continue
        text = read_utf8(path)
        for line_number, line in enumerate(text.splitlines(), start=1):
            for pattern in EXTERNAL_RUNTIME_PATTERNS:
                if pattern.search(line):
                    issues.append(f"{relative}:{line_number}: {line.strip()}")
    return issues


def link_is_template_example(target: str) -> bool:
    """排除会在目标项目中生成的示例路径，而非技能包引用。"""

    normalized = target.replace("\\", "/")
    return (
        "<" in normalized
        or ">" in normalized
        or normalized.startswith("./src/")
        or normalized.startswith("../src/")
    )


def check_local_links(manifest: dict) -> list[str]:
    issues: list[str] = []
    for relative in manifest["runtime_entry_files"]:
        path = REFERENCES_ROOT / relative
        if not path.is_file():
            issues.append(f"{relative}: 文件不存在")
            continue
        text = read_utf8(path)
        for match in MARKDOWN_LINK.finditer(text):
            raw_target = match.group(1).strip()
            if raw_target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(raw_target.split("#", 1)[0])
            if not target or link_is_template_example(target):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(SKILL_ROOT.resolve())
            except ValueError:
                line = text.count("\n", 0, match.start()) + 1
                issues.append(f"{relative}:{line}: 链接越出技能目录 -> {raw_target}")
                continue
            if not resolved.exists():
                line = text.count("\n", 0, match.start()) + 1
                issues.append(f"{relative}:{line}: 本地链接不存在 -> {raw_target}")
    return issues


def path_matches_pattern(relative: str, pattern: str) -> bool:
    return fnmatch.fnmatchcase(relative, pattern)


def check_tracked_reference_files(manifest: dict) -> list[str]:
    tracked_patterns = [
        pattern
        for source in manifest["sources"]
        for pattern in source["tracked_local_paths"]
    ]
    reserved = set(manifest["reserved_local_paths"])
    issues: list[str] = []
    for path in sorted(REFERENCES_ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(REFERENCES_ROOT).as_posix()
        if relative in reserved:
            continue
        if not any(path_matches_pattern(relative, pattern) for pattern in tracked_patterns):
            issues.append(relative)
    return issues


def check_source_metadata(manifest: dict) -> list[str]:
    issues: list[str] = []
    required = {
        "id",
        "repository",
        "url",
        "branch",
        "commit",
        "license",
        "source_tree_sha256",
        "source_paths",
        "tracked_local_paths",
        "local_adaptations",
    }
    seen_ids: set[str] = set()
    for index, source in enumerate(manifest.get("sources", []), start=1):
        missing = required - set(source)
        if missing:
            issues.append(f"sources[{index}] 缺字段: {', '.join(sorted(missing))}")
            continue
        source_id = source["id"]
        if source_id in seen_ids:
            issues.append(f"来源 ID 重复: {source_id}")
        seen_ids.add(source_id)
        if not HEX40.fullmatch(source["commit"]):
            issues.append(f"{source_id}: commit 不是 40 位十六进制")
        if not HEX64.fullmatch(source["source_tree_sha256"]):
            issues.append(f"{source_id}: source_tree_sha256 不是 64 位十六进制")
        if not source["source_paths"]:
            issues.append(f"{source_id}: source_paths 为空")
        if not source["tracked_local_paths"]:
            issues.append(f"{source_id}: tracked_local_paths 为空")
    return issues


def check_encoding() -> list[str]:
    issues: list[str] = []
    for path in iter_text_files():
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            issues.append(f"{path.relative_to(SKILL_ROOT)}: UTF-8 解码失败: {error}")
            continue
        if "\ufffd" in text:
            issues.append(f"{path.relative_to(SKILL_ROOT)}: 包含 Unicode 替换字符")
        if re.search(r"\?{4,}", text):
            issues.append(f"{path.relative_to(SKILL_ROOT)}: 包含连续问号，疑似中文降级")
        if (
            CJK.search(text)
            and path.suffix.lower() in {".md", ".json", ".txt"}
            and path.name != "SKILL.md"
            and not raw.startswith(b"\xef\xbb\xbf")
        ):
            issues.append(f"{path.relative_to(SKILL_ROOT)}: 中文文本缺少 UTF-8 BOM")
    return issues


def check_orchestrator_policy() -> list[str]:
    issues: list[str] = []
    skill_text = read_utf8(SKILL_ROOT / "SKILL.md")
    frontmatter_match = re.match(r"^---\n(.*?)\n---", skill_text, re.DOTALL)
    if not frontmatter_match:
        issues.append("SKILL.md frontmatter 无效")
    else:
        keys = {
            line.split(":", 1)[0].strip()
            for line in frontmatter_match.group(1).splitlines()
            if ":" in line
        }
        unexpected = keys - {"name", "description"}
        if unexpected:
            issues.append(f"SKILL.md frontmatter 含非允许字段: {sorted(unexpected)}")
    forbidden_literals = {
        "supported_platforms": "仍包含旧的 supported_platforms 字段",
        "不适用场景（直接走轻量路径": "仍包含技能内任务规模判断",
        "发现即调用": "仍包含外部 skill 自动发现逻辑",
    }
    for literal, message in forbidden_literals.items():
        if literal in skill_text:
            issues.append(message)
    if re.search(r"(?<!Y)YYY-MM-DD(?!Y)", skill_text):
        issues.append("仍包含错误日期占位符 YYY-MM-DD")
    required_literals = (
        "用户调用本技能，即表示已决定走完整六阶段流程",
        "references/grill-me.md",
        "references/grilling.md",
        "references/grill-with-docs.md",
        "references/domain-modeling.md",
        "references/context-format.md",
        "references/adr-format.md",
        "不得提交、推送、创建 PR、合并、删除分支",
    )
    for literal in required_literals:
        if literal not in skill_text:
            issues.append(f"主流程缺少必要规则: {literal}")
    return issues


def main() -> int:
    try:
        manifest = load_manifest()
    except Exception as error:  # noqa: BLE001 - 校验器必须报告清晰错误
        print(f"MANIFEST_ERROR={error}")
        return 1

    external = check_external_runtime_dependencies(manifest)
    broken_links = check_local_links(manifest)
    untracked = check_tracked_reference_files(manifest)
    metadata = check_source_metadata(manifest)
    encoding = check_encoding()
    policy = check_orchestrator_policy()

    print(f"EXTERNAL_RUNTIME_DEPENDENCIES={len(external)}")
    print(f"BROKEN_LOCAL_REFERENCES={len(broken_links)}")
    print(f"UNTRACKED_REFERENCE_FILES={len(untracked)}")
    print(f"MISSING_SOURCE_METADATA={len(metadata)}")
    print(f"ENCODING_ERRORS={len(encoding)}")
    print(f"POLICY_ERRORS={len(policy)}")

    all_issues = (
        [f"外部依赖: {item}" for item in external]
        + [f"本地链接: {item}" for item in broken_links]
        + [f"未登记文件: {item}" for item in untracked]
        + [f"来源元数据: {item}" for item in metadata]
        + [f"编码: {item}" for item in encoding]
        + [f"主流程: {item}" for item in policy]
    )
    if all_issues:
        for issue in all_issues:
            print(f"ERROR: {issue}")
        print("BUNDLE_VALID=False")
        return 1

    print("BUNDLE_VALID=True")
    return 0


if __name__ == "__main__":
    sys.exit(main())
