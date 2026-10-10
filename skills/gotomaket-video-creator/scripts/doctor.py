#!/usr/bin/env python3
# 用途：只读检查当前工程所需的工具与固定版本依赖。
# 参数：--project 工程路径。
# 输出：JSON 环境报告。
# 退出码：0=依赖齐备，1=缺项或出错
# Known Issues: 浏览器存在不证明沙箱允许启动，需在渲染阶段实测。
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='检查视频工程依赖')
    parser.add_argument('--project', required=True, type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    package = json.loads((project / 'package.json').read_text())
    checks = []
    for name in ('node', 'npm', 'ffmpeg', 'ffprobe'):
        executable = shutil.which(name)
        ok, detail = False, '缺少工具'
        if executable:
            result = subprocess.run([executable, '--version' if name in ('node', 'npm') else '-version'], capture_output=True, text=True)
            detail = (result.stdout or result.stderr).splitlines()[0] if (result.stdout or result.stderr) else '无版本输出'
            ok = result.returncode == 0
            if name == 'node' and ok:
                ok = int(detail.lstrip('v').split('.')[0]) >= 22
        checks.append({'name': name, 'ok': ok, 'detail': detail})
    for name, expected in {**package.get('dependencies', {}), **package.get('devDependencies', {})}.items():
        file = project / 'node_modules' / name / 'package.json'
        version = json.loads(file.read_text()).get('version') if file.is_file() else None
        checks.append({'name': name, 'ok': version == expected, 'detail': version or '未安装', 'expected': expected})
    browser = os.environ.get('REMOTION_BROWSER_EXECUTABLE') or os.environ.get('HYPERFRAMES_BROWSER_PATH')
    checks.append({'name': '浏览器提示', 'ok': True, 'detail':
                   '已指定浏览器，启动权限待渲染验证' if browser else '使用引擎默认浏览器；缺少时按官方说明安装'})
    ok = all(x['ok'] for x in checks)
    print(json.dumps({'ok': ok, 'checks': checks}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print('环境检查失败：' + str(exc), file=sys.stderr)
        sys.exit(1)
