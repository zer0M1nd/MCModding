English | [简体中文](README.zh-CN.md)

# Minecraft Mod Development Starter Repository

This is a starter repository for developing Minecraft Java Edition mods. It includes documentation that AI agents and maintainers can use to set up a project, follow development and testing workflows, and coordinate work across agents. Start with [AGENTS.md](AGENTS.md) and the [new session guide](Docs/START-HERE.md).

The documentation uses **Minecraft 1.20.1 / Forge / Java 17** as an example. If you choose a different version or mod loader, check the relevant APIs, mappings, build setup, and testing tools.

The workspace also includes Git ignore rules and a ready-to-use [multi-agent coordination tool](Docs/Coordination/TOOLS.md). Set up mod source code, a Gradle project, and game testing tools for your own project. The documentation's commands and protocol snippets serve as references, with the coordination tool included for direct use. `ExampleMod` is a documentation example.

## Getting started

1. Have your agent read the root [AGENTS.md](AGENTS.md) and the [new session guide](Docs/START-HERE.md).
2. In [Project configuration](Docs/PROJECT-CONFIG.md), record your project goals, mod ID, platform versions, compatibility requirements, and the verification you authorize. Use the documented defaults for routine work where no preference is specified.
3. Adapt the [example module](Docs/Projects/ExampleMod/CURRENT.md) and its [session entry point](Sessions/ExampleMod/AGENTS.md) to your project. Put your mod code in `Code/<module>/` and its documentation in `Docs/Projects/<module>/`.
4. Follow the [development workflow](Docs/DEVELOPMENT.md). When multiple agents are working together, follow the [coordination protocol](Docs/CONCURRENCY.md) before writing files. Use the available tools to claim resources, or coordinate claims one at a time if tooling is unavailable. You can also implement your own tool following the protocol.

You can give a new agent the following prompt.

> Read AGENTS.md and Docs/START-HERE.md first, then check the project configuration, current state, and resource claims. Implement one complete feature based on the current requirements, verify the affected behavior, and record the evidence and any remaining work. Check the current implementation before relying on templates or historical records.

## Documentation

The linked guides are written in Chinese.

| Task | Guide |
| --- | --- |
| Understand the directory layout, permissions, and working conventions | [Workspace rules](Docs/WORKSPACE-RULES.md) |
| Define, implement, debug, and deliver features | [Development workflow](Docs/DEVELOPMENT.md) |
| Classify bugs, suggestions, and differences introduced by porting | [Bug policy](Docs/BUG-POLICY.md) |
| Port a mod from an older version | [Porting goals and practices](Docs/PORTING.md) |
| Choose tests and collect evidence | [Testing guide](Docs/TESTING.md) |
| Operate a real client | [MC Pilot and client tools](Docs/Testing/CLIENT-TOOLS.md) |
| Check game logic | [GameTest and temporary test code](Docs/Testing/GAME-TEST.md) |
| Investigate lag and performance | [Performance testing](Docs/Testing/PERFORMANCE.md) |
| Coordinate multiple agents | [Coordination protocol](Docs/CONCURRENCY.md) · [Resource claims](Docs/Coordination/CLAIMS.md) |
| Choose version numbers and prepare releases | [Versioning](Docs/VERSIONING.md) · [Release guide](Docs/RELEASE.md) |
| Create textures, models, and GUIs | [Visual assets](Docs/VISUAL-ASSETS.md) |
| Look up common development pitfalls | [Common pitfalls](Docs/PITFALLS.md) |
| Find official resources | [References](Docs/REFERENCES.md) |
| Record decisions and hand off work | [Template index](Docs/Templates/INDEX.md) · [Knowledge maintenance](Docs/KNOWLEDGE-MAINTENANCE.md) |

The template keeps private account details, device settings, internal network addresses, chat logs, and restricted third-party material out of the repository. Its scope covers development and isolated local testing, including server-side game logic. See the [template notes](Docs/TEMPLATE-NOTES.md) for its origins and scope.
