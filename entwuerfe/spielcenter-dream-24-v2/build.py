"""Baut die Seiten des Dream-Entwurfs, Fassung 2 („Nachtfassung“).

Aufruf:  python3 entwuerfe/spielcenter-dream-24-v2/build.py
Quelle hier, fertige Seiten nach demos/entwuerfe/spielcenter-dream-24-v2/ (wird hochgeladen).
Jede Datei in seiten/ beginnt mit einer Kopfzeile:
  <!-- titel: … | beschreibung: … | nav: standorte -->
Platzhalter im Inhalt:
  {{LICHT}}              Lichthof und Funken für die Bühne
  {{AUTOMAT}}            Spielautomat der Startseite: fünf Walzen, Intro in main.js
  {{AUTOMAT_KLEIN}}      kleiner Automat mit drei Walzen, steht still (Angebot)
  {{ANZEIGE}} … {{/ANZEIGE}}  Anzeigetafel im Stil des Automaten; {{ANZEIGE:ruhig}} ohne Lauflicht
  {{FINDER}}             Knopf „Nächstes Dream finden“
  {{HAEUSER_JETZT}}      Tafel „Die Häuser jetzt“ mit allen Häusern (Kontakt)
  {{HAEUSER_DATEN}}      unsichtbare Häuserliste für die Live-Zeile (Jobs)
  {{ZIER}}               der Stern aus dem Logo zwischen zwei Linien
  {{FOTO:hoch|quer|breit:Bildidee}}  Fotoplatz mit Bildidee und Format
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
import hashlib
import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent
SEITEN = HIER / "seiten"
ROOT = HIER.parent.parent / "demos" / "entwuerfe" / "spielcenter-dream-24-v2"

# Standorte: dieselben Angaben wie in Fassung 1 (Quellen dort in der README).
# open: Öffnungsstunde Mo..So (Feiertage wie Sonntag), close: Schluss am
# Folgetag um diese Stunde (0 = Mitternacht). alter: None = unbekannt.
# region: Großraum zur Orientierung. marke: Name des Hauses vor Ort, falls belegt.
# geo: Breite, Länge aus OpenStreetMap (Nominatim) zur Adresse, 25.10.2026 (für „Nächstes Dream“).
# Reihenfolge von Norden nach Süden, passend zu „Von Wiesbaden bis Füssen“.
STANDORTE = {
    "wiesbaden": {
        "name": "Wiesbaden-Biebrich", "region": "am Rhein", "strasse": "Didierstr. 27a", "zusatz": "",
        "plz": "65203", "ort": "Wiesbaden", "tel": "0611 608382", "alter": 21,
        "open": [10, 10, 10, 10, 10, 10, 12], "close": 4,
        "hinweis": "Adresse prüfen: manche Verzeichnisse nennen Äppelallee 27a",
        "geo": (50.04788, 8.23878),  # nur die Straße gefunden
    },
    "heidenheim": {
        "name": "Heidenheim-Schnaitheim", "region": "an der Brenz", "strasse": "Riedstr. 3", "zusatz": "",
        "plz": "89520", "ort": "Heidenheim an der Brenz", "tel": "07321 609343", "alter": 18,
        "open": [6, 6, 6, 6, 6, 7, 8], "close": 0, "hinweis": "", "geo": (48.71460, 10.16133),
    },
    "senden": {
        "name": "Senden", "region": "bei Ulm", "strasse": "Berliner Str. 9", "zusatz": "im Iller-Center",
        "plz": "89250", "ort": "Senden", "tel": "07307 32320", "alter": 21,
        "open": [9, 9, 9, 9, 9, 9, 11], "close": 3, "hinweis": "", "geo": (48.33084, 10.03914),
    },
    "kaufering": {
        "name": "Kaufering", "region": "bei Landsberg am Lech", "strasse": "Viktor-Frankl-Str. 15", "zusatz": "",
        "plz": "86916", "ort": "Kaufering", "tel": "08191 4299104", "alter": 21, "marke": "Spielcenter Dream 24",
        "open": [9, 9, 9, 9, 9, 9, 11], "close": 3,
        "hinweis": "Zeiten prüfen: ein Verzeichnis nennt täglich 6 bis 3 Uhr", "geo": (48.08014, 10.85458),
    },
    "fuessen": {
        "name": "Füssen", "region": "im Allgäu", "strasse": "Kemptener Str. 129", "zusatz": "",
        "plz": "87629", "ort": "Füssen", "tel": "08362 926299", "alter": None,
        "open": [9, 9, 9, 9, 9, 9, 11], "close": 3, "hinweis": "", "geo": (47.56845, 10.66793),
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

# Winzige Funken links und rechts vom Automaten: x %, y %, Durchmesser px
FUNKEN = [(13, 19, 2), (19, 33, 3), (23, 13, 2), (16, 45, 2), (79, 16, 3), (84, 31, 2), (88, 22, 2), (81, 44, 3)]

# Tabler Icons (MIT), Outline, Strichstärke 2
ICONS = {
    "phone": '<path d="M5 4h4l2 5l-2.5 1.5a11 11 0 0 0 5 5l1.5 -2.5l5 2v4a2 2 0 0 1 -2 2a16 16 0 0 1 -15 -15a2 2 0 0 1 2 -2"/>',
    "route": '<path d="M3 19a2 2 0 1 0 4 0a2 2 0 0 0 -4 0"/><path d="M19 7a2 2 0 1 0 0 -4a2 2 0 0 0 0 4"/><path d="M11 19h5.5a3.5 3.5 0 0 0 0 -7h-8a3.5 3.5 0 0 1 0 -7h4.5"/>',
    "pin": '<path d="M9 11a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"/><path d="M17.657 16.657l-4.243 4.243a2 2 0 0 1 -2.827 0l-4.244 -4.243a8 8 0 1 1 11.314 0"/>',
    "pfeil": '<path d="M5 12l14 0"/><path d="M13 18l6 -6"/><path d="M13 6l6 6"/>',
    "extern": '<path d="M17 7l-10 10"/><path d="M8 7l9 0l0 9"/>',
    "mail": '<path d="M3 7a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v10a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-10z"/><path d="M3 7l9 6l9 -6"/>',
    "pause": '<path d="M6 6a1 1 0 0 1 1 -1h2a1 1 0 0 1 1 1v12a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1l0 -12"/><path d="M14 6a1 1 0 0 1 1 -1h2a1 1 0 0 1 1 1v12a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1l0 -12"/>',
    "play": '<path d="M7 4v16l13 -8l-13 -8"/>',
}

# Symbole auf den Walzen des Automaten (Tabler Icons, MIT), mit feinerer Linie
WALZEN_ICONS = {
    "glocke": '<path d="M10 5a2 2 0 1 1 4 0a7 7 0 0 1 4 6v3a4 4 0 0 0 2 3h-16a4 4 0 0 0 2 -3v-3a7 7 0 0 1 4 -6"/><path d="M9 17v1a3 3 0 0 0 6 0v-1"/>',
    "kirsche": '<path d="M4 16.5a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0 -7 0"/><path d="M14 18a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"/><path d="M9 13c.366 -2 1.866 -3.873 4.5 -5.6"/><path d="M17 15c-1.333 -2.333 -2.333 -5.333 -1 -9"/><path d="M5 6c3.667 -2.667 7.333 -2.667 11 0c-3.667 2.667 -7.333 2.667 -11 0"/>',
    "krone": '<path d="M12 6l4 6l5 -4l-2 10h-14l-2 -10l5 4l4 -6"/>',
}

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <radialGradient id="lg" cx="50%" cy="55%" r="60%">
      <stop offset="0" stop-color="#ffd23a"/><stop offset=".45" stop-color="#ff8a1e"/><stop offset="1" stop-color="#e3171b"/>
    </radialGradient>
    <symbol id="stern" viewBox="364 44 48 46"><path d="M388 46l6 15 16 1-12 10 4 16-14-9-14 9 4-16-12-10 16-1z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/></symbol>
    <symbol id="logo" viewBox="0 0 480 230">
      <ellipse cx="240" cy="115" rx="232" ry="107" fill="#e3171b" stroke="#fff" stroke-width="7"/>
      <ellipse cx="240" cy="115" rx="218" ry="94" fill="url(#lg)"/>
      <text x="236" y="152" text-anchor="middle" font-family="Lobster, cursive" font-size="132" fill="#fff" stroke="#c40f12" stroke-width="5" paint-order="stroke" transform="rotate(-6 240 115)">dream</text>
      <path d="M388 46l6 15 16 1-12 10 4 16-14-9-14 9 4-16-12-10 16-1z" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>
    </symbol>
""" + "\n".join(
    f'    <symbol id="i-{n}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    f'stroke-linecap="round" stroke-linejoin="round">{p}</symbol>' for n, p in ICONS.items()
) + "\n" + "\n".join(
    f'    <symbol id="w-{n}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" '
    f'stroke-linecap="round" stroke-linejoin="round">{p}</symbol>' for n, p in WALZEN_ICONS.items()
) + """
  </defs>
</svg>"""

