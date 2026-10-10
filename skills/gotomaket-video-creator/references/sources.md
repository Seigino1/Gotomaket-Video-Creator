# 来源与打包范围

核实日期：2026-10-09。精确提交/依赖见 [upstream-lock.json](upstream-lock.json)。

| 来源 | 整合方式 | 许可/访问 |
|---|---|---|
| [HyperFrames](https://github.com/heygen-com/hyperframes) | 固定 npm 0.8.143、验证 CLI、独立 HTML 适配模板 | npm 声明 Apache-2.0，包自身携带许可证；无需模型 API Key 本地渲染 |
| [归藏产品视频](https://github.com/op7418/guizang-product-video-skill) | 选定流程/提示词/参考/原创音效/声音工具快照 | 保留 AGPL-3.0 原文和来源；未打包 BUSL CodePilot fallback |
| Remotion 最佳实践 | 用户指定本地 skill 的规则快照，按需读取 | 框架依赖按其自身条款使用；不声称所有商业使用免费 |
| [Prompt Motion](https://prompt-motion.com) | 按镜头现场查案例与作者，原创 Codex 适配说明 | 参考内容归作者；不打包完整第三方 prompt 或原片 |
| [Higgsfield 官方文档](https://docs.higgsfield.ai/docs/llms.txt) | 可选 API/网页工作流，协调层调用 | 账号、额度、模型和素材外传授权；默认不启用 |
| 本次 Works 制片 | 通用提炼产品证据、真实组件、双语、反馈与审片方法 | 不打包客户数据、产品源码、凭证或本片 MP4 |

本包自身入口、模板与脚本独立编写，上游内容隔离在 vendor 及规则参考目录。分发时保留对应原版许可；若把上游代码作为闭源/白标产品内置，按它的许可或作者协议核对，不用本包改变上游授权。

此 skill 的“免额外鉴权”指当前 Agent 会话推理与本地制片不要求另配模型 API Key；不是替代宿主订阅，也不免除 optional 生成服务费用或第三方素材许可。
