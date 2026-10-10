# 安装与跨 Agent 使用

Codex 用户目录：`~/.codex/skills/gotomaket-video-creator/`，入口是 SKILL.md；显示名为 Gotomaket-Video-Creator，调用名为 `$gotomaket-video-creator`。新会话或技能列表刷新后使用。

`python3 <skill-dir>/scripts/install_skill.py` 安装到 Codex 用户目录；`--skills-dir <其他Agent技能目录>` 可指定目标。已有目录时拒绝覆盖。更新先比较现有版本并保留备份，再按用户授权处理。

其他 Agent 将同一目录放其支持的 Agent Skills 目录即可，保留相对目录结构。若只支持项目说明，直接让它读取 SKILL.md 和对应 Playbook。`agents/openai.yaml` 仅用于 Codex 显示，核心流程不依赖它；不绑定 Codex 历史、MCP、Claude 插件或某家模型名。

依赖按运行时检查，不在用户安装 skill 时强制安装所有框架。Prompt Motion 是开放参考来源，无需额外生成服务账号；订阅推理和本地渲染是默认路径。Higgsfield 账号/计费只属于用户主动选择的增强分支。

示例调用：

> 用 $gotomaket-video-creator，根据 https://example.com 制作产品宣传视频。先分析产品并给我脚本和视觉方向，再通过对话完成中英文成片。优先使用当前订阅能力和本地工具，不调用额外付费 API。

分发使用 `python3 <skill-dir>/scripts/package_skill.py --output <新文件名.zip>`。包不含 node_modules、凭证、生成媒体与缓存；制作工程自己的 lockfile 和资产应作为成片工程另行交付。