# Kopfskript der Startseite, vor dem ersten Bild: übernimmt „Bewegung anhalten“ aus einem früheren
# Besuch und entscheidet, ob das Intro läuft (einmal je Besuch, nicht bei „Bewegung reduzieren“ oder
# angehaltener Bewegung). Notaus nach 3 s, falls main.js nicht lädt (main.js startet das Intro ohnehin
# nur, wenn es in den ersten 2,5 s ankommt).
INTRO_SKRIPT = ('<script>try{var d=document.documentElement,aus=localStorage.getItem("dream-bewegung")==="aus";'
                'if(aus)d.classList.add("bewegung-aus");'
                'if(!aus&&!matchMedia("(prefers-reduced-motion: reduce)").matches&&!sessionStorage.getItem("dream-intro"))'
                '{d.classList.add("intro");window.dreamNotaus=setTimeout(function(){d.classList.remove("intro","intro-an")},3000)}'
                '}catch(e){}</script>')


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


def geo(s):
    return f'data-geo="{s["geo"][0]},{s["geo"][1]}"'


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
    funken = "".join(f'<span style="left:{x}%;top:{y}%;--d:{d}px"></span>' for x, y, d in FUNKEN)
    return f'<div class="licht" aria-hidden="true"><div class="licht-schein"></div><div class="funken">{funken}</div></div>'


