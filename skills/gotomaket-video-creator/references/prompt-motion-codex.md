# Prompt Motion → Codex 动效适配

入口：[Prompt Motion](https://prompt-motion.com)。需要动效时按镜头查 Product UI、Charts、Diagrams、Kinetic type、Shapes 等类别，选一到三个参考。内容归作者；默认只借鉴手法，不下载别人的原片或完整搬运 prompt。

1. 打开案例页读可见 prompt/skill、作者、实现栈与原帖。无法读取换可访问案例，或让用户提供参考文本，不猜复制按钮内容。
2. 保存 `evidence/motion-references.json`：URL、作者、标题、业务作用、采用手法、改写和许可情况。
3. 去除 Claude 模型/effort、`/plugin marketplace`、`/plugin install`、`.claude` 路径、假设工具，转换为 Codex 实际工具及本 skill 工程流程。改模型名不等于适配。
4. 参考是 skill 时先读公开源码及许可，只提取本镜头所需方法，不自动安装未知插件。
5. 按下面说明实现，检查关键帧、短片、回退定位。

## Codex 镜头说明模板（原创）

> 在当前独立工程用 {引擎} 实现 {shot_id}，时长 {frames}/{fps}。参考 {作者/URL} 的 {动作结构}，用本产品 {品牌 token/真实素材} 改写。
> 叙事作用：{需要看懂的动作与结果}；主体：{对象}；首状态：{状态}；末状态：{状态}。
> 运动：{入场、轨迹、先后、缓动、停留、出场}；构图：{安全区、字号、重点与留白}。
> 文字、数值与 logo 准确，素材冻结在本地。HyperFrames 同步构建并注册暂停时间轴；Remotion 用 useCurrentFrame，不保留 CSS 自动播放动画。
> 出首/中/末帧并验证回退，渲染短片，记录与参考差异，不保证不同模型复现相同效果。

## 示例

- [ViralGrow product promo](https://prompt-motion.com/samuel-yostt-891f87)，@samuel_yostt：借鉴短片与官网视觉一致的思路，改为本产品主视觉引出真实工作区、一次操作呈现结果和 CTA 的任务，不保留原模型要求或 prompt 全文。
- [Cinetic skill launch film](https://prompt-motion.com/lexnlin-6161a6)，@LexnLin：研究品牌、配乐与代码成片统一，事实/资源仍由本 skill 管理。
- [Reddit marketing tool launch video](https://prompt-motion.com/anthonyriera-9b1b2a)，@anthonyriera：Claude 插件命令转换为阅读参考及隔离 Remotion 工程，不假设 Codex 有同名插件。

网站不可用时按模板原创实现，不能声称已查网站。使用原片、代码或素材时核对各自许可。
