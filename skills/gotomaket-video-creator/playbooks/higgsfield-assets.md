# Playbook: Higgsfield 生成素材

## 目的
为确定镜头生成可审阅本地素材，纳入统一时间轴，可选服务不阻塞核心制片。

## 前提条件
- 已有镜头目的、prompt、比例、时长和用途。
- 提交前具备服务访问、现行模型文档和授权费用/次数上限；密钥仅服务端环境变量，网页需已登录。
- 私有素材外传已有授权。缺项先准备请求和本地替代，不提交。

## 步骤
1. 查 [控制台](https://console.higgsfield.ai) 和 [官方索引](https://docs.higgsfield.ai/docs/llms.txt)，选定模型的最新文档确定 endpoint/schema/参数；OpenAPI 只辅助，不以缺项推断不可用。
2. 保存 `evidence/higgsfield-shot-<id>.json`：模型、文档、prompt、参数、费用/次数上限、素材与外传授权、状态。不放密钥，文字/logo/数值后期叠加。
3. API：Codex 协调层通过可用 HTTP 或官方 SDK 工具调用，不写入确定性 Scripts。REST 认证 `Authorization: Key KEY_ID:KEY_SECRET`；可选 TypeScript SDK `@higgsfield/client`，变量 `HF_CREDENTIALS`。使用 REST 无需额外 npm 依赖。
4. 提交前保存恢复键，按当前 [Quickstart](https://docs.higgsfield.ai/docs/quickstart) 和 [请求契约](https://docs.higgsfield.ai/docs/concepts/requests) 使用 `Idempotency-Key`。保存返回 request_id/status_url。超时同键恢复；无法验证模型支持时先查任务历史，不盲重试扣费。
5. 轮询返回 status_url，按文档退避，单次等待 ≤60 秒；完成才下载输出，失败/取消/过滤保留原因。重新生成遵守预算次数。
6. 网页：API 不可用但有账号，用浏览器选择实际可见功能、填写 prompt/参数并等待。网页独有模板不能直接当 API 参数，“生成中”不等于完成。
7. 检查解码、尺寸、时长、变形、首尾和声音，保存 `public/generated/`，计算哈希并加入计划。生成不确定，冻结已验收文件后再渲染。
8. 主引擎导入素材，叠加准确文字/品牌。需裁切/重排/调色用 FFmpeg 或 Remotion，不假定 HyperFrames 有超出当前文档的编辑能力。

## 判断标准
- 凭证和预算齐备 → API；只有网页账号 → 浏览器；都没有 → 本地素材/代码继续，交付说明未启用。
- 准确交互、算法、文字 → 真实 UI/代码；摄影、氛围、空间运镜 → 可选生成素材。
- 排队 → 保存 ID 后继续其他制作；完成 → 下载并验收。
- 双语 → 优先复用无对白镜头；选择生成对白时验证语言/唇形。
- 原生声音与旁白冲突 → 显式选择静音/保留，再统一混音。
- 403/额度/超时 → D 类，保留状态，不无限购买、换账号或重复提交。

## 验证
- 最终文件存在、可解码且已查看，任务与预算可追溯。
- 资产记录服务、模型、文档、prompt 摘要、任务 ID、本地哈希，无密钥。
- 本地渲染不再访问生成接口。
