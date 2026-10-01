#!/usr/bin/env python3
"""Create the global library and per-video project skeletons for oral-video-workflow.

Usage:
  python init_workspace.py library <library_path>
  python init_workspace.py project <projects_root> <title> [--library <library_path>] [--date YYYYMMDD]

Never overwrites existing files. Standard library only.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

LEDGER_HEADER = ("asset_id,kind,file,desc,tags,source,source_url,license,author,"
                 "attribution_required,spec,sha1,added,used_in,status\n")
STYLES_HEADER = "style_id,name,kind,status,date,project,files,note\n"
USED_HEADER = "asset_id,timecode,purpose,note\n"

LIBRARY_README = """# 素材与经验库

跨视频共用。大文件只存这一份，项目只引用不复制。

- `lessons.md`      个人经验库
- `styles/`         已确认的样式（索引见 STYLES.md）
- `assets/`         素材（台账见 ASSET_LEDGER.csv）；新下载的先进 `_inbox/`，审核通过再入库
- `tools/`          可复用脚本

规则见 skill 里的 references/project-management.md。建议定期备份本目录。
"""

LESSONS_HEADER = """# 我的经验库

每条写：发生了什么 -> 原因 -> 以后怎么做（以及第几步该发现它）。
通用的坑在 skill 自带的 references/lessons.md；这里放你自己的口味和项目经验。

"""

PREFS_TEMPLATE = """# PREFS · {title}

- 发布平台与规格：
- 受众：
- 风格偏好：
- 文化 / 品牌禁忌：
- 素材位置：
- 可用工具与预算：
- 库的位置：{library}
- 备注：
"""

STATE_FALLBACK = """# 工作流状态 · {title}

- 当前阶段：
- 当前版本：
- 偏好文件：PREFS.md

## 关卡
| 关卡 | 内容 | 状态 | 用户决定（原话）|
|---|---|---|---|
| ◆1 | 粗剪表 | | |
| ◆2 | 时间轴锁定 | | |
| ◆3 | 方案与分镜表 | | |
| ◆4 | 样式 / 配乐 / 封面小样 | | |
| ◆5 | 成片审片 | | |

## 锁定清单（已认可）

## 已否决

## 版本记录
"""


def write_new(path: Path, text: str) -> bool:
    """Write text to path unless it exists. Returns True if created."""
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def state_template(title: str) -> str:
    ref = Path(__file__).resolve().parent.parent / "references" / "state-template.md"
    if ref.exists():
        m = re.search(r"```markdown\n(.*?)```", ref.read_text(encoding="utf-8"), re.S)
        if m:
            return m.group(1).replace("<项目名>", title)
    return STATE_FALLBACK.format(title=title)


def init_library(path: Path) -> list:
    created = []
    for d in ["styles/_candidates", "assets/footage", "assets/images", "assets/music",
              "assets/sfx", "assets/_inbox", "assets/_rejected", "tools"]:
        (path / d).mkdir(parents=True, exist_ok=True)
    files = {
        "README.md": LIBRARY_README,
        "lessons.md": LESSONS_HEADER,
        "styles/STYLES.md": STYLES_HEADER,
        "assets/ASSET_LEDGER.csv": LEDGER_HEADER,
    }
    for rel, text in files.items():
        if write_new(path / rel, text):
            created.append(rel)
    return created


def init_project(root: Path, title: str, library: str, day: str) -> Path:
    safe = re.sub(r'[\\/:*?"<>|]', "_", title).strip() or "untitled"
    proj = root / f"{day}_{safe}"
    for d in ["00_source", "01_transcript", "02_plan", "03_assets", "04_work",
              "05_deliver/_待删除", "06_qa"]:
        (proj / d).mkdir(parents=True, exist_ok=True)
    lib = library or "（未设置，第 1 步时问用户并建库）"
    write_new(proj / "PROJECT.md",
              f"# {title}\n\n- 库的位置：{lib}\n- 发布平台：\n- 当前版本：\n")
    write_new(proj / "00_source" / "SOURCE.md",
              "# 原片位置\n\n只记录路径，大文件不复制。\n\n- 路径：\n- 时长 / 编码 / 备注：\n")
    write_new(proj / "02_plan" / "PREFS.md", PREFS_TEMPLATE.format(title=title, library=lib))
    write_new(proj / "02_plan" / "WORKFLOW_STATE.md", state_template(title))
    write_new(proj / "03_assets" / "USED.csv", USED_HEADER)
    return proj


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("library")
    a.add_argument("path")
    b = sub.add_parser("project")
    b.add_argument("root")
    b.add_argument("title")
    b.add_argument("--library", default="")
    b.add_argument("--date", default=date.today().strftime("%Y%m%d"))
    args = ap.parse_args()

    if args.cmd == "library":
        p = Path(args.path).expanduser()
        created = init_library(p)
        print(f"Library ready: {p}")
        print("Created files:" if created else "Nothing new to create (already initialized).")
        for c in created:
            print("  +", c)
    else:
        proj = init_project(Path(args.root).expanduser(), args.title, args.library, args.date)
        print(f"Project ready: {proj}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