# Automat: fünf Walzen, fünf Häuser. Jede Walze bleibt auf dem Dream-Schild stehen, daneben
# die klassischen Symbole, je Walze in eigener Reihenfolge (sonst sehen die Nachbarn über und
# unter der Linie nach Muster aus). Ohne JS steht der Endzustand da; main.js lässt die Walzen
# beim ersten Besuch drehen.
WALZEN_FOLGEN = [
    ["sieben", "glocke", "kirsche", "stern", "krone"],
    ["kirsche", "krone", "sieben", "glocke", "stern"],
    ["stern", "sieben", "krone", "kirsche", "glocke"],
    ["glocke", "stern", "kirsche", "krone", "sieben"],
    ["krone", "stern", "glocke", "sieben", "kirsche"],
]
WALZEN_RUNDEN = 8   # so oft wiederholt sich die Symbolfolge auf jedem Streifen (Anlauf fürs Drehen)
WALZEN_ZIEL = 6     # Zelle mit dem Dream-Schild, die am Ende auf der Gewinnlinie steht
LAMPEN = 24         # Lampen je Reihe


def symbol(name):
    if name == "dream":
        return '<svg class="sym sym-dream" viewBox="0 0 480 230"><use href="#logo"/></svg>'
    if name == "sieben":
        return '<span class="sym sym-sieben">7</span>'
    if name == "stern":
        return '<svg class="sym sym-linie" viewBox="0 0 48 46"><use href="#stern"/></svg>'
    return f'<svg class="sym sym-linie" viewBox="0 0 24 24"><use href="#w-{name}"/></svg>'


