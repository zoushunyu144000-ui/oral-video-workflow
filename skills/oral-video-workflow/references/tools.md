# 工具清单

只说"有什么、擅长什么、有什么限制"。具体怎么用，由你按当时的素材和版本自己判断。标注"已验证"的是作者环境里实际跑通过的；标注"未验证"的不要当作事实告诉用户。

## 目录
1. 剪辑与导出：ChatCut Desktop
2. ffmpeg
3. 转写
4. 执行 Agent：把脏活派出去
5. 找素材的来源与授权

---

## 1. 剪辑与导出：ChatCut Desktop（MCP）

ChatCut Desktop 暴露一组 MCP 工具，能直接操作桌面端当前打开的项目。使用前先确认当前项目，再读时间线，改完回读验证。下面按名称和用途归纳，**参数以连接后 `tools/list` 返回为准**。

| 用途 | 工具（名称） |
|---|---|
| 确认并切换项目、读项目 | `get_active_project` `target_project` `read_project` `list_projects` |
| 转写与逐字稿 | `trigger_transcript` `manage_transcript` `find_transcript` |
| 按脚本剪辑口播（去口癖、去停顿） | `read_script` `clean_script` `apply_script` |
| 剪口音频平滑 | `smooth_audio` |
| 时间线与素材 | `manage_timelines` `edit_track` `edit_item` `split_item` `detach_audio` `inspect_item` |
| 字幕 | `read_captions` `edit_captions` `search_fonts` |
| 动效与图形 | `create_motion_graphic_from_code` `manage_design_style` |
| 导入与素材库 | `import_url` `browse_assets` `browse_library` `search_stock_media` |
| 预览与导出 | `preview_timeline` `local_export` |
| 人声净化 | `isolate_voice` |
| 生成类（`submit_image` `submit_video` `submit_music` 等） | **会消耗账户额度**，没有额度或用户没同意前不要用 |

已验证的限制：
- 导出期间项目会被锁住（正片通常十几分钟），这段时间并行做素材和检查，不要碰项目。
- 项目里的"像素类 LUT 特效"在作者的版本上导出后没有生效；调色改用 ffmpeg 预处理后再换入。
- 改时间线之前先复制一条备份时间线。
- 把导出目录指到空间充足的磁盘，不要用默认的系统盘。

## 2. ffmpeg

常用的几条（均为标准用法）：

```bash
# 停顿检测（找过长停顿）
ffmpeg -i voice.wav -af silencedetect=noise=-50dB:d=0.4 -f null -
# 响度与峰值
ffmpeg -i final.mp4 -af ebur128=peak=true -f null -
# 母带响度（建议两遍；目标值按平台）
ffmpeg -i in.wav -af loudnorm=I=-14:TP=-1:LRA=11 out.wav
# 黑场检测
ffmpeg -i final.mp4 -vf blackdetect=d=0.03:pic_th=0.97:pix_th=0.06 -an -f null -
# 抽帧接触表（每 6 秒一帧，5×4 拼图）
ffmpeg -i final.mp4 -vf "fps=1/6,scale=320:-1,tile=5x4" -frames:v 1 sheet.jpg
# 素材统一规格（1080p30、无音轨）
ffmpeg -i in.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30" -an -c:v libx264 -pix_fmt yuv420p out.mp4
# HLG 手机素材转 SDR（需要带 libzimg 的 ffmpeg 构建；已验证）
ffmpeg -i hlg.mov -vf "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p" sdr.mp4
```

混音思路（具体数值每条素材都不同，自己听）：人声、音乐、音效分三轨 stem；人声说话时音乐轻微闪避；音乐要在手机外放也听得见，别压得太深。

## 3. 转写

用 ChatCut 自带转写，或本地 Whisper 类工具，任选。转写结果一定要校对：专名、同音字、数字。需要把转写模型放在磁盘空间充足的位置。

## 4. 执行 Agent：把脏活派出去

原则：强模型只做方案、审美判断、画面审核；搜索、下载、授权检查、转码、扫描这类机械活派给执行 Agent。统一用任务单协议（见 `task-templates.md`）：**任务单进，清单和报告出**，换哪个 Agent 都能接。

按能力分三档：

**① 全自动：命令行 Codex（`codex exec`）** ——已验证
```bash
codex exec --skip-git-repo-check -m <模型名> -s workspace-write -C <任务目录> "<提示词>" < /dev/null > run.log
```
- 默认沙箱是只读，要写文件用 `-s workspace-write`；要联网下载加 `-c sandbox_workspace_write.network_access=true`。
- Windows 上若 shell 调用报沙箱错误，可试 `-c 'windows.sandbox="unelevated"'`。
- 提示词里写明"文本文件一律 UTF-8"，否则中文可能乱码。
- 模型名按你的账号可用的来；有些模型别名在特定账号下会被拒绝，换一个即可。
- `codex exec resume --last "<新任务>"` 可接着上一次会话继续。
- 官方文档：子 Agent 继承父级沙箱，可在 `.codex/agents/*.toml` 里给每个子 Agent 单独指定模型。是否能在 `exec` 模式下的子 Agent 里用浏览器工具，**文档没写，未验证**。

**② 半自动：桌面版 Codex + 你生成提示词，用户粘贴**
- computer use 只有桌面版有，命令行没有；在 Windows 上只能在前台运行、会接管鼠标键盘，所以让用户在不用电脑的时候跑。
- 涉及登录态网页（例如图生视频站点）走这一档。
- 任务单里**不要限制操作方式**。写"可以使用 Chrome 标签页接口或 computer use，哪个能用用哪个，用户已授权"。限制过死，Codex 会停下来等授权。
- 视频生成这类站点的额度可能用完，永远不要替用户买额度。

**③ 人工：通用提示词**
同一份 `TASK.md` 生成一段完整提示词，让用户手动贴给任何 Agent。提示词必须自包含（不依赖聊天记录）。

**其他可选**：Grok 命令行可无界面运行并联网搜索（`grok --prompt-file p.txt --output-format plain`，已验证），适合查找素材线索；真正的下载与授权检查仍交给上面三档。

## 5. 找素材的来源与授权

- 实拍优先：Pexels、Pixabay、Mixkit、Coverr、Wikimedia Commons、Internet Archive 等免费商用站点。需要登录的站点，不要替用户注册或登录。
- 每个镜头找 2–3 个候选，记录来源链接、作者、授权类型。授权不明确就不下载。
- CC-BY 之类的素材和音乐，必须在发布简介里署名。
- AI 生成的画面只补缺口；在分镜表里写明"搜过但没找到 / 为什么用 AI"；发布简介里注明是情景重现。
- 代码合成的拟音（钢琴、纸声）听起来假，只适合低频铺底、空气声这类。
