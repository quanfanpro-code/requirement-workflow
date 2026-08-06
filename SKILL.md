---
name: requirement-workflow
description: 需求先行的六阶段完整开发工作流。用户手动调用后，必须按需求澄清、方案设计、实施计划、TDD 编码执行、验收审查、交付完成依次推进；适用于需要完整需求与设计过程的开发任务。所有流程规则、严苛追问、领域建模、计划、测试、审查和交付指引均内置在本技能的 references/ 中，运行时不依赖其他技能目录。
---

<!--
  requirement-workflow — 需求先行六阶段开发工作流
  Copyright (C) 2026 quanfanpro-code

  本文件是 requirement-workflow 的原创编排层,采用 GNU Affero General Public
  License v3.0 (AGPL-3.0) 发布。
  完整协议见项目根目录 LICENSE 文件(AGPL-3.0)。

  本项目的 references/ 目录包含来自第三方 MIT 项目的资料,
  它们保留各自的原始许可证(详见 NOTICE 和 references/licenses/)。
-->

# Requirement Workflow

## 执行契约

1. 用户调用本技能，即表示已决定走完整六阶段流程。不要判断任务轻重，不要绕过任何阶段。
2. 运行时只读取本技能目录内的 `SKILL.md`、`references/` 和 `scripts/`。不得读取 `.agents/skills`、`.codex/skills`等技能目录或在线技能正文。
3. 上游仓库、提交号和本机来源路径仅供维护更新，记录在 `references/SOURCES.json`；它们不是运行时依赖。
4. 每次进入一个阶段前，完整读取该阶段列出的本地文件。不要凭记忆复述规则。
5. 本地引用缺失、损坏或校验失败时，停止流程并报告“技能包完整性错误”。不要静默改用外部 skill，也不要用简化问题集冒充原流程。
6. 宿主的安全、编码、备份、权限和删除规则始终有效。流程文件与宿主规则冲突时，以宿主规则和用户本轮明确指令为准。
7. 维护一个六阶段清单。阶段内连续执行，只有本文件列出的阶段检查点才需要等待用户确认；不要在每个 TDD 小步骤后反复打断用户。
8. 未经用户明确授权，不得提交、推送、创建 PR、合并、删除分支、删除工作区、安装依赖或启动并行 agent。

## 红线与反例黑名单

| 禁止行为 | 错误反例 |
|---|---|
| 判断任务较轻而跳过阶段 | “只是改个错别字，直接处理，不走六阶段。” |
| 用自编问题替代内置严苛追问链 | “参考 `grill-me` 的思路，简单问三个问题即可。” |
| 运行时读取外部技能目录或在线技能正文 | “本地版本不确定，去其他 skill 目录找最新版。” |
| 本地引用缺失、损坏或校验失败后静默继续 | “少一个参考文件不影响，凭经验往下做。” |
| 在阶段 1、2、3 的用户检查点前进入下一阶段或开始实现 | “方案大致清楚，先写代码再补确认。” |
| 未获用户明确授权就启动并行 agent | “这个任务适合并行，自动分给多个 agent。” |
| 未获用户明确授权就执行 Git 写操作、删除或安装依赖 | “为了交付方便，直接提交并清理分支。” |
| 没有刚刚取得的验证证据就声称完成 | “代码看起来没问题，应该已经完成。” |

## 启动检查

开始阶段 1 前：

1. 确认当前项目范围、宿主规则和已有用户指令。
2. 如 Python 可用，运行 `python scripts/validate_bundle.py`。若校验失败，按完整性错误处理。
3. 建立阶段清单：
   - [ ] 阶段 1：需求澄清
   - [ ] 阶段 2：方案设计
   - [ ] 阶段 3：实施计划
   - [ ] 阶段 4：TDD 编码执行
   - [ ] 阶段 5：验收审查
   - [ ] 阶段 6：交付完成

完整依赖关系和按需加载入口见 `references/DEPENDENCY-MAP.md`。

## 阶段 1：需求澄清

### 必读文件

按顺序完整读取：

1. `references/brainstorming.md`
2. `references/writing-clearly-and-concisely.md`
3. `references/grill-me.md`
4. `references/grilling.md`

需要外部事实、现成方案、官方资料或 GitHub 调研时，再读取：

- `references/agent-reach.md`
- 与任务对应的 `references/agent-reach/*.md`

### 执行

1. 阅读项目规则、相关文档、代码和历史证据，先理解现状。
2. 一次只提出一个关键澄清问题；优先弄清目标、用户、范围、约束、失败表现和成功标准。
3. 对可能变化的外部事实进行实时核验，并记录来源、日期和结论。
4. 按 `grill-me.md` 与 `grilling.md` 对需求执行完整严苛追问，不得替换成自编的简化问题集。
5. 把已确认内容和仍待确认的假设分开记录。
6. 写入 `docs/requirements/YYYY-MM-DD-<topic>-requirement.md`，至少包括：
   - 背景与问题
   - 用户与使用场景
   - 功能范围
   - 明确不做的内容
   - 约束与风险
   - 验收标准
   - 调研摘要与来源
   - 待确认项

