"""Baut den privaten VEIT-Entwurf.

Aufruf:  python3 entwuerfe/veit/build.py
Quelle:  seiten/*.html, jede beginnt mit
         <!-- titel: … | beschreibung: … | nav: produkte -->
Ergebnis: demos/entwuerfe/veit/  (geht über GitHub Pages online)

Platzhalter im Inhalt:
  {{TEL_ZENTRALE}} {{TEL_ZENTRALE_LINK}} {{MAIL}} {{ADRESSE}}
  {{HOTLINES}}        Service-Hotlines je Region (Liste mit Anruf-Links)
  {{PARTNER}}         Vertriebspartner-Suche (Attrappe)
  {{OFFEN:Text}}      gelber Platzhalter für Ungeprüftes
  {{ICON:name}}       Strich-Icon (pfeil, extern, telefon, mail, route, download, play)
Alle Kontaktdaten stehen nur in FIRMA und HOTLINES.
"""
import sys as _sys
if "--alt" not in _sys.argv:
    _sys.exit("Abgelöst: Die Vorschau ist jetzt demos/entwuerfe/veit/komplett/. "
              "build.py würde die Weiterleitungen überschreiben. Nur mit --alt ausführen.")

import hashlib
import pathlib
import re
import shutil

HIER = pathlib.Path(__file__).resolve().parent
SEITEN = HIER / "seiten"
ASSETS = HIER / "assets"
SITE = HIER.parent.parent / "demos" / "entwuerfe" / "veit"

# Quelle: veit.de/kontakt/ und veit.de/services/support/ (03.11.2026)
FIRMA = {
    "name": "VEIT GmbH",
    "strasse": "Justus-von-Liebig-Str. 15",
    "plz": "86899",
    "ort": "Landsberg am Lech",
    "land": "Deutschland",
    "tel": "+49 8191 479 0",
    "mail": "info@veit.de",
    "shop": "https://www.veit.de/shop/",
}
HOTLINES = [
    ("Deutschland", "+49 8191 479 133", "service@veit.de"),
    ("Europa", "+49 8191 479 252", "service@veit.de"),
    ("Amerika", "+1 770 868 8060", ""),
    ("Asien", "+852 2111 9795", ""),
]
DURCHWAHLEN = [
    ("Zentrale", "+49 8191 479 0"),
    ("Vertrieb", "+49 8191 479 100"),
    ("Kundendienst national", "+49 8191 479 133"),
    ("Kundendienst international", "+49 8191 479 252"),
    ("Personal", "+49 8191 479 192"),
    ("Einkauf", "+49 8191 479 280"),
    ("Buchhaltung", "+49 8191 479 193"),
    ("Geschäftsleitung", "+49 8191 479 141"),
]
# Länderliste der Vertriebspartner-Suche auf veit.de (gekürzt auf die Auswahl im Feld)
LAENDER = ("Ägypten Albanien Algerien Australien Bangladesch Belgien Bosnien Brasilien Bulgarien Chile China "
           "Dänemark Deutschland Dominikanische_Republik Estland Finnland Frankreich Griechenland Großbritannien "
           "Indien Indonesien Irland Island Israel Italien Japan Jordanien Kambodscha Kanada Katar Kenia Kroatien "
           "Laos Litauen Luxemburg Madagaskar Malaysia Malta Marokko Mauritius Mexiko Moldawien Myanmar "
           "Neuseeland Niederlande Norwegen Österreich Pakistan Peru Philippinen Polen Portugal Rumänien Schweden "
           "Schweiz Serbien Singapur Slowakei Slowenien Spanien Sri_Lanka Südafrika Südkorea Taiwan Thailand "
           "Tschechien Tunesien Türkei Ukraine Ungarn USA Usbekistan Vereinigte_Arabische_Emirate Vietnam Zypern")

NAV = [
    ("produkte", "Produkte"),
    ("anwendungen", "Anwendungen"),
    ("service", "Service"),
    ("unternehmen", "Unternehmen"),
    ("karriere", "Karriere"),
]

ICONS = {
    "pfeil": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "extern": '<path d="M14 5h5v5M19 5l-8 8M11 6H6a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-5"/>',
    "telefon": '<path d="M6.6 3.6 9 3l1.6 4-2 1.3a11 11 0 0 0 7.1 7.1l1.3-2 4 1.6-.6 2.4a2 2 0 0 1-2 1.5A16 16 0 0 1 5.1 5.6a2 2 0 0 1 1.5-2z"/>',
    "mail": '<path d="M4 6h16v12H4z"/><path d="m4 7 8 6 8-6"/>',
    "route": '<path d="M12 21s-6-5.6-6-11a6 6 0 0 1 12 0c0 5.4-6 11-6 11z"/><circle cx="12" cy="10" r="2.2"/>',
    "download": '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
    "play": '<path d="M8 5v14l11-7z"/>',
    "menue": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "zu": '<path d="M6 6l12 12M18 6 6 18"/>',
}


