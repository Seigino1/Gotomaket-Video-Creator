#!/usr/bin/env python3
# 用途：将计划中的字幕精确导出为各语言 SRT 与 VTT。
# 参数：plan.json。
# 输出：导出的字幕路径。
# 退出码：0=成功，1=出错
# Known Issues: 无。
import argparse
import sys
from pathlib import Path
from validate_plan import read_plan


def timestamp(frame, fps, separator):
    milliseconds = (frame * 1000 + fps // 2) // fps
    seconds, ms = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02}{separator}{ms:03}'


def main():
    parser = argparse.ArgumentParser(description='导出各语言字幕')
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    plan = read_plan(args.plan)
    target = args.plan.resolve().parent / 'captions'
    target.mkdir(exist_ok=True)
    for lang in plan['languages']:
        srt, vtt = [], ['WEBVTT\n']
        for index, cap in enumerate(plan['captions'][lang], 1):
            start, end, text = cap['startFrame'], cap['endFrame'], cap['text']
            srt.append(f"{index}\n{timestamp(start, plan['fps'], ',')} --> {timestamp(end, plan['fps'], ',')}\n{text}\n")
            vtt.append(f"{timestamp(start, plan['fps'], '.')} --> {timestamp(end, plan['fps'], '.')}\n{text}\n")
        for suffix, lines in [('srt', srt), ('vtt', vtt)]:
            path = target / (lang + '.' + suffix)
            path.write_text('\n'.join(lines), encoding='utf-8')
            print('字幕已导出：' + str(path))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        print('字幕导出失败：' + str(exc), file=sys.stderr)
        sys.exit(1)
