#!/usr/bin/env node
// 用途：把统一计划与本地素材烘焙为所选语言的 HyperFrames HTML。
// 参数：可选语言，默认计划第一种语言。
// 输出：index.html 和本地 GSAP 资源。
// 退出码：0=成功，1=出错
// Known Issues: 语言版本顺序构建；媒体节点缺 id 曾被 lint 拦截，已补稳定唯一 id。
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root = path.dirname(fileURLToPath(import.meta.url));
process.chdir(root);
const plan = JSON.parse(fs.readFileSync('plan.json', 'utf8'));
const language = process.argv[2] || plan.languages[0];
if (!plan.languages.includes(language)) throw new Error('语言未在计划声明');
const esc = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
const js = value => JSON.stringify(value).replaceAll('<', '\\u003c');
const id = 'promo-' + language;
const duration = plan.durationFrames / plan.fps;
const scale = Math.min(plan.width, plan.height);
const media = [], scenes = [], tweens = [];
for (const shot of plan.shots) {
  const start = shot.startFrame / plan.fps, length = shot.durationFrames / plan.fps;
  const asset = plan.assets.find(x => x.id === shot.assetId);
  const sid = `shot-${shot.id}`;
  const image = asset?.kind === 'image' ? `<img src="${esc(asset.file)}" style="width:100%;height:${plan.height * .34}px;object-fit:contain" />` : '';
  scenes.push(`<section id="${sid}" class="clip scene" data-start="${start}" data-duration="${length}" data-track-index="1"><div class="brand">${esc(plan.product)}</div><h1>${esc(shot.title[language])}</h1><p>${esc(shot.body[language])}</p>${image}<div class="bar"><div id="bar-${shot.id}" class="fill"></div></div></section>`);
  if (asset?.kind === 'video') {
    media.push(`<video id="video-${shot.id}" class="clip" src="${esc(asset.file)}" muted data-start="${start}" data-duration="${length}" data-track-index="2" style="position:absolute;left:6.5%;top:48%;width:87%;height:34%;object-fit:contain"></video>`);
  }
  tweens.push(`tl.fromTo(${js('#bar-' + shot.id)}, {scaleX:0}, {scaleX:1,duration:${Math.max(1/plan.fps, length-1/plan.fps)},ease:'none'},${start});`);
  if (shot.startFrame !== 0) tweens.push(`tl.fromTo(${js('#' + sid)}, {opacity:0,y:18}, {opacity:1,y:0,duration:${Math.min(.3, length / 2)},ease:'power2.out'},${start});`);
}
for (const [index, caption] of plan.captions[language].entries()) {
  scenes.push(`<div class="clip caption" data-start="${caption.startFrame / plan.fps}" data-duration="${(caption.endFrame-caption.startFrame)/plan.fps}" data-track-index="3" id="caption-${index}">${esc(caption.text)}</div>`);
}
const track = plan.audio[language];
if (track.file) media.push(`<audio id="audio-${language}" class="clip" src="${esc(track.file)}" data-start="0" data-duration="${duration}" data-track-index="4"></audio>`);
fs.mkdirSync('public/vendor', {recursive: true});
fs.copyFileSync('node_modules/gsap/dist/gsap.min.js', 'public/vendor/gsap.min.js');
const html = `<!doctype html><html lang="${esc(language)}"><head><meta charset="utf-8"><title>${esc(plan.product)}</title><style>
html,body{margin:0;background:${esc(plan.theme.background)};width:${plan.width}px;height:${plan.height}px}
*{box-sizing:border-box}#root{position:relative;width:${plan.width}px;height:${plan.height}px;overflow:hidden;color:${esc(plan.theme.text)};font-family:${esc(plan.theme.fontFamily)}}
.scene{position:absolute;inset:0;padding:6.5%;display:flex;flex-direction:column;justify-content:center;gap:${plan.height * .025}px}
.brand{font-size:${scale * .025}px;letter-spacing:3px;color:${esc(plan.theme.accent)}}
h1{font-size:${scale * .07}px;line-height:1.18;max-width:100%;margin:0;overflow-wrap:anywhere}p{font-size:${scale * .036}px;line-height:1.5;margin:0;max-width:95%;overflow-wrap:anywhere}
.bar{position:absolute;left:6.5%;bottom:14%;width:87%;height:4px;background:#ffffff22}.fill{display:block;width:100%;height:4px;background:${esc(plan.theme.accent)};transform-origin:left}
.caption{position:absolute;left:7%;bottom:3.5%;width:86%;text-align:center;font-size:${scale * .035}px;line-height:1.4;padding:12px 20px;background:#000000b3;color:white;border-radius:8px;white-space:pre-line}
</style></head><body><div id="root" data-composition-id="${id}" data-width="${plan.width}" data-height="${plan.height}" data-fps="${plan.fps}" data-duration="${duration}">${scenes.join('')}${media.join('')}</div><script src="public/vendor/gsap.min.js"></script><script>
const tl=gsap.timeline({paused:true});${tweens.join('\n')}window.__timelines=window.__timelines||{};window.__timelines[${js(id)}]=tl;
</script></body></html>`;
fs.writeFileSync('index.html', html);
console.log(`已构建 ${language} HTML；画面数据在构建时冻结。`);
