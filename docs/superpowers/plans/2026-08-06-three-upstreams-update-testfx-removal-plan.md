# 三个上游升级与 TestFX 移除实施计划

> **执行说明：** 用户未授权子代理，按 `executing-plans.md` 在当前会话串行执行。步骤使用复选框跟踪。

**目标：** 升级 Obra、Matt Pocock 和 Agent Reach 三个来源，移除 Microsoft TestFX 来源及 21 个文件，同步文档并推送 `origin/main`。

**架构：** 从已核验的固定提交提取选定来源，只对有变化的文件重放已登记本地适配；TestFX 文件备份后逐个送入 Windows 回收站；来源、依赖、README、NOTICE 和测试保持一致。

**技术栈：** Markdown、JSON、Python 标准库、Git、GitHub CLI、Windows 回收站接口、PowerShell 与 Git Bash。

## 全局约束

- 当前分支为 `main`，用户已明确授权本轮完成后提交并推送 `origin/main`。
- 不启动子代理、不安装依赖、不强推、不读取外部 Skill 作为运行时依赖。
- 所有现有文件修改或删除前统一备份到 `C:\Users\27651\BackUp\requirement-workflow_<时间戳>\` 并核验 SHA-256。
- 21 个已确认文件只能送入 Windows 回收站；接口不可用时停止，不改用永久删除。
- 中文 Markdown、JSON 和文本使用 UTF-8 with BOM，并检查替换字符和连续问号。
- Grilling 采用设计树和前沿排序，但一次只提一个关键问题；子代理必须先获用户授权。
- Agent Reach 只保留中文运行时入口，根入口链接转换为 `agent-reach/*.md`。

---

### 任务 1：建立备份和失败测试

**文件：**

- 新建：`scripts/test_three_upstreams_and_testfx_removal.py`
- 备份：本计划涉及的全部现有文件和 21 个 TestFX 文件

**接口：**

- 输入：技能包根目录、`SOURCES.json`、主流程、README 和本地引用。
- 输出：标准库 `unittest`，验证三来源固定值、TestFX 移除、Grilling 兼容规则和 Agent Reach 金融入口。

- [x] **步骤 1：建立统一备份**

备份 `SKILL.md`、`README.md`、`NOTICE`、`test-prompts.json`、`references/SOURCES.json`、`references/DEPENDENCY-MAP.md`、Matt 与 Agent Reach 待修改引用、需求文档，以及已确认删除的 21 个文件。逐项核验源文件和备份 SHA-256 相等。

- [x] **步骤 2：写入失败测试**

测试至少断言：

```python
self.assertEqual(sources["obra-superpowers"]["commit"], OBRA_COMMIT)
self.assertEqual(sources["mattpocock-skills"]["commit"], MATT_COMMIT)
self.assertEqual(sources["agent-reach"]["commit"], AGENT_REACH_COMMIT)
self.assertNotIn("microsoft-testfx", sources)
self.assertFalse((references / "code-testing-agent.md").exists())
self.assertFalse((references / "code-testing-extensions.md").exists())
self.assertIn("agent-reach/finance.md", agent_reach_text)
self.assertIn("one question", grilling_text.lower())
```

- [x] **步骤 3：运行测试确认红灯**

运行 `python -X utf8 -m unittest scripts.test_three_upstreams_and_testfx_removal -v`。预期因旧提交、TestFX 文件仍存在和 `finance.md` 尚未加入而失败。

### 任务 2：移除 TestFX 来源和运行时调用

**文件：**

- 修改：`SKILL.md`
- 修改：`references/SOURCES.json`
- 修改：`references/DEPENDENCY-MAP.md`
- 修改：`NOTICE`
- 删除到回收站：用户确认的 21 个 TestFX 来源文件

**接口：**

- 输入：已核验备份和删除清单。
- 输出：不再包含 `microsoft-testfx`、`code-testing-agent` 或 `code-testing-extensions` 的自包含流程。

- [x] **步骤 1：移除主流程调用和来源登记**

从阶段 4 必读列表、`runtime_entry_files`、来源对象、依赖图和 NOTICE 中删除 TestFX 相关条目；保留 TDD、高质量测试、Ponytail、Karpathy 和按需并行规则。

- [x] **步骤 2：将 21 个文件逐个送入回收站**

使用 `Microsoft.VisualBasic.FileIO.FileSystem.DeleteFile(..., RecycleOption.SendToRecycleBin)`。完成后核对 21 个文件均不存在；不永久删除遗留空目录。

- [x] **步骤 3：运行定向测试**

预期 TestFX 移除断言通过；三来源升级相关断言仍保持红灯。

### 任务 3：升级 Obra 与 Matt Pocock 来源

**文件：**

- 修改：`references/SOURCES.json`
- 修改：`references/DEPENDENCY-MAP.md`
- 修改：`references/grilling.md`
- 修改：`references/upstream-metadata/mattpocock/grilling/openai.yaml`

**接口：**

- 输入：固定提交 `44c9b2d...`、`6acc160...` 及已计算的来源树哈希。
- 输出：Obra 元数据更新；Matt Grilling 新版结构和本地兼容适配。

- [x] **步骤 1：更新 Obra 元数据**

将提交改为 `44c9b2d6e889982ac18c27d05a19fefe335194e1`，来源树 SHA-256 改为 `4be45bea8eac905ff83de80583aff8e8339cba865e50410ce37ee65828e7c234`；不改写 Obra 引用正文。

- [x] **步骤 2：更新 Matt 内容和元数据**

将提交改为 `6acc160e4e0cd062dbbbd7a1b26ae92855edf07e`，来源树 SHA-256 改为 `bad07f3098f09854b822c5c38020c9eada76897910ee198ca8a311937cd905ea`。以新版 Grilling 为基底，局部改成单题前沿询问和需授权子代理；同步上游 OpenAI 元数据。

- [x] **步骤 3：运行定向测试**

预期 Obra、Matt 提交与 Grilling 兼容规则通过；Agent Reach 仍保持红灯。

### 任务 4：升级 Agent Reach 本地快照

**文件：**

- 修改：`references/agent-reach.md`
- 修改：`references/agent-reach/career.md`
- 新建：`references/agent-reach/finance.md`
- 修改：`references/agent-reach/search.md`
- 修改：`references/agent-reach/social.md`
- 修改：`references/agent-reach/video.md`
- 修改：`references/agent-reach/web.md`
- 修改：`references/SOURCES.json`
- 修改：`references/DEPENDENCY-MAP.md`

**接口：**

- 输入：固定提交 `1221ecd...` 的中文入口和分类参考。
- 输出：本地中文运行时快照、金融入口和明确的本地适配记录。

- [x] **步骤 1：提取目标提交文件**

从固定提交复制中文入口和 5 份变化参考，新增 `finance.md`；`dev.md` 因内容未变化不重写。

- [x] **步骤 2：重放本地链接适配**

仅把根入口中的 Markdown 目标 `references/<分类>.md` 转为 `agent-reach/<分类>.md`，不得修改正文提到的上游通配描述。记录不内置 `SKILL_en.md` 的取舍。

- [x] **步骤 3：更新来源元数据**

将提交改为 `1221ecd0c3e0502ee37406f03543bedf7503f2c7`，来源树 SHA-256 改为 `ddf84ced300ffac533076b063e0bac3f3e48ccad4c089795ea29164d92aecee5`，依赖图加入 `finance.md`。

- [x] **步骤 4：运行测试和 bundle 校验**

运行集成测试和 `python -X utf8 scripts/validate_bundle.py`。预期测试全部通过，`BUNDLE_VALID=True`。

### 任务 5：同步 README、行为提示和审查记录

**文件：**

- 修改：`README.md`
- 修改：`test-prompts.json`
- 新建：`docs/reviews/2026-08-06-three-upstreams-update-testfx-removal-review.md`

**接口：**

- 输入：已完成的来源和运行时结构。
- 输出：面向普通用户的变更说明、行为样例和完整审查证据。

- [x] **步骤 1：更新 README**

记录三个来源的新固定版本、实际内容变化、TestFX 移除原因、阶段 4 剩余测试规则和独立更新方式。

- [x] **步骤 2：更新行为提示**

增加 Grilling 单题前沿、Agent Reach 金融入口和阶段 4 不得读取 TestFX 的场景。

- [x] **步骤 3：执行完整审查**

逐项检查来源哈希、运行时断链、许可证、外部路径、权限边界、回收站结果、编码和过度工程；写入审查记录。

- [x] **步骤 4：运行最终验证**

```powershell
python -X utf8 -m unittest discover -s scripts -p 'test_*.py' -v
python -X utf8 scripts/validate_bundle.py
python -X utf8 scripts/check_upstream.py --json
git diff --check
git status --short
```

成功标准：全部测试通过；bundle 有效；三个升级来源均为 `current`；`mattpocock-diagnosing-bugs` 仍为 `current`；无编码和空白错误。

### 任务 6：提交并推送

**文件：** 当前全部已审查变更。

**接口：**

- 输入：任务 5 的新鲜验证证据。
- 输出：`main` 上的新提交和同步后的 `origin/main`。

- [x] **步骤 1：确认远程未领先**

运行 `git fetch origin main`，比较 `HEAD`、`origin/main` 和共同祖先；远程前进则停止，不强推。

- [x] **步骤 2：创建提交**

仅暂存已审查文件并运行 `git diff --cached --check`，提交消息使用：

```text
chore: 更新三个来源并移除 TestFX
```

- [ ] **步骤 3：推送并验证**

执行 `git push origin main`；核对本地 HEAD 与 `origin/main` 一致且工作区干净。
