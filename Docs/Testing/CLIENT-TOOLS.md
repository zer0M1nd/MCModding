# 真实客户端测试：MC Pilot 优先

## 识别工具与固定版本

采用 [kzheart/mc-pilot](https://github.com/kzheart/mc-pilot)，CLI 为 `mct`，npm 包为 `@kzheart_/mc-pilot`，通过控制 Mod 与真实客户端通信。模板不包含该工具，也没有自动安装器。

来自既有流程的可参考基线是 [v0.20.0](https://github.com/kzheart/mc-pilot/releases/tag/v0.20.0)：CLI 0.20.0，发行包中的 Mod 标识为 `mct`、版本为 0.10.0，Forge 1.20.1 文件为 `mct-client-mod-forge-1.20.1.jar`。这是历史兼容基线，**不是“当前最新版”推荐或本模板的实机验收**。采用其他版本时重新核对元数据和协议。

安装前确认 Minecraft、Loader、JDK、Node、CLI、控制 Mod 六者匹配，下载指定 release 而非不透明的 latest，计算实际 SHA。对既有实例升级 CLI 不等于升级控制 Mod；按 modid 检查重复 JAR。客户端控制 Mod 不放进专服。

## 首次接入步骤

1. 准备本轮隔离客户端与目标产品/依赖；核对 `gameDir`、native、日志、配置和输出路径。保持目标 Loader 版本，不为自动建实例工具降级。
2. 查看固定版本 CLI 帮助/`mct schema`、[actions](https://github.com/kzheart/mc-pilot/blob/v0.20.0/protocol/actions.json)、[queries](https://github.com/kzheart/mc-pilot/blob/v0.20.0/protocol/queries.json)及相应 handler；不能从函数名猜参数或能力。
3. 使用工具自己的实例管理，或接入已启动的隔离客户端。直接接入需按该版协议实现请求驱动；本模板不提供驱动脚本，不假设有通用 `attach` 或 Java `eval`。
4. 在启动 Java 前设置该版本支持的控制端口环境变量；上述基线使用 `MCT_CLIENT_WS_PORT`，连接本机 WebSocket。每客户端端口独立且确认空闲，不结束其他进程来腾端口。
5. 启动后查询世界状态，确认玩家身份与维度，执行 [测试规范](../TESTING.md) 的容器往返自检并查看真实截图。CLI 的 ready 状态不替代业务自检。

固定基线的直接请求形状示意：

```json
{"id":"unique-request-id","action":"status.all","params":{},"timeoutMs":30000}
```

响应须核对对应 id、成功/失败字段及返回数据。实际 action/参数以所用版本为准。发送成功不代表动作完成，动作完成也不代表业务正确。请求超时后先读取状态，不盲目重复非幂等动作。

## 选择正确的输入层

| 目标 | 合适接口/方法 | 限制 |
| --- | --- | --- |
| 确认进世界、物品、菜单 | `status.all`、`inventory.get`、`gui.snapshot`、`gui.layout` | 接口结果只是被查询侧的状态 |
| 普通方块/槽位交互 | `look.at`、`block.interact`、`gui.click`，使用实际坐标和 slot ID | 直接调用交互可能绕过鼠标命中，不足以验证鼠标问题 |
| 按钮、拖动、键盘焦点 | `input.click/drag/scroll`、按键/文本输入 | 要用实际 Screen 路径；完成后释放所有按键 |
| 截图与动画 | `capture.screenshot` 或该版 CLI 截图/录制 | 打开画面审阅；动画需多个时刻，不能仅有文件 |
| 专有 GUI/缓存 | 独立客户端观测桥接，或实际输入 | 不借桥接直接设置“正确状态” |
| 无接口/旧版对照 | 电脑操作工具 | 使用当前工具技能，不假定旧 MC 支持现代控制 JAR |

GUI 坐标与截图像素不同。读取 `screen.size` 和 layout 后换算：GUI 坐标 = framebuffer 坐标 × GUI 尺寸 ÷ framebuffer 尺寸；有窗口偏移、裁剪或缩放时进一步校正。普通容器优先实际 slot ID，自定义按钮必须根据当前布局操作。

## 必须检查的客户端行为

- 真实进入世界、打开与关闭界面、正确输入焦点、搜索/滚动/拖动、快捷移动、副手与快捷栏交换。
- 物品在物品栏、手持、地面、展示框等所声明场景；方块各面、旋转、邻接、上下方向和透明遮挡。
- 粒子、动画、多帧时序、明暗背景、远近距离、相机旋转、第一/第三人称。
- 配方浏览器/手册与真实消耗输出一致；NBT/物品数据不同的预览不能误用旧缓存。
- 资源重载、切维度、断线重连、保存重开后的菜单和特效清理。
- 有渲染兼容需求时分别测试无优化 Mod、装加载器但关光影、开启代表性光影包。每个结果绑定精确包版本和设置。

旧版对照只在判定还原目标确有需要时进行，尽量统一场景、视角、时间和缩放。普通缺图检查无需每次重开旧版。

## 既有流程中的工具陷阱

这些是上述固定基线的历史实现检查结果；升级后重新核对，不能推广到所有版本：

- CLI 的 1.20.1 Forge 自动实例目录曾固定为 47.3.0，不支持任意 `--forge-version`。自动下载默认 release 与 CLI 版本也曾不一致；显式核对 `MCT_MOD_RELEASE_TAG` 和实际 JAR。
- `channel.send/listen`、`effects.sounds/particles` 曾存在未实现占位；空响应不能证明没有粒子或声音。
- 普通槽位接口未必覆盖自定义 Screen。输入可能调用窗口/GLFW，不能承诺绝不影响用户焦点。
- CLI 管理的实例和手工启动实例生命周期不同；不能对手工启动实例随意套用 CLI wait/stop。
- 某些命令发送接口直达逻辑服务端，可能绕过客户端命令处理。`/sparkc` 等需走真实聊天输入并查看反馈。
- 旧 Minecraft 版本不在支持列表时不能拿其他版本控制 JAR 代替。Node 的 CLI 最低要求与直接使用内建 WebSocket 的最低要求也可能不同。

默认静音减少干扰；音效验收需要在允许的范围内开启声音并实际观察/听取结果。录像要确认正常结束、帧数、时长和可解码性；若只是抽帧审阅，报告不能写成完整逐帧观看。
