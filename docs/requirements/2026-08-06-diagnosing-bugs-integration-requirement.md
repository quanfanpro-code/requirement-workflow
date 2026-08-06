# diagnosing-bugs 自包含集成需求

## 背景与问题

`requirement-workflow` 已具备六阶段流程、TDD、审查和验证规则，但遇到难以立即解释的测试、构建、运行或性能故障时，没有一套完整的“复现—最小化—假设—探针—修复—回归”诊断分支。外部 `diagnosing-bugs` 已提供这套方法，但当前执行契约禁止运行时读取其他 Skill 目录，因此不能直接调用外部版本。

## 用户与使用场景

维护者希望把 `diagnosing-bugs` 作为 `requirement-workflow` 的内置子能力：仅在阶段 4 或阶段 5 遇到疑难故障时自动进入，诊断完成后回到原阶段继续 TDD 修复或验收。技能包复制到其他电脑后仍应独立运行，不依赖外部 Skill 是否安装。

## 功能范围

- 内置 `diagnosing-bugs` 的完整运行正文和 HITL 脚本。
- 保留上游 `agents/openai.yaml` 作为非运行时维护元数据。
- 在阶段 4、阶段 5 增加条件触发和返回规则，不改变六阶段主顺序。
- 在 `SOURCES.json` 中建立独立来源条目，记录仓库、URL、分支、固定提交、许可证、来源路径、来源树哈希、本地路径和本地适配。
- 在 `DEPENDENCY-MAP.md`、`NOTICE`、README 和校验规则中登记该子能力。
- 让上游检查脚本能够独立报告该来源是否有更新。

## 明确不做的内容

- 不在每次普通测试失败时启动疑难诊断。
- 不允许运行时读取 `D:\BaiduSyncdisk\workbuddy skills\diagnosing-bugs` 或任何外部 Skill 目录。
- 不升级或改写现有 Matt Pocock 的 grill、domain-modeling 等其他固定来源。
- 不安装新依赖，不创建 PR；完成全部验证后，更新 README、创建本地提交并推送到当前 `origin/main`。

## 触发边界

满足以下任一条件时读取内置 `references/diagnosing-bugs.md`：

1. 测试、构建、运行或性能失败无法由当前证据立即解释；
2. 同一失败经过一次针对性修复后仍复现；
3. 不同环境表现不一致，或需要日志、HAR、截图、性能基线等证据定位；
4. 阶段 5 发现缺陷，但根因尚不明确。

明显的拼写、缺文件、普通配置错误，以及正常的 TDD 红灯不触发。需求或设计不成立时回退相应阶段，不能用诊断流程代替需求澄清。

## 约束与风险

- 上游仓库为 `mattpocock/skills`，来源路径为 `skills/engineering/diagnosing-bugs`，许可证为 MIT。
- 2026-08-06 核验时，仓库 `main` 为 `6acc160e4e0cd062dbbbd7a1b26ae92855edf07e`；该路径最近内容提交为 `bda79a3c3ca23d19d9ca483808580b5b4cc3d8e2`。
- 新来源条目应与现有 `mattpocock-skills` 条目分离，避免升级该子能力时误改其他固定版本。
- 所有中文文件采用 UTF-8 with BOM；修改前必须备份到 `C:\Users\27651\BackUp\` 并校验。
- 脱敏规则必须保留，日志、命令和捕获物展示前不得泄露凭证。

## 验收标准

1. 运行时入口和所有伴随文件都位于 `requirement-workflow` 内部。
2. `SOURCES.json` 能单独追溯 `diagnosing-bugs` 的固定快照和本地适配。
3. `DEPENDENCY-MAP.md` 能看出触发阶段、伴随脚本和返回路径。
4. `validate_bundle.py` 能发现正文、脚本、来源登记或触发入口缺失。
5. `check_upstream.py` 能单独输出该来源的更新状态。
6. 正常、边界和错误场景测试覆盖“应触发、不得触发、缺文件即失败”。
7. 最终校验结果保持 `EXTERNAL_RUNTIME_DEPENDENCIES=0` 和 `BUNDLE_VALID=True`。
8. README 用大白话说明自动诊断分支、触发边界、自包含来源和升级入口。
9. 最终提交只包含已审查的 `requirement-workflow` 变更，并成功同步到 `origin/main`。

## 调研摘要与来源

- 本地项目：`SKILL.md`、`references/SOURCES.json`、`references/DEPENDENCY-MAP.md`、`NOTICE`、README、校验及更新脚本。
- 上游项目：`mattpocock/skills` 的 `skills/engineering/diagnosing-bugs`，包含 `SKILL.md`、`agents/openai.yaml`、`scripts/hitl-loop.template.sh`。
- 当前外部 Skill 仅用于维护核验；完成集成后不构成运行时依赖。

## 待确认项

- 推荐采用“独立来源条目 + 完整本地快照 + 条件触发”的方案，而不是把它并入现有 Matt 综合来源条目，也不只摘录几段规则。
- 用户已授权完成后创建提交并推送到 `origin/main`；推送前仍须核对并审查仓库中已有的未提交改动。
