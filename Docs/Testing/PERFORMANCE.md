# 性能验证

先明确症状：客户端帧卡顿、逻辑 tick 过长、启动慢、内存持续增长、查询过多或磁盘阻塞。客户端 FPS、帧耗时与服务端 TPS/MSPT 是不同指标；不能相互替代。

## 使用 spark

按 [安装说明](https://spark.lucko.me/docs/Installation)选择兼容目标版本与加载器的包，记录安装侧、版本和 SHA，避免重复 modid。只装到本轮隔离实例。按 [命令文档](https://spark.lucko.me/docs/Command-Usage)及当前版本帮助核对参数。

常用命令参考：

```text
/spark profiler start
/spark profiler info
/spark profiler stop --save-to-file

/sparkc profiler start --thread *
/sparkc profiler info
/sparkc profiler stop --save-to-file
```

`/sparkc` 属于客户端命令；若自动化命令直接发往服务端，改用真实聊天框输入。确认 profiler 状态及最终本地文件，而非只确认命令已发送。尽量本地保存，向外部分析页面上传日志/profile 前核对当前授权和内容。

## 实验设计

1. 固定世界、模组版本、配置、操作、视距、分辨率和采样时长；记录候选与基线哈希。
2. 先预热，再分别记录空闲和问题操作。典型操作采样可取 30–60 秒，长期泄漏需更长且另有设计。
3. 比较相同条件下的重复结果，报告耗时分布、长暂停、内存/GC 和热点调用栈。采样不足时写“初步观察”。
4. 必要时用临时计数器记录查询次数、缓存命中/失效和重建次数；次数本身不是耗时结论。
5. 保存本地 profile、命令、时段、操作次数及实际用户体验证据。性能探针和录像有开销，必要时做不录制/移除探针对照。

采样后端或分配分析不支持时，记录限制，使用兼容的 Java sampler 或 JFR。不要把无法采样记成性能通过，也不要将高开销 heap dump 变成每轮必跑项目。

同一 JVM 中集成逻辑与客户端采样可能竞争；不能并行时依次进行。发现实体“停住再追赶”，先用同一时间基准比较权威状态、客户端 tick、帧耗时及多个实体，避免把整个客户端暂停误判为某一实体同步错误。
