# ExampleMod 会话入口

先显式读取工作区根 [AGENTS](../../AGENTS.md)，再读 [START-HERE](../../Docs/START-HERE.md)、[工作区约定](../../Docs/WORKSPACE-RULES.md)、[项目配置](../../Docs/PROJECT-CONFIG.md)、[当前全局状态](../../Docs/CURRENT-STATE.md) 和 [模块 CURRENT](../../Docs/Projects/ExampleMod/CURRENT.md)。不能假定 Agent 客户端会跨嵌套 Git 仓库自动加载外层规则。

模块源码将位于工作区根的 `Code/ExampleMod/`，文档位于 `Docs/Projects/ExampleMod/`；当前没有实际代码工程。改名时同步这些路径与根项目配置。

修改、生成、构建或测试前，按 [协作协议](../../Docs/CONCURRENCY.md) 优先调用可用工具认领 `module:ExampleMod` 及其他全部相关资源。共享报告/规范需要 Docs；本轮实例需要唯一 test 资源。只有没有工具时才手动串行协调。

工具命令在工作区根执行，模块 Git/Gradle 命令在真实代码位置执行。不要在 Sessions 中建立第二份源码、缓存或游戏目录。
