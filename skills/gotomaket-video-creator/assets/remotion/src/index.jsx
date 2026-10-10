import React from 'react';
import {registerRoot, Composition} from 'remotion';
import plan from '../plan.json';
import {Promo} from './Promo.jsx';

const Root = () => <>{plan.languages.map(language => <Composition
  key={language} id={`Promo-${language}`} component={Promo}
  width={plan.width} height={plan.height} fps={plan.fps}
  durationInFrames={plan.durationFrames} defaultProps={{plan, language}}
/>)}</>;
registerRoot(Root);
