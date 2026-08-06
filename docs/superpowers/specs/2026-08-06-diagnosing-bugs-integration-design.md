# diagnosing-bugs 自包含集成设计

## 方案比较

### 方案一：只摘录诊断规则

从上游正文摘出若干关键段落，直接写进 `SKILL.md`。改动最少，但会丢失完整流程、HITL 脚本、上游元数据和清晰的升级边界，后续很难判断本地内容对应哪个上游版本。

### 方案二：独立来源条目和完整本地快照（推荐）

把 `diagnosing-bugs` 的正文、脚本和 OpenAI 元数据完整放入 `references`，在 `SOURCES.json` 中为它建立独立来源条目；主流程只增加条件触发和返回规则。该方案保持运行时自包含，也允许以后单独核验、比较和升级，不会带动 Matt Pocock 仓库中的其他内置子能力。

### 方案三：运行时调用外部 Skill

在触发故障时读取外部 `diagnosing-bugs` 目录。维护文件最少，但违反现有执行契约；换电脑、目录变动或外部 Skill 缺失时会中断，因此不采用。

## 推荐结构

```text
requirement-workflow/
├── SKILL.md
├── README.md
├── test-prompts.json
├── scripts/
│   ├── validate_bundle.py
│   ├── check_upstream.py
│   └── test_diagnosing_integration.py
└── references/
    ├── diagnosing-bugs.md
    ├── diagnosing-bugs/
    │   └── scripts/hitl-loop.template.sh
    ├── upstream-metadata/mattpocock/diagnosing-bugs/openai.yaml
    ├── SOURCES.json
    └── DEPENDENCY-MAP.md
```

上游 `SKILL.md` 保存为 `references/diagnosing-bugs.md`；上游脚本保持相对路径关系；`agents/openai.yaml` 只作为维护元数据，不进入运行时依赖。

## 来源与升级模型

新增独立来源 ID `mattpocock-diagnosing-bugs`：

- 仓库：`mattpocock/skills`
- 分支：`main`
- 固定仓库快照：实施时重新核验的 40 位提交号
- 来源路径：`skills/engineering/diagnosing-bugs` 和仓库许可证
- 本地路径：正文、伴随脚本、上游元数据
- 许可证：复用现有 `references/licenses/mattpocock-skills-LICENSE.txt`
- 本地适配：由主编排器条件触发、作为本地引用而非独立 Skill 注册、诊断完成后返回原阶段

现有 `mattpocock-skills` 来源继续固定在原提交，不升级其 grill、grilling、domain-modeling 等内容。为避免来源归属重叠，原来的 `upstream-metadata/mattpocock/**` 宽泛跟踪规则改成四个现有子目录的明确路径，新来源只跟踪 `diagnosing-bugs` 元数据目录。

`check_upstream.py` 无需增加专用分支；它会根据新增来源条目自动独立报告更新状态。`validate_bundle.py` 增加入口、来源和主流程触发规则检查，使正文、脚本、元数据或触发入口缺失时直接失败。

## 自动触发与返回

### 阶段 4

出现无法由当前证据立即解释的测试、构建、运行或性能失败，或者同一失败经过一次针对性修复仍复现时，完整读取 `references/diagnosing-bugs.md`。按其流程建立可重复的红灯反馈环、最小化、排列假设、添加针对性探针、写回归测试并修复。诊断完成后回到当前 TDD 任务的 VERIFY 步骤。

### 阶段 5

验收发现缺陷且根因不明确时，读取同一引用完成诊断；明确根因后回到阶段 4，用 TDD 修复，再重新进入阶段 5 审查。

### 不触发

- 正常的 TDD 首次失败；
- 明显拼写、缺文件或普通配置错误；
- 需求、领域模型或设计本身不成立。

前两类在当前步骤直接处理；后一类回退相应阶段。

## 数据流

```text
阶段 4/5 发现异常
  → 判断是否满足疑难故障条件
  → 读取本地 diagnosing-bugs 正文和必要脚本
  → 建立反馈环并取得脱敏证据
  → 定位根因
  → 回到阶段 4 按 TDD 修复
  → 重新验证并继续原六阶段流程
```

## 测试策略

先增加一个标准库测试脚本，使当前版本因缺少内置引用、来源登记和触发入口而失败。最小实现后验证：

1. 正常路径：阶段 4 疑难失败和阶段 5 未知根因均有条件入口；
2. 边界路径：正常 TDD 红灯和明显错误明确不触发；
3. 错误路径：正文、脚本、元数据或来源条目缺失会失败；
4. 自包含：外部技能目录引用计数保持 0；
5. 来源：新增来源能被 `check_upstream.py` 单独枚举；
6. 编码：全部中文 Markdown、JSON 和文本为 UTF-8 with BOM，无替换字符；
7. 回归：原有 bundle 校验与测试提示仍通过。

## README 与交付

README 增加大白话说明：什么时候自动进入排错分支、排错完成回到哪里、为什么无需安装外部 Skill、到哪里查看来源和升级状态。现有未提交的 frontmatter 和 BOM 修正纳入同一轮审查。全部验证成功后提交当前已审查变更并推送到 `origin/main`。

## 回滚

实施前把所有待修改文件备份到 `C:\Users\27651\BackUp\requirement-workflow_<时间戳>`。若测试或完整性校验失败，使用局部补丁修复；若方案根本不成立，则从备份恢复本次文件并回退设计阶段。不会使用永久删除命令。

## ADR 判断

本设计延续既有“运行时自包含、来源元数据仅供维护”的架构，没有引入新的不可逆架构决策，因此不新增 ADR。
