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
demos/entwuerfe/robots.txt   sperrt Suchmaschinen aus
demos/entwuerfe/<name>/      die fertigen Seiten mit assets/
                             → https://ordeshop.github.io/orde-demos/<name>/
entwuerfe/pdf-erzeugen.py    macht aus einem Entwurf das PDF zum Weiterschicken
```

`<name>` ist derselbe Slug wie das spätere Kunden-Repo: klein, Bindestriche,
ä→ae, ö→oe, ü→ue, ß→ss. Aus „Spielcenter Dream 24“ wird `spielcenter-dream-24`.

## Umfang

So viele Seiten, wie der Kunde haben will. Will er nur eine Startseite, gibt
es eine. Will er mehrere Seiten oder hat er heute schon mehrere, bekommt er
alle davon im Entwurf. Unklar? Nach der bestehenden Website richten.

## Bauen

1. Einen vorhandenen Entwurf als Gerüst kopieren, im Moment
   `entwuerfe/spielcenter-dream-24/`. `build.py` setzt Kopf, Fuß und Menü einmal
   für alle Seiten; Inhalte stehen in `seiten/`. Die Gestaltung wird aber neu
   gemacht: eigene Farben aus dem Logo, eigene Schriften, eigenes Layout.
   Zwei Entwürfe dürfen sich nicht ähneln.
2. Gestaltung mit den Skills aus `orde-design` und der Demo der Branche als
   Ausgangspunkt, wie bei einem echten Auftrag.
3. Schriften und Bibliotheken **lokal** unter `assets/` (keine Google Fonts,
   keine CDNs, DSGVO).
4. Oben der Entwurfs-Hinweis, `noindex`, **kein** Rückkehr-Balken.
5. Inhalte nur aus dem, was belegt ist: bestehende Website, Angaben des
   Kunden, Branchenverzeichnis. Alles Ungeprüfte als gelber Platzhalter.
   Impressum und Datenschutz bleiben Platzhalter, Formulare sind Attrappen.
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

## Prüfen

- Desktop und Handy, auch bei 360 px: nichts ragt über den Rand
- keine toten Links, Menü am Handy geht, Fokus sichtbar
- bei „Bewegung reduzieren“ stehen die Animationen still

## Zeigen

1. Commit und Push auf `main`. Nach ein bis zwei Minuten ist der Entwurf
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
  soll nicht dauerhaft öffentlich herumliegen.

## Checkliste

Jede `entwuerfe/<name>/README.md` enthält die Checkliste aus
`ABLAUF-KUNDENAUFTRAG.md` und wird laufend abgehakt.