def automat():
    walzen = []
    for j in range(len(STANDORTE)):
        zellen = (["dream"] + WALZEN_FOLGEN[j % len(WALZEN_FOLGEN)]) * WALZEN_RUNDEN
        n = len(zellen)
        streifen = "".join(f'<span class="zelle{" treffer" if k == WALZEN_ZIEL else ""}">{symbol(s)}</span>'
                           for k, s in enumerate(zellen))
        # Die Zielzelle steht in der mittleren Reihe; das Fenster zeigt 2,6 Zellen, oben 0,8 angeschnitten
        lage = -(WALZEN_ZIEL - .8) / n * 100
        walzen.append(f'<div class="walze" style="--j:{j}"><div class="streifen" data-streifen data-n="{n}" data-ziel="{WALZEN_ZIEL}" '
                      f'style="--ziel:{lage:.4f}%">{streifen}</div></div>')
    return (f'<div class="automat" data-automat aria-hidden="true" style="--lampen:{LAMPEN}">'
            f'<span class="automat-streif"></span><span class="automat-blitz"></span>'
            f'<div class="automat-rahmen">{lampen("oben")}'
            f'<div class="walzen" style="--n:{len(STANDORTE)}"><span class="gewinnlinie"></span>{"".join(walzen)}</div>'
            f'<span class="zeiger zeiger-l"></span><span class="zeiger zeiger-r"></span>'
            f'{lampen("unten")}</div></div>')


def lampen(reihe):
    """Eine Reihe Lampen; --k ist der Platz im Lauflicht."""
    return f'<span class="lampen lampen-{reihe}">' + "".join(f'<i style="--k:{k}"></i>' for k in range(LAMPEN)) + "</span>"


# Kleiner Automat für „Angebot“: drei Walzen, steht still. Auf der Linie 7 · Dream · Glocke, also kein Treffer.
KLEIN_WALZEN = [["krone", "sieben", "kirsche"], ["stern", "dream", "glocke"], ["kirsche", "glocke", "sieben"]]


def automat_klein():
    lage = -(1 - .8) / 3 * 100  # mittlere von drei Zellen auf der Linie, wie beim großen Automaten
    walzen = "".join(f'<div class="walze"><div class="streifen" style="--ziel:{lage:.4f}%">'
                     + "".join(f'<span class="zelle">{symbol(s)}</span>' for s in zellen) + "</div></div>"
                     for zellen in KLEIN_WALZEN)
    return (f'<div class="automat automat-klein buehne-anzeige" aria-hidden="true" style="--lampen:{LAMPEN}">'
            f'<div class="automat-rahmen">{lampen("oben")}'
            f'<div class="walzen" style="--n:{len(KLEIN_WALZEN)}"><span class="gewinnlinie"></span>{walzen}</div>'
            f'<span class="zeiger zeiger-l"></span><span class="zeiger zeiger-r"></span>{lampen("unten")}</div></div>')


def anzeige_anfang(art=""):
    """Anzeigetafel im Stil des Automaten (Rahmen, Goldkante, Lampen) für die Bühne der Unterseiten.
    Inhalt zwischen {{ANZEIGE}} und {{/ANZEIGE}}; {{ANZEIGE:ruhig}} ohne Lauflicht."""
    klasse = " ".join(filter(None, ["anzeige", "buehne-anzeige", art]))
    return f'<div class="{klasse}" style="--lampen:{LAMPEN}">{lampen("oben")}<div class="anzeige-in">'


def anzeige_ende():
    return f'</div>{lampen("unten")}</div>'


def finder():
    """Knopf „Nächstes Dream finden“; main.js zeigt ihn nur, wenn der Browser orten kann."""
    return (f'<div class="finder" data-finder hidden>'
            f'<button class="btn btn-kontur" type="button" data-finder-knopf>{icon("pin")}<span>Nächstes Dream finden</span></button>'
            f'<p class="finder-hinweis">Ihr Standort bleibt auf Ihrem Gerät.</p>'
            f'<div class="finder-ergebnis" data-finder-ergebnis aria-live="polite"></div></div>')


