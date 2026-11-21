[English](README.md) | 简体中文

# Minecraft Mod 开发起步仓库

这是一个用于开发 Minecraft Java 版 Mod 的起步仓库，内置多份可供 Agent 使用的文档，涵盖项目配置、开发流程、测试验收和多 Agent 协作。Agent 可以从 [AGENTS.md](AGENTS.md) 和[新会话入口](Docs/START-HERE.md) 开始阅读。

文档以 **Minecraft 1.20.1 / Forge / Java 17** 为示例。使用其他版本或加载器时，请核对对应的 API、映射、构建和测试工具。

工作区还随附 Git 忽略规则和一套可直接使用的[多 Agent 协调工具](Docs/Coordination/TOOLS.md)。Mod 源码、Gradle 工程和游戏测试工具需按实际项目自行准备。除明确随附的协调工具外，文档中的命令与协议片段供参考。`ExampleMod` 仅提供模块文档示例。

## 开始使用

1. 让 Agent 读取根目录 [AGENTS.md](AGENTS.md) 与 [新会话入口](Docs/START-HERE.md)。
2. 在 [项目配置](Docs/PROJECT-CONFIG.md) 填写目标、modid、技术版本、兼容边界及本次允许执行的验证；未指定的普通流程采用文档默认值。
3. 将 [示例模块](Docs/Projects/ExampleMod/CURRENT.md) 和 [模块会话入口](Sessions/ExampleMod/AGENTS.md) 改为实际模块。业务源码以后放 `Code/<模块>/`，说明仍放 `Docs/Projects/<模块>/`。
4. 依据 [开发流程](Docs/DEVELOPMENT.md) 开始工作。多 Agent 写入前先执行 [协作协议](Docs/CONCURRENCY.md)：有可用工具优先使用工具，没有工具才串行手动协调；也可按协议自行编写工具。

可将这段话交给新 Agent：

> 先读 AGENTS.md 和 Docs/START-HERE.md，检查项目配置、当前状态与资源认领。依据当前需求完成一个完整功能系统，按影响范围验证，记录证据和未完成项。不要把模板或历史记录当作当前实现事实。

## 阅读导航

| 要做的事 | 入口 |
| --- | --- |
| 理解目录、权限与工作方式 | [工作区约定](Docs/WORKSPACE-RULES.md) |
| 定义需求、实现、调试、交付 | [开发流程](Docs/DEVELOPMENT.md) |
| 判断 Bug、建议、迁移差异 | [Bug 判定](Docs/BUG-POLICY.md) |
| 从旧版迁移到新版 | [移植目标与方法](Docs/PORTING.md) |
| 选择三种测试与证据 | [测试规范](Docs/TESTING.md) |
| 操作真实客户端 | [MC Pilot 与客户端工具](Docs/Testing/CLIENT-TOOLS.md) |
| 执行游戏逻辑断言 | [GameTest 与临时测试代码](Docs/Testing/GAME-TEST.md) |
| 分析卡顿与性能 | [性能测试](Docs/Testing/PERFORMANCE.md) |
| 协调多 Agent | [协作协议](Docs/CONCURRENCY.md) · [认领表](Docs/Coordination/CLAIMS.md) |
| 选择版本号与准备发布 | [版本协议](Docs/VERSIONING.md) · [交付规范](Docs/RELEASE.md) |
| 制作材质、模型、GUI | [视觉资源](Docs/VISUAL-ASSETS.md) |
| 查通用开发经验 | [常见陷阱](Docs/PITFALLS.md) |
| 查官方资料 | [参考链接](Docs/REFERENCES.md) |
| 记录和交接 | [模板索引](Docs/Templates/INDEX.md) · [知识维护](Docs/KNOWLEDGE-MAINTENANCE.md) |

本模板不包含私人账号、设备配置、内网地址、聊天记录或第三方受限资源，也不提供远程服务器运维、自动部署或群聊接入功能。测试中的“服务端”仅指本地隔离游戏逻辑环境。模板来源和整理边界见 [整理说明](Docs/TEMPLATE-NOTES.md)。
