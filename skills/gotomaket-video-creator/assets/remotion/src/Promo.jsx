import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate, Img, OffthreadVideo, Audio, staticFile} from 'remotion';

const mediaPath = file => staticFile(file.replace(/^public\//, ''));

function Shot({shot, plan, language}) {
  const frame = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const progress = interpolate(frame, [0, Math.max(1, shot.durationFrames - 1)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const reveal = shot.startFrame === 0 ? 1 : interpolate(frame, [0, Math.min(Math.round(.3 * fps), shot.durationFrames - 1)], [0, 1], {extrapolateRight: 'clamp'});
  const portrait = height > width;
  const asset = plan.assets.find(x => x.id === shot.assetId);
  return <AbsoluteFill style={{padding: width * .065, justifyContent: 'center', gap: height * .035, opacity: reveal}}>
    <div style={{fontSize: Math.min(width, height) * .025, color: plan.theme.accent, letterSpacing: 3}}>{plan.product}</div>
    <div style={{fontSize: Math.min(width, height) * .07, fontWeight: 700, maxWidth: width * .85, lineHeight: 1.18, overflowWrap: 'anywhere', transform: `translateY(${(1 - reveal) * 20}px)`}}>{shot.title[language]}</div>
    {shot.body[language] && <div style={{fontSize: Math.min(width, height) * .036, maxWidth: width * .8, lineHeight: 1.5, overflowWrap: 'anywhere'}}>{shot.body[language]}</div>}
    {asset && <div style={{height: height * (portrait ? .3 : .4), width: '100%', position: 'relative', overflow: 'hidden', borderRadius: 20}}>
      {asset.kind === 'image' ? <Img src={mediaPath(asset.file)} style={{width: '100%', height: '100%', objectFit: 'contain'}} /> :
        asset.kind === 'video' ? <OffthreadVideo src={mediaPath(asset.file)} muted style={{width: '100%', height: '100%', objectFit: 'contain'}} /> : null}
    </div>}
    <div style={{position: 'absolute', left: width * .065, bottom: height * .14, width: width * .87, height: 4, background: '#ffffff22'}}>
      <div style={{height: '100%', width: `${progress * 100}%`, background: plan.theme.accent}} />
    </div>
  </AbsoluteFill>;
}

export function Promo({plan, language}) {
  const frame = useCurrentFrame();
  const {height, width} = useVideoConfig();
  const caption = plan.captions[language].find(x => x.startFrame <= frame && frame < x.endFrame);
  const track = plan.audio[language];
  return <AbsoluteFill style={{background: plan.theme.background, color: plan.theme.text, fontFamily: plan.theme.fontFamily}}>
    {plan.shots.map(shot => <Sequence key={shot.id} from={shot.startFrame} durationInFrames={shot.durationFrames}>
      <Shot shot={shot} plan={plan} language={language}/>
    </Sequence>)}
    {track.file && <Audio src={mediaPath(track.file)} />}
    {caption && <div style={{position: 'absolute', bottom: height * .035, left: width * .07, width: width * .86, boxSizing: 'border-box', fontSize: Math.min(width, height) * .035, lineHeight: 1.4, textAlign: 'center', background: '#000000b3', color: 'white', padding: '12px 20px', borderRadius: 8, whiteSpace: 'pre-line'}}>{caption.text}</div>}
  </AbsoluteFill>;
}
