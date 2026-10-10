#!/usr/bin/env node
// 用途：按语言顺序构建、检查并渲染 HyperFrames 关键帧或 MP4。
// 参数：stills|video all|语言 [秒数...]。
// 输出：检查报告、关键帧或视频。
// 退出码：0=成功，1=出错
// Known Issues: 浏览器与本地服务需要执行权限；HYPERFRAMES_BROWSER_PATH 可指定现有浏览器。
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root = path.dirname(fileURLToPath(import.meta.url));
process.chdir(root);
const plan = JSON.parse(fs.readFileSync('plan.json', 'utf8'));
const mode = process.argv[2] || 'stills', selection = process.argv[3] || 'all';
if (!['stills', 'video'].includes(mode)) throw new Error('模式须为 stills 或 video');
const languages = selection === 'all' ? plan.languages : [selection];
if (languages.some(x => !plan.languages.includes(x))) throw new Error('语言未在计划声明');
const times = process.argv.slice(4).map(Number);
if (times.some(x => !Number.isFinite(x) || x < 0 || x >= plan.durationFrames / plan.fps)) throw new Error('关键帧时间越界');
const at = times.length ? times : [0, ...plan.shots.map(x => (x.startFrame + Math.floor(x.durationFrames / 2)) / plan.fps), (plan.durationFrames - 1) / plan.fps];
const cli = path.join(root, 'node_modules/hyperframes/bin/hyperframes.mjs');
function run(args) {
  const result = spawnSync(process.execPath, args, {stdio: 'inherit', cwd: root});
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error('命令失败，退出码：' + result.status);
}
for (const language of languages) {
  run(['build.mjs', language]);
  run([cli, 'lint', '.', '--json']);
  run([cli, 'check', '.', '--json']);
  if (mode === 'stills') {
    run([cli, 'snapshot', '.', '--at', [...new Set(at)].join(','), '--output', `evidence/${language}`]);
    fs.mkdirSync('covers', {recursive: true});
    const first = fs.readdirSync(`evidence/${language}`).sort().find(x => x.endsWith('.png'));
    if (first) fs.copyFileSync(`evidence/${language}/${first}`, `covers/${language}.png`);
  } else {
    fs.mkdirSync('renders', {recursive: true});
    run([cli, 'render', '.', '--quality', 'high', '--strict', '--workers', '2', '--output', `renders/${language}.mp4`]);
    if (!fs.existsSync(`renders/${language}.mp4`) || !fs.statSync(`renders/${language}.mp4`).size) throw new Error('渲染未产生视频');
  }
}
