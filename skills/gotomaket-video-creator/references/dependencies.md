# 依赖与免额外 API Key 核心流程

## 核心路径

产品理解、导演、脚本、设计与翻译使用当前 Agent 已有订阅/会话推理能力；不引入 OpenAI、Anthropic 或其他模型 API Key，不调用额外计费模型接口。浏览器、文件与命令执行用宿主已有工具。本 skill 不要求专属 Codex MCP，其他 Agent 可读取同一 `SKILL.md` 和 Playbook，用自身等效工具完成。

订阅的具体工具权限、额度与媒体生成能力由宿主决定，不能承诺所有 Agent 订阅都有图片、TTS 或视频生成。已包含且当前可用的媒体工具优先；没有时仍可用产品截图、代码动画、用户素材、已有本地语音/声音完成制片。

必需本地依赖：Python ≥3.9（脚本仅标准库）、Node ≥22、npm、浏览器、FFmpeg/FFprobe。依赖包固定在两个模板的 package.json，首次 `npm install` 生成 lockfile，后续用 `npm ci`。只安装所选引擎，不装两个引擎来完成同一片子。

| 路径 | 固定版本与用途 |
|---|---|
| Remotion | remotion、@remotion/cli、bundler、renderer 4.0.534；React/react-dom 19.2.3 |
| HyperFrames | hyperframes 0.8.143；GSAP 3.15.0；已核实 Node ≥22 |
| 音频 | FFmpeg；有 macOS `say` 时可用已安装系统声音；其他系统用现有本地 TTS 或用户文件 |
| 增强 | Higgsfield API/网页可选，独立账号/额度；默认关闭。无需 SDK，使用 REST 时零额外包 |

如果用户已授权接入真实产品组件，按其实际 package.json 补 UI/provider/样式依赖，适配隔离在视频工程，不改源产品配置。Remotion 相关包必须同版本。

```bash
# 在工程内，先检查依赖再按缺项安装
python3 <skill-dir>/scripts/doctor.py --project .
npm install
# 第二次及之后
npm ci
```

FFmpeg/浏览器优先复用已有可执行文件，通过 PATH 或 `REMOTION_BROWSER_EXECUTABLE`、`HYPERFRAMES_BROWSER_PATH` 指定。每条调用 FFmpeg 的校验/混音/音效命令都要继承相同 PATH；单条命令前的 PATH 设置不会自动应用到下一条命令。无系统工具时按官方安装方式补，遵守宿主权限；只因浏览器无法启动不重新安装整个工程。

doctor 的浏览器提示只说明来源，实际启动与资源加载由短样片验证。宿主拒绝网络、浏览器、localhost 或技能安装目录写入时，按正式权限机制处理并记录 D 类环境前提，不绕过沙箱。

本地渲染不产生模型 API 费用；软件/字体/第三方资产的使用条款仍由各自许可证决定，详见来源清单。不要把“免额外鉴权”扩写为所有商业场景和生成服务都免费。
