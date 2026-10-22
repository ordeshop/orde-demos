"""Baut die Seiten des Dream-Entwurfs aus Layout + Seiteninhalt.

Aufruf:  python3 entwuerfe/casino-dream-24/build.py
Quelle hier, fertige Seiten nach demos/entwuerfe/casino-dream-24/ (wird hochgeladen).
Jede Datei in seiten/ beginnt mit einer Kopfzeile:
  <!-- titel: … | beschreibung: … | nav: standorte -->
Platzhalter im Inhalt: {{ZEITEN:<slug>}} (Öffnungszeiten-Tabelle),
{{OFFEN:<slug>}} (data-Attribute für den Live-Status), {{STANDORTE_DETAIL}},
{{STANDORTE_UEBERSICHT}}, {{STANDORT_SPRUNG}}, {{STANDORT_OPTIONEN}}, {{STANDORTE_TELEFON}},
{{STANDORT_NAMEN}}, {{ANZAHL}}, {{ZENTRALE_TEL}}, {{ZENTRALE_TEL_LINK}},
{{ZENTRALE_MAIL}}, {{FIRMA}}. Alle Standortangaben stehen nur in STANDORTE.
PDF zum Weiterschicken danach mit:  python3 entwuerfe/pdf-erzeugen.py casino-dream-24
"""
import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent
SEITEN = HIER / "seiten"
ROOT = HIER.parent.parent / "demos" / "entwuerfe" / "casino-dream-24"

