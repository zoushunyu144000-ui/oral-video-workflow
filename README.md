# oral-video-workflow

**口播视频剪辑工作流 skill** —— 把一段口播原片剪成有设计感的成片：强模型出方案，人在关键点点头，AI 一路执行。

> *A skill for editing talking-head / spoken-word video: a strong model plans, you approve at five key gates, the agent executes. Written in Chinese; the workflow is language-agnostic.*

## 这个 skill 做什么

固定的流程，加上根据内容做出的个性化调整，加上自我检查与迭代，加上对工具的调用。

- **12 步、5 个环节、5 次点头**：摸底 → 粗剪 → 设计 → 制作 → 交付。前四次点头都在导出之前，越早点头，返工越便宜。
- **不当许愿机**：每个关卡先出人看得懂的方案或小样，点头了才执行。
- **放手让模型发挥审美**：构图、节奏、配色、素材选择由模型决定；人只做喜好判断、内容取舍、事实把关。
- **反馈先复述**：改之前先说一遍"我理解你要的效果"，确认再动手。
- **自我迭代**：每次审片的意见沉淀到 `references/lessons.md`，同一个坑只踩一次。
- **派活给执行 Agent**：搜素材、下载、转码这类脏活，派给 Codex 等执行 Agent；有全自动、半自动、人工提示词三档。

## 安装：把下面这段发给你的 Agent

```
请帮我安装一个开源的口播剪辑 skill：
1. 把仓库 https://github.com/zoushunyu144000-ui/oral-video-workflow 下载到本地（git clone 或下载 zip 均可）。
2. 按你自己的 skill / 插件机制，把其中的 skills/oral-video-workflow 目录保存到本地能被你调用的位置，并告诉我保存在了哪里。
3. 先完整阅读 SKILL.md 和 README，用三句话告诉我这个 skill 能做什么、需要哪些工具。
4. 检查我的电脑缺哪些依赖（如 ffmpeg），列出清单，先不要安装，等我确认。
5. 都完成后，问我要剪哪条视频。
```

> 开源 skill 建议先读一遍再运行。上面的提示词让 Agent 先读、先列依赖、先不安装，就是为了这个。

## 最低配置

必备：
1. 一个能读写文件、执行命令的 Agent（建议用最强的模型，审美和方案质量取决于它）
2. [ffmpeg](https://ffmpeg.org/)
3. 转写工具（本地或在线）
4. 剪辑与导出工具（当前流程基于 ChatCut Desktop 的 MCP；换成别的剪辑软件，流程和关卡照用，工具部分自己替换）

可选（提效）：Codex 等执行 Agent、图生视频工具、免费素材站。

## 目录

```
skills/oral-video-workflow/
├─ SKILL.md                     一页：目标、12 步骨架、工具、注意事项
└─ references/
   ├─ tools.md                  工具清单与限制（含派活的三档做法）
   ├─ lessons.md                经验库（会自动增长）
   ├─ platforms.md              各平台标题 / 简介 / 封面档案模板
   ├─ task-templates.md         给执行 Agent 的任务单与通用提示词
   └─ state-template.md         WORKFLOW_STATE.md 模板
```

## 参与

欢迎提交你踩过的坑：在 `references/lessons.md` 里按"发生了什么 → 原因 → 以后怎么做"的格式追加。

## License

MIT，见 [LICENSE](LICENSE)。
