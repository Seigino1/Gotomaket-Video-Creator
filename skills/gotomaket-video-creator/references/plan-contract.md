# 统一计划契约

`plan.json` 是每支视频的时间和内容唯一来源。版本 1 使用整数帧：秒数 = 帧数 / fps；镜头严格连续，转场在镜头内部实现，不用重叠镜头绕过校验。

| 字段 | 说明 |
|---|---|
| schemaVersion / demo / engine | 1；技术样片=true，完成调研后=false；remotion 或 hyperframes |
| product / inputSources / scope | 产品名、来源列表、版本与平台范围 |
| width / height / fps / durationFrames | 正整数，H.264 尺寸为偶数，镜头覆盖全片 |
| languages | 任意合法语言标签，如 zh-CN、en-US、ja-JP |
| theme | background、text、accent、fontFamily；本地字体见声音/语言参考 |
| evidence | id、claim、source、status；状态为 official-claim / code-implemented / runtime-verified |
| assets | id、kind（image/video/audio/font）、file、source、license；file 在 public/ 内 |
| shots | id、type、startFrame、durationFrames、title/body/narration、claimIds、assetId |
| captions | 每语言数组：startFrame、endFrame（不包含该帧）、text；不允许越界或重叠 |
| audio | 每语言对象：file（public/ 下）或 silentReason（明确记录静音原因） |

`title/body/narration` 是语言标签到字符串的映射，全部语言必须存在，允许 body/narration 为空。模板只负责结构，初始中文/英文样片文案不能冒充其他语言译文；第三种语言要由协调层填写。

```json
{
  "id": "feature",
  "type": "ui",
  "startFrame": 150,
  "durationFrames": 240,
  "title": {"zh-CN": "从问题到结果", "en-US": "From question to outcome"},
  "body": {"zh-CN": "展示真实操作", "en-US": "Show the real workflow"},
  "narration": {"zh-CN": "在此填写旁白", "en-US": "Write narration here"},
  "claimIds": ["core-workflow"],
  "assetId": "workspace"
}
```

正式制作运行 `validate_plan.py --production`：拒绝 demo、缺证据、无证据镜头、缺语言、素材缺失、时间空隙/重叠、声音缺少配置。它无法判断来源是否真的支持主张，也无法测量 UI 可读性，这些由协调层审阅。

`state.json` 记录阶段、confirmed、assumptions、completed，以及可选的渲染版本、生成任务 ID。恢复先读该文件和已有媒体，保留确认输入，不重跑已完成的付费生成。

高级真实组件/算法动画可扩展 shots 数据，由工程自己的场景组件读取；保留上述基础字段与时间源。字幕文件由同一计划导出，旁白的实测长度决定字幕窗口，不能用单纯均分字符声称精准对齐。
