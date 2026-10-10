#!/usr/bin/env python3
# 用途：完整解码并校验成片时长、尺寸、帧率和音轨，输出可追溯报告。
# 参数：plan.json --video 视频 --language 语言；可选 --production --report。
# 输出：JSON 媒体检查报告。
# 退出码：0=通过，1=出错或不匹配
# Known Issues: 媒体检查不能判断文案、画面质量或是否已经试听。
import argparse
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from validate_plan import read_plan


def main():
    parser = argparse.ArgumentParser(description='验证实际视频交付')
    parser.add_argument('plan', type=Path)
    parser.add_argument('--video', required=True, type=Path)
    parser.add_argument('--language', required=True)
    parser.add_argument('--production', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    plan = read_plan(args.plan, args.production)
    if args.language not in plan['languages']:
        raise ValueError('语言未在计划中声明')
    if not args.video.is_file() or args.video.stat().st_size == 0:
        raise ValueError('视频不存在或为空')
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(args.video)], capture_output=True, text=True)
    if probe.returncode:
        raise ValueError(probe.stdout + probe.stderr)
    metadata = json.loads(probe.stdout)
    videos = [x for x in metadata['streams'] if x['codec_type'] == 'video']
    audios = [x for x in metadata['streams'] if x['codec_type'] == 'audio']
    if len(videos) != 1:
        raise ValueError('需要且只能有一条视频流')
    video = videos[0]
    expected_duration = plan['durationFrames'] / plan['fps']
    actual_duration = float(video.get('duration', metadata['format'].get('duration', 0)))
    checks = {
        '尺寸': video['width'] == plan['width'] and video['height'] == plan['height'],
        '帧率': abs(float(Fraction(video['avg_frame_rate'])) - plan['fps']) < 0.01,
        '时长': abs(actual_duration - expected_duration) <= 2 / plan['fps'],
        '音轨': bool(audios) if plan['audio'][args.language].get('file') else not audios,
        '编码': video.get('codec_name') == 'h264',
    }
    result = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(args.video), '-f', 'null', '-'], capture_output=True, text=True)
    checks['完整解码'] = result.returncode == 0
    if result.returncode:
        print(result.stdout + result.stderr, file=sys.stderr)
    digest = hashlib.sha256()
    with args.video.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    report = {'ok': all(checks.values()), 'video': str(args.video.resolve()), 'language': args.language,
              'sha256': digest.hexdigest(), 'duration': actual_duration, 'checks': checks,
              '视觉审查': '未由本脚本执行', '试听': '未由本脚本执行'}
    output = args.report or args.plan.resolve().parent / 'evidence' / ('media-' + args.language + '.json')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as exc:
        print('媒体检查失败：' + str(exc), file=sys.stderr)
        sys.exit(1)