def icon(name):
    return (f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" '
            f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def tel_link(nr):
    return "tel:" + re.sub(r"[^\d+]", "", nr)


def hotlines():
    zeilen = []
    for region, nr, mail in HOTLINES:
        m = f'<a class="hot-mail" href="mailto:{mail}">{mail}</a>' if mail else ""
        zeilen.append(f'<li><span class="hot-region">{region}</span>'
                      f'<a class="hot-nr" href="{tel_link(nr)}">{nr}</a>{m}</li>')
    return '<ul class="hotlines" role="list">' + "".join(zeilen) + "</ul>"


def partner():
    laender = "".join(f"<option>{l.replace('_', ' ')}</option>" for l in LAENDER.split())
    return f"""<form class="partner" action="#" data-attrappe>
  <div class="feld"><label for="p-branche">Branche</label>
    <select id="p-branche" required><option value="">Bitte wählen</option>
      <option>Bekleidungsindustrie</option><option>Textilpflege</option><option>Interieur</option></select></div>
  <div class="feld"><label for="p-land">Land</label>
    <select id="p-land" required><option value="">Bitte wählen</option>{laender}</select></div>
  <button class="knopf" type="submit">Ansprechpartner anzeigen {icon('pfeil')}</button>
  <p class="partner-ergebnis" role="status" aria-live="polite" hidden></p>
</form>"""


def durchwahlen():
    z = "".join(f'<tr><th scope="row">{n}</th><td><a href="{tel_link(t)}">{t}</a></td></tr>' for n, t in DURCHWAHLEN)
    return f'<table class="durchwahlen"><caption class="vh">Durchwahlen</caption><tbody>{z}</tbody></table>'


def ersetzen(html):
    html = html.replace("{{TEL_ZENTRALE}}", FIRMA["tel"]).replace("{{TEL_ZENTRALE_LINK}}", tel_link(FIRMA["tel"]))
    html = html.replace("{{MAIL}}", FIRMA["mail"]).replace("{{SHOP}}", FIRMA["shop"])
    html = html.replace("{{ADRESSE}}", f'{FIRMA["strasse"]}<br>{FIRMA["plz"]} {FIRMA["ort"]}<br>{FIRMA["land"]}')
    html = html.replace("{{HOTLINES}}", hotlines()).replace("{{PARTNER}}", partner())
    html = html.replace("{{DURCHWAHLEN}}", durchwahlen())
    html = re.sub(r"\{\{OFFEN:(.+?)\}\}", r'<mark class="offen">\1</mark>', html)
    html = re.sub(r"\{\{ICON:(\w+)\}\}", lambda m: icon(m.group(1)), html)
    return html


def fingerabdruck(datei):
    return hashlib.sha1(datei.read_bytes()).hexdigest()[:8]


def kopf(titel, beschreibung, aktiv, css_v, js_v):
    nav = "".join(
        f'<li><a href="{s}.html"{" aria-current=page" if s == aktiv else ""}>{t}</a></li>' for s, t in NAV)
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{titel}</title>
<meta name="description" content="{beschreibung}">
<link rel="icon" href="assets/bilder/veit-logo.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/instrument-sans-latin-standard-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css?v={css_v}">
<script src="assets/main.js?v={js_v}" defer></script>
</head>
<body>
<a class="sprung" href="#inhalt">Zum Inhalt springen</a>
<p class="entwurf">Gestaltungsentwurf für eine neue veit.de · Inhalte und Bilder von veit.de · <mark class="offen">gelb</mark> = noch zu prüfen</p>
<header class="kopfzeile">
  <div class="kopfzeile-innen">
    <a class="logo" href="index.html"><img src="assets/bilder/veit-logo.svg" width="250" height="71" alt="VEIT, zur Startseite"></a>
    <nav class="hauptnav" aria-label="Hauptmenü"><ul role="list">{nav}</ul></nav>
    <div class="kopf-rechts">
      <a class="kopf-shop" href="{FIRMA['shop']}">Ersatzteil-Shop {icon('extern')}</a>
      <span class="sprache"><a href="index.html" aria-current="true" lang="de">DE</a><a href="#" lang="en" data-attrappe-link>EN</a></span>
      <a class="knopf knopf-klein" href="kontakt.html">Kontakt</a>
    </div>
    <button class="menue-knopf" type="button" aria-expanded="false" aria-controls="menue">{icon('menue')}<span>Menü</span></button>
  </div>
  <div class="menue" id="menue" hidden>
    <div class="menue-innen">
      <button class="menue-zu" type="button">{icon('zu')}<span>Schließen</span></button>
      <a class="menue-hotline" href="{tel_link(HOTLINES[0][1])}">{icon('telefon')} Service-Hotline {HOTLINES[0][1]}</a>
      <ul role="list">{nav}<li><a href="kontakt.html">Kontakt</a></li></ul>
      <p class="menue-unten"><a href="{FIRMA['shop']}">Ersatzteil-Shop {icon('extern')}</a> · <a href="index.html" lang="de">DE</a> / <a href="#" lang="en" data-attrappe-link>EN</a></p>
    </div>
  </div>
</header>
<main id="inhalt">
"""


def fuss():
    nav = "".join(f'<li><a href="{s}.html">{t}</a></li>' for s, t in NAV)
    return f"""</main>
<footer class="fuss">
  <div class="fuss-innen">
    <div class="fuss-firma">
      <img src="assets/bilder/veit-logo.svg" width="250" height="71" alt="VEIT" class="fuss-logo">
      <p><strong>{FIRMA['name']}</strong><br>{FIRMA['strasse']}<br>{FIRMA['plz']} {FIRMA['ort']}</p>
      <p><a href="{tel_link(FIRMA['tel'])}">{FIRMA['tel']}</a><br><a href="mailto:{FIRMA['mail']}">{FIRMA['mail']}</a></p>
    </div>
    <nav aria-label="Seiten"><h2>Seiten</h2><ul role="list">{nav}<li><a href="kontakt.html">Kontakt</a></li><li><a href="{FIRMA['shop']}">Ersatzteil-Shop</a></li></ul></nav>
    <nav aria-label="Service"><h2>Service</h2><ul role="list">
      <li><a href="service.html#auftrag">Serviceauftrag</a></li><li><a href="service.html#ersatzteile">Ersatzteile</a></li>
      <li><a href="service.html#wartung">Wartungsvertrag</a></li><li><a href="service.html#unterlagen">Prospekte und Datenblätter</a></li>
      <li><a href="index.html#partner">Vertriebspartner</a></li></ul></nav>
    <nav aria-label="Rechtliches"><h2>Rechtliches</h2><ul role="list">
      <li><a href="#" data-attrappe-link>Impressum</a></li><li><a href="#" data-attrappe-link>Datenschutz</a></li>
      <li><a href="#" data-attrappe-link>AGB</a></li><li><a href="#" data-attrappe-link>Zahlungs- und Lieferbedingungen</a></li></ul>
      <p class="fuss-klein">Rechtstexte übernimmt VEIT unverändert.</p></nav>
  </div>
  <p class="fuss-zeile">© VEIT GmbH · Pressing for Excellence · <a href="https://www.facebook.com/VEITGroupIntl">Facebook</a> · <a href="https://www.youtube.com/user/veitmarketing">YouTube</a> · <a href="https://www.xing.com/companies/veitgmbh">XING</a></p>
</footer>
</body>
</html>
"""


def bauen():
    if SITE.exists():
        shutil.rmtree(SITE)
    shutil.copytree(ASSETS, SITE / "assets")
    css_v = fingerabdruck(ASSETS / "style.css")
    js_v = fingerabdruck(ASSETS / "main.js")
    seiten = sorted(SEITEN.glob("*.html"))
    for datei in seiten:
        roh = datei.read_text(encoding="utf-8")
        m = re.match(r"<!--\s*titel:\s*(.+?)\s*\|\s*beschreibung:\s*(.+?)\s*\|\s*nav:\s*(\w*)\s*-->\n?", roh)
        if not m:
            raise SystemExit(f"Kopfzeile fehlt in {datei.name}")
        titel, beschreibung, aktiv = m.groups()
        inhalt = ersetzen(roh[m.end():])
        (SITE / datei.name).write_text(kopf(titel, beschreibung, aktiv, css_v, js_v) + inhalt + fuss(), encoding="utf-8")
    # tote interne Links und fehlende Bilder melden
    namen = {d.name for d in seiten}
    fehler = []
    for d in SITE.glob("*.html"):
        t = d.read_text(encoding="utf-8")
        for ziel in re.findall(r'href="([\w-]+\.html)(?:#[\w-]+)?"', t):
            if ziel not in namen:
                fehler.append(f"{d.name}: Link auf {ziel}")
        for bild in re.findall(r'src="(assets/[^"?]+)"', t):
            if not (SITE / bild).exists():
                fehler.append(f"{d.name}: Bild fehlt {bild}")
        if t.count("<h1") != 1:
            fehler.append(f"{d.name}: {t.count('<h1')} h1")
        for img in re.findall(r"<img\b[^>]*>", t):
            if " alt=" not in img:
                fehler.append(f"{d.name}: Bild ohne alt: {img[:80]}")
    print(f"{len(seiten)} Seiten nach {SITE.relative_to(HIER.parent.parent)}/")
    for f in fehler:
        print("  !", f)
    offen = sum(d.read_text(encoding='utf-8').count('class="offen"') for d in SITE.glob("*.html")) - len(seiten)
    print(f"  {offen} gelbe Platzhalter im Inhalt")


if __name__ == "__main__":
    bauen()
