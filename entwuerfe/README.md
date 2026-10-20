# Entwürfe für echte Betriebe

Kostenlose Gestaltungsvorschläge **vor** einem Auftrag. Der Ablauf drumherum
(wann es einen Entwurf gibt, was danach kommt) steht im Business-Handbuch in
`ABLAUF-KUNDENAUFTRAG.md`, Schritt 1a. Hier steht, wie er gebaut und gezeigt
wird.

## Ordner

```
entwuerfe/<name>/            Quelle: build.py, seiten/, README.md, PDF
                             (wird nicht hochgeladen)
demos/entwuerfe/<name>/      die fertigen Seiten mit assets/
                             → https://ordeshop.github.io/orde-demos/demos/entwuerfe/<name>/
entwuerfe/pdf-erzeugen.py    macht aus einem Entwurf das PDF zum Weiterschicken
```

`<name>` ist derselbe Slug wie das spätere Kunden-Repo: klein, Bindestriche,
ä→ae, ö→oe, ü→ue, ß→ss. Aus „Dream Spielcenter“ wird `dream-spielcenter`.

## Umfang

So viele Seiten, wie der Kunde haben will. Will er nur eine Startseite, gibt
es eine. Will er mehrere Seiten oder hat er heute schon mehrere, bekommt er
alle davon im Entwurf. Unklar? Nach der bestehenden Website richten.

## Bauen

1. Einen vorhandenen Entwurf als Gerüst kopieren, im Moment
   `entwuerfe/dream-spielcenter/`. `build.py` setzt Kopf, Fuß und Menü einmal
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

## Prüfen

- Desktop und Handy, auch bei 360 px: nichts ragt über den Rand
- keine toten Links, Menü am Handy geht, Fokus sichtbar
- bei „Bewegung reduzieren“ stehen die Animationen still

## Zeigen

1. Commit und Push auf `main`. Nach ein bis zwei Minuten ist der Entwurf
   unter dem Pages-Link oben online. **Den Link selbst öffnen**, bevor er
   rausgeht.
2. `python3 entwuerfe/pdf-erzeugen.py <name>` – das PDF zeigt alle Seiten am
   Desktop und am Handy und geht per WhatsApp oder Mail.
3. Dem Kunden nie eine HTML-Datei schicken. Die kann am Handy niemand öffnen.

## Danach

- Wird es ein Auftrag: Inhalte nach `orde-kunde-<name>` übernehmen, dann
  beide Ordner hier löschen.
- Wird es keiner: beide Ordner löschen. Der Entwurf zeigt einen echten
  Betrieb und soll nicht dauerhaft öffentlich herumliegen.
