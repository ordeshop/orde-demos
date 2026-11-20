# -*- coding: utf-8 -*-
"""Prüft einen Entwurf, bevor ihn jemand außerhalb von ORDÉ sieht.

Findet die Fehler, die ein fremder Prüfer sofort sieht: fehlende Seitentitel,
Reste aus WordPress oder einem anderen System ([formidable id=…], wp-block,
Lorem ipsum), tote Links, Dateien von fremden Servern, Seiten ohne
Entwurfs-Hinweis oder ohne noindex.

Aufruf (im Repo-Ordner):
    python3 entwuerfe/pruefen.py <name>

Ergebnis: Liste nach Art des Fehlers. Endet mit Code 1, solange ein Fehler
da ist. Warnungen sperren nicht, gehören aber in den Bericht an Artur.
pdf-erzeugen.py ruft diese Prüfung selbst auf und bricht bei Fehlern ab.
"""
import os
import re
import sys
from collections import defaultdict
from urllib.parse import unquote, urlparse

QUELLE = os.path.join("demos", "entwuerfe")
PAGES_PFAD = "/orde-demos/"          # so beginnen absolute Links auf GitHub Pages
SEITEN_WARNUNG = 40                  # ab hier: wurde wirklich jede Seite fertig gemacht?
GROESSE_WARNUNG_MB = 15

# Reste aus dem alten System. Jeder Treffer im sichtbaren Text ist ein Fehler.
RESTE = [
    (r"\[/?[a-z][a-z0-9_-]*(?:\s+[a-z_-]+=[^\]]*)?\]", "Shortcode (z. B. [formidable id=…])"),
    (r"\{\{.*?\}\}|\{%.*?%\}", "Vorlagen-Platzhalter {{ }} / {% %}"),
    (r"lorem ipsum", "Lorem ipsum"),
    (r"\b(TODO|FIXME|XXX)\b", "TODO/FIXME im Text"),
]
# Reste im Quelltext (auch in <style>/<script>): das Haus des alten Systems.
RESTE_QUELLTEXT = [
    (r"wp-block|wp-content|wp-includes|elementor|et_pb_|vc_row", "WordPress-/Baukasten-Reste im Code"),
]
# Ausnahmen: harmlose Klammern im Text (Fußnoten, Tastenkürzel).
SHORTCODE_ERLAUBT = {"[x]", "[ ]"}


