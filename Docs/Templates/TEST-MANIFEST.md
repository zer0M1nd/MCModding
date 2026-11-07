# 测试环境与结果数据模板

下列 JSON 是未执行示例，可复制到 `Data/Verification/<run-id>/` 后填写。null 表示尚未核实，不是默认成功。对外分享前去除设备绝对路径、账户、地址及原始日志中的私人信息。

## manifest.json

```json
{
  "schemaVersion": 1,
  "runId": "replace-with-run-id",
  "source": {"commit": null, "workingTreeSummary": null},
  "runtime": {"minecraft": null, "loader": null, "loaderVersion": null, "java": null},
  "artifacts": [],
  "testTools": [],
  "configDigests": {},
  "dataPacks": [],
  "resourcePacks": [],
  "world": {"seed": null, "seedEvidence": null, "lifecycle": null},
  "graphics": {"renderer": null, "shaderPack": null, "settings": null},
  "commands": [],
  "userRestrictions": [],
  "startedAt": null,
  "finishedAt": null
}
```

`artifacts` 与 `testTools` 分开：每项记录 modid/name、版本、SHA-256、来源及加载侧。用户未允许分享的机器信息只在本地保存。世界种子和配置从本轮真实环境核对，不沿用脚本的默认常量。

## results.json 中的单用例

```json
{
  "id": "example.system.scenario",
  "artifactSha256": null,
  "environment": null,
  "driver": null,
  "expected": "replace-with-observable-behavior",
  "actual": null,
  "coverage": [],
  "status": "not-run",
  "evidence": [],
  "visualReviewed": false,
  "reason": "template only",
  "reusedFrom": null
}
```

coverage 只填实际获得的 `unit / server-logic / dedicated-runtime / client-input / client-sync / client-visual / client-audio / persistence / performance`。联合场景可以多标签，但测试计数不因此翻倍。

状态为 `pass / fail / blocked / not-run / deferred-by-user / not-applicable`。用例应包含来源日志范围/请求 ID，防止读到旧 PASS。截图证据还需记录看过哪些画面或片段；仅字段为 true 不能替代审阅记录。