def haeuser_jetzt():
    """Tafel „Die Häuser jetzt“ (Kontakt): main.js setzt den Live-Status, ohne JavaScript stehen die Zeiten von Montag da."""
    zeilen = "".join(f'<li {offen(s)}><span class="tafel-name">{s["name"].split("-")[0]}</span>'
                     f'<span class="status"><span class="lampe" aria-hidden="true"></span><span data-status>{heute_text(s)}</span></span></li>'
                     for s in STANDORTE.values())
    return f'<ul class="tafel" role="list">{zeilen}</ul>'


def haeuser_daten():
    """Unsichtbare Häuserliste für die Live-Zeile auf Seiten ohne Häuser (Jobs)."""
    return "<ul hidden>" + "".join(f'<li data-name="{s["name"].split("-")[0]}" {offen(s)}></li>' for s in STANDORTE.values()) + "</ul>"


def zier():
    """Der Stern aus dem Dream-Logo zwischen zwei feinen Linien, das einzige Ornament."""
    return '<div class="zier" aria-hidden="true"><svg viewBox="0 0 48 46"><use href="#stern"/></svg></div>'


FORMATE = {"hoch": "Hochformat 4 : 5", "quer": "Querformat 3 : 2", "breit": "Breitformat 21 : 9"}


def foto(format_, idee):
    """Fotoplatz mit Bildidee: zeigt dem Betreiber, welches Foto hierher gehört."""
    return (f'<figure class="rahmen rahmen-{format_}"><div class="rahmen-bild" role="img" aria-label="Platzhalter für ein Foto: {idee}">'
            f'<p class="rahmen-text"><span class="rahmen-marke">Foto folgt</span><span class="rahmen-idee">{idee}</span>'
            f'<span class="rahmen-format">{FORMATE[format_]}</span></p></div></figure>')


# ---------- Listen ----------

