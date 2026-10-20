# ORDÉ Demos

Die sechs Beispielseiten, mit denen ORDÉ zeigt, wie eine Seite aussehen kann.
Keine echten Betriebe. Arbeitssprache Deutsch.

| Ordner | Betrieb | Branche |
|---|---|---|
| `cafe/` | MØRK, mehrseitig | Restaurant, Café |
| `salon/` | Studio Nové | Friseur |
| `fitness/` | FORGE | Studio |
| `komla/` | KOMLA | Fotograf |
| `praxis/` | Praxisseite | Praxis |
| `elektro/` | Elektrobetrieb | Handwerk |

Jede Demo ist eine einzelne HTML-Datei mit eingebettetem CSS plus einem
Bilderordner. Kein Build, kein Framework.

## Entwürfe für echte Betriebe

`demos/entwuerfe/<name>/` sind Gestaltungsvorschläge für **echte** Betriebe,
vor einem Auftrag. Sie gehören nicht zu den sechs Beispielseiten: nicht in
`BRANCHEN` eintragen, keine Vorschaubilder, kein Rückkehr-Balken, `noindex`.
Der Link geht nur an den Betrieb. Quelle und Bauskript liegen außerhalb des
Upload-Ordners unter `entwuerfe/<name>/`. Wird daraus ein Auftrag, zieht das
Projekt in sein eigenes `orde-kunde-<name>`-Repo um und wird hier gelöscht.

**Wie ein Entwurf gebaut, geprüft und gezeigt wird: `entwuerfe/README.md`.**
Kurz: so viele Seiten, wie der Kunde haben will; Link ist
`https://vorschau.byorde.com/<name>/`; dazu das PDF
aus `entwuerfe/pdf-erzeugen.py`; nie eine HTML-Datei an den Kunden.

## Englische Fassungen für den US-Markt

Fünf Demos haben eine englische Fassung neben der deutschen: `en.html`
(beim Café zusätzlich `menu-en.html` und `about-en.html`). Gleiche
Gestaltung, gleiche Bilder, aber eigene Texte: erfundener Standort in den
USA, Preise in Dollar, Uhrzeiten mit am/pm. Die Praxis hat bewusst keine
(Gesundheitsdaten, HIPAA).

Der Rückkehr-Balken führt dort auf die englischen ORDÉ-Seiten unter `/en/`.

Ändert sich an einer Demo Aufbau oder Gestaltung, muss die englische Datei
von Hand nachgezogen werden. `vorschau-erzeugen.py` erzeugt die englischen
Vorschaubilder von selbst mit (`<name>-en.webp`, `<name>-en-handy.webp`).

Für richtige Vorschaubilder müssen die Schriften erreichbar sein: Die Demos
laden sie aus `../../assets/fonts/`, also aus dem Repo `orde-website`. Fehlt
der Ordner, entstehen die Bilder mit Ersatzschriften.

## Nach jeder Änderung an einer Demo

**Vorschaubilder neu erzeugen**, sonst zeigt die ORDÉ-Startseite wochenlang
den alten Stand:

```bash
python3 vorschau-erzeugen.py cafe      # nur diese
python3 vorschau-erzeugen.py           # alle sechs
```

Braucht `playwright` und `pillow`. Liegt Chromium schon irgendwo, kann der
Pfad über `PLAYWRIGHT_CHROMIUM` gesetzt werden.

Das ist der häufigste Fehler in diesem Repo — eine geänderte Demo ohne neues
Vorschaubild fällt niemandem auf, bis ein Kunde sich wundert.

## Eine neue Demo

1. Ordner unter `demos/` anlegen
2. Den Rückkehr-Balken unten einbauen — so wie in den anderen. Ohne ihn
   kommt der Besucher nicht zurück zu ORDÉ, und der Hinweis „Beispielseite ·
   kein echter Betrieb" fehlt.
3. `python3 vorschau-erzeugen.py <name>`
4. Im Repo `orde-website` in `build.py` unter `BRANCHEN` eintragen

## Gestaltung

Diese Demos sind das Schaufenster — sie müssen besser aussehen als die
WordPress-Seiten der Mitbewerber. Für Änderungen die Skills aus dem Plugin
`orde-design` benutzen (in `ordeshop/Claude-test` unter
`plugins/orde-design/`), besonders `high-end-visual-design` und
`design-taste-frontend`.

Die Demos sind zugleich Ausgangspunkt für echte Kundenprojekte: Passt eine
zur Branche des Kunden, wird sie dort als Grundlage genommen und für den
Betrieb umgebaut — nicht kopiert.

## Wo das online liegt

**Kunden-Vorschauen:** `demos/entwuerfe/` geht über GitHub Pages unter
**`https://vorschau.byorde.com/<slug>/`** online, und nur dieser Ordner
(`.github/workflows/vorschau-veroeffentlichen.yml`). Nach jedem Push auf
`main` dauert es ein bis zwei Minuten. Die Startseite `vorschau.byorde.com`
zeigt bewusst keine Kundenliste, `robots.txt` sperrt Suchmaschinen aus.
Eingerichtet in Settings → Pages: Source „GitHub Actions“, Custom domain
`vorschau.byorde.com`, HTTPS erzwungen; DNS-Eintrag bei Hostinger
(CNAME `vorschau` → `ordeshop.github.io`).

**Die sechs Beispielseiten** auf der eigenen Seite:

Auf dem Server unter `/demos/`, also `ordeshop.net/demos/cafe/`. Eigener
FTP-Upload, getrennt von der Website. Beide schreiben in verschiedene Ordner
und löschen nichts voneinander (`dangerous-clean-slate: false`).

## Bilder

Teils selbst erzeugt, teils gestellt. Für echte Kundenseiten gilt: Bilder
stellt der Kunde und sichert die Rechte daran zu (ORDÉ-AGB § 7).

Neue Bilder vor dem Einbauen nach WebP wandeln und verkleinern. Die Demos
waren einmal 20 MB schwer und die Seite dadurch unbenutzbar.
