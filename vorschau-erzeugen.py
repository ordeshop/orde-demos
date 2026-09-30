# -*- coding: utf-8 -*-
"""Erzeugt die Vorschaubilder der Beispielseiten.

Fuer jede Demo entstehen zwei Bilder:
  vorschau/<name>.webp         Desktop, 1100 x 705
  vorschau/<name>-handy.webp   Handy,   640 x 1313

Diese Bilder zeigt die ORDE-Website auf der Startseite und unter
"Beispiele". Aendert sich eine Demo, muss dieses Skript einmal laufen,
sonst zeigt die Website noch den alten Stand.

Aufruf:
    python3 vorschau-erzeugen.py            alle Demos
    python3 vorschau-erzeugen.py cafe salon nur diese

Voraussetzung: playwright und Pillow.
    pip install playwright pillow --break-system-packages
    playwright install chromium      (entfaellt, wenn Chromium schon da ist)
"""
import os
import sys
import glob

DEMOS = "demos"
ZIEL = "vorschau"

# Desktop: breit, fuer die grossen Vorschaukarten
BREIT = {"breite": 1100, "hoehe": 705, "endung": ".webp", "faktor": 2}
# Handy: hochkant, fuer die Handy-Attrappe auf der Startseite
SCHMAL = {"breite": 640, "hoehe": 1313, "endung": "-handy.webp", "faktor": 2}

GUETE = 72   # WebP-Qualitaet. Hoeher = schoener und groesser.


def demos_finden(auswahl):
    namen = sorted(
        os.path.basename(os.path.dirname(p))
        for p in glob.glob(os.path.join(DEMOS, "*", "index.html"))
    )
    if not auswahl:
        return namen
    unbekannt = [a for a in auswahl if a not in namen]
    if unbekannt:
        print("Unbekannte Demo(s): %s" % ", ".join(unbekannt))
        print("Vorhanden: %s" % ", ".join(namen))
        sys.exit(1)
    return [a for a in auswahl if a in namen]


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright fehlt. Installieren mit:")
        print("  pip install playwright pillow --break-system-packages")
        sys.exit(1)
    from PIL import Image

    namen = demos_finden(sys.argv[1:])
    if not namen:
        print("Keine Demos unter %s/ gefunden." % DEMOS)
        sys.exit(1)

    os.makedirs(ZIEL, exist_ok=True)
    browser_pfad = os.environ.get("PLAYWRIGHT_CHROMIUM") or None

    with sync_playwright() as p:
        start = {"executable_path": browser_pfad} if browser_pfad else {}
        browser = p.chromium.launch(**start)
        for name in namen:
            seite_datei = os.path.abspath(
                os.path.join(DEMOS, name, "index.html"))
            for form in (BREIT, SCHMAL):
                seite = browser.new_page(
                    viewport={"width": form["breite"], "height": form["hoehe"]},
                    device_scale_factor=form["faktor"],
                )
                seite.goto("file://" + seite_datei)
                seite.wait_for_load_state("networkidle")
                # Animationen abschalten, damit das Bild nicht mitten in
                # einer Einblendung entsteht
                seite.add_style_tag(content="*{animation:none!important;"
                                            "transition:none!important;"
                                            "opacity:1!important}")
                seite.wait_for_timeout(400)
                roh = os.path.join(ZIEL, name + ".png")
                seite.screenshot(path=roh)
                seite.close()

                ziel = os.path.join(ZIEL, name + form["endung"])
                bild = Image.open(roh).convert("RGB")
                bild = bild.resize((form["breite"], form["hoehe"]),
                                   Image.LANCZOS)
                bild.save(ziel, "WEBP", quality=GUETE, method=6)
                os.remove(roh)
                print("  %-28s %6.1f KB"
                      % (ziel, os.path.getsize(ziel) / 1024))
        browser.close()

    print("\nFertig. %d Demo(s), %d Bilder." % (len(namen), len(namen) * 2))
    print("Die Website liest sie unter demos/vorschau/ - dort landen sie "
          "beim Hochladen von selbst.")


if __name__ == "__main__":
    main()
