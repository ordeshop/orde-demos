"""Baut die Seiten des Dream-Entwurfs, Fassung 2 („Nachtfassung“).

Aufruf:  python3 entwuerfe/spielcenter-dream-24-v2/build.py
Quelle hier, fertige Seiten nach demos/entwuerfe/spielcenter-dream-24-v2/ (wird hochgeladen).
Jede Datei in seiten/ beginnt mit einer Kopfzeile:
  <!-- titel: … | beschreibung: … | nav: standorte -->
Platzhalter im Inhalt:
  {{LICHT}}              Lichtschein und unscharfe Lichtpunkte für die Bühne
  {{ZEITPLAN}}           alle Häuser als Zeitstrahl untereinander (Standorte)
  {{ZEILEN}}             alle Häuser als Zeilen mit kleinem Zeitstrahl
  {{STANDORTE_DETAIL}}   alle Häuser ausführlich mit Zeitstrahl und Tabelle
  {{STANDORT_SPRUNG}}    Sprungmarken zu den Häusern
  {{STANDORT_OPTIONEN}}, {{STANDORTE_TELEFON}}, {{STANDORT_NAMEN}},
  {{ANZAHL}}, {{ZAHLWORT}} (Fünf), {{ZAHLWORT_KLEIN}} (fünf),
  {{ZENTRALE_TEL}}, {{ZENTRALE_TEL_LINK}}, {{ZENTRALE_MAIL}}, {{FIRMA}},
  {{ICON:name}}          Icon aus dem Sprite (phone, route, pin, pfeil, extern, mail)
Alle Standortangaben stehen nur in STANDORTE.
PDF zum Weiterschicken danach mit:  python3 entwuerfe/pdf-erzeugen.py spielcenter-dream-24-v2
"""
import math
import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent
SEITEN = HIER / "seiten"
ROOT = HIER.parent.parent / "demos" / "entwuerfe" / "spielcenter-dream-24-v2"

