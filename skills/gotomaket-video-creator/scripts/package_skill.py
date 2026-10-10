#!/usr/bin/env python3
# 用途：按固定文件顺序和时间戳打包 skill，排除缓存、密钥和测试产物。
# 参数：--output 压缩包路径。
# 输出：压缩包路径与文件数。
# 退出码：0=成功，1=出错
# Known Issues: 无。
import argparse
import sys
import zipfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='打包可分发视频 skill')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    target = args.output.resolve()
    if target.exists():
        raise ValueError('压缩包已存在，请使用新版本文件名，不覆盖未知文件')
    if root == target or root in target.parents:
        raise ValueError('压缩包必须位于 skill 包以外')
    target.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob('*')):
            relative = path.relative_to(root)
            if not path.is_file() or path.is_symlink():
                continue
            if any(x in ('.git', '.tmp', '__pycache__', 'node_modules', '.pytest_cache') for x in relative.parts):
                continue
            if path.name.startswith('.env') or path.suffix in ('.pyc', '.zip', '.mp4'):
                continue
            info = zipfile.ZipInfo(str(Path(root.name) / relative), date_time=(2026, 10, 9, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
            count += 1
    print('打包完成：' + str(target) + '，文件数：' + str(count))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        print('打包失败：' + str(exc), file=sys.stderr)
        sys.exit(1)
