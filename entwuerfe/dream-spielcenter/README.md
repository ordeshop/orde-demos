# Entwurf Dream Spielcenter

Gestaltungsvorschlag für dream-spielcenter.de, einen **echten Betrieb**. Noch
kein Auftrag: kein Briefing, keine Anzahlung. Wird es einer, zieht das Projekt
nach `ordeshop/orde-kunde-dream-spielcenter` um und wird hier gelöscht.

Online (nach dem Upload): `ordeshop.net/demos/entwuerfe/dream-spielcenter/`.
Nirgends verlinkt, nicht in `BRANCHEN` der ORDÉ-Website, `noindex`. Kein
Rückkehr-Balken, weil der Link an den Betreiber geht; stattdessen oben der
Entwurfs-Hinweis.

## Seiten

Start, Angebot, Standorte (mit Öffnungszeiten), Jobs (mit Bewerbung),
Spielerschutz, Kontakt, Impressum und Datenschutz (Platzhalter).

## Bauen

    python3 entwuerfe/dream-spielcenter/build.py      # Seiten nach demos/entwuerfe/dream-spielcenter/
    python3 entwuerfe/dream-spielcenter/vorschau.py   # dream-demo.html hier: alles in einer Datei

Inhalte nur in `seiten/` ändern, Kopf, Fuß und Öffnungszeiten (`STANDORTE`)
in `build.py`. Die HTML-Dateien im Demos-Ordner werden überschrieben.
`Dream-Entwurf.pdf` sind Screenshots aller Seiten zum Weiterschicken.

## Technik

GSAP 3.12.5, Tabler Icons 3.19.0, Barlow, Barlow Condensed und Lobster liegen
lokal unter `assets/`. Nichts wird von Google oder CDNs geladen (DSGVO).

## Offen (vom Betreiber)

- Original-Logo als Datei (jetzt SVG-Nachbau)
- Fotos: außen, innen, Geräte, Team
- alle Standorte mit Adresse und Zeiten (bekannt nur Kaufering, aus Branchenverzeichnis)
- Telefon, E-Mail, Betreiber laut Impressum, Social-Links
- echte offene Stellen (jetzt Beispiele)
- Altersgrenze 21 bestätigen, Ausstattung (Parken, Getränke, Klima, Nichtraucher)
- Impressum und Datenschutzerklärung (vom Betreiber, nicht von ORDÉ)
- Formulare sind Attrappen; für den Live-Gang Versand per PHP bauen