# Standorte. Quelle: Standortseite dream-spielcenter.de/spielhallen (Stand
# laut Suchindex etwa 2024) und Branchenverzeichnisse, abgeglichen 20.10.2026.
# open: Öffnungsstunde Mo..So (Feiertage wie Sonntag), close: Schluss am
# Folgetag um diese Stunde (0 = Mitternacht). alter: None = unbekannt.
# region: Großraum zur Orientierung. marke: Name des Hauses vor Ort, falls belegt.
# Kaufering heißt laut Verzeichnis (werkenntdenbesten.de) und Domain
# casino-dream24.de „Casino Dream 24“; die Domain leitet auf dream-spielcenter.de.
STANDORTE = {
    "fuessen": {
        "name": "Füssen", "region": "im Allgäu", "strasse": "Kemptener Str. 129", "zusatz": "",
        "plz": "87629", "ort": "Füssen", "tel": "08362 926299", "alter": None,
        "open": [9, 9, 9, 9, 9, 9, 11], "close": 3, "hinweis": "",
    },
    "heidenheim": {
        "name": "Heidenheim-Schnaitheim", "region": "", "strasse": "Riedstr. 3", "zusatz": "",
        "plz": "89520", "ort": "Heidenheim an der Brenz", "tel": "07321 609343", "alter": 18,
        "open": [6, 6, 6, 6, 6, 7, 8], "close": 0, "hinweis": "",
    },
    "kaufering": {
        "name": "Kaufering", "region": "bei Landsberg am Lech", "strasse": "Viktor-Frankl-Str. 15", "zusatz": "",
        "plz": "86916", "ort": "Kaufering", "tel": "08191 4299104", "alter": 21, "marke": "Casino Dream 24",
        "open": [9, 9, 9, 9, 9, 9, 11], "close": 3,
        "hinweis": "Zeiten prüfen: ein Verzeichnis nennt täglich 6 bis 3 Uhr",
    },
    "senden": {
        "name": "Senden", "region": "bei Ulm", "strasse": "Berliner Str. 9", "zusatz": "im Iller-Center",
        "plz": "89250", "ort": "Senden", "tel": "07307 32320", "alter": 21,
        "open": [9, 9, 9, 9, 9, 9, 11], "close": 3, "hinweis": "",
    },
    "wiesbaden": {
        "name": "Wiesbaden-Biebrich", "region": "", "strasse": "Didierstr. 27a", "zusatz": "",
        "plz": "65203", "ort": "Wiesbaden", "tel": "0611 608382", "alter": 21,
        "open": [10, 10, 10, 10, 10, 10, 12], "close": 4,
        "hinweis": "Adresse prüfen: manche Verzeichnisse nennen Äppelallee 27a",
    },
}
ZENTRALE = {
    "firma": "MSW Spiel + Freizeit GmbH", "ort": "Eislingen/Fils",
    "tel": "07161 98824-0", "mail": "info@dream-spielcenter.de",
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


def uhr(h):
    return "24:00" if h == 0 else f"{h:02d}:00"


def tel_link(nr):
    return "tel:+49" + nr.replace(" ", "").replace("-", "")[1:]


def maps_link(s):
    q = f"{s['strasse']} {s['plz']} {s['ort']}".replace(" ", "+")
    return f"https://www.google.com/maps/search/?api=1&amp;query={q}"


def zeiten(slug):
    """Tage mit gleichen Zeiten in eine Zeile, z. B. „Montag – Samstag“."""
    s = STANDORTE[slug]
    gruppen = []
    for i in range(7):
        if gruppen and s["open"][gruppen[-1][-1]] == s["open"][i]:
            gruppen[-1].append(i)
        else:
            gruppen.append([i])
    rows = []
    for g in gruppen:
        tage = TAGE[g[0]] if len(g) == 1 else f"{TAGE[g[0]]} – {TAGE[g[-1]]}"
        d = " ".join(str((i + 1) % 7) for i in g)  # JS-Wochentage: So = 0
        rows.append(f'<tr data-d="{d}"><th scope="row">{tage}</th><td>{uhr(s["open"][g[0]])} – {uhr(s["close"])}</td></tr>')
    return ('<table>\n<caption>Öffnungszeiten · an Feiertagen wie sonntags '
            '<span class="todo" style="margin:0 0 0 8px">bitte prüfen</span></caption>\n<tbody>\n'
            + "\n".join(rows) + "\n</tbody>\n</table>")


def offen(slug):
    s = STANDORTE[slug]
    return f'data-open="{",".join(map(str, s["open"]))}" data-close="{s["close"]}"'


def alter(s):
    if s["alter"]:
        return f'<li><i class="ti ti-id" aria-hidden="true"></i>Zutritt ab {s["alter"]}</li>'
    return '<li><i class="ti ti-id" aria-hidden="true"></i>Zutritt ab <span class="todo">18 oder 21?</span></li>'


def marke(s):
    return f'<p class="marke">{s["marke"]}</p>' if s.get("marke") else ""


def region(s):
    return f'<p class="region">{s["region"]}</p>' if s["region"] else ""


def standort_sprung():
    links = "".join(f'<li><a href="#{slug}">{s["name"].split("-")[0]}</a></li>' for slug, s in STANDORTE.items())
    return f'<nav class="jump h-a" aria-label="Zu einem Standort springen"><ul>{links}</ul></nav>'


def adresse(s):
    zusatz = f'<br>{s["zusatz"]}' if s["zusatz"] else ""
    return f'{s["strasse"]}{zusatz}<br>{s["plz"]} {s["ort"]}'


def standorte_detail():
    teile = []
    for n, (slug, s) in enumerate(STANDORTE.items()):
        hinweis = f'<span class="todo">{s["hinweis"]}</span>' if s["hinweis"] else ""
        wechsel = " flip" if n % 2 else ""
        teile.append(f"""      <article class="site-detail{wechsel}" id="{slug}" {offen(slug)}>
        <div class="loc-img rv" role="img" aria-label="Platzhalter für ein Foto der Außenansicht in {s["name"]}"><span class="photo">Foto Außenansicht</span><span class="neon" aria-hidden="true">dream</span><span class="no" aria-hidden="true">{n + 1:02d}</span></div>
        <div class="site-card rv" id="zeiten-{slug}">
          <span class="status" aria-live="polite">Öffnungszeiten prüfen</span>
          <div>{marke(s)}<h2>{s["name"]}</h2>{region(s)}</div>
          <address style="font-style:normal;color:var(--muted)">{adresse(s)}</address>{hinweis}
{zeiten(slug)}
          <ul class="facts" aria-label="Hinweise zum Standort">
            {alter(s)}
            <li><i class="ti ti-parking" aria-hidden="true"></i>Parken <span class="todo">?</span></li>
          </ul>
          <div class="loc-links">
            <a href="{maps_link(s)}" target="_blank" rel="noopener"><i class="ti ti-route" aria-hidden="true"></i>Route<span class="sr"> nach {s["name"]} (öffnet Google Maps)</span></a>
            <a href="{tel_link(s["tel"])}"><i class="ti ti-phone" aria-hidden="true"></i>{s["tel"]}</a>
          </div>
        </div>
      </article>""")
    return "\n".join(teile)


def standorte_uebersicht():
    teile = []
    for slug, s in STANDORTE.items():
        bis = {0: "bis Mitternacht"}.get(s["close"], f"bis {s['close']} Uhr nachts")
        teile.append(f"""        <article class="loc rv" {offen(slug)}>
          <div class="loc-body">
            <span class="status" aria-live="polite">Öffnungszeiten prüfen</span>
            <h3>{s["name"]}</h3>{region(s)}
            <address>{adresse(s)}</address>
            <p class="hint">Täglich geöffnet, {bis}</p>
            <div class="loc-links">
              <a href="standorte.html#{slug}"><i class="ti ti-clock" aria-hidden="true"></i>Zeiten<span class="sr"> in {s["name"]}</span></a>
              <a href="{maps_link(s)}" target="_blank" rel="noopener"><i class="ti ti-route" aria-hidden="true"></i>Route<span class="sr"> nach {s["name"]} (öffnet Google Maps)</span></a>
            </div>
          </div>
        </article>""")
    return "\n".join(teile)


def standort_optionen():
    return "".join(f"<option>{s['name']}</option>" for s in STANDORTE.values())


def standorte_telefon():
    return "\n".join(
        f'          <a href="{tel_link(s["tel"])}"><i class="ti ti-map-pin" aria-hidden="true"></i><span><small>{s["name"]}</small>{s["tel"]}</span></a>'
        for s in STANDORTE.values())


def standort_namen():
    namen = [s["name"].split("-")[0] for s in STANDORTE.values()]
    return ", ".join(namen[:-1]) + " und " + namen[-1]


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
    <p class="copy">© <span class="year">2026</span> Dream Spielcenter · {ZENTRALE["firma"]} · Teilnahme ab 18 Jahren, an vielen Standorten ab 21 · Glücksspiel kann süchtig machen. Hilfe: <a href="tel:08001372700">0800 1 37 27 00</a></p>
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
        ersatz = {
            "{{STANDORTE_DETAIL}}": standorte_detail(),
            "{{STANDORTE_UEBERSICHT}}": standorte_uebersicht(),
            "{{STANDORT_SPRUNG}}": standort_sprung(),
            "{{STANDORT_OPTIONEN}}": standort_optionen(),
            "{{STANDORTE_TELEFON}}": standorte_telefon(),
            "{{STANDORT_NAMEN}}": standort_namen(),
            "{{ANZAHL}}": str(len(STANDORTE)),
            "{{ZENTRALE_TEL}}": ZENTRALE["tel"],
            "{{ZENTRALE_TEL_LINK}}": tel_link(ZENTRALE["tel"]),
            "{{ZENTRALE_MAIL}}": ZENTRALE["mail"],
            "{{FIRMA}}": ZENTRALE["firma"],
        }
        for alt, neu in ersatz.items():
            inhalt = inhalt.replace(alt, neu)
        html = layout(datei.stem, meta["titel"], meta["beschreibung"], inhalt.rstrip())
        (ROOT / datei.name).write_text(html)
        print("gebaut:", datei.name)


if __name__ == "__main__":
    main()
