# Entwürfe für echte Betriebe

Hier liegt die Vorschau jedes Kunden: erst der kostenlose Entwurf, nach der
Zusage der aktuelle Baustand. Der Ablauf drumherum steht im Business-Handbuch
in `ABLAUF-KUNDENAUFTRAG.md` (Phase 2 Entwurf, Phase 8 Vorschau während des
Auftrags). Hier steht, wie gebaut und gezeigt wird.

## Ordner

```
entwuerfe/<name>/            Quelle: build.py, seiten/, README.md, PDF
                             (wird nicht hochgeladen)
demos/entwuerfe/index.html   neutrale Startseite der Vorschau-Adresse (keine Kundenliste)
demos/entwuerfe/404.html     Seite für falsche oder gelöschte Links
demos/entwuerfe/robots.txt   wirkt nicht (liegt nicht im Wurzelverzeichnis der
                             Domain); jede Seite braucht noindex
demos/entwuerfe/<name>/      die fertigen Seiten mit assets/
                             → https://ordeshop.github.io/orde-demos/<name>/
demos/entwuerfe/veit/komplett/  Sonderfall: fertige Vorschau ohne build.py (mit _theme/,
                             _bilder/); die *.html darüber leiten nur dorthin weiter,
                             deshalb bricht entwuerfe/veit/build.py ab
demos/entwuerfe/front/       kein Kundenentwurf, sondern ein Showreel-Entwurf
                             (über Pages erreichbar, nicht auf byorde.com; siehe CLAUDE.md)
entwuerfe/pruefen.py         prüft einen Entwurf, bevor ihn jemand sieht
entwuerfe/pdf-erzeugen.py    macht aus einem Entwurf das PDF zum Weiterschicken
```

`<name>` ist derselbe Slug wie das spätere Kunden-Repo: klein, Bindestriche,
ä→ae, ö→oe, ü→ue, ß→ss. Aus „Spielcenter Dream 24“ wird `spielcenter-dream-24`.

## Umfang

So viele Seiten, wie der Kunde haben will. Will er nur eine Startseite, gibt
es eine. Will er mehrere Seiten oder hat er heute schon mehrere, bekommt er
alle davon im Entwurf. Unklar? Nach der bestehenden Website richten.

**Jede Seite, die gezeigt wird, ist von Hand fertig.** Nie eine automatisch
übernommene Kopie der alten Seite zeigen: Ein Fremder findet darin in fünf
Minuten Reste des alten Systems und fehlende Titel, und dann zählt die
Gestaltung nicht mehr. Hat die alte Seite sehr viele Seiten, kommen die
wichtigsten in den Entwurf (Start, Hauptprodukt, Leistung, Service, Kontakt),
und die aber ganz. Der Rest steht als Liste in der README.

## Bauen

1. Einen vorhandenen Entwurf als Gerüst kopieren, im Moment
   `entwuerfe/spielcenter-dream-24/`. `build.py` setzt Kopf, Fuß und Menü einmal
   für alle Seiten; Inhalte stehen in `seiten/`. Die Gestaltung wird aber neu
   gemacht: eigene Farben aus dem Logo, eigene Schriften, eigenes Layout.
   Zwei Entwürfe dürfen sich nicht ähneln.
2. Gestaltung nach `Business-Handbuch/ORDE-STIL.md` mit den Werkzeugen aus
   `Business-Handbuch/werkzeuge/website/` und der Demo der Branche als
   Ausgangspunkt, wie bei einem echten Auftrag.
3. Schriften und Bibliotheken **lokal** unter `assets/` (keine Google Fonts,
   keine CDNs, DSGVO).
4. Oben der Entwurfs-Hinweis, `noindex`, **kein** Rückkehr-Balken.
5. Inhalte nur aus dem, was belegt ist: bestehende Website, Angaben des
   Kunden, Branchenverzeichnis. Alles Ungeprüfte als gelber Platzhalter.
   Impressum und Datenschutz bleiben Platzhalter, Formulare sind Attrappen.
   **Bilder nur echte vom Betrieb** (bestehende Website, Google-Profil,
   vom Kunden geschickt). Keine KI-Bilder, die den Betrieb, seine Räume oder
   seine Leute zeigen, als wären sie echt: Das wäre ein Deepfake im Sinne
   des EU AI Act (Art. 50 Abs. 4) und täuscht obendrein den Kunden. Geht es
   nicht ohne, dann eine neutrale Stimmung ohne erkennbare Personen, und am
   Bild sichtbar „KI-Platzhalter, wird durch echte Fotos ersetzt“.
