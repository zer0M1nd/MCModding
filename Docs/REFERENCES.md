# 常用公开资料

先选 **Minecraft 版本 + 加载器 + 精确依赖版本 + 映射体系**，再读文档和源码。以下是公开入口，不是全部项目都应安装的依赖清单。链接指向版本选择页时切到实际目标版本；不要将 latest 文档直接用于旧版本。

## 平台与工程

| 资料 | 用途 |
| --- | --- |
| [Forge 1.20.1 文档](https://docs.minecraftforge.net/en/1.20.1/) | 默认示例的平台入口，注册、侧别、数据、网络、资源等 |
| [Forge 入门](https://docs.minecraftforge.net/en/1.20.1/gettingstarted/) | MDK、JDK 和工程配置 |
| [Forge 逻辑侧/物理侧](https://docs.minecraftforge.net/en/1.20.1/concepts/sides/) | 避免客户端类误加载，分清集成环境两侧 |
| [Forge 注册表](https://docs.minecraftforge.net/en/1.20.1/concepts/registries/) | 注册时机、ID 与扩展 |
| [Forge 网络](https://docs.minecraftforge.net/en/1.20.1/networking/simpleimpl/) | 消息处理、线程与数据校验 |
| [Forge 能力](https://docs.minecraftforge.net/en/1.20.1/datastorage/capabilities/) | 库存/能量等接口、生命周期 |
| [Forge 数据生成](https://docs.minecraftforge.net/en/1.20.1/datagen/) | 生成资源与 provider |
| [MinecraftForge 源码](https://github.com/MinecraftForge/MinecraftForge) | 固定分支/标签/提交后核对真实实现 |
| [NeoForge 文档](https://docs.neoforged.net/) | NeoForge 项目与版本迁移入口，不与 Forge 混用 |
| [Fabric 开发文档](https://docs.fabricmc.net/develop/) | Fabric 项目入口，切换目标版本 |
| [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html) | 固定构建版本；实际工程用对应版本文档 |
| [JUnit 5 指南](https://docs.junit.org/5.11.0/user-guide/) | 一份固定版本的单元测试参考，依赖版本另行选择 |

## 游戏测试与诊断

| 资料 | 用途 |
| --- | --- |
| [Forge GameTest](https://docs.minecraftforge.net/en/1.20.x/misc/gametest/) | 世界逻辑测试、注册和结构模板 |
| [Forge 1.20.1 GameTest 启用源码](https://github.com/MinecraftForge/MinecraftForge/blob/1.20.1/src/main/java/net/minecraftforge/gametest/ForgeGameTestHooks.java) | 核对开发/production 条件 |
| [MC Pilot](https://github.com/kzheart/mc-pilot) · [固定 v0.20.0](https://github.com/kzheart/mc-pilot/releases/tag/v0.20.0) | 真实客户端驱动；历史可参考基线，非最新版声明 |
| [MC Pilot actions](https://github.com/kzheart/mc-pilot/blob/v0.20.0/protocol/actions.json) · [queries](https://github.com/kzheart/mc-pilot/blob/v0.20.0/protocol/queries.json) | 固定版协议，还需查看 handler 判断实际支持 |
| [spark 安装](https://spark.lucko.me/docs/Installation) · [命令](https://spark.lucko.me/docs/Command-Usage) | 兼容包与本地性能采样 |
| [FFmpeg 文档](https://ffmpeg.org/documentation.html) | 录像解码、帧数、时长及抽帧检查 |

## 视觉与可选联动参考

| 资料 | 用途 |
| --- | --- |
| [Aseprite 文档](https://www.aseprite.org/docs/) · [脚本 API](https://www.aseprite.org/api/) | 像素编辑、动画、CLI/Lua |
| [Blockbench Wiki](https://www.blockbench.net/wiki/) | 模型格式、UV 和编辑方法 |
| [Curios 文档](https://docs.illusivesoulworks.com/) | 饰品类联动；选择目标 MC 版本 |
| [JEI 源码与 Wiki](https://github.com/mezz/JustEnoughItems) | 配方展示/转移 API；查看精确版本分支 |
| [Create 源码](https://github.com/Creators-of-Create/Create) | 机械/加工/结构联动；大版本 API 差异要单独适配 |
| [Applied Energistics 2 源码](https://github.com/AppliedEnergistics/Applied-Energistics-2) | 存储与网络联动接口；核对实际 API 契约 |
| [Git 文档](https://git-scm.com/docs) | 差分、提交、worktree；不能代替项目单写入者协议 |

## 引用与版本记录

记录每项采用资料的 URL、版本/提交、用途与查看日期。官方文档说明意图，目标依赖源码说明真实签名与实现；玩家 Wiki 可解释体验，不独自决定 API 或完整还原范围。

本文整理时抽查了平台、测试和美术主要入口；未证明每个链接永久有效、每个依赖可在目标整合环境运行。链接失效时从官方主页找同版本资料，不擅自更改项目依赖。精确工具版本说明与实机结果分开记录。
