# -*- coding: utf-8 -*-
"""Macht aus einem Entwurf ein PDF zum Weiterschicken (WhatsApp, Mail).

Nimmt alle Seiten aus demos/entwuerfe/<name>/ in der Reihenfolge des
Hauptmenüs der index.html und legt je Seite einen ganzseitigen Screenshot
ab: zuerst alle Seiten am Desktop, dann alle am Handy. Impressum und
Datenschutz bleiben draußen.

Ergebnis: entwuerfe/<name>/Entwurf-<name>.pdf  (wird nicht hochgeladen)

Aufruf (im Repo-Ordner):
    python3 entwuerfe/pdf-erzeugen.py spielcenter-dream-24

Voraussetzung wie bei vorschau-erzeugen.py: playwright und Pillow.
Liegt Chromium schon irgendwo, den Pfad über PLAYWRIGHT_CHROMIUM setzen.
"""
import io
import os
import re
import sys

QUELLE = os.path.join("demos", "entwuerfe")
ZIEL = "entwuerfe"
OHNE = {"impressum", "datenschutz"}

DESKTOP = {"breite": 1366, "hoehe": 900, "faktor": 1}
HANDY = {"breite": 390, "hoehe": 844, "faktor": 2}


def seiten_finden(ordner):
    vorhanden = {f[:-5] for f in os.listdir(ordner) if f.endswith(".html")}
    if "index" not in vorhanden:
        print("Keine index.html in %s" % ordner)
        sys.exit(1)
    start = open(os.path.join(ordner, "index.html"), encoding="utf-8").read()
    menue = start.split('id="menu"', 1)[-1].split("</ul>", 1)[0]
    reihe = ["index"]
    for name in re.findall(r'href="(\w[\w-]*)\.html', menue):
        if name in vorhanden and name not in reihe and name not in OHNE:
            reihe.append(name)
    # Seiten, die nicht im Menü stehen, hinten anhängen
    reihe += sorted(vorhanden - set(reihe) - OHNE)
    return reihe


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    name = sys.argv[1]
    ordner = os.path.join(QUELLE, name)
    if not os.path.isdir(ordner):
        print("Entwurf nicht gefunden: %s" % ordner)
        sys.exit(1)

    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image
    except ImportError:
        print("playwright oder Pillow fehlt. Installieren mit:")
        print("  pip install playwright pillow --break-system-packages")
        sys.exit(1)

    seiten = seiten_finden(ordner)
    bilder = []
    with sync_playwright() as p:
        pfad = os.environ.get("PLAYWRIGHT_CHROMIUM")
        browser = p.chromium.launch(executable_path=pfad) if pfad else p.chromium.launch()
        for ansicht in (DESKTOP, HANDY):
            seite = browser.new_page(
                viewport={"width": ansicht["breite"], "height": ansicht["hoehe"]},
                device_scale_factor=ansicht["faktor"],
                reduced_motion="reduce",
            )
            for s in seiten:
                url = "file://" + os.path.abspath(os.path.join(ordner, s + ".html"))
                seite.goto(url, wait_until="networkidle")
                seite.wait_for_timeout(400)
                bild = Image.open(io.BytesIO(seite.screenshot(full_page=True))).convert("RGB")
                if ansicht["faktor"] > 1:
                    bild = bild.resize((bild.width // ansicht["faktor"], bild.height // ansicht["faktor"]), Image.LANCZOS)
                bilder.append(bild)
                print("  %-14s %s" % (s, "Desktop" if ansicht is DESKTOP else "Handy"))
            seite.close()
        browser.close()

    os.makedirs(os.path.join(ZIEL, name), exist_ok=True)
    ausgabe = os.path.join(ZIEL, name, "Entwurf-%s.pdf" % name)
    bilder[0].save(ausgabe, save_all=True, append_images=bilder[1:], resolution=110, quality=82)
    print("Fertig: %s (%d Seiten, %d KB)" % (ausgabe, len(bilder), os.path.getsize(ausgabe) // 1024))


if __name__ == "__main__":
    main()
