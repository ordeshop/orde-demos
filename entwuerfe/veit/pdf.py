"""Macht aus dem gebauten Entwurf ein PDF: jede Seite am Desktop (1440 px) und am Handy (390 px).
Aufruf: python3 entwuerfe/veit/pdf.py   (vorher build.py)"""
import pathlib, subprocess, sys, tempfile
from PIL import Image
HIER = pathlib.Path(__file__).resolve().parent
SEITEN = ["index", "produkte", "tunnelfinisher-tf-57", "anwendungen", "service", "unternehmen", "karriere", "kontakt"]
JS = r"""
const { chromium } = require('playwright');
const [site, out, seiten] = [process.argv[2], process.argv[3], process.argv[4].split(',')];
(async () => { const b = await chromium.launch();
 for (const [art, vp] of [['desktop', { width: 1440, height: 900 }], ['handy', { width: 390, height: 844 }]]) {
  const c = await b.newContext({ viewport: vp, reducedMotion: 'reduce', deviceScaleFactor: art === 'handy' ? 2 : 1 });
  for (const s of seiten) { const p = await c.newPage(); await p.goto('file://' + site + '/' + s + '.html');
   await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); });
   await p.waitForTimeout(400); await p.screenshot({ path: `${out}/${s}-${art}.png`, fullPage: true }); await p.close(); }
  await c.close(); }
 await b.close(); })();
"""
with tempfile.TemporaryDirectory() as tmp:
    js = pathlib.Path(tmp) / "shots.js"; js.write_text(JS)
    subprocess.run(["node", str(js), str(HIER.parent.parent / "demos" / "entwuerfe" / "veit"), tmp, ",".join(SEITEN)], check=True)
    seiten = []
    for s in SEITEN:
        d = Image.open(f"{tmp}/{s}-desktop.png").convert("RGB")
        h = Image.open(f"{tmp}/{s}-handy.png").convert("RGB")
        h = h.resize((h.width // 2, h.height // 2))
        # Desktop links, Handy rechts, auf einer Seite
        H = max(d.height, h.height) + 120
        blatt = Image.new("RGB", (d.width + h.width + 180, H), "#e9edf1")
        blatt.paste(d, (60, 60)); blatt.paste(h, (d.width + 120, 60))
        seiten.append(blatt)
    ziel = HIER / "Entwurf-veit.pdf"
    seiten[0].save(ziel, save_all=True, append_images=seiten[1:], resolution=110, quality=82)
    print(ziel, round(ziel.stat().st_size / 1e6, 1), "MB")