6. **Recherche:** zuerst die bestehende Website, dann Google-Profil und
   Branchenverzeichnisse. Ist die alte Seite nicht direkt abrufbar, ihre
   Inhalte über die Websuche mit `allowed_domains` auf die Domain des Kunden
   holen. Nur übernehmen, was die offizielle Seite belegt; Abweichungen
   zwischen Quellen als Platzhalter markieren und in der README des Entwurfs
   mit Quelle festhalten.
   Vorher prüfen, wohin die alte Domain weiterleitet (`curl -sI http://<domain>/`)
   und ob es den Betrieb unter anderem Namen schon unter `entwuerfe/` gibt.
   Ein Betrieb hat oft mehrere Domains und Namen (Beispiel: casino-dream24.de
   leitet auf dream-spielcenter.de). Ein Kunde, ein Entwurf, ein Link.
7. Angaben, die auf mehreren Seiten vorkommen (Standorte, Zeiten, Telefon),
   nur an **einer** Stelle in `build.py` pflegen.
8. **Fakten-Freigabeliste** in der README: jeder Name, jede Zahl, jedes Jahr
   mit Quelle. Namen von Personen, Mitarbeiterzahlen und Standorte gegen eine
   zweite Quelle prüfen (Impressum, Handelsregister, Chronik). Was sich
   widerspricht, steht nicht auf der Seite, sondern als gelber Platzhalter
   (`class="todo"`) mit der Frage.
9. **Lücken erklären:** Formulare sind echte Felder mit `data-demo` und dem
   Satz „In der Vorschau wird nichts verschickt“, nie ein Kürzel aus dem alten
   System. Rechtsseiten sagen, warum der Text noch fehlt.
10. Jede Seite mit eigenem `<title>` und `<meta name="description">`.

## Prüfen

- **`python3 entwuerfe/pruefen.py <name>` ohne Fehler.** Findet fehlende
  Titel und Beschreibungen, Reste aus WordPress und Co. (`[formidable id=…]`,
  `wp-block`, Lorem ipsum), tote Links, Dateien von fremden Servern, Bilder
  ohne `alt`, fehlenden Entwurfs-Hinweis und `noindex`. Warnungen gehören in
  den Bericht an Artur. `pdf-erzeugen.py` prüft selbst noch einmal und macht
  bei Fehlern kein PDF.
- Desktop und Handy, auch bei 360 px: nichts ragt über den Rand
- keine toten Links, Menü am Handy geht, Fokus sichtbar
- bei „Bewegung reduzieren“ stehen die Animationen still
- die README liest womöglich auch der Kunde (das Repo ist öffentlich): sachlich
  schreiben, keine internen Wertungen

## Zeigen

1. Commit und Push auf `main`. Vorher bedenken: Der Link ist öffentlich.
   Logo, Fotos und Texte des Betriebs stehen damit offen im Netz. Bei Firmen
   mit eigener Marken- oder Rechtsabteilung erst Artur fragen; dann lieber
   nur das PDF schicken. Nach ein bis zwei Minuten ist der Entwurf
   unter `https://ordeshop.github.io/orde-demos/<name>/` online (Lauf „Vorschau
   veröffentlichen“ unter Actions). **Den Link selbst öffnen**, bevor er
   rausgeht.
2. `python3 entwuerfe/pdf-erzeugen.py <name>` – das PDF zeigt alle Seiten am
   Desktop und am Handy und geht per WhatsApp oder Mail.
3. Dem Kunden nie eine HTML-Datei schicken. Die kann am Handy niemand öffnen.

## Danach

- **Zusage:** Gestaltung und Inhalte nach `orde-kunde-<name>` übernehmen. Der
  Link bleibt derselbe: ab jetzt wird `site/` aus dem Kunden-Repo hierher nach
  `demos/entwuerfe/<name>/` gespiegelt (ohne `*.php`). `entwuerfe/<name>/`
  mit dem alten Bauskript löschen.
- **Live-Gang:** `demos/entwuerfe/<name>/` löschen.
- **Absage:** beide Ordner löschen. Der Entwurf zeigt einen echten Betrieb und
  soll nicht dauerhaft öffentlich herumliegen. In der Git-Historie dieses
  öffentlichen Repos bleibt er trotzdem lesbar, deshalb nie Privates in
  Entwürfe oder READMEs schreiben.

## Checkliste

Jede `entwuerfe/<name>/README.md` enthält die Checkliste aus
`ABLAUF-KUNDENAUFTRAG.md` und wird laufend abgehakt.
