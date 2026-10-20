"""Baut die Seiten des Dream-Entwurfs aus Layout + Seiteninhalt.

Aufruf:  python3 entwuerfe/dream-spielcenter/build.py
Quelle hier, fertige Seiten nach demos/entwuerfe/dream-spielcenter/ (wird hochgeladen).
Jede Datei in seiten/ beginnt mit einer Kopfzeile:
  <!-- titel: … | beschreibung: … | nav: standorte -->
Platzhalter im Inhalt: {{ZEITEN:<slug>}} (Öffnungszeiten-Tabelle),
{{OFFEN:<slug>}} (data-Attribute für den Live-Status).
Danach baut vorschau.py die Ein-Datei-Vorschau.
"""
import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent
SEITEN = HIER / "seiten"
ROOT = HIER.parent.parent / "demos" / "entwuerfe" / "dream-spielcenter"

# Standorte. Öffnungsstunden Mo..So, Schluss am Folgetag um CLOSE Uhr.
STANDORTE = {
    "kaufering": {"open": [9, 9, 9, 9, 9, 9, 11], "close": 3},
}
TAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

NAV = [
    ("index", "Start"),
    ("angebot", "Angebot"),
    ("standorte", "Standorte"),
    ("jobs", "Jobs"),
    ("spielerschutz", "Spielerschutz"),
    ("kontakt", "Kontakt"),
]

LOGO = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <radialGradient id="lg" cx="50%" cy="55%" r="60%">
      <stop offset="0" stop-color="#ffd23a"/><stop offset=".45" stop-color="#ff8a1e"/><stop offset="1" stop-color="#e3171b"/>
    </radialGradient>
    <symbol id="logo" viewBox="0 0 480 230">
      <ellipse cx="240" cy="115" rx="232" ry="107" fill="#e3171b" stroke="#fff" stroke-width="7"/>
      <ellipse cx="240" cy="115" rx="218" ry="94" fill="url(#lg)"/>
      <text x="236" y="152" text-anchor="middle" font-family="Lobster, cursive" font-size="132" fill="#fff" stroke="#c40f12" stroke-width="5" paint-order="stroke" transform="rotate(-6 240 115)">dream</text>
      <path d="M388 46l6 15 16 1-12 10 4 16-14-9-14 9 4-16-12-10 16-1z" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>
    </symbol>
  </defs>
</svg>"""


def zeiten(slug):
    s = STANDORTE[slug]
    rows = []
    for i, tag in enumerate(TAGE):
        d = (i + 1) % 7  # JS-Wochentag: So = 0
        rows.append(f'<tr data-d="{d}"><th scope="row">{tag}</th><td>{s["open"][i]:02d}:00 – {s["close"]:02d}:00</td></tr>')
    return "<table>\n<caption>Öffnungszeiten <span class=\"todo\" style=\"margin:0 0 0 8px\">bitte prüfen</span></caption>\n<tbody>\n" + "\n".join(rows) + "\n</tbody>\n</table>"


def offen(slug):
    s = STANDORTE[slug]
    return f'data-open="{",".join(map(str, s["open"]))}" data-close="{s["close"]}"'


def layout(name, titel, beschreibung, inhalt):
    menu = []
    for slug, label in NAV[1:]:
        cur = ' aria-current="page"' if slug == name else ""
        menu.append(f'<li><a href="{slug}.html"{cur}>{label}</a></li>')
    fuss = "".join(f'<li><a href="{s}.html">{l}</a></li>' for s, l in NAV[1:])
    voll_titel = "Dream Spielcenter – Willkommen im Dream" if name == "index" else f"{titel} – Dream Spielcenter"
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{voll_titel}</title>
<meta name="description" content="{beschreibung}">
<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="assets/icons/tabler-icons.min.css">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<div class="draft" role="note"><b>Entwurf</b> – Gestaltungsvorschlag von ORDÉ. Fotos, Texte und Angaben werden mit Ihnen abgestimmt.</div>

<!-- Logo als SVG-Nachbau; wird durch die Original-Logodatei ersetzt -->
{LOGO}

<header class="top">
  <div class="wrap top-in">
    <a class="logo" href="index.html" aria-label="Dream Spielcenter – zur Startseite"><svg viewBox="0 0 480 230"><use href="#logo"/></svg></a>
    <button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Menü öffnen"><span></span><span></span><span></span></button>
    <nav aria-label="Hauptnavigation">
      <ul class="menu" id="menu">
        {"".join(menu)}
        <li><a class="cta-s" href="standorte.html"><i class="ti ti-map-pin" aria-hidden="true"></i>&nbsp;Standort finden</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="inhalt">
{inhalt}
</main>

<footer>
  <div class="wrap">
    <div class="foot">
      <a class="logo" href="index.html" aria-label="Zur Startseite"><svg viewBox="0 0 480 230"><use href="#logo"/></svg></a>
      <ul>{fuss}<li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li></ul>
      <div class="social">
        <a href="#" aria-label="Dream auf Facebook"><i class="ti ti-brand-facebook" aria-hidden="true"></i></a>
        <a href="#" aria-label="Dream auf Instagram"><i class="ti ti-brand-instagram" aria-hidden="true"></i></a>
      </div>
    </div>
    <p class="copy">© <span class="year">2026</span> Dream Spielcenter · Teilnahme ab 21 Jahren · Glücksspiel kann süchtig machen. Hilfe: <a href="tel:08001372700">0800 1 37 27 00</a></p>
  </div>
</footer>

<script src="assets/js/gsap.min.js"></script>
<script src="assets/js/ScrollTrigger.min.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>
"""


def main():
    for datei in sorted(SEITEN.glob("*.html")):
        text = datei.read_text()
        kopf, inhalt = text.split("\n", 1)
        meta = dict(teil.split(":", 1) for teil in kopf.strip()[4:-3].split("|"))
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        inhalt = re.sub(r"\{\{ZEITEN:(\w+)\}\}", lambda m: zeiten(m.group(1)), inhalt)
        inhalt = re.sub(r"\{\{OFFEN:(\w+)\}\}", lambda m: offen(m.group(1)), inhalt)
        html = layout(datei.stem, meta["titel"], meta["beschreibung"], inhalt.rstrip())
        (ROOT / datei.name).write_text(html)
        print("gebaut:", datei.name)


if __name__ == "__main__":
    main()
