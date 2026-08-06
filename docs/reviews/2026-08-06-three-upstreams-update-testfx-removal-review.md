# 三个上游升级与 TestFX 移除审查记录

## 审查范围

- 需求：`docs/requirements/2026-08-06-four-upstream-sources-update-requirement.md`
- 设计：`docs/superpowers/specs/2026-08-06-three-upstreams-update-testfx-removal-design.md`
- 计划：`docs/superpowers/plans/2026-08-06-three-upstreams-update-testfx-removal-plan.md`
- 实现：主流程、README、来源清单、依赖图、NOTICE、三来源引用、测试和 TestFX 删除
- 上游快照：`obra/superpowers@44c9b2d6e889982ac18c27d05a19fefe335194e1`、`mattpocock/skills@6acc160e4e0cd062dbbbd7a1b26ae92855edf07e`、`Panniantong/Agent-Reach@1221ecd0c3e0502ee37406f03543bedf7503f2c7`

## 逐项结论

| 审查项 | 结果 | 证据 |
|---|---|---|
| 变更范围 | 通过 | 只更新 obra-superpowers、mattpocock-skills、agent-reach；未改动其他四个已有新版来源 |
| 自包含 | 通过 | 运行时入口、Agent Reach 参考文件和 Grilling 元数据均在本仓库；无外部 Skill 运行时路径 |
| 上游溯源 | 通过 | `SOURCES.json` 固定提交、来源路径、本地路径、适配说明和来源树 SHA-256 均已更新 |
| Obra 处理 | 通过 | 新提交只有上游 README 招聘文字变动，选定本地来源内容无变化，因此仅更新提交和哈希，不无谓重写文件 |
| Grilling 适配 | 通过 | 吸收新版设计树和前沿排序，同时保留每轮单题及子代理须获用户明确授权的本地边界 |
| Agent Reach | 通过 | 5 份既有参考已更新，新增 `agent-reach/finance.md`；中文入口链接已改为本地 `agent-reach/` 路径，未引入英文运行时入口 |
| TestFX 移除 | 通过 | 21 个确认文件均已送入 Windows 回收站；运行时清单、依赖图、NOTICE 和阶段 4 必读列表已清除相关引用 |
| README | 通过 | 记录三个来源升级、新增金融参考和 TestFX 移除原因及数量 |
| 编码与格式 | 通过 | 修改的中文 Markdown、JSON、NOTICE 使用 UTF-8 with BOM；未发现替换字符、乱码或 diff 空白错误 |
| 过度工程 | 通过 | 复用现有来源清单、更新检查和 bundle 校验，只增加一个标准库行为测试，不新增依赖或同步框架 |

## 审查发现与处理

1. 初稿把 Agent Reach 的既有参考数量写成 6 份，复核固定提交后更正为 5 份既有参考加 1 份新增 `finance.md`。
2. 上游 Matt Grilling 新版包含批量提问和子代理建议；本地正文保留新版设计内容，但明确恢复单题交互和用户授权边界，避免改变 `requirement-workflow` 既有权限模型。
3. TestFX 目录的空目录未作为 Git 文件保留；21 个文件均已不存在，备份位于 `C:\Users\27651\BackUp\requirement-workflow_20260806_230636`，备份哈希无不一致。
4. 未发现阻断交付的正确性、安全性、兼容性或过度工程问题。

## 验证证据

- `python -X utf8 -m unittest scripts.test_diagnosing_integration scripts.test_three_upstreams_and_testfx_removal -v`：10 项通过，0 失败。
- `python -X utf8 scripts/validate_bundle.py`：外部运行时依赖、断链、未跟踪引用、缺失来源元数据、编码错误和策略错误均为 0，`BUNDLE_VALID=True`。
- `python -X utf8 scripts/check_upstream.py --json`：三个目标来源及其他已登记来源均为 `current`，`UPDATES=0`、`ERRORS=0`。
- `git diff --check`：退出码 0。
- 三个固定提交的确定性来源树哈希分别为 `4be45bea8eac905ff83de80583aff8e8339cba865e50410ce37ee65828e7c234`、`bad07f3098f09854b822c5c38020c9eada76897910ee198ca8a311937cd905ea`、`ddf84ced300ffac533076b063e0bac3f3e48ccad4c089795ea29164d92aecee5`，与 `SOURCES.json` 一致。

## 残余风险

- 上游以后可能继续更新；维护者需先运行 `check_upstream.py`，只升级明确批准的来源，再复核本地适配、测试和 bundle 完整性。
- TestFX 文件可从 Windows 回收站或本轮备份恢复；本次未永久删除。
- 行为测试能守住关键边界，但具体业务任务仍需以实际证据和阶段检查点为准。

## 审查结论

通过。阻断项 0，重要未处理项 0，可以进入最终验证、提交和推送阶段。