# Standorte: dieselben Angaben wie in Fassung 1 (Quellen dort in der README).
# open: Öffnungsstunde Mo..So (Feiertage wie Sonntag), close: Schluss am
# Folgetag um diese Stunde (0 = Mitternacht). alter: None = unbekannt.
# region: Großraum zur Orientierung. marke: Name des Hauses vor Ort, falls belegt.
STANDORTE = {
    "fuessen": {
        "name": "Füssen", "region": "im Allgäu", "strasse": "Kemptener Str. 129", "zusatz": "",
        "plz": "87629", "ort": "Füssen", "tel": "08362 926299", "alter": None,
        "open": [9, 9, 9, 9, 9, 9, 11], "close": 3, "hinweis": "",
    },
    "heidenheim": {
        "name": "Heidenheim-Schnaitheim", "region": "an der Brenz", "strasse": "Riedstr. 3", "zusatz": "",
        "plz": "89520", "ort": "Heidenheim an der Brenz", "tel": "07321 609343", "alter": 18,
        "open": [6, 6, 6, 6, 6, 7, 8], "close": 0, "hinweis": "",
    },
    "kaufering": {
        "name": "Kaufering", "region": "bei Landsberg am Lech", "strasse": "Viktor-Frankl-Str. 15", "zusatz": "",
        "plz": "86916", "ort": "Kaufering", "tel": "08191 4299104", "alter": 21, "marke": "Spielcenter Dream 24",
        "open": [9, 9, 9, 9, 9, 9, 11], "close": 3,
        "hinweis": "Zeiten prüfen: ein Verzeichnis nennt täglich 6 bis 3 Uhr",
    },
    "senden": {
        "name": "Senden", "region": "bei Ulm", "strasse": "Berliner Str. 9", "zusatz": "im Iller-Center",
        "plz": "89250", "ort": "Senden", "tel": "07307 32320", "alter": 21,
        "open": [9, 9, 9, 9, 9, 9, 11], "close": 3, "hinweis": "",
    },
    "wiesbaden": {
        "name": "Wiesbaden-Biebrich", "region": "am Rhein", "strasse": "Didierstr. 27a", "zusatz": "",
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
ZAHLWORTE = {2: "Zwei", 3: "Drei", 4: "Vier", 5: "Fünf", 6: "Sechs", 7: "Sieben", 8: "Acht"}

NAV = [
    ("index", "Start"),
    ("standorte", "Standorte"),
    ("angebot", "Angebot"),
    ("jobs", "Jobs"),
    ("spielerschutz", "Spielerschutz"),
    ("kontakt", "Kontakt"),
]

# Unscharfe Lichtpunkte auf der Bühne: x %, y %, Durchmesser px, Farbe, Deckkraft
BOKEH = [
    (61, 22, 96, "246,115,31", .30), (70, 72, 58, "255,201,40", .34), (88, 28, 124, "227,23,27", .22),
    (94, 66, 74, "246,115,31", .28), (64, 88, 42, "227,23,27", .36), (82, 15, 44, "255,201,40", .34),
    (56, 48, 30, "255,201,40", .40), (97, 42, 50, "246,115,31", .26), (78, 93, 88, "227,23,27", .18),
    (73, 40, 9, "255,236,205", .9), (86, 55, 11, "255,236,205", .85), (58, 76, 8, "255,236,205", .9),
    (92, 85, 7, "255,236,205", .8), (66, 10, 8, "255,236,205", .75),
]

# Tabler Icons (MIT), Outline, Strichstärke 2
ICONS = {
    "phone": '<path d="M5 4h4l2 5l-2.5 1.5a11 11 0 0 0 5 5l1.5 -2.5l5 2v4a2 2 0 0 1 -2 2a16 16 0 0 1 -15 -15a2 2 0 0 1 2 -2"/>',
    "route": '<path d="M3 19a2 2 0 1 0 4 0a2 2 0 0 0 -4 0"/><path d="M19 7a2 2 0 1 0 0 -4a2 2 0 0 0 0 4"/><path d="M11 19h5.5a3.5 3.5 0 0 0 0 -7h-8a3.5 3.5 0 0 1 0 -7h4.5"/>',
    "pin": '<path d="M9 11a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"/><path d="M17.657 16.657l-4.243 4.243a2 2 0 0 1 -2.827 0l-4.244 -4.243a8 8 0 1 1 11.314 0"/>',
    "pfeil": '<path d="M5 12l14 0"/><path d="M13 18l6 -6"/><path d="M13 6l6 6"/>',
    "extern": '<path d="M17 7l-10 10"/><path d="M8 7l9 0l0 9"/>',
    "mail": '<path d="M3 7a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v10a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-10z"/><path d="M3 7l9 6l9 -6"/>',
}

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
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
""" + "\n".join(
    f'    <symbol id="i-{n}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    f'stroke-linecap="round" stroke-linejoin="round">{p}</symbol>' for n, p in ICONS.items()
) + """
  </defs>
</svg>"""


def icon(name):
    return f'<svg class="i" aria-hidden="true"><use href="#i-{name}"/></svg>'


def uhr_kurz(h):
    return "24" if h == 0 else str(h)


def uhr_lang(h):
    return "24:00" if h == 0 else f"{h:02d}:00"


def tel_link(nr):
    return "tel:+49" + nr.replace(" ", "").replace("-", "")[1:]


def maps_link(s):
    q = f"{s['strasse']} {s['plz']} {s['ort']}".replace(" ", "+")
    return f"https://www.google.com/maps/search/?api=1&amp;query={q}"


def gruppen(s):
    """Tage mit gleicher Öffnungsstunde zusammenfassen: [[0..5], [6]] usw."""
    g = []
    for i in range(7):
        if g and s["open"][g[-1][-1]] == s["open"][i]:
            g[-1].append(i)
        else:
            g.append([i])
    return g


def js_tage(g):
    return " ".join(str((i + 1) % 7) for i in g)  # JS-Wochentage: So = 0


def offen(s):
    return f'data-open="{",".join(map(str, s["open"]))}" data-close="{s["close"]}"'


def todo(text):
    return f'<span class="todo">{text}</span>'


def alter_text(s):
    return f"Zutritt ab {s['alter']}" if s["alter"] else "Zutritt ab " + todo("18 oder 21?")


def adresse(s, trenner="<br>"):
    zusatz = f'{trenner}{s["zusatz"]}' if s["zusatz"] else ""
    return f'{s["strasse"]}{zusatz}{trenner}{s["plz"]} {s["ort"]}'


def heute_text(s):
    """Text ohne JavaScript: Zeiten von Montag."""
    return f"{uhr_kurz(s['open'][0])} bis {uhr_kurz(s['close'])} Uhr"


# ---------- Zeitstrahl ----------
# Ein Tag läuft von 6 Uhr morgens bis 6 Uhr am nächsten Morgen, so bleiben
# Zeiten über Mitternacht ein durchgehender Balken. main.js setzt Balken und
# Strich „jetzt“ live; ohne JavaScript zeigt der Balken die Zeiten von Montag.

TAG_BEGINN = 6


def balken_stil(auf, zu):
    ende = 24 if zu == 0 else 24 + zu
    links = (auf - TAG_BEGINN) / 24 * 100
    breite = (ende - auf) / 24 * 100
    return f"left:{links:.2f}%;width:{breite:.2f}%"


ACHSE = [(0, "6"), (25, "12"), (50, "18"), (75, "24"), (100, "6")]


def achse(klasse):
    marken = "".join(f'<span style="left:{x}%">{text}</span>' for x, text in ACHSE)
    return f'<div class="{klasse}" aria-hidden="true">{marken}</div>'


def zeitband(s, mit_achse=False):
    band = (f'<div class="zeitband" aria-hidden="true">'
            f'<span class="zeitband-balken" style="{balken_stil(s["open"][0], s["close"])}" data-balken></span>'
            f'<span class="zeitband-jetzt" data-jetzt></span></div>')
    return band + (achse("zeitband-achse") if mit_achse else "")


def zeitplan():
    """Alle Häuser untereinander, ein gemeinsamer Strich für die Uhrzeit jetzt."""
    zeilen = "".join(
        f'<div class="zeitplan-zeile" {offen(s)}><span class="zeitplan-name">{s["name"].split("-")[0]}</span>{zeitband(s)}</div>'
        for s in STANDORTE.values())
    return (f'<figure class="zeitplan" aria-hidden="true">'
            f'<div class="zeitplan-flaeche">{zeilen}'
            f'<div class="zeitplan-jetzt" data-plan-jetzt><span data-uhrzeit></span></div></div>'
            f'{achse("zeitplan-achse")}</figure>')


# ---------- Bühne ----------

def licht():
    punkte = "".join(
        f'<span{" class=\"fern\"" if d < 16 else (" class=\"gross\"" if d >= 60 else "")} style="left:{x}%;top:{y}%;width:{d}px;height:{d}px;--farbe:{f};--deck:{o}"></span>'
        for x, y, d, f, o in BOKEH)
    return f'<div class="licht" aria-hidden="true"><div class="licht-schein"></div><div class="bokeh">{punkte}</div></div>'


# ---------- Listen ----------

def zeilen():
    teile = []
    for slug, s in STANDORTE.items():
        teile.append(f"""        <li class="zeile" {offen(s)}>
          <div class="zeile-ort">
            <h3><a href="standorte.html#{slug}">{s["name"]}</a></h3>
            <p>{s["region"]}</p>
          </div>
          <address>{adresse(s)}</address>
          <div class="zeile-zeit">
            {zeitband(s)}
            <p class="status"><span class="lampe" aria-hidden="true"></span><span data-status>{heute_text(s)}</span></p>
          </div>
          <div class="wege">
            <a class="weg" href="{maps_link(s)}" target="_blank" rel="noopener">{icon("route")}Route<span class="sr"> nach {s["name"]} (öffnet Google Maps)</span></a>
            <a class="weg" href="{tel_link(s["tel"])}">{icon("phone")}Anrufen<span class="sr"> in {s["name"]}: {s["tel"]}</span></a>
          </div>
        </li>""")
    return '<ul class="zeilen" role="list">\n' + "\n".join(teile) + "\n      </ul>"


def zeiten_tabelle(s):
    rows = []
    for g in gruppen(s):
        tage = TAGE[g[0]] if len(g) == 1 else f"{TAGE[g[0]]} – {TAGE[g[-1]]}"
        rows.append(f'<tr data-d="{js_tage(g)}"><th scope="row">{tage}</th>'
                    f'<td>{uhr_lang(s["open"][g[0]])} – {uhr_lang(s["close"])}</td></tr>')
    return ('<table class="zeiten">\n<caption>Öffnungszeiten, an Feiertagen wie sonntags '
            + todo("bitte prüfen") + '</caption>\n<tbody>\n' + "\n".join(rows) + "\n</tbody>\n</table>")


def standort_sprung():
    links = "".join(f'<li><a href="#{slug}">{s["name"].split("-")[0]}</a></li>' for slug, s in STANDORTE.items())
    return f'<nav class="sprung" aria-label="Zu einem Haus springen"><ul role="list">{links}</ul></nav>'


def standorte_detail():
    teile = []
    for slug, s in STANDORTE.items():
        hinweis = f'<p>{todo(s["hinweis"])}</p>' if s["hinweis"] else ""
        unterzeile = " · ".join(t for t in (s.get("marke"), s["region"]) if t)
        teile.append(f"""      <article class="detail" id="{slug}" {offen(s)}>
        <div class="detail-kopf">
          <h2>{s["name"]}</h2>
          <p class="detail-unter">{unterzeile}</p>
          <p class="status"><span class="lampe" aria-hidden="true"></span><span data-status>{heute_text(s)}</span></p>
          <div class="detail-band">{zeitband(s, mit_achse=True)}</div>
        </div>
        <div class="detail-zeiten">
          {zeiten_tabelle(s)}
        </div>
        <div class="detail-info">
          <address>{adresse(s)}</address>
          {hinweis}
          <ul class="fakten" role="list">
            <li>{alter_text(s)}, Ausweis mitbringen</li>
            <li>Parken {todo("vor dem Haus?")}</li>
          </ul>
          <div class="wege">
            <a class="weg" href="{maps_link(s)}" target="_blank" rel="noopener">{icon("route")}Route<span class="sr"> nach {s["name"]} (öffnet Google Maps)</span></a>
            <a class="weg" href="{tel_link(s["tel"])}">{icon("phone")}{s["tel"]}</a>
          </div>
        </div>
      </article>""")
    return "\n".join(teile)


def standort_optionen():
    return "".join(f"<option>{s['name']}</option>" for s in STANDORTE.values())


def standorte_telefon():
    return "\n".join(
        f'          <li><a href="{tel_link(s["tel"])}"><span>{s["name"]}</span><span class="nr">{s["tel"]}</span></a></li>'
        for s in STANDORTE.values())


def standort_namen():
    namen = [s["name"].split("-")[0] for s in STANDORTE.values()]
    return ", ".join(namen[:-1]) + " und " + namen[-1]


# ---------- Seite ----------

def layout(name, titel, beschreibung, inhalt):
    menu = []
    for slug, label in NAV[1:]:
        cur = ' aria-current="page"' if slug == name else ""
        menu.append(f'<li><a href="{slug}.html"{cur}>{label}</a></li>')
    fuss = "".join(f'<li><a href="{s}.html">{l}</a></li>' for s, l in NAV[1:])
    voll_titel = "Dream Spielcenter – Spielhallen von Wiesbaden bis Füssen" if name == "index" else f"{titel} – Dream Spielcenter"
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{voll_titel}</title>
<meta name="description" content="{beschreibung}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#050505">
<meta name="color-scheme" content="dark">
<link rel="preload" href="assets/fonts/bodoni-moda-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<aside class="entwurf" aria-label="Hinweis zum Entwurf"><p><b>Entwurf</b> · Gestaltungsvorschlag von ORDÉ. Fotos, Texte und Angaben stimmen wir mit Ihnen ab.</p></aside>

<!-- Logo als SVG-Nachbau; wird durch die Original-Logodatei ersetzt -->
{SPRITE}

<header class="kopf">
  <div class="wrap kopf-in">
    <a class="logo" href="index.html" aria-label="Dream Spielcenter – zur Startseite"><svg viewBox="0 0 480 230"><use href="#logo"/></svg></a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu"><span class="sr">Menü</span><span class="burger-striche" aria-hidden="true"></span></button>
    <nav aria-label="Hauptnavigation">
      <ul class="menu" id="menu" role="list">
        {"".join(menu)}
      </ul>
    </nav>
  </div>
</header>

<main id="inhalt">
{inhalt}
</main>

<footer class="fuss">
  <div class="wrap fuss-in">
    <div class="fuss-marke">
      <a class="logo" href="index.html" aria-label="Zur Startseite"><svg viewBox="0 0 480 230"><use href="#logo"/></svg></a>
      <p>Dream Spielcenter<br>{ZENTRALE["firma"]}<br>{ZENTRALE["ort"]}</p>
    </div>
    <div class="fuss-kontakt">
      <a href="{tel_link(ZENTRALE["tel"])}">{icon("phone")}{ZENTRALE["tel"]}</a>
      <a href="mailto:{ZENTRALE["mail"]}">{icon("mail")}{ZENTRALE["mail"]}</a>
    </div>
    <nav aria-label="Seiten im Fuß">
      <ul role="list">{fuss}<li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li></ul>
    </nav>
  </div>
  <div class="wrap fuss-recht">
    <p>Zutritt ab 18 Jahren, an den meisten Standorten ab 21. Glücksspiel kann süchtig machen. Kostenlose Beratung der BZgA: <a href="tel:08001372700">0800 1 37 27 00</a></p>
    <p>© <span class="jahr">2026</span> Dream Spielcenter</p>
  </div>
</footer>

<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


def main():
    anzahl = len(STANDORTE)
    ersatz = {
        "{{LICHT}}": licht,
        "{{ZEITPLAN}}": zeitplan,
        "{{ZEILEN}}": zeilen,
        "{{STANDORTE_DETAIL}}": standorte_detail,
        "{{STANDORT_SPRUNG}}": standort_sprung,
        "{{STANDORT_OPTIONEN}}": standort_optionen,
        "{{STANDORTE_TELEFON}}": standorte_telefon,
        "{{STANDORT_NAMEN}}": standort_namen,
        "{{ANZAHL}}": lambda: str(anzahl),
        "{{ZAHLWORT}}": lambda: ZAHLWORTE.get(anzahl, str(anzahl)),
        "{{ZAHLWORT_KLEIN}}": lambda: ZAHLWORTE.get(anzahl, str(anzahl)).lower(),
        "{{ZENTRALE_TEL}}": lambda: ZENTRALE["tel"],
        "{{ZENTRALE_TEL_LINK}}": lambda: tel_link(ZENTRALE["tel"]),
        "{{ZENTRALE_MAIL}}": lambda: ZENTRALE["mail"],
        "{{FIRMA}}": lambda: ZENTRALE["firma"],
    }
    for alt in ROOT.glob("*.html"):
        alt.unlink()
    for datei in sorted(SEITEN.glob("*.html")):
        text = datei.read_text()
        kopf, inhalt = text.split("\n", 1)
        meta = dict(teil.split(":", 1) for teil in kopf.strip()[4:-3].split("|"))
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        for alt, neu in ersatz.items():
            if alt in inhalt:
                inhalt = inhalt.replace(alt, neu())
        inhalt = re.sub(r"\{\{ICON:(\w+)\}\}", lambda m: icon(m.group(1)), inhalt)
        rest = re.findall(r"\{\{[^}]+\}\}", inhalt)
        if rest:
            raise SystemExit(f"{datei.name}: unbekannte Platzhalter {rest}")
        html = layout(datei.stem, meta["titel"], meta["beschreibung"], inhalt.rstrip())
        (ROOT / datei.name).write_text(html)
        print("gebaut:", datei.name)


if __name__ == "__main__":
    main()