### 🔴 CHECKPOINT 1 · 需求确认

**🛑 STOP：**向用户展示需求摘要、边界和验收标准并等待确认。确认后标记阶段 1 完成并进入阶段 2。

## 阶段 2：方案设计

### 必读文件

按顺序完整读取：

1. `references/grill-with-docs.md`
2. `references/grilling.md`
3. `references/domain-modeling.md`
4. `references/context-format.md`
5. `references/adr-format.md`

面对陌生、大型或结构不清的代码库时，再读取：

- `references/nexus-mapper.md`
- `references/nexus-mapper/references/probe-protocol.md`
- `references/nexus-mapper/references/output-schema.md`
- 需要非标准语言支持时读取 `references/nexus-mapper/references/language-customization.md`

### 执行

1. 基于已确认需求提出 2 至 3 个可行方案。
2. 比较每个方案的实现成本、维护成本、风险、兼容性、测试难度和可逆性。
3. 按 `grill-with-docs.md` 再做一轮完整追问，同时应用 `domain-modeling.md`：
   - 术语一旦澄清，按 `context-format.md` 更新对应 `CONTEXT.md`。
   - 只有满足 ADR 门槛的决策，才按 `adr-format.md` 写入 `docs/adr/`。
4. 优先复用现有代码、标准库、平台能力和已安装依赖；确有必要时才设计新代码或新依赖。
5. 写入 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`，包含方案比较、推荐方案、数据流、错误处理、测试策略、迁移与回滚方式。

### 🔴 CHECKPOINT 2 · 方案批准

**🛑 STOP：**展示方案对比和推荐理由，等待用户选择或批准。确认后标记阶段 2 完成并进入阶段 3。

## 阶段 3：实施计划

### 必读文件

按顺序完整读取：

1. `references/writing-plans.md`
2. `references/executing-plans.md`

根据实际执行方式按需读取：

- 需要隔离工作区：`references/using-git-worktrees.md`
- 用户明确授权使用子 agent：`references/subagent-driven-development.md`
- 子 agent 需要独立审查：`references/requesting-code-review.md`

### 执行

1. 将设计拆成短小、可验证、按依赖排序的任务。
2. 每个实现任务必须写成“失败测试 → 最小实现 → 全量验证”。
3. 写明准确文件路径、预期改动、测试命令和成功输出。
4. 保存到 `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`。
5. 默认采用 `executing-plans.md` 的串行执行方式。只有用户明确授权且任务相互独立时，才采用子 agent 方式。
6. 计划可以列出建议的提交点，但不得把“自动提交”写成默认执行动作。

### 🔴 CHECKPOINT 3 · 计划批准

**🛑 STOP：**展示任务清单、依赖顺序、风险点和验证方法，等待用户批准。确认后标记阶段 3 完成并进入阶段 4。

## 阶段 4：TDD 编码执行

### 首次进入阶段时必读

按顺序完整读取：

1. `references/test-driven-development.md`
2. `references/writing-good-tests.md`
3. `references/ponytail.md`
4. `references/karpathy-guidelines.md`

需要并行且已获用户授权时，再读取 `references/dispatching-parallel-agents.md`。

### 复杂故障诊断分支

正常的 TDD 红灯是预期反馈，**不触发**复杂故障诊断。简单错别字、明显缺少配置，以及需求或设计本身无效的情况同样不触发；分别按当前任务直接修正，或回退到对应需求、设计阶段。

只有同时满足以下条件时，才完整读取并执行 `references/diagnosing-bugs.md`：

1. 失败现象无法由当前证据立即解释，且需要提出多个可证伪假设；
2. 已完成一次针对性修复后仍复现，或故障只在跨环境、并发、性能、时序等条件下出现；
3. 继续盲改的风险高于先建立稳定复现与证据链。

诊断时可按上游指引使用本地模板 `references/diagnosing-bugs/scripts/hitl-loop.template.sh`，但不得把它当作必须执行的固定脚本。查明根因并完成针对性修复后，回到当前 TDD 任务的 VERIFY，运行定向测试和受影响范围验证，再继续原任务清单。

### 每个任务的循环

1. **RED**：先写一个能证明目标行为且会因缺少实现而失败的测试，运行并确认失败原因正确。
2. **GREEN**：遵循 `ponytail.md` 和 `karpathy-guidelines.md`，只写让测试通过的最少代码。
3. **REFACTOR**：在测试保护下清理本次新增的重复和命名问题，不扩大范围。
4. **VERIFY**：运行定向测试，再运行受影响范围的测试、静态检查和构建。
5. 记录实际命令、退出码、通过数量和仍存在的限制。
6. 更新任务清单后直接推进下一项；只有出现需求歧义、权限扩大、破坏性操作或计划外重大风险时才暂停询问。

不得为了覆盖率编写只验证 mock 调用或实现细节的空洞测试。测试至少覆盖正常路径、边界条件和错误路径。

完成全部任务并取得新鲜验证证据后，标记阶段 4 完成并进入阶段 5。

## 阶段 5：验收审查

### 必读文件

按顺序完整读取：

1. `references/code-reviewer.md`
2. `references/ponytail-review.md`
3. `references/verification-before-completion.md`

从 `references/code-reviewer/reference/` 读取与项目语言、架构、安全和性能相关的指南。只有用户授权独立 reviewer 时，才读取并执行 `references/requesting-code-review.md`。

若验收复现出阶段 4 遗留的复杂故障，并且符合“无法由当前证据立即解释、一次针对性修复后仍复现”等触发条件，完整读取 `references/diagnosing-bugs.md`，回到阶段 4 建立诊断闭环；修复后回到当前 TDD 任务的 VERIFY，再重新执行本阶段审查。正常验收失败若原因明确，则直接按 TDD 修复，不触发该分支。

### 执行

1. 将实现逐项对照需求文档、设计文档和实施计划。
2. 审查正确性、安全性、数据损失风险、兼容性、性能、可维护性和过度工程。
3. 审查测试是否真正验证行为，以及正常、边界、错误路径是否齐全。
4. 对发现的问题按严重程度修复；修复仍遵循 TDD。
5. 重新运行完整验证，不复用旧输出。
6. 写入 `docs/reviews/YYYY-MM-DD-<topic>-review.md`，记录审查范围、发现、修复、验证证据和残余风险。

若审查发现需求或架构根本不成立，回退到对应阶段并更新文档，不得只修表面症状。

完成审查和新鲜验证后，标记阶段 5 完成并进入阶段 6。

## 阶段 6：交付完成

### 必读文件

按顺序完整读取：

1. `references/verification-before-completion.md`
2. `references/finishing-a-development-branch.md`

### 执行

1. 重新运行最终测试、构建和必要的质量检查。
2. 检查工作区状态，列出实际变更文件、验证结果、未解决风险和后续事项。
3. 若当前工作位于 Git 仓库，向用户提供适用选项：
   - 保留当前变更，不执行 Git 写操作
   - 创建本地提交
   - 推送并创建 PR
   - 合并到指定分支
   - 清理工作分支或工作区

### 🔴 CHECKPOINT 4 · 交付动作授权

**🛑 STOP：**等待用户明确选择后，才执行相应操作。删除或清理仍须遵守宿主的删除确认与可恢复要求。

4. 仅执行用户明确选择的交付动作。
5. 只有全部必要验证刚刚成功，才能声称完成。

标记阶段 6 完成并提交最终交付摘要。

## 完整性失败与工具降级

| 触发条件 | 第一处理动作 | 仍失败时 |
|---|---|---|
| 本地引用缺失、损坏或校验失败 | 运行 `scripts/validate_bundle.py`，报告具体文件和错误 | 停止流程并标记“技能包完整性错误”；不得读取外部技能目录或凭经验替代 |
| 调研所需网络或资料源不可用 | 记录无法核验的事实、已用来源和时间范围 | 停在阶段 1，由用户决定等待联网还是接受明确标注的离线假设 |
| 陌生代码库的自动探测脚本失败 | 按本地 `nexus-mapper` 参考文档手工完成仓库地图与证据索引 | 证据仍不足时停在阶段 2，不得凭目录名猜测架构 |
| 无法建立能正确失败的测试 | 回查验收标准、真实调用链和现有测试方式，修正测试边界 | 回退阶段 1 或阶段 3，先修需求或计划；不得先写实现 |
| 测试、构建或静态检查持续失败 | 定位共同根因，缩小变更范围并重跑最小复现 | 不进入阶段 5；报告阻塞证据、已尝试动作和所需决策 |
| 审查发现需求、领域模型或架构不成立 | 回退对应阶段并同步更新需求、设计、ADR 或计划 | 重新通过该阶段检查点前，不得只修表面症状或继续交付 |
| Git 不可用或项目不是 Git 仓库 | 跳过 Git 交付选项，完成文件级验证和变更清单 | 明确说明未执行的 Git 动作，不得伪造提交或分支状态 |
| 辅助脚本、并行 agent 或平台能力不可用 | 依据同一份本地参考文档串行手工执行相同步骤 | 记录未执行的自动化检查；若人工证据不足，则停在当前阶段 |

## 维护入口

- 查看完整依赖闭包：`references/DEPENDENCY-MAP.md`
- 查看来源、提交和本地适配：`references/SOURCES.json`
- 校验自包含包：`python scripts/validate_bundle.py`
- 检查上游是否更新：`python scripts/check_upstream.py`

维护操作可以访问上游仓库；六阶段运行流程不得借此读取外部 skill 正文。
