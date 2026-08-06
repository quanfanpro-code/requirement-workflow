# Requirement Workflow 依赖闭包

## 运行时边界

- 六阶段执行只读取本技能目录内的文件。
- 本文列出的上游名称用于维护溯源，不代表运行时调用外部 skill。
- `SOURCES.json` 记录固定提交、来源路径、许可证状态、来源树哈希和本地适配。
- `upstream-metadata/` 保留上游技能自带的界面元数据，仅用于完整同步和更新比对。
- 任一本地入口或伴随文件缺失时，必须停止并报告完整性错误。

## 阶段 1：需求澄清

| 本地入口 | 伴随文件 | 用途 |
|---|---|---|
| `brainstorming.md` | `brainstorming/spec-document-reviewer-prompt.md`、`brainstorming/visual-companion.md`、`brainstorming/scripts/` | 探索上下文、逐项澄清、形成需求与设计输入 |
| `writing-clearly-and-concisely.md` | `writing-clearly-and-concisely/elements-of-style.md` | 改善面向用户文档的表达 |
| `grill-me.md` | `grilling.md` | 对需求和初步方案执行完整严苛追问 |
| `agent-reach.md` | `agent-reach/search.md`、`social.md`、`career.md`、`dev.md`、`web.md`、`video.md` | 需要最新外部证据时进行实时调研 |

## 阶段 2：方案设计

| 本地入口 | 伴随文件 | 用途 |
|---|---|---|
| `grill-with-docs.md` | `grilling.md`、`domain-modeling.md` | 追问方案并同步沉淀领域知识 |
| `domain-modeling.md` | `context-format.md`、`adr-format.md` | 维护术语、上下文和满足门槛的 ADR |
| `nexus-mapper.md` | `nexus-mapper/references/`、`nexus-mapper/scripts/` | 对陌生或大型代码库建立结构化知识图谱 |

## 阶段 3：实施计划

| 本地入口 | 间接依赖 | 用途 |
|---|---|---|
| `writing-plans.md` | `writing-plans/plan-document-reviewer-prompt.md` | 编写可执行、可验证的实施计划 |
| `executing-plans.md` | `using-git-worktrees.md`、`finishing-a-development-branch.md` | 串行执行计划和最终收尾 |
| `subagent-driven-development.md` | `subagent-driven-development/`、`requesting-code-review.md` | 用户授权后进行任务隔离和双阶段审查 |
| `using-superpowers-tools/` | 无外部 skill 依赖 | 不同宿主的工具名称映射，仅供本地参考 |

## 阶段 4：TDD 编码

| 本地入口 | 伴随文件 | 用途 |
|---|---|---|
| `test-driven-development.md` | `writing-good-tests.md` | RED、GREEN、REFACTOR 与高质量测试规则 |
| `writing-good-tests.md` | `writing-skills.md`、`writing-skills/` | 测试行为而不是实现细节；文档型 skill 的测试方法 |
| `diagnosing-bugs.md` | `diagnosing-bugs/scripts/hitl-loop.template.sh` | 仅在难以解释、针对性修复后仍复现的复杂故障中建立假设、取证和复现闭环；完成后返回当前 TDD 任务的 VERIFY |
| `ponytail.md` | 无 | 优先复用和最小实现 |
| `karpathy-guidelines.md` | 无 | 显式假设、外科式修改、可验证目标 |
| `code-testing-agent.md` | `code-testing-agent/`、`code-testing-extensions.md`、`code-testing-extensions/extensions/` | 测试调研、计划、实现和语言适配 |
| `dispatching-parallel-agents.md` | 无 | 仅在用户授权且任务独立时并行 |

## 阶段 5：验收审查

| 本地入口 | 伴随文件 | 用途 |
|---|---|---|
| `code-reviewer.md` | `code-reviewer/reference/`、`assets/`、`scripts/` | 代码、架构、安全、性能和语言专项审查 |
| `ponytail-review.md` | 无 | 过度工程专项审查 |
| `requesting-code-review.md` | `requesting-code-review/code-reviewer-prompt.md` | 用户授权时进行独立审查 |
| `verification-before-completion.md` | 无 | 用新鲜证据约束完成声明 |
| `diagnosing-bugs.md` | `diagnosing-bugs/scripts/hitl-loop.template.sh` | 验收复现出阶段 4 未解决的复杂故障时回到诊断闭环；完成后返回阶段 4 的 VERIFY |

## 阶段 6：交付完成

| 本地入口 | 伴随文件 | 用途 |
|---|---|---|
| `verification-before-completion.md` | 无 | 最终测试、构建和质量检查 |
| `finishing-a-development-branch.md` | 无 | 展示 Git 交付选项并等待用户选择 |

## 上游来源

| 来源 | 固定提交 | 本地内容 |
|---|---|---|
| `obra/superpowers` | `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9` | brainstorming、计划、TDD、并行、审查、验证和收尾 |
| `mattpocock/skills` | `ed37663cc5fbef691ddfecd080dff42f7e7e350d` | grill-me、grilling、grill-with-docs、domain-modeling 和格式 |
| `mattpocock/skills`（diagnosing-bugs 独立快照） | `6acc160e4e0cd062dbbbd7a1b26ae92855edf07e` | diagnosing-bugs 正文、HITL 循环脚本模板和上游界面元数据 |
| `Panniantong/Agent-Reach` | `b4d52c46c9113cb0f653d6df4cf71ebadf4930ac` | 调研路由和六类详细参考 |
| `Haaaiawd/Nexus-skills` | `09d5601ea8be34a83b54b8d48e24f0b6700cf403` | nexus-mapper 正文、协议、Schema 和脚本 |
| `DietrichGebert/ponytail` | `16f29800fd2681bdf24f3eb4ccffe38be3baec6b` | ponytail 与 ponytail-review |
| `awesome-skills/code-review-skill` | `95c707b999295f6c8ee2d0d3d1c61cc0c2e1a52c` | 完整代码审查入口、语言指南、资产和脚本 |
| `microsoft/testfx` | `81f5fb81acf8a6f6354d10deecb7c1ebd50756ce` | code-testing-agent 与全部语言扩展 |
| `multica-ai/andrej-karpathy-skills` | `2c606141936f1eeef17fa3043a72095b4765b9c2` | karpathy-guidelines |
| `obra/the-elements-of-style` | `6099c505c2a8eb066f3777f83a97d9d828f7954c` | writing-clearly-and-concisely 与完整写作参考 |
