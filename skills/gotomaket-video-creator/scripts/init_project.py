#!/usr/bin/env python3
# 用途：从随包模板初始化隔离、双语可配置的视频技术样片。
# 参数：--output --engine --product --source --languages；可选 --width --height --fps。
# 输出：工程位置和下一步。
# 退出码：0=成功，1=出错
# Known Issues: 无。
import argparse
import json
import shutil
import sys
from pathlib import Path
from validate_plan import validate


def main():
    parser = argparse.ArgumentParser(description='初始化独立宣传视频工程')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--engine', choices=['remotion', 'hyperframes'], required=True)
    parser.add_argument('--product', required=True)
    parser.add_argument('--source', action='append', required=True)
    parser.add_argument('--languages', nargs='+', default=['zh-CN'])
    parser.add_argument('--width', type=int, default=1920)
    parser.add_argument('--height', type=int, default=1080)
    parser.add_argument('--fps', type=int, default=30)
    args = parser.parse_args()
    target = args.output.expanduser().resolve()
    skill = Path(__file__).resolve().parents[1]
    if target == skill or skill in target.parents:
        raise ValueError('输出目录必须位于 skill 包以外')
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise ValueError('输出目录已存在且非空，保留现有内容，不覆盖')
    languages = args.languages
    duration = args.fps * 6
    shots = []
    for index, (zh, en) in enumerate([
        ('制作链路样片', 'Production pipeline sample'),
        ('统一时间轴与语言', 'One timeline, multiple languages'),
        ('等待产品内容接入', 'Ready for product content'),
    ]):
        titles = {lang: zh if lang.startswith('zh') else en if lang.startswith('en') else '技术样片' for lang in languages}
        shots.append({'id': 'sample-' + str(index + 1), 'type': 'title', 'startFrame': index * args.fps * 2,
                      'durationFrames': args.fps * 2, 'title': titles,
                      'body': {lang: args.product for lang in languages},
                      'narration': {lang: '' for lang in languages}, 'claimIds': [], 'assetId': None})
    plan = {'schemaVersion': 1, 'demo': True, 'product': args.product, 'engine': args.engine,
            'inputSources': args.source, 'scope': {'versions': '整体产品（建议）', 'platforms': ['待调研']},
            'width': args.width, 'height': args.height, 'fps': args.fps, 'durationFrames': duration,
            'languages': languages, 'theme': {'background': '#101820', 'text': '#f3f5f7', 'accent': '#6ee7b7',
            'fontFamily': 'sans-serif'}, 'evidence': [], 'assets': [], 'shots': shots,
            'captions': {lang: [] for lang in languages},
            'audio': {lang: {'file': None, 'silentReason': '技术样片暂不含音轨，正式制作按用户要求配置'} for lang in languages}}
    errors = validate(plan, target)
    if errors:
        raise ValueError('\n'.join(errors))
    shutil.copytree(skill / 'assets' / args.engine, target, dirs_exist_ok=True)
    for name in ('public', 'evidence', 'renders', 'captions', 'covers', '.tmp'):
        (target / name).mkdir(exist_ok=True)
    (target / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (target / 'state.json').write_text(json.dumps({'stage': '产品调研', 'confirmed': {}, 'assumptions': {
        'duration': '约60秒', 'aspect': '16:9', 'style': '沿用品牌'}, 'completed': ['工程初始化']}, ensure_ascii=False, indent=2) + '\n')
    for filename, content in {
        'BRIEF.md': '# 制作说明\n\n当前为技术样片；在此记录产品、受众、渠道、范围、语言、声音与用户决定。\n',
        'DIRECTION.md': '# 影片方向\n\n调研后填写品牌、设计规范、参考、选定方向与镜头表。\n',
        'SCRIPT.md': '# 宣传脚本\n\n调研后填写逐镜头叙事、画面、旁白、字幕与声音。\n',
        'DELIVERY.md': '# 交付记录\n\n当前尚未完成产品制作。分别记录媒体检查、实际视觉审查、播放与试听。\n',
        '.gitignore': 'node_modules/\n.tmp/\n.env*\n',
    }.items():
        (target / filename).write_text(content, encoding='utf-8')
    print('工程初始化完成：' + str(target))
    print('当前为6秒技术样片；先调研产品、完成方向与计划，再制作正式影片。')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        print('初始化失败：' + str(exc), file=sys.stderr)
        sys.exit(1)
