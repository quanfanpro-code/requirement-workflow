# 三个上游升级与 TestFX 移除设计

## 目标

在不破坏 `requirement-workflow` 自包含和权限边界的前提下，升级 `obra-superpowers`、`mattpocock-skills`、`agent-reach`，完整移除 `microsoft-testfx` 及其 21 个文件，并同步 README、来源清单、依赖图、NOTICE、测试和审查记录。

## 方案比较

### 方案 A：直接用三个上游目录覆盖本地引用

- 优点：复制步骤少，表面上最接近上游。
- 缺点：会恢复外部 `references/*.md` 链接、自动派子代理规则和批量提问方式，破坏已确认的本地适配；还可能复制英文入口等非运行时文件。
- 结论：不采用。

### 方案 B：从固定提交提取选定来源，再重放明确的本地适配

- 优点：来源内容可逐字节核验；只更新 `source_paths` 里的目标；每项本地差异都能在 `local_adaptations` 和测试中解释；无内容变化的 Obra 不重写文件。
- 缺点：需要维护少量确定性的转换和逐文件验证。
- 结论：推荐并采用。

### 方案 C：引入长期补丁系统或自动同步生成器

- 优点：以后可自动重放适配。
- 缺点：为三个低频来源增加生成器、补丁格式和维护成本；本次变更规模不值得。
- 结论：不采用。

## 组件与边界

### Obra Superpowers

- 目标提交：`44c9b2d6e889982ac18c27d05a19fefe335194e1`。
- 选定来源内容与当前固定提交完全相同。
- 只更新 `SOURCES.json` 的提交和来源树哈希，以及依赖图中的固定提交。
- 不改写任何 Obra 本地引用文件。

### Matt Pocock Skills

- 目标提交：`6acc160e4e0cd062dbbbd7a1b26ae92855edf07e`。
- 只更新 `grilling.md` 和 `upstream-metadata/mattpocock/grilling/openai.yaml`。
- 从新版保留“设计树、依赖前沿、每次回答后重新计算顺序”。
- 本地适配继续覆盖两项冲突：每次只提一个关键问题；事实由当前实例优先查找，子代理只有在用户明确授权后才可启动。
- 其他 Matt 子技能及独立的 `mattpocock-diagnosing-bugs` 不改动。

### Agent Reach

- 目标提交：`1221ecd0c3e0502ee37406f03543bedf7503f2c7`。
- 更新中文入口 `agent-reach.md` 和 5 份既有参考 `career.md`、`search.md`、`social.md`、`video.md`、`web.md`；新增 `finance.md`。
- `dev.md` 在目标提交中未变化，保持现有文件。
- 根入口中的上游链接 `references/*.md` 确定性转换为本地 `agent-reach/*.md`。
- 不内置 `SKILL_en.md`；在 `local_adaptations` 明确记录中文运行时入口取舍。
- 保留隐藏输入、登录态边界、只读验收、字幕重试链、雪球行情声明和 Windows Git Bash 相关修复。

### Microsoft TestFX 移除

- 先将 21 个文件与全部关联修改文件备份到 `C:\Users\27651\BackUp\requirement-workflow_<时间戳>\` 并核验 SHA-256。
- 21 个文件只能送入 Windows 回收站，不使用永久删除命令。
- 从 `SKILL.md` 阶段 4 必读列表删除 `code-testing-agent`、`code-testing-extensions` 和语言扩展读取规则。
- 从 `SOURCES.json` 删除两个运行时入口和完整 `microsoft-testfx` 来源对象。
- 从依赖图、NOTICE、README 和测试中清除该来源。
- 阶段 4 保留 TDD、高质量测试、最小实现和按需并行规则，测试职责不留空洞。

## 数据流

1. 读取三个固定提交和对应 `source_paths`。
2. 对有变化的 Matt、Agent Reach 提取目标文件。
3. 对提取内容执行已登记的最小本地转换。
4. 用行为测试比对目标提交、来源哈希、本地文件、链接和权限边界。
5. 更新来源、依赖、NOTICE、README 和审查文档。
6. 将 TestFX 文件送入回收站后运行完整性校验，确认没有断链或漏登记。
7. 最终验证成功后提交并推送 `origin/main`。

## 错误处理与停止条件

- 任一备份哈希不一致：立即停止，不修改或删除。
- Windows 回收站接口不可用：停止并请用户手动删除，不改用永久删除。
- 固定提交文件、来源树哈希或目标路径不一致：停止升级对应来源。
- 本地适配造成链接断裂或外部 Skill 路径：测试必须失败，修正后再继续。
- `check_upstream.py` 对三个目标来源仍显示 `update_available`：重新核验是否上游在实施期间前进；不静默换提交。
- 远程 `main` 在提交前前进：停止推送，先处理远程差异；不强推。

## 测试策略

新增一组标准库测试，至少验证：

1. 三个来源的仓库、目标提交和来源树哈希准确。
2. `microsoft-testfx` 来源、运行时入口和 21 个文件均不存在。
3. `SKILL.md` 阶段 4 不再引用 TestFX，但仍包含 TDD 与测试质量入口。
4. Grilling 保留设计树思路、单题交互和子代理授权边界。
5. Agent Reach 包含本地 `finance.md`，入口链接不越出本仓库。
6. README 明确记录三个来源升级和 TestFX 移除。
7. `validate_bundle.py`、`check_upstream.py`、`git diff --check` 和编码检查通过。

## 迁移与回滚

- 文件修改前统一备份；删除文件另有同一备份副本和 Windows 回收站副本。
- 若升级验证失败，从备份目录恢复本轮文件即可回到提交 `ba437de389046bb759800ff8c345c7be975c6892` 的内容状态。
- 不删除分支、不清理工作区、不强推。

## 文档决策

- 不新增 `CONTEXT.md`：本次只维护来源与编排，不产生新的业务领域术语。
- 不新增 ADR：采用固定提交提取并重放本地适配，是现有来源体系的延续，容易回滚，也没有新的长期架构锁定。