def zeilen():
    teile = []
    for slug, s in STANDORTE.items():
        kurz = s["name"].split("-")[0]
        teile.append(f"""        <li class="zeile" data-name="{kurz}" {offen(s)} {geo(s)}>
          <div class="zeile-ort">
            <h3><a href="standorte.html#{slug}">{s["name"]}</a></h3>
            <p>{s["region"]}</p>
            <p class="entfernung" data-entfernung hidden></p>
          </div>
          <div class="zeile-zeit">
            {zeitband(s)}
            <p class="status"><span class="lampe" aria-hidden="true"></span><span data-status>{heute_text(s)}</span></p>
          </div>
          <address>{adresse(s)}</address>
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
        teile.append(f"""      <article class="detail" id="{slug}" {offen(s)} {geo(s)}>
        <div class="detail-kopf">
          <h2>{s["name"]}</h2>
          <p class="detail-unter">{unterzeile}</p>
          <p class="entfernung" data-entfernung hidden></p>
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

def stand(datei):
    """Prüfwert für ?v= hinter CSS und JS: ändert sich mit dem Inhalt, damit
    kein Browser nach einer Änderung noch die alte Datei aus dem Zwischenspeicher zeigt."""
    return hashlib.sha1((ROOT / datei).read_bytes()).hexdigest()[:8]


def layout(name, titel, beschreibung, inhalt):
    menu = []
    for slug, label in NAV[1:]:
        cur = ' aria-current="page"' if slug == name else ""
        menu.append(f'<li><a href="{slug}.html"{cur}>{label}</a></li>')
    fuss = "".join(f'<li><a href="{s}.html">{l}</a></li>' for s, l in NAV[1:])
    fuss_haeuser = "".join(
        f'<li><a href="standorte.html#{slug}"><span>{s["name"]}</span><span class="nr">{s["tel"]}</span></a></li>'
        for slug, s in STANDORTE.items())
    voll_titel = "Dream Spielcenter – Spielhallen von Wiesbaden bis Füssen" if name == "index" else f"{titel} – Dream Spielcenter"
    kopfskript = "\n" + INTRO_SKRIPT if name == "index" else ""
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
<link rel="preload" href="assets/fonts/spectral-500-italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/lobster.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/style.css?v={stand('assets/css/style.css')}">{kopfskript}
</head>
<body data-seite="{name}">
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<aside class="entwurf" aria-label="Hinweis zum Entwurf"><p><b>Entwurf</b> · Gestaltungsvorschlag von ORDÉ. Fotos, Texte und Angaben stimmen wir mit Ihnen ab.</p></aside>

<!-- Logo als SVG-Nachbau; wird durch die Original-Logodatei ersetzt -->
{SPRITE}

<header class="kopf" data-kopf>
  <div class="wrap kopf-in">
    <a class="logo" href="index.html" aria-label="Dream Spielcenter – zur Startseite"><svg viewBox="0 0 480 230"><use href="#logo"/></svg></a>
    <nav aria-label="Hauptnavigation">
      <ul class="menu" id="menu" role="list">
        {"".join(menu)}
      </ul>
    </nav>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu"><span class="sr">Menü</span><span class="burger-striche" aria-hidden="true"></span></button>
  </div>
</header>

<main id="inhalt">
{inhalt}
</main>

<footer class="fuss">
  <div class="wrap fuss-kopf">
    <a class="logo" href="index.html" aria-label="Zur Startseite"><svg viewBox="0 0 480 230"><use href="#logo"/></svg></a>
    <p class="fuss-satz">{ZAHLWORTE.get(len(STANDORTE), len(STANDORTE))}mal <em>Dream.</em> Von Wiesbaden bis Füssen.</p>
  </div>
  <div class="wrap fuss-in">
    <div>
      <h2 class="fuss-titel">Die Häuser</h2>
      <ul class="fuss-haeuser" role="list">{fuss_haeuser}</ul>
    </div>
    <div>
      <h2 class="fuss-titel">Zentrale</h2>
      <p>{ZENTRALE["firma"]}<br>{ZENTRALE["ort"]}</p>
      <div class="fuss-kontakt">
        <a href="{tel_link(ZENTRALE["tel"])}">{icon("phone")}{ZENTRALE["tel"]}</a>
        <a href="mailto:{ZENTRALE["mail"]}">{icon("mail")}{ZENTRALE["mail"]}</a>
      </div>
    </div>
    <nav aria-label="Seiten im Fuß">
      <h2 class="fuss-titel">Seiten</h2>
      <ul role="list">{fuss}<li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li></ul>
    </nav>
  </div>
  <div class="wrap fuss-recht">
    <p>Zutritt ab 18 Jahren, an den meisten Standorten ab 21. Glücksspiel kann süchtig machen. Kostenlose Beratung der BZgA: <a href="tel:08001372700">0800 1 37 27 00</a></p>
    <p>© <span class="jahr">2026</span> Dream Spielcenter</p>
  </div>
</footer>

<script src="assets/js/main.js?v={stand('assets/js/main.js')}" defer></script>
</body>
</html>
"""


def main():
    anzahl = len(STANDORTE)
    ersatz = {
        "{{LICHT}}": licht,
        "{{AUTOMAT}}": automat,
        "{{AUTOMAT_KLEIN}}": automat_klein,
        "{{ANZEIGE}}": anzeige_anfang,
        "{{/ANZEIGE}}": anzeige_ende,
        "{{FINDER}}": finder,
        "{{HAEUSER_JETZT}}": haeuser_jetzt,
        "{{HAEUSER_DATEN}}": haeuser_daten,
        "{{ZIER}}": zier,
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
        inhalt = re.sub(r"\{\{ANZEIGE:(\w+)\}\}", lambda m: anzeige_anfang(m.group(1)), inhalt)
        inhalt = re.sub(r"\{\{ICON:(\w+)\}\}", lambda m: icon(m.group(1)), inhalt)
        inhalt = re.sub(r"\{\{FOTO:(hoch|quer|breit):([^}]+)\}\}", lambda m: foto(m.group(1), m.group(2)), inhalt)
        rest = re.findall(r"\{\{[^}]+\}\}", inhalt)
        if rest:
            raise SystemExit(f"{datei.name}: unbekannte Platzhalter {rest}")
        html = layout(datei.stem, meta["titel"], meta["beschreibung"], inhalt.rstrip())
        (ROOT / datei.name).write_text(html)
        print("gebaut:", datei.name)


if __name__ == "__main__":
    main()
