#!/usr/bin/env python3
# 用途：校验统一计划的时间、语言、证据、本地素材和声音字段。
# 参数：plan.json；--production 开启正式制作检查。
# 输出：中文错误列表或成功信息。
# 退出码：0=成功，1=出错
# Known Issues: 非法主题与素材引用类型曾未被完整拦截，已补字段检查。
import argparse
import json
import re
import sys
from pathlib import Path


def integer(value, minimum=0):
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


def local_file(base, name):
    if not isinstance(name, str) or not name or Path(name).is_absolute():
        raise ValueError('素材路径必须为非空相对路径')
    candidate = (base / name).resolve()
    if base.resolve() not in candidate.parents:
        raise ValueError('素材路径不能越出工程目录')
    return candidate


def validate(plan, base, production=False):
    errors = []
    if not isinstance(plan, dict):
        return ['计划必须为 JSON 对象']
    if plan.get('schemaVersion') != 1:
        errors.append('schemaVersion 必须为 1')
    if plan.get('engine') not in ('remotion', 'hyperframes'):
        errors.append('engine 必须为 remotion 或 hyperframes')
    for key in ('width', 'height', 'fps', 'durationFrames'):
        if not integer(plan.get(key), 1):
            errors.append(key + ' 必须为正整数')
    for key in ('width', 'height'):
        if integer(plan.get(key), 1) and plan[key] % 2:
            errors.append(key + ' 必须为偶数，以便输出 H.264')
    if integer(plan.get('fps'), 1) and plan['fps'] > 120:
        errors.append('fps 不能超过 120')
    if not isinstance(plan.get('product'), str) or not plan['product'].strip():
        errors.append('产品名称不能为空')
    if not isinstance(plan.get('demo'), bool):
        errors.append('demo 必须为布尔值')
    sources = plan.get('inputSources')
    if not isinstance(sources, list) or not sources or any(not isinstance(x, str) or not x.strip() for x in sources):
        errors.append('inputSources 必须为非空来源数组')
    theme = plan.get('theme')
    if not isinstance(theme, dict):
        errors.append('theme 必须为对象')
    else:
        for key in ('background', 'text', 'accent', 'fontFamily'):
            if not isinstance(theme.get(key), str) or not theme[key].strip():
                errors.append('主题字段缺失：' + key)
    if production and plan.get('demo') is not False:
        errors.append('技术样片不能作为正式成片，需完成调研并设置 demo=false')
    languages = plan.get('languages', [])
    if (not isinstance(languages, list) or not languages or
            any(not isinstance(x, str) or not re.fullmatch(r'[a-zA-Z]{2,3}(?:-[a-zA-Z0-9]{2,8})*', x) for x in languages)):
        errors.append('languages 必须为非空语言标签数组')
        languages = []
    if len(set(languages)) != len(languages):
        errors.append('语言标签不能重复')
    evidence = plan.get('evidence', [])
    if not isinstance(evidence, list):
        errors.append('evidence 必须为数组'); evidence = []
    evidence_ids = set()
    for item in evidence:
        if not isinstance(item, dict) or not isinstance(item.get('id'), str):
            errors.append('证据缺少 id'); continue
        if item['id'] in evidence_ids:
            errors.append('证据 id 重复：' + item['id'])
        evidence_ids.add(item['id'])
        if item.get('status') not in ('official-claim', 'code-implemented', 'runtime-verified'):
            errors.append('证据状态无效：' + item['id'])
        if not all(isinstance(item.get(k), str) and item[k].strip() for k in ('claim', 'source')):
            errors.append('证据缺少主张或来源：' + item['id'])
    if production and not evidence:
        errors.append('正式影片至少需要一项可追溯产品证据')
    assets = plan.get('assets', [])
    if not isinstance(assets, list):
        errors.append('assets 必须为数组'); assets = []
    asset_ids = set()
    for asset in assets:
        if not isinstance(asset, dict) or not isinstance(asset.get('id'), str):
            errors.append('素材缺少 id'); continue
        if asset['id'] in asset_ids:
            errors.append('素材 id 重复：' + asset['id'])
        asset_ids.add(asset['id'])
        if asset.get('kind') not in ('image', 'video', 'audio', 'font'):
            errors.append('素材类型无效：' + asset['id'])
        try:
            path = local_file(base, asset.get('file'))
            if not path.is_file():
                errors.append('素材不存在：' + asset['id'])
            if not str(asset['file']).startswith('public/'):
                errors.append('渲染素材必须位于 public/：' + asset['id'])
        except ValueError as exc:
            errors.append(str(exc) + '：' + asset['id'])
        if production and not all(isinstance(asset.get(k), str) and asset[k].strip() for k in ('source', 'license')):
            errors.append('素材缺少来源或许可状态：' + asset['id'])
    shots = plan.get('shots', [])
    if not isinstance(shots, list) or not shots:
        errors.append('shots 必须为非空镜头数组'); shots = []
    cursor, shot_ids = 0, set()
    for shot in shots:
        if not isinstance(shot, dict):
            errors.append('镜头必须为对象'); continue
        sid = shot.get('id')
        if not isinstance(sid, str) or not re.fullmatch(r'[a-zA-Z0-9-]+', sid) or sid in shot_ids:
            errors.append('镜头 id 无效或重复'); continue
        shot_ids.add(sid)
        if not integer(shot.get('startFrame')) or not integer(shot.get('durationFrames'), 1):
            errors.append('镜头时间必须为整数帧：' + sid); continue
        if shot['startFrame'] != cursor:
            errors.append('镜头存在空隙或重叠：' + sid)
        cursor = shot['startFrame'] + shot['durationFrames']
        for field in ('title', 'body', 'narration'):
            texts = shot.get(field)
            if not isinstance(texts, dict):
                errors.append('镜头缺少语言字段 ' + field + '：' + sid); continue
            for lang in languages:
                if not isinstance(texts.get(lang), str) or (field == 'title' and not texts[lang].strip()):
                    errors.append('镜头语言缺失 ' + field + '/' + lang + '：' + sid)
        refs = shot.get('claimIds', [])
        if not isinstance(refs, list) or any(not isinstance(x, str) or x not in evidence_ids for x in refs):
            errors.append('镜头关联了未知证据：' + sid)
        if shot.get('assetId') is not None and (not isinstance(shot['assetId'], str) or shot['assetId'] not in asset_ids):
            errors.append('镜头关联了未知素材：' + sid)
    if cursor != plan.get('durationFrames'):
        errors.append('镜头结束帧与全片 durationFrames 不一致')
    if production and evidence_ids and not any(s.get('claimIds') for s in shots if isinstance(s, dict)):
        errors.append('正式影片必须有镜头使用产品证据')
    captions, audio = plan.get('captions', {}), plan.get('audio', {})
    if not isinstance(captions, dict):
        errors.append('captions 必须为对象'); captions = {}
    if not isinstance(audio, dict):
        errors.append('audio 必须为对象'); audio = {}
    for lang in languages:
        entries = captions.get(lang)
        if not isinstance(entries, list):
            errors.append('字幕语言缺失：' + lang); entries = []
        end = 0
        for cap in entries:
            if (not isinstance(cap, dict) or not integer(cap.get('startFrame')) or
                    not integer(cap.get('endFrame'), 1) or not isinstance(cap.get('text'), str) or not cap['text'].strip()):
                errors.append('字幕条目无效：' + lang); continue
            if cap['startFrame'] < end or cap['endFrame'] <= cap['startFrame'] or cap['endFrame'] > plan.get('durationFrames', 0):
                errors.append('字幕时间重叠或越界：' + lang)
            end = cap['endFrame']
        track = audio.get(lang)
        if not isinstance(track, dict):
            errors.append('声音配置缺失：' + lang); continue
        if track.get('file'):
            try:
                path = local_file(base, track['file'])
                if not path.is_file() or not track['file'].startswith('public/'):
                    errors.append('音轨缺失或不在 public/：' + lang)
            except ValueError as exc:
                errors.append(str(exc) + '：' + lang)
        elif not isinstance(track.get('silentReason'), str) or not track['silentReason'].strip():
            errors.append('无音轨时必须记录静音原因：' + lang)
    return errors


def read_plan(path, production=False):
    path = Path(path).resolve()
    plan = json.loads(path.read_text(encoding='utf-8'))
    errors = validate(plan, path.parent, production)
    if errors:
        raise ValueError('\n'.join(errors))
    return plan


def main():
    parser = argparse.ArgumentParser(description='校验宣传片统一计划')
    parser.add_argument('plan', type=Path)
    parser.add_argument('--production', action='store_true')
    args = parser.parse_args()
    try:
        read_plan(args.plan, args.production)
        print('计划校验通过。')
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print('计划校验失败：\n' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
