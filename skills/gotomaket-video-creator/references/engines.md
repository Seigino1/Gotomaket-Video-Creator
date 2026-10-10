# 主渲染引擎与通用 Agent 接口

协调层只需要六类宿主能力：读文件、写文件、命令执行、网页检索、浏览器查看、媒体展示。Codex 使用其原生工具，其他 Agent 映射为等效工具；不包含 Claude 插件命令、模型名、固定工具 ID 或用户绝对路径。

## Remotion

初始化 `--engine remotion`。已有 React 组件优先此路径；模板是最小技术样片，不是正式产品模板。根据产品修改 `src/Promo.jsx`、布局与 scene 组件，使用 plan 的事实与时间。

```bash
npm install
node render.mjs stills all
node render.mjs video all
npm run preview
```

也可 `node render.mjs stills en-US 0 2.4 5.9`。每次渲染重新 bundle，不使用失败构建后的旧产物。输出 `renders/<语言>.mp4`、`evidence/<语言>/` 和 `covers/<语言>.png`。

必须按需读内置 [最佳实践](remotion/SKILL.md)，重点：animations、compositions、timing、sequencing、images/videos/audio、fonts、measuring-text、transitions。所有动画由 `useCurrentFrame()` 驱动，秒乘 fps；禁止 CSS 自动播放动画、CSS transition 和 Tailwind 动画类。不要直接复制 Prompt Motion 的 GSAP 自动运行代码到 Remotion，需改为帧驱动插值。

素材/字体冻结在 `public/`，用 `staticFile()`、Img/OffthreadVideo 或当前固定版本支持的媒体组件加载；真实组件 provider 与 fixture 放隔离工程。字体加载完成后才能渲染，多语言使用支持对应字符的本地字体。

## HyperFrames

初始化 `--engine hyperframes`，内置 build.mjs 将统一计划烘焙到 HTML。运行时不联网取数据。每语言顺序构建 `index.html`，不要多进程同时改写。

```bash
npm install
node build.mjs zh-CN
npx --no-install hyperframes lint . --json
npx --no-install hyperframes check . --json
node render.mjs stills all
node render.mjs video all
npm run preview
```

命令已按 0.8.143 核实：`check` 集成静态/运行时/布局检查；`validate` 仍可用但已弃用。doctor 即使输出缺项也可能退出 0，检查 JSON 的 `ok`，不能只看退出码。

技术契约：

- 独立 index 的 composition 根直接在 body 内，有明确 width/height 和 data-width/data-height/data-duration/data-fps；不包 template。
- 定时片段 class=clip，data-start/data-duration/data-track-index；同轨不能无意重叠。
- `gsap.timeline({paused:true})` 同步创建，注册 `window.__timelines[composition-id]`；播放器控制时间。
- 子合成必须 template，样式/脚本在 template 内，host ID、内部 ID 和 timeline key 一致；额外验证挂载后的关键帧。
- video/audio 放主根直接子节点，由框架驱动，不自行 play/currentTime；资产本地化。
- 不以时钟、随机值、联网、无限 repeat 控制视觉。采用明确首/末状态与有界循环，回退定位同样正确。
- 不把 inline span 缩放当成可见运动，设置块级及尺寸；字号、首帧、最高缩放位置和边界要实际查看。

可按官方文档补复杂子合成、Three.js、Lottie 或 shader；框架参考不是默认要全装的依赖。素材编辑交给当前明确支持的工具，不能把所有剪辑能力归给 HTML 动效引擎。

## 生成素材接入

宿主订阅已有媒体生成工具或用户文件 → 本地资源 → 计划资产 → 主引擎。Higgsfield 同样只提供素材。不让任一渲染帧重新调用生成模型。
