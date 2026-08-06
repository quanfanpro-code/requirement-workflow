# diagnosing-bugs 自包含集成审查记录

## 审查范围

- 需求：`docs/requirements/2026-08-06-diagnosing-bugs-integration-requirement.md`
- 设计：`docs/superpowers/specs/2026-08-06-diagnosing-bugs-integration-design.md`
- 计划：`docs/superpowers/plans/2026-08-06-diagnosing-bugs-integration-plan.md`
- 实现：主流程、README、来源清单、依赖图、许可证声明、校验器、行为提示和集成测试
- 上游快照：`mattpocock/skills@6acc160e4e0cd062dbbbd7a1b26ae92855edf07e`

## 逐项结论

| 审查项 | 结果 | 证据 |
|---|---|---|
| 自包含 | 通过 | 正文、HITL 脚本模板和 OpenAI 元数据均在本仓库；运行时入口不含外部 Skill 路径 |
| 触发边界 | 通过 | 只有无法由证据立即解释、针对性修复后仍复现且继续盲改风险更高时才进入诊断分支 |
| 非触发边界 | 通过 | 正常 TDD 红灯、明显拼写或配置错误不进入；需求或设计无效时回退对应阶段 |
| 返回路径 | 通过 | 阶段 4 和阶段 5 都明确回到当前 TDD 任务的 VERIFY，再继续原流程 |
| 来源溯源 | 通过 | 使用独立来源 ID，记录仓库、链接、分支、固定提交、来源路径、来源树哈希、本地路径和适配说明 |
| 来源隔离 | 通过 | 原 Matt Pocock 来源的宽泛元数据路径已收窄为四个明确目录，不会吞并 diagnosing-bugs 元数据 |
| 上游一致性 | 通过 | 三个本地文件与固定提交逐字节一致；确定性归档 SHA-256 为 `dff8cc167215259536e5a1828d772e2125c28a1886c9eb3ab826c4312a87a6dd` |
| 许可证 | 通过 | 复用已有 Matt Pocock MIT 许可证全文，NOTICE 已加入 diagnosing-bugs |
| 安全与隐私 | 通过 | 没有新增依赖、密钥、动态命令执行或外部运行时路径；上游模板只作为按需参考，不强制执行 |
| 过度工程 | 通过 | 复用既有来源清单、依赖图、更新检查和完整性校验机制，只新增一个标准库测试文件 |
| README | 通过 | 已用大白话说明进入、非进入、返回、自包含和独立升级方法 |
| 编码 | 通过 | 中文 Markdown、JSON 和 NOTICE 使用 UTF-8 with BOM；未发现替换字符或连续问号乱码 |

## 审查发现与处理

1. 审查时发现 `NOTICE` 原文件没有 UTF-8 BOM。本次已修改该文件，因此按项目编码规则补加 BOM；正文内容未改变。
2. `check_upstream.py --json` 返回退出码 2，因为现有的四个其他来源存在可用更新。这是脚本约定的“发现更新”状态，不是执行错误；新来源 `mattpocock-diagnosing-bugs` 显示为 `current`。其他来源升级不属于本次范围，未改动。
3. 未发现阻断交付的正确性、安全性、兼容性或过度工程问题。

## 验证证据

- `python -X utf8 -m unittest scripts.test_diagnosing_integration -v`：5 项通过，0 失败。
- `python -X utf8 scripts/validate_bundle.py`：外部运行时依赖、断链、未跟踪引用、缺失来源元数据、编码错误和策略错误均为 0，`BUNDLE_VALID=True`。
- `python -X utf8 scripts/check_upstream.py --json`：唯一列出 `mattpocock-diagnosing-bugs`，状态为 `current`；无检查错误。
- `git diff --check`：退出码 0。
- 固定提交逐文件比较：3 个文件均为 `MATCH`。

## 残余风险

- 上游以后可能继续更新；维护者需先运行 `check_upstream.py`，只升级独立来源并重新生成来源树哈希，再执行集成测试和 bundle 校验。
- 行为提示和字面量测试可以防止关键规则被意外删除，但模型在具体故障中的判断仍需以实际证据为准。

## 审查结论

通过。阻断项 0，重要未处理项 0，可以进入最终验证和交付阶段。