def sichtbarer_text(html):
    html = re.sub(r"<(script|style|template|noscript)\b.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html)


def attribut(tag, name):
    m = re.search(r'\b%s\s*=\s*("([^"]*)"|\'([^\']*)\'|([^\s>]+))' % name, tag, re.I)
    if not m:
        return None
    return next(g for g in m.groups()[1:] if g is not None)


def ziel_finden(wurzel, datei, url):
    """Lokalen Pfad zu einem Link bestimmen, None = nicht prüfbar/extern."""
    u = urlparse(url)
    if u.scheme or url.startswith(("#", "//")):
        return None
    pfad = unquote(u.path)
    if not pfad:
        return None
    if pfad.startswith(PAGES_PFAD):
        basis = os.path.join(QUELLE, pfad[len(PAGES_PFAD):])
    elif pfad.startswith("/"):
        basis = os.path.join(QUELLE, pfad.lstrip("/"))
    else:
        basis = os.path.normpath(os.path.join(os.path.dirname(datei), pfad))
    if os.path.isdir(basis) or pfad.endswith("/"):
        basis = os.path.join(basis, "index.html")
    return basis


def pruefen(name):
    wurzel = os.path.join(QUELLE, name)
    if not os.path.isdir(wurzel):
        print("Entwurf nicht gefunden: %s" % wurzel)
        return 2

    fehler = defaultdict(list)
    warnung = defaultdict(list)
    hinweis = defaultdict(list)
    titel_je_seite = defaultdict(list)

    html_dateien = []
    groesse = 0
    for ordner, _, dateien in os.walk(wurzel):
        for f in dateien:
            p = os.path.join(ordner, f)
            groesse += os.path.getsize(p)
            if f.endswith(".html"):
                html_dateien.append(p)
            if f.endswith(".css"):
                css = open(p, encoding="utf-8", errors="replace").read()
                if re.search(r"(@import\s+url\(|url\()\s*['\"]?https?://", css):
                    fehler["Datei von fremdem Server (CSS)"].append(p)

    for p in sorted(html_dateien):
        roh = open(p, encoding="utf-8", errors="replace").read()
        rel = os.path.relpath(p, wurzel)

        # Weiterleitungsseiten (nur meta refresh) nicht weiter prüfen
        if re.search(r'http-equiv=["\']refresh', roh, re.I) and "<h1" not in roh.lower():
            continue

        kopf = roh.split("</head>", 1)[0]
        t = re.search(r"<title[^>]*>(.*?)</title>", kopf, re.S | re.I)
        if not t or not t.group(1).strip():
            fehler["kein Seitentitel <title>"].append(rel)
        else:
            titel_je_seite[t.group(1).strip()].append(rel)
        if not re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'][^"\']{20,}', kopf, re.I):
            fehler["keine Beschreibung <meta name=description>"].append(rel)
        if not re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', kopf, re.I):
            fehler["kein noindex"].append(rel)
        if not re.search(r"<html[^>]+lang=", roh, re.I):
            fehler["<html> ohne lang"].append(rel)
        if not re.search(r'class=["\'][^"\']*\b(entwurf|draft)\b', roh, re.I):
            fehler["kein sichtbarer Entwurfs-Hinweis (class=\"entwurf\" oder \"draft\")"].append(rel)

        h1 = len(re.findall(r"<h1\b", roh, re.I))
        if h1 != 1:
            fehler["nicht genau eine h1 (%s)" % ("keine" if h1 == 0 else "mehrere")].append(rel)

        text = sichtbarer_text(roh)
        for muster, art in RESTE:
            treffer = [m.group(0) for m in re.finditer(muster, text, re.I)]
            if art.startswith("Shortcode"):
                treffer = [x for x in treffer if x not in SHORTCODE_ERLAUBT]
            if treffer:
                fehler[art].append("%s: %s" % (rel, ", ".join(sorted(set(treffer))[:3])))
        for muster, art in RESTE_QUELLTEXT:
            if re.search(muster, roh, re.I):
                fehler[art].append(rel)

        for tag in re.findall(r"<(?:script|link|img|source|video|audio|iframe)\b[^>]*>", roh, re.I):
            for a in ("src", "href", "srcset", "poster"):
                wert = attribut(tag, a)
                if not wert:
                    continue
                if tag.lower().startswith("<link") and a == "href":
                    rel_attr = (attribut(tag, "rel") or "").lower()
                    if rel_attr in ("canonical", "alternate"):
                        continue
                for teil in wert.split(","):
                    url = teil.strip().split(" ")[0]
                    if re.match(r"(https?:)?//", url):
                        fehler["Datei von fremdem Server (Schrift, Skript, Bild, Einbettung)"].append(
                            "%s: %s" % (rel, url[:80]))
        if re.search(r"<iframe\b", roh, re.I):
            warnung["Einbettung <iframe> (Datenschutz prüfen)"].append(rel)

        for tag in re.findall(r"<img\b[^>]*>", roh, re.I):
            if attribut(tag, "alt") is None:
                fehler["Bild ohne alt"].append("%s: %s" % (rel, (attribut(tag, "src") or "")[-50:]))

        for tag in re.findall(r"<a\b[^>]*>", roh, re.I):
            href = attribut(tag, "href")
            if not href or href.startswith(("mailto:", "tel:", "javascript:", "data:")):
                continue
            ziel = ziel_finden(wurzel, p, href)
            if ziel and not os.path.exists(ziel):
                fehler["toter Link"].append("%s → %s" % (rel, href[:80]))

        for tag in re.findall(r"<form\b[^>]*>", roh, re.I):
            if "data-demo" in tag:
                hinweis["Formular-Attrappe (beim Zeigen dazusagen)"].append(rel)
            else:
                warnung["Formular ohne data-demo: schickt es wirklich etwas ab?"].append(rel)

        offen = len(re.findall(r'class=["\'][^"\']*\btodo\b', roh))
        if offen:
            hinweis["gelbe Platzhalter (Liste „was der Kunde liefern muss“)"].append("%s: %d" % (rel, offen))

    for titel, seiten in titel_je_seite.items():
        if len(seiten) > 1:
            warnung["gleicher Seitentitel auf mehreren Seiten"].append("„%s“: %s" % (titel[:60], ", ".join(seiten[:4])))

    seiten = len(html_dateien)
    if seiten > SEITEN_WARNUNG:
        warnung["%d Seiten: Wurde jede einzeln fertig gemacht und angesehen? Lieber wenige perfekte Seiten" % seiten].append(name)
    mb = groesse / 1024 / 1024
    if mb > GROESSE_WARNUNG_MB:
        warnung["Entwurf ist %.0f MB groß" % mb].append(name)

    def ausgeben(titel, gruppen):
        if not gruppen:
            return
        print("\n%s" % titel)
        for art, liste in sorted(gruppen.items()):
            print("  %s (%d)" % (art, len(liste)))
            for eintrag in liste[:5]:
                print("     %s" % eintrag)
            if len(liste) > 5:
                print("     … und %d weitere" % (len(liste) - 5))

    print("Prüfung Entwurf „%s“: %d Seiten, %.1f MB" % (name, seiten, mb))
    ausgeben("FEHLER (sperren das Zeigen):", fehler)
    ausgeben("WARNUNGEN (in den Bericht an Artur):", warnung)
    ausgeben("HINWEISE:", hinweis)
    if fehler:
        print("\n%d Arten von Fehlern. So geht der Entwurf nicht raus." % len(fehler))
        return 1
    print("\nKeine Fehler. Jetzt noch von Hand: Desktop und Handy ansehen, Link selbst öffnen,"
          " Fakten gegen die Quelle (Freigabe-Liste in der README).")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(pruefen(sys.argv[1]))
