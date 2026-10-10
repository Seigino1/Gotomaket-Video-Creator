# GTM · Video Creator Skill

[中文](README.md) · Created by Seigi

![GTM Video Creator Skill cover](docs/images/cover.jpg)

**Every product deserves a good story.**

Start with a repository, product website, or files. Work with your agent to turn product research into a script, branded motion design, and a finished promotional video. The skill is named **Gotomaket-Video-Creator**; invoke it with `$gotomaket-video-creator`.

## From a link to a finished film

1. **Understand the product** — identify its audience, positioning, and evidence-backed strengths.
2. **Set the brief** — confirm language, duration, aspect ratio, and distribution channel.
3. **Choose the story** — prioritize a clear message over a list of features.
4. **Design the storyboard** — shape the script, brand treatment, scenes, and motion.
5. **Preview and refine** — review frames and footage, then apply specific feedback.
6. **Deliver** — export MP4, subtitles, cover, script, and an editable project.

![Product analysis and positioning](docs/images/product-analysis.jpg)

The TourMind example combines reliable travel supply with AI capabilities, highlighting its Trip Planning Skill and Booking Skills.

![Turning AI capabilities into a story](docs/images/ai-story.jpg)

Confirm important decisions through conversation. Refine visuals, pacing, and copy without losing choices already made.

![Preview and feedback](docs/images/preview-feedback.jpg)

Keep the finished film and the source project ready for the next revision.

![Video and project delivery](docs/images/delivery.jpg)

These frames come from a **72-second Chinese workflow film**, with original background music and no narration. Its conversation UI is a staged workflow demonstration based on a real case, not a recording of historical chats. The English documentation shares these original Chinese screenshots. This repository distributes only the skill and illustrated documentation; videos and website source are not included.

## Install in Codex

Copy this message into Codex:

```text
Install the gotomaket-video-creator Skill from https://github.com/Seigino1/Gotomaket-Video-Creator.
The skill is in skills/gotomaket-video-creator. Install that complete folder into this Codex user's skills directory, preserving all subfolders and dependency files.
If a skill with the same name already exists, compare and back it up before updating. Verify SKILL.md and its relative references, then explain how to invoke it. Do not place the demo or ZIP archives inside the installed skill folder.
```

Then start a new conversation:

```text
Use $gotomaket-video-creator to make a product video from https://example.com.
Analyze the product first, then help me confirm the audience, language, script, and visual direction. Prefer tools available in my current subscription and local rendering.
```

Alternatively, download the complete Skill ZIP from [Releases](https://github.com/Seigino1/Gotomaket-Video-Creator/releases/latest), then place the extracted `gotomaket-video-creator` folder in `~/.codex/skills/`. Other agents can use their supported Skills directory or read `SKILL.md` directly.

## Capabilities and requirements

- **Core:** the current agent session plus local production; no additional model API key is required for the core workflow.
- **Rendering:** HyperFrames or Remotion, one primary engine per film. Templates and dependency lockfiles are included.
- **References:** Guizang's product-video workflow, Remotion best practices, and a Codex adaptation of Prompt Motion references.
- **Optional:** Higgsfield-generated assets. Disabled by default; account access, permission, and charges are separate.
- **Local tools:** Python 3.9+, Node.js 22+, npm, a browser, and FFmpeg/FFprobe. Install dependencies only for the engine you choose.

Image, voice, and video generation depend on the tools and quotas available in the host. The skill does not promise free media generation in every agent. Multilingual versions can share visuals while adapting copy, subtitles, and audio.

## Website and examples

The website includes a workflow demonstration, a TourMind / Works / JourniOne video carousel, feedback and installation controls, and a local like-sticker interaction. Likes select from 30 outlined emoji stickers and unlock an Easter egg at 1,000. Records stay in the current browser. The voting URL is not configured yet.

The website and example videos are maintained separately and are not distributed in this skill repository.

| Directory | Contents |
|---|---|
| `skills/gotomaket-video-creator/` | Complete installable skill, prompts, templates, scripts, and upstream references |
| `docs/images/` | Compressed cover and video frames, approximately 364 KB total |

[Send feedback](https://alidocs.dingtalk.com/notable/share/form/v01NpQlK57AQbbQDqDv_wSW69Lr_Jw8xtNM?source=link)

See [sources.md](skills/gotomaket-video-creator/references/sources.md) for upstream origins and licenses. The Guizang snapshot retains AGPL-3.0; frameworks, fonts, and example media retain their respective rights and terms.
