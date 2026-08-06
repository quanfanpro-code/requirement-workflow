# diagnosing-bugs 自包含集成实施计划

> **执行说明：** 用户未授权子代理，按 `executing-plans.md` 在当前会话串行执行。步骤使用复选框跟踪。

**目标：** 将 `diagnosing-bugs` 作为来源可追溯、可独立升级的本地诊断分支内置到 `requirement-workflow`，并在验证后提交、推送到 `origin/main`。

**架构：** 上游正文和伴随脚本作为运行时引用保存在 `references`；OpenAI 元数据只用于维护；主编排器在阶段 4 和阶段 5 条件触发，诊断后回到阶段 4 TDD 修复。来源、许可证、依赖图和升级入口继续使用现有 `SOURCES.json` 体系。

**技术栈：** Markdown、JSON、Python 标准库、Git/GitHub CLI、Windows PowerShell 与 Git Bash。

## 全局约束

- 运行时不得读取任何外部 Skill 目录或在线技能正文。
- 不升级现有 Matt Pocock 的其他固定子能力。
- 所有修改前先按 `requirement-workflow_yyyyMMdd_HHmmss` 命名备份目录，放入 `C:\Users\27651\BackUp\` 并校验哈希。
- 中文 Markdown、JSON 和文本保存为 UTF-8 with BOM。
- 不安装依赖、不删除文件、不启动子代理。
- 全部验证成功后提交当前已审查的相关变更并推送 `origin/main`。

---

### 任务 1：建立失败测试和上游固定快照

**文件：**

- 新建：`scripts/test_diagnosing_integration.py`
- 读取：`references/SOURCES.json`
- 读取：上游 `mattpocock/skills/skills/engineering/diagnosing-bugs`

**接口：**

- 输入：技能包根目录、`SKILL.md`、`README.md`、`SOURCES.json` 和本地引用文件。
- 输出：标准库 `unittest` 测试，分别验证运行时文件、来源登记、触发、非触发和 README 说明。

- [x] **步骤 1：备份全部待修改的现有文件**

备份 `SKILL.md`、`README.md`、`test-prompts.json`、`NOTICE`、`references/SOURCES.json`、`references/DEPENDENCY-MAP.md`、`scripts/validate_bundle.py`，并为每个文件记录源与备份 SHA-256 相等。

- [x] **步骤 2：写入失败测试**

测试必须包含以下断言：

```python
self.assertTrue((references / "diagnosing-bugs.md").is_file())
self.assertTrue((references / "diagnosing-bugs/scripts/hitl-loop.template.sh").is_file())
self.assertTrue((references / "upstream-metadata/mattpocock/diagnosing-bugs/openai.yaml").is_file())
self.assertIn("mattpocock-diagnosing-bugs", source_ids)
self.assertIn("references/diagnosing-bugs.md", skill_text)
self.assertIn("正常的 TDD", skill_text)
self.assertIn("不触发", skill_text)
self.assertIn("diagnosing-bugs", readme_text)
```

测试还要验证新来源的 `repository`、`commit`、`source_tree_sha256`、`source_paths`、`tracked_local_paths` 和 `local_adaptations` 均符合现有 Schema。

- [x] **步骤 3：运行测试确认红灯**

运行：

```powershell
python -X utf8 -m unittest scripts.test_diagnosing_integration -v
```

预期：因 `references/diagnosing-bugs.md` 和来源条目尚不存在而失败，失败原因与目标行为一致。

- [x] **步骤 4：重新核验上游并固定快照**

使用 GitHub CLI 读取 `main` 当前提交，在系统临时目录获取该提交；确认来源路径包含 `SKILL.md`、`agents/openai.yaml`、`scripts/hitl-loop.template.sh`。通过对固定提交的来源目录生成确定性归档并计算 SHA-256，记录提交号和来源树哈希。

### 任务 2：内置运行时引用和来源元数据

**文件：**

- 新建：`references/diagnosing-bugs.md`
- 新建：`references/diagnosing-bugs/scripts/hitl-loop.template.sh`
- 新建：`references/upstream-metadata/mattpocock/diagnosing-bugs/openai.yaml`
- 修改：`references/SOURCES.json`
- 修改：`references/DEPENDENCY-MAP.md`
- 修改：`NOTICE`

**接口：**

- 输入：任务 1 固定的上游提交和来源树哈希。
- 输出：独立来源 ID `mattpocock-diagnosing-bugs` 和完整本地引用闭包。

- [x] **步骤 1：复制固定上游内容**

正文保持上游内容；脚本保持 `scripts/hitl-loop.template.sh` 相对路径；OpenAI 元数据存入 `upstream-metadata`，不列入运行时入口。

- [x] **步骤 2：新增独立来源条目**

按现有 Schema 写入：

```json
{
  "id": "mattpocock-diagnosing-bugs",
  "repository": "mattpocock/skills",
  "url": "https://github.com/mattpocock/skills",
  "branch": "main",
  "commit": "6acc160e4e0cd062dbbbd7a1b26ae92855edf07e",
  "license": "MIT",
  "source_tree_sha256": "dff8cc167215259536e5a1828d772e2125c28a1886c9eb3ab826c4312a87a6dd",
  "source_paths": ["skills/engineering/diagnosing-bugs", "LICENSE"],
  "tracked_local_paths": [
    "diagnosing-bugs.md",
    "diagnosing-bugs/**",
    "upstream-metadata/mattpocock/diagnosing-bugs/**"
  ],
  "local_adaptations": [
    "作为主流程的条件诊断分支，而不是独立运行时 Skill",
    "诊断完成后回到阶段 4 按 TDD 修复并验证",
    "保留 HITL 脚本的本地相对路径和脱敏规则"
  ]
}
```

同时把原 `mattpocock-skills` 的 `upstream-metadata/mattpocock/**` 改成四个现有子目录的明确跟踪路径，避免来源归属重叠。

- [x] **步骤 3：更新依赖图和许可证声明**

在阶段 4、阶段 5表格中登记触发和返回关系；在上游来源表及 NOTICE 的 Matt Pocock 项目说明中加入 `diagnosing-bugs`。复用现有 Matt MIT 许可证文件，不复制第二份。

- [x] **步骤 4：运行定向测试**

运行 `python -X utf8 -m unittest scripts.test_diagnosing_integration -v`。预期：文件和来源测试通过；主流程与 README 测试仍失败。

### 任务 3：接入阶段 4、阶段 5 与完整性校验

**文件：**

- 修改：`SKILL.md`
- 修改：`scripts/validate_bundle.py`
- 修改：`test-prompts.json`

**接口：**

- 输入：任务 2 的本地入口 `references/diagnosing-bugs.md`。
- 输出：阶段 4/5 条件触发、返回规则和可自动验证的强制字面量。

- [x] **步骤 1：接入阶段 4**

增加按需读取入口和触发条件：无法立即解释的测试、构建、运行或性能失败；一次针对性修复后仍复现；跨环境差异或依赖日志、HAR、截图、性能基线。诊断完成后回到当前 TDD 任务的 VERIFY。

- [x] **步骤 2：接入阶段 5**

验收发现缺陷且根因不明时读取诊断引用；根因明确后回到阶段 4 TDD 修复，再重新执行阶段 5。

- [x] **步骤 3：明确非触发条件**

正常 TDD 红灯、明显拼写、缺文件和普通配置错误直接在当前步骤处理；需求或设计不成立则回退相应阶段。

- [x] **步骤 4：强化校验器**

把 `diagnosing-bugs.md` 加入 `runtime_entry_files`；在 `check_orchestrator_policy` 的必要字面量中加入本地入口、触发和非触发规则。文件缺失、链接越界、来源未登记或外部路径出现时必须使 `BUNDLE_VALID=False`。

- [x] **步骤 5：增加行为测试提示**

在 `test-prompts.json` 增加两项：疑难跨环境失败应进入诊断分支；正常 TDD 首次红灯不得进入诊断分支。

- [x] **步骤 6：运行测试和 bundle 校验**

```powershell
python -X utf8 -m unittest scripts.test_diagnosing_integration -v
python -X utf8 scripts/validate_bundle.py
```

预期：全部 unittest 通过，且输出 `EXTERNAL_RUNTIME_DEPENDENCIES=0`、`BUNDLE_VALID=True`。

### 任务 4：同步 README、审查和上游检查

**文件：**

- 修改：`README.md`
- 新建：`docs/reviews/2026-08-06-diagnosing-bugs-integration-review.md`

**接口：**

- 输入：已实现的条件触发和来源体系。
- 输出：面向普通用户的说明、完整审查证据和可独立升级入口。

- [x] **步骤 1：更新 README**

用大白话说明：自动排错分支解决什么问题、何时进入、何时不进入、排错后回到哪里、为什么无需安装外部 Skill，以及通过 `SOURCES.json` 和 `check_upstream.py` 查看来源及更新。

- [x] **步骤 2：验证上游枚举**

运行：

```powershell
python -X utf8 scripts/check_upstream.py --json
```

预期：输出中包含唯一来源 ID `mattpocock-diagnosing-bugs`。如果仓库在实施期间出现新提交，可以报告 `update_available`，但不得静默改换已固定内容。

- [x] **步骤 3：执行完整审查**

逐项对照需求、设计和计划；检查外部依赖、路径闭包、许可证、编码、敏感信息规则、触发边界和过度工程。将发现、修复、验证命令及残余风险写入审查报告。

- [x] **步骤 4：运行最终验证**

```powershell
python -X utf8 -m unittest scripts.test_diagnosing_integration -v
python -X utf8 scripts/validate_bundle.py
python -X utf8 scripts/check_upstream.py --json
git diff --check
git status --short
```

成功标准：测试零失败、bundle 有效、来源可枚举、Git diff 无空白错误，所有变更均属于已审查范围。

### 任务 5：提交并推送

**文件：** 当前全部已审查变更。

**接口：**

- 输入：任务 4 的新鲜验证证据。
- 输出：`main` 上的本地提交和同步后的 `origin/main`。

- [x] **步骤 1：确认远程未领先**

运行 `git fetch origin main`，比较 `HEAD`、`origin/main` 和共同祖先；若远程出现新提交，停止并先整合，不强推。

- [ ] **步骤 2：创建提交**

仅暂存已审查文件，检查 staged diff 后提交，建议消息：

```text
feat: 内置 diagnosing-bugs 诊断分支
```

- [ ] **步骤 3：推送并验证**

执行 `git push origin main`，再核对本地 HEAD 与远程 `origin/main` 一致；不创建 PR，不强推，不清理其他工作区。
