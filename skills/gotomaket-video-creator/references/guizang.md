# 归藏制片流程适配

源：[guizang-product-video-skill](https://github.com/op7418/guizang-product-video-skill)。随包快照在 `vendor/guizang/`，提交与许可见 upstream-lock.json。新入口采用本 skill 的免额外 API Key 核心路径、统一计划和通用 Agent 协调，保留真实组件、产品气质、导演、原创配乐、动作音效和实际审片经验。

按当前阶段读这些参考：

- 产品与组件：`vendor/guizang/references/repo-and-style.md`、`component-pipeline.md`。
- 导演与文案：`direction.md`、`story-and-copy.md`、`visual-vocabulary.md`。
- 声音与审片：`audio-sourcing.md`、`audio-and-qa.md`、`review.md`。

这些是原版技术/创作参考，提到上游完整仓库独有的 starter、fallback 或脚本时，不视为本包具备同名资源；执行入口以本 skill 为准。未打包 CodePilot 默认样式，默认用用户产品品牌，所有新增工程采用自有模板。

可直接运行的上游工具：

```bash
python3 <skill-dir>/vendor/guizang/scripts/sfx_landmarks.py <音效文件...>
```

`mix_audio.py` 使用上游秒制 plan，不能直接把本 skill 帧制 plan 传进去。需要该混音工具时，由协调层生成工程内 `audio/guizang-mix-plan.json`，字段如下：

```json
{
  "duration": 6,
  "fps": 30,
  "shots": [{"start": 0, "end": 6, "actions": [{"id": "click", "at": 2, "soundRequired": true}]}],
  "audio": {
    "music": {"file": "music.wav", "gain": 0.6},
    "ducking": {"enabled": true},
    "cues": [{"actionId": "click", "at": 2, "file": "click.wav", "gain": 0.8, "role": "sfx", "kind": "click"}]
  }
}
```

素材路径相对此混音 JSON；动作和音效时间来自同一计划的帧转换。运行 `mix_audio.py <音频计划>` 后查看实际输出位置与报告，再把 master 加入本片对应语言的完整音轨。该工具只混音乐和动作音效，旁白需进一步以 FFmpeg 或选定本地音频工具合入。没有动作音效的静音/旁白片不强行调用此工具。

声音工具与固定 WAV 保持原版许可和源说明；未打包含噪声采样逻辑的 make_sfx/示例配乐脚本，保证本包执行脚本不含随机逻辑。音效 SOURCE 中提到的这些文件属于完整上游仓库。上游脚本可能输出英文，不改动以免丢失来源，本 skill 自有协调文档和用户交流使用中文。
