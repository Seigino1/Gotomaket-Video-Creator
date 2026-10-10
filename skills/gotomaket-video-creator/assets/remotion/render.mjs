#!/usr/bin/env node
// 用途：从当前计划重新构建并渲染各语言关键帧或 MP4。
// 参数：stills|video all|语言 [秒数...]。
// 输出：渲染进度和文件位置。
// 退出码：0=成功，1=出错
// Known Issues: 浏览器启动需要环境权限；可用 REMOTION_BROWSER_EXECUTABLE 指定既有浏览器。
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';
import {openBrowser, selectComposition, renderStill, renderMedia} from '@remotion/renderer';

const root = path.dirname(fileURLToPath(import.meta.url));
process.chdir(root);
const plan = JSON.parse(fs.readFileSync('plan.json', 'utf8'));
const mode = process.argv[2] || 'stills';
const selection = process.argv[3] || 'all';
if (!['stills', 'video'].includes(mode)) throw new Error('模式须为 stills 或 video');
const languages = selection === 'all' ? plan.languages : [selection];
if (languages.some(x => !plan.languages.includes(x))) throw new Error('语言不在计划内');
const seconds = process.argv.slice(4).map(Number);
if (seconds.some(x => !Number.isFinite(x) || x < 0 || x >= plan.durationFrames / plan.fps)) throw new Error('关键帧时间越界');
const frames = seconds.length ? seconds.map(x => Math.round(x * plan.fps)) :
  [...new Set([0, ...plan.shots.map(x => x.startFrame + Math.floor(x.durationFrames / 2)), plan.durationFrames - 1])];
const serveUrl = await bundle({entryPoint: path.join(root, 'src/index.jsx'), publicDir: path.join(root, 'public')});
const browserExecutable = process.env.REMOTION_BROWSER_EXECUTABLE;
const browser = await openBrowser('chrome', {browserExecutable});
try {
  for (const language of languages) {
    const opts = {serveUrl, id: `Promo-${language}`, browserExecutable, puppeteerInstance: browser};
    const composition = await selectComposition(opts);
    if (mode === 'stills') {
      const folder = path.join(root, 'evidence', language);
      fs.mkdirSync(folder, {recursive: true});
      for (const frame of frames) {
        if (frame >= plan.durationFrames) throw new Error('关键帧超过最后一帧');
        await renderStill({...opts, composition, frame, imageFormat: 'png', output: path.join(folder, `frame-${frame}.png`)});
        console.log(`${language} 关键帧 ${frame}`);
      }
      fs.mkdirSync('covers', {recursive: true});
      await renderStill({...opts, composition, frame: 0, imageFormat: 'png', output: path.join(root, 'covers', `${language}.png`)});
    } else {
      fs.mkdirSync('renders', {recursive: true});
      let last = -1;
      await renderMedia({...opts, composition, codec: 'h264', pixelFormat: 'yuv420p', audioCodec: 'aac', crf: 18,
        outputLocation: path.join(root, 'renders', `${language}.mp4`), concurrency: 2,
        onProgress: p => {const n = Math.floor(p.progress * 100); if (n >= last + 10) {console.log(`${language} 渲染 ${n}%`); last = n;}}});
      console.log(`视频已输出：renders/${language}.mp4`);
    }
  }
} finally {
  await browser.close({silent: true});
}
