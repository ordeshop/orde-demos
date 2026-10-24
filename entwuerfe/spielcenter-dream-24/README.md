# Entwurf Spielcenter Dream 24 / Dream Spielcenter

Gestaltungsvorschlag für einen **echten Betrieb**: MSW Spiel + Freizeit GmbH,
Spielhallen unter dem Namen „Dream“. Persönlicher Kontakt (Einzelheiten nur
bei Artur, nicht in dieses öffentliche Repo). Noch kein Auftrag: kein Briefing, keine Anzahlung. Wird es
einer, zieht das Projekt nach `ordeshop/orde-kunde-spielcenter-dream-24` um und
wird hier gelöscht.

Vorschau-Link: https://ordeshop.github.io/orde-demos/spielcenter-dream-24/
Nirgends verlinkt, nicht in `BRANCHEN` der ORDÉ-Website, `noindex`. Kein
Rückkehr-Balken, weil der Link an den Betreiber geht; stattdessen oben der
Entwurfs-Hinweis.

**Ein Betrieb, zwei Namen.** casino-dream24.de leitet per 301 auf
dream-spielcenter.de weiter (geprüft 22.10.2026). Der Entwurf entstand am
20.10.2026 als `dream-spielcenter` und ist am 22.10.2026 auf den Slug
`casino-dream-24` umgezogen, weil Artur den Betrieb unter diesem Namen
anfragte, und noch am selben Tag auf Arturs Anweisung auf
`spielcenter-dream-24`: „Spielcenter“ statt „Casino“, auch im Namen auf der
Seite. Die alten Links sind damit weg; keiner war verschickt.

## Stand

```
- [x] 1  Anfrage: DACH, Unternehmen (GmbH), persönlicher Kontakt, Slug spielcenter-dream-24
- [ ] 1  Prüfung Nebentätigkeit (Artur), Seitenzahl bestätigen (Annahme: wie alte Seite)
- [x] 2  Entwurf gebaut und geprüft (8 Seiten), Link geöffnet, PDF erzeugt, Mail-Entwurf an Artur
- [ ] 3  Angebot raus (mit AGB/Widerruf)
- [ ] 4  Zusage, Auftragsbestätigung mit Briefing-Link
- [ ] 5  Anzahlung da
- [ ] 6  Briefing vollständig
- [ ] 7  Repo angelegt, gebaut, geprüft
- [ ] 8  Vorschau gezeigt, Korrekturrunde erledigt
- [ ] 9  Relaunch (Fall B): Anbieter von Domain/Hosting klären, alte Seite sichern, Weiterleitungen, Secrets, umschalten, testen
- [ ] 10 Abnahme, Schlussrechnung bezahlt
- [ ] 11 Live, Vorschau-Ordner gelöscht, Übergabe, Referenz erfragt
- [ ] 12 Betreuung bis: –
```

## Seiten

Start, Angebot, Standorte (mit Öffnungszeiten), Jobs (mit Bewerbung),
Spielerschutz, Kontakt, Impressum und Datenschutz (Platzhalter).

## Bauen

    python3 entwuerfe/spielcenter-dream-24/build.py          # Seiten nach demos/entwuerfe/spielcenter-dream-24/
    python3 entwuerfe/pdf-erzeugen.py spielcenter-dream-24   # PDF hier im Ordner

Inhalte nur in `seiten/` ändern, Kopf, Fuß und Standorte (`STANDORTE`) in
`build.py`. Die HTML-Dateien im Demos-Ordner werden überschrieben.
`Entwurf-spielcenter-dream-24.pdf` sind Screenshots aller Seiten zum Weiterschicken.

## Technik

GSAP 3.12.5, Tabler Icons 3.19.0, Barlow, Barlow Condensed und Lobster liegen
lokal unter `assets/`. Nichts wird von Google oder CDNs geladen (DSGVO).

## Quellen der Angaben

Die alte Seite ist von der Arbeitsumgebung aus nicht abrufbar: Das
SSL-Zertifikat von dream-spielcenter.de ist **abgelaufen**, das von
casino-dream24.de selbst ausgestellt (22.10.2026). Besucher sehen im Browser
eine Sicherheitswarnung – ein gutes Argument für den Relaunch.

- Offizielle Seite laut Suchindex (`/spielhallen/`, `/impressum/`, etwa 2024):
  fünf Standorte Füssen, Heidenheim-Schnaitheim, Kaufering, Senden
  (Iller-Center), Wiesbaden-Biebrich; Betreiber MSW Spiel + Freizeit GmbH,
  Eislingen/Fils, Tel. 07161 98824-0, info@dream-spielcenter.de.
  Füssen zusätzlich mit Billard und „Fun4Four“ (nicht übernommen, bestätigen).
- werkenntdenbesten.de (22.10.2026): „MSW-Spiel + Freizeit GmbH Casino Dream
  24“, Viktor-Frankl-Str. 15, 86916 Kaufering, Tel. 08191 4299104, Website
  casino-dream24.de, „Billard • Casino • Internet-Café“, täglich 6–3 Uhr.
  Weicht von den Zeiten der offiziellen Seite ab (Mo–Sa 9–3, So 11–3) →
  Hinweis auf der Seite.
- Branchenverzeichnisse vom 20.10.2026 (Das Örtliche, Gelbe Seiten, Cylex,
  Öffnungszeitenbuch) für Telefon und Zeiten der übrigen Standorte.
- Ulm und Landsberg (Arturs Angabe „laut alter Seite“): kein eigener Standort
  belegt. Senden liegt bei Ulm, Kaufering bei Landsberg am Lech – wohl sind
  diese gemeint. Auf der Seite deshalb als Region angegeben, nicht als
  eigene Standorte. Bestätigen lassen.
- Nicht übernommen: ein Eintrag „Dream Spielcenter“ in Waldkraiburg, der nicht
  auf der offiziellen Liste steht.

## Offen (vom Betreiber)

- Name und Domain der neuen Seite: „Dream Spielcenter“ (dream-spielcenter.de)
  für alle Häuser, oder „Spielcenter Dream 24“? Entwurf nutzt „Dream“, Kaufering
  trägt „Spielcenter Dream 24“ (Verzeichnisse nennen dort „Casino Dream 24“)
- Ulm und Landsberg: eigene Standorte (dann Adresse, Telefon, Zeiten) oder
  Senden und Kaufering gemeint?
- Original-Logo als Datei (jetzt SVG-Nachbau)
- Fotos: außen, innen, Geräte, Team – je Standort
- alle Öffnungszeiten bestätigen, besonders Kaufering (9–3 oder 6–3?)
- Füssen: Altersgrenze 18 oder 21?
- Wiesbaden: Adresse Didierstr. 27a oder Äppelallee 27a (Adler-Center)?
- Ausstattung je Standort (Billard, Internet-Café, Parken, Getränke, Klima, Nichtraucher)
- Social-Links (Facebook-Seite „Dream Spielhalle“ gefunden, bestätigen; Instagram?)
- echte offene Stellen (jetzt Beispiele)
- Impressum und Datenschutzerklärung (vom Betreiber, nicht von ORDÉ)
- Formulare sind Attrappen; für den Live-Gang Versand per PHP bauen
- Wer betreut Domain und Hosting heute? (Zertifikate sind abgelaufen)
