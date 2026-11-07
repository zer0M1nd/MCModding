# 可复制模板

复制到任务或模块目录后填写实际内容。`待填写`、空列表、null 和 `not-run` 都是诚实的初始状态，不能机械替换成“通过”。示例 ID 不代表已有功能或产物。

| 模板 | 用途与建议位置 |
| --- | --- |
| [功能规格](FEATURE-SPEC.md) | `Docs/Projects/<模块>/SPEC.md` 或系统专题 |
| [Agent 任务](AGENT-TASK.md) | `Docs/Tasks/<task-id>/TASK.md` |
| [Bug 报告](BUG-REPORT.md) | `Docs/Tasks/<task-id>/BUGS.md` |
| [迁移变化](MIGRATION-CHANGE.md) | 模块的变化台账 |
| [设计决策](DECISION.md) | 模块设计决策目录 |
| [测试计划](TEST-PLAN.md) | `Docs/Verification/<run-id>/PLAN.md` |
| [环境与结果数据](TEST-MANIFEST.md) | 运行时填入本轮 Data 目录，不提交私密值 |
| [测试报告](TEST-REPORT.md) | `Docs/Verification/<run-id>/REPORT.md` |
| [发布说明](RELEASE-NOTES.md) | 本次交付目录或模块发布记录 |
| [交接](HANDOFF.md) | `Docs/Tasks/<task-id>/HANDOFF.md` |
| [示例 CURRENT](../Projects/ExampleMod/CURRENT.md) | 新模块状态入口 |
| [示例 SPEC](../Projects/ExampleMod/SPEC.md) | 简短模块规格入口 |

Agent 不必为极小任务创建所有文件；使用最少能清楚表达需求、实现、证据和交接的文档。共同信息引用同一真源，不复制多份状态表。
