# Entwurf Dream Spielcenter

Gestaltungsvorschlag für dream-spielcenter.de, einen **echten Betrieb**. Noch
kein Auftrag: kein Briefing, keine Anzahlung. Wird es einer, zieht das Projekt
nach `ordeshop/orde-kunde-dream-spielcenter` um und wird hier gelöscht.

Vorschau-Link: https://vorschau.byorde.com/dream-spielcenter/
Nirgends verlinkt, nicht in `BRANCHEN` der ORDÉ-Website, `noindex`. Kein
Rückkehr-Balken, weil der Link an den Betreiber geht; stattdessen oben der
Entwurfs-Hinweis.

## Stand

```
- [x] 1  Anfrage: DACH, Unternehmen, persönlicher Kontakt, Slug dream-spielcenter
- [ ] 1  Veit-Prüfung, gewünschte Seitenzahl bestätigen
- [x] 2  Entwurf gebaut und geprüft (8 Seiten), PDF erzeugt
- [ ] 2  Link geöffnet (wartet auf GitHub Pages), Mail-Entwurf an Artur
- [ ] 3  Angebot raus (mit AGB/Widerruf)
- [ ] 4  Zusage, Auftragsbestätigung mit Briefing-Link
- [ ] 5  Anzahlung da
- [ ] 6  Briefing vollständig
- [ ] 7  Repo angelegt, gebaut, geprüft
- [ ] 8  Vorschau gezeigt, Korrekturrunde erledigt
- [ ] 9  Hosting/Domain gebucht, Secrets eingetragen, Upload läuft
- [ ] 10 Abnahme, Schlussrechnung bezahlt
- [ ] 11 Live, Vorschau-Ordner gelöscht, Übergabe, Referenz erfragt
- [ ] 12 Betreuung bis: –
```

## Seiten

Start, Angebot, Standorte (mit Öffnungszeiten), Jobs (mit Bewerbung),
Spielerschutz, Kontakt, Impressum und Datenschutz (Platzhalter).

## Bauen

    python3 entwuerfe/dream-spielcenter/build.py      # Seiten nach demos/entwuerfe/dream-spielcenter/
    python3 entwuerfe/pdf-erzeugen.py dream-spielcenter   # PDF hier im Ordner

Inhalte nur in `seiten/` ändern, Kopf, Fuß und Öffnungszeiten (`STANDORTE`)
in `build.py`. Die HTML-Dateien im Demos-Ordner werden überschrieben.
`Entwurf-dream-spielcenter.pdf` sind Screenshots aller Seiten zum Weiterschicken.

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
