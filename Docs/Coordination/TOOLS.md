# 协调工具使用与故障处理

提供 [claims.py](../../Tools/Coordination/claims.py) 与 [回归测试](../../Tools/Coordination/test_claims.py)。要求 Python 3.10 或更高，仅标准库，无安装、网络、外部服务或账户依赖。其他 Agent 可以直接调用；它不自动构建 Mod、不管理游戏进程，也不会强制拦截任意文件写入。

## 命令

在工作区根目录运行；资源和 owner 例子都是占位身份：

```text
python Tools/Coordination/claims.py status
python Tools/Coordination/claims.py claim --owner agent-a --task "模块功能开发" --resources module:ExampleMod Docs
python Tools/Coordination/claims.py check --owner agent-a --resources module:ExampleMod Docs
python Tools/Coordination/claims.py handoff --owner agent-a --to-owner agent-b --task "已约定的后续任务" --resources module:ExampleMod Docs
python Tools/Coordination/claims.py release --owner agent-b --resources module:ExampleMod Docs
python -m unittest discover -s Tools/Coordination -p "test_*.py" -v
```

`status` 不创建状态目录；空工作区显示空表。`check` 只读核验，不能获得认领或替代后续协作约束。重复认领自身已持有资源幂等，不覆盖原任务时间；新资源仅在全批无冲突时加入。`release` 与 `handoff` 校验整批所有权，不部分释放/转交。

handoff 需双方已约定并完成现场交接。工具不会验证接收方存在，也不能通过 owner 字符串认证身份；不要冒用他人的 owner。持有 Layout 时不可只转交部分资源造成全局锁与模块分属不同 owner。

资源名统一小写，owner 保持原字符串并精确比较。名称只作逻辑标识，不映射文件路径，也不推断自定义子资源间的关系。使用 [协作协议](../CONCURRENCY.md) 的统一资源命名，不用新的别名绕过已有认领。

所有参与者须使用相同的 `--state-dir`。独立 checkout/worktree 默认各有本地 `.coord`，因此必须显式传入共同的状态目录；只复制工具文件不能构成共享协调。状态目录默认不进入 Git。

## 输出与退出码

成功输出 JSON，包含 schema、revision、claims；状态还显示短事务元数据。失败写 stderr，业务错误为 JSON，参数错误采用 argparse 帮助。自动化必须检查退出码，不按输出含有某个词判成功。

| 退出码 | 含义 |
| --- | --- |
| 0 | 成功 |
| 1 | 文件系统错误；检查是否写入已完成，不能假定完全未发生 |
| 2 | 参数错误 |
| 3 | 认领冲突、所有权不符或交接违反全局互斥 |
| 4 | 状态损坏/不支持，拒绝重置或覆盖 |
| 5 | 短事务占用超时，没有抢锁 |

`--wait-seconds` 默认为 5，上限 60。它仅限制等待短事务的时间，**不是认领有效期**。正常状态用 UTF-8 JSON，通过独占目录串行修改、临时文件 fsync 后原子替换；不宣称具有跨机器一致性或所有硬件断电条件下的事务保证。

## 异常退出与恢复

`.coord/.transaction/process.json` 记录事务 UUID、PID 和开始时间。进程异常退出可能遗留事务目录或 `.pending-*` 文件；超时只报告忙，不自动删除。

1. 暂停新写入，读取状态及事务元数据，核对 PID、开始时间和实际进程身份；PID 存在不代表仍是同一进程，PID 不存在也不代表业务认领可全部释放。
2. 只有确认原事务进程已结束、所有参与者均停止状态修改后，指定一个协调者备份状态和残留目录，记录恢复理由。
3. 由该协调者将已核实的残留事务目录移至同一状态目录内的唯一归档名，再重新读取状态。不要在仍可能有存活事务时移动目录，也不要删除整个 `.coord`。
4. `.pending-*` 不能盲目覆盖正式 claims.json；以已提交且结构有效的正式状态为准。损坏时保留原件并依据各 owner 的确认恢复，而非清成空表。
5. 业务认领另行处理：原 owner 正常释放/交接；无法恢复 owner 时，核实该会话与其构建/游戏进程均结束，由维护者明确记录恢复决定后协调修复。没有自动抢占或 force-release 命令。

原子替换前中断保留旧表，替换后中断可能已经提交新表；因此重试前查询状态。正常工具操作不删除认领记录以外的产品文件，也不终止任何游戏进程。

## 扩展工具

可在协议契约下新增模块目录登记、构建前 check、测试实例预约或报告索引。修改协调工具和状态 schema 时先取得 Layout，全体停止旧工具写入，测试并迁移，再恢复协作。不能让不同版本工具同时解释不同状态格式。

随附测试使用系统临时目录和短生命周期 Python 子进程，不调用游戏、不读写真实认领表。跨操作系统/网络文件系统支持须在对应环境重新验证；本次已执行环境见 [整理说明](../TEMPLATE-NOTES.md)。
