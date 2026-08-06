# 三个旧来源升级与 TestFX 来源移除需求

## 背景与问题

`scripts/check_upstream.py --json` 在 2026-08-06 实时检查到 4 个旧来源的固定提交落后于各自 `main`。核验后确认 `microsoft-testfx` 提供的是一套与现有六阶段和 TDD 规则重复的多 Agent 测试生成流程。用户决定完整移除该来源及其 21 个文件，只升级另外 3 个来源，同时继续遵守 `requirement-workflow` 现有的自包含、来源溯源和本地引用体系。

## 用户与使用场景

维护者希望运行时仍只依赖本仓库内容；以后查看 `references/SOURCES.json` 即可知道每个上游来源的仓库、固定提交、来源路径、快照哈希、本地文件和适配原因，并能通过 `check_upstream.py` 独立检查后续更新。

## 已核验的三个升级来源

| 来源 ID | 当前固定提交 | 目标提交 | 选定来源路径的实际变化 |
|---|---|---|---|
| `obra-superpowers` | `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9` | `44c9b2d6e889982ac18c27d05a19fefe335194e1` | 无；上游新提交只删除仓库 README 的招聘段落，不影响本地选定来源 |
| `mattpocock-skills` | `ed37663cc5fbef691ddfecd080dff42f7e7e350d` | `6acc160e4e0cd062dbbbd7a1b26ae92855edf07e` | 仅 `grilling/SKILL.md` 和 `grilling/agents/openai.yaml` 改动；追问方式从逐题改为按设计树前沿分轮提问 |
| `agent-reach` | `b4d52c46c9113cb0f653d6df4cf71ebadf4930ac` | `1221ecd0c3e0502ee37406f03543bedf7503f2c7` | 中文入口和 5 份现有参考更新，新增 `finance.md`；主要涉及安全输入、后端验证、Exa、LinkedIn、视频重试链、雪球和 Windows 适配 |

## 功能范围

1. 将三个保留来源的固定提交和来源树 SHA-256 更新到本次核验值。
2. 对有实际变化的 `mattpocock-skills`、`agent-reach` 更新对应本地引用。
3. 对无实际内容变化的 `obra-superpowers` 只更新来源元数据，不无意义重写本地文件。
4. 保留现有本地适配：运行时相对链接、用户授权前不启动子代理、中文入口优先和外部 Skill 目录禁用。
5. 为 Agent Reach 新增本地 `agent-reach/finance.md`，并确保入口链接仍留在本仓库。
6. 从主流程、运行时入口、来源清单、依赖图和 NOTICE 中清除 `microsoft-testfx`、`code-testing-agent`、`code-testing-extensions` 及其许可证声明。
7. 将用户已确认的 21 个 TestFX 来源文件备份后送入 Windows 回收站。
8. 更新 README 的维护记录、行为测试和审查记录。
9. 验证后提交并推送 `origin/main`。

## 明确不做的内容

- 不更新已经独立固定且当前为最新的 `mattpocock-diagnosing-bugs`。
- 不把四个上游仓库中未列入 `source_paths` 的其他 Skill 或代码复制进来。
- 不安装新依赖，不启动子代理，不删除文件或目录。
- 不直接用整仓覆盖破坏本地相对链接和授权规则。

其中“不删除文件或目录”不适用于用户已经逐项确认的 21 个 TestFX 来源文件；这些文件只能使用 Windows 回收站删除。

## 本地适配决策待确认

新版 `grilling` 要求同一轮询问全部“当前可回答的问题”，并建议自动派出子代理查事实；这与主流程当前的“一次只提出一个关键澄清问题”和“子代理必须先获用户授权”存在冲突。用户已确认采用兼容策略：吸收新版的“设计树、依赖前沿、重新计算问题顺序”方法，但每次仍只问一个关键问题；事实优先由当前实例使用工具核验，只有用户明确授权才启动子代理。

## 约束与风险

- 固定提交更新必须重新计算确定性来源归档哈希，不能只改提交号。
- 删除 TestFX 后，阶段 4 仍须由 `test-driven-development.md`、`writing-good-tests.md`、`ponytail.md` 和 `karpathy-guidelines.md` 完整覆盖测试与最小实现规则。
- Agent Reach 上游入口使用 `references/*.md`，本地根入口必须继续改成 `agent-reach/*.md`。
- Agent Reach 上游包含英文入口 `SKILL_en.md`，本地运行时只保留中文入口；该取舍需要在 `local_adaptations` 中明确记录。
- 新增金融参考涉及行情信息，必须保留“可能延迟、不构成投资建议”和登录态边界。
- GitHub 比较接口对大型仓库最多返回 300 个文件；本次已通过固定提交的 Git 路径比较核验 TestFX 目标目录确实无变化。

## 验收标准

1. 三个升级来源均固定到上表目标提交，来源树哈希与固定提交确定性归档一致。
2. `check_upstream.py --json` 对这三个来源均返回 `current`，且无检查错误。
3. Matt Pocock 本地更新只影响 `grilling` 正文和元数据，并保留单题交互与子代理授权边界。
4. Agent Reach 本地入口、5 份现有分类参考和新增 `finance.md` 与目标提交一致或仅包含已登记的本地链接适配。
5. 21 个 TestFX 来源文件已进入 Windows 回收站；主流程、来源清单、依赖图、NOTICE 和 README 不再把它作为子能力。
6. `validate_bundle.py` 输出外部运行时依赖、断链、未跟踪文件、缺失来源、编码和策略错误均为 0，且 `BUNDLE_VALID=True`。
7. 行为测试覆盖三来源提交、哈希、无内容变更来源、Grilling 冲突适配、Agent Reach 新金融入口、TestFX 移除和外部路径禁用。
8. README、依赖图、来源清单和审查记录相互一致；中文文件无乱码。
9. 推送后本地 HEAD 与 `origin/main` 一致，工作区干净。

## 调研摘要与来源

- GitHub 实时检查：`scripts/check_upstream.py --json`，2026-08-06。
- GitHub Compare API：核验提交数量、提交摘要和初步文件列表。
- 固定提交 Git 路径比较：核验四个 `source_paths` 的实际文件变化，规避大型仓库 API 文件上限。
- 确定性 `git archive --format=tar`：计算三个目标提交的来源树 SHA-256。

## 待确认项

无。删除 21 个文件、只升级另外三个来源、采用 Grilling 兼容策略、同步 README 并推送 `origin/main` 均已由用户确认。
