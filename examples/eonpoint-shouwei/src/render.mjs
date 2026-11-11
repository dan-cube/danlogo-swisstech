// SVG -> PNG with resvg.
// usage: node render.mjs in.svg out.png [width=1600] [--fonts]
//   --fonts  load system fonts (needed only when the SVG contains <text>, e.g. scene mock-ups).
//            Logo files themselves should contain outlines only, never <text>.
//            Fonts resvg can reach: macOS — Hiragino Sans GB, STHeiti, Helvetica Neue, Avenir Next, Menlo
//            (PingFang lives in a system asset folder resvg cannot see); Linux — Noto Sans CJK SC, DejaVu Sans.
//            List several families in font-family; prefer half-width punctuation in labels.
import { createRequire } from 'module';
import fs from 'fs';
import os from 'os';
import path from 'path';

const base = process.env.DANLOGO_HOME || path.join(os.homedir(), '.danlogo');
const require = createRequire(path.join(base, 'node', 'package.json'));
let Resvg;
try {
  ({ Resvg } = require('@resvg/resvg-js'));
} catch (e) {
  console.error(`@resvg/resvg-js not found under ${base}/node — run scripts/setup.sh first.`);
  process.exit(1);
}

const args = process.argv.slice(2);
const fonts = args.includes('--fonts');
const [inp, out, w] = args.filter(a => a !== '--fonts');
if (!inp || !out) {
  console.error('usage: node render.mjs in.svg out.png [width] [--fonts]');
  process.exit(1);
}
const svg = fs.readFileSync(inp, 'utf8');
const r = new Resvg(svg, {
  fitTo: { mode: 'width', value: parseInt(w || '1600', 10) },
  font: { loadSystemFonts: fonts, defaultFontFamily: 'Hiragino Sans GB' },
});
fs.writeFileSync(out, r.render().asPng());
