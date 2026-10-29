---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask **one question** from the frontier per round and give your recommended answer. Then wait for the user's answer before recomputing the frontier and continuing.

## 每轮提问的说明要求

遵守 [主流程的提问与决策说明](../SKILL.md)。先结合完整对话核实事实，再解释本轮具体场景、当前做法、问题依据和为什么需要用户决定；必要时用具体例子说明。已确认的决定不重复询问。

选项必须说明结果差异、代价或风险，推荐必须给出理由。能查证的事实由当前实例先查证；尚未验证的假设不能包装成必须二选一的难题，也不能把可由改进实现解决的问题直接转成人工操作或限制。

每轮仍只问一个关键问题，但要提供回答所需的上下文。下面的格式是组织信息的参考，简单问题可合并为几句话，不需要机械保留所有栏目。

```
**Q1：<本轮需要决定的问题>**

背景与现状：<具体场景、目前怎样处理；必要时给出一个例子。>

已查明的情况：<已证实的问题或约束；如果还有待验证内容，明确区分。>

需要你决定：<为什么需要用户作取舍；如有选项，说清各自对结果的影响、代价或风险。>

我的建议：<推荐选项及理由。>
```

如果用户质疑问题前提或要求解释来龙去脉，先说明依据并补查；前提不成立或证据不足时修正、搁置问题，再调整决策树。不要跳过用户的疑问，也不要催促其在没有讲清楚的选项中选择。

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), use the current instance's tools to find it; don't ask the user for anything you could look up yourself. Dispatch a sub-agent only when the user explicitly authorizes it. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
