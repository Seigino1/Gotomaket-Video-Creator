#!/usr/bin/env python3
# 用途：将完整 skill 复制到指定 Agent 技能目录，不覆盖现有安装。
# 参数：--skills-dir 可选，默认 Codex 用户技能目录。
# 输出：安装目录。
# 退出码：0=成功，1=出错
# Known Issues: 技能目录写入权限由宿主控制；已有安装需要先明确更新范围。
import argparse
import os
import shutil
import sys
from pathlib import Path


def main():
    default = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills'
    parser = argparse.ArgumentParser(description='安装宣传视频 skill')
    parser.add_argument('--skills-dir', type=Path, default=default)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    target = args.skills_dir.expanduser().resolve() / root.name
    if target == root or root in target.parents:
        raise ValueError('安装目录必须在源 skill 以外')
    if target.exists():
        raise ValueError('目标安装已存在，保留现有版本，不覆盖')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(root, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'node_modules', '.git', '.tmp', '.env*'))
    print('skill 已安装：' + str(target))
    print('在新会话或技能列表刷新后调用 $gotomaket-video-creator。')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        print('安装失败：' + str(exc), file=sys.stderr)
        sys.exit(1)
