# requirement-workflow — 需求先行六阶段开发工作流
# Copyright (C) 2026 quanfanpro-code
#
# 本文件是 requirement-workflow 的原创编排层,采用 GNU Affero General Public
# License v3.0 (AGPL-3.0) 发布。
# 完整协议见项目根目录 LICENSE 文件(AGPL-3.0)。
##!/usr/bin/env python3
"""检查 SOURCES.json 中固定的 GitHub 提交是否已有更新。"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SKILL_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = SKILL_ROOT / "references" / "SOURCES.json"


def load_sources() -> list[dict]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))
    return manifest["sources"]


def latest_commit_via_gh(repository: str, branch: str, timeout: float) -> str:
    """优先复用已登录的 GitHub CLI，避免匿名 API 限流。"""

    completed = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{repository}/commits/{branch}",
            "--jq",
            ".sha",
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "gh api 调用失败")
    commit = completed.stdout.strip()
    if len(commit) != 40:
        raise ValueError(f"GitHub CLI 返回了无效提交号: {commit}")
    return commit


def latest_commit_via_http(repository: str, branch: str, timeout: float) -> str:
    """在 GitHub CLI 不可用时回退到匿名 HTTP API。"""

    url = f"https://api.github.com/repos/{repository}/commits/{branch}"
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "requirement-workflow-upstream-checker",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    return payload["sha"]


def latest_commit(repository: str, branch: str, timeout: float) -> str:
    if shutil.which("gh"):
        return latest_commit_via_gh(repository, branch, timeout)
    return latest_commit_via_http(repository, branch, timeout)


def main() -> int:
    parser = argparse.ArgumentParser(description="检查 requirement-workflow 上游更新")
    parser.add_argument("--timeout", type=float, default=15.0, help="单个请求超时秒数")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    results: list[dict] = []
    errors = 0
    updates = 0
    for source in load_sources():
        try:
            latest = latest_commit(source["repository"], source["branch"], args.timeout)
            status = "current" if latest == source["commit"] else "update_available"
            if status == "update_available":
                updates += 1
            result = {
                "id": source["id"],
                "repository": source["repository"],
                "status": status,
                "pinned": source["commit"],
                "latest": latest,
            }
        except (
            HTTPError,
            URLError,
            TimeoutError,
            KeyError,
            ValueError,
            RuntimeError,
            subprocess.TimeoutExpired,
        ) as error:
            errors += 1
            result = {
                "id": source["id"],
                "repository": source["repository"],
                "status": "error",
                "pinned": source["commit"],
                "error": str(error),
            }
        results.append(result)

    if args.json:
        print(
            json.dumps(
                {"updates": updates, "errors": errors, "sources": results},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for result in results:
            if result["status"] == "error":
                print(f"{result['id']}|ERROR|{result['error']}")
            else:
                print(
                    f"{result['id']}|{result['status'].upper()}|"
                    f"{result['pinned']}|{result['latest']}"
                )
        print(f"UPDATES_AVAILABLE={updates}")
        print(f"CHECK_ERRORS={errors}")

    if errors:
        return 1
    if updates:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
