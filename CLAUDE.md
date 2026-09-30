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

Auf dem Server unter `/demos/`, also `ordeshop.net/demos/cafe/`. Eigener
FTP-Upload, getrennt von der Website. Beide schreiben in verschiedene Ordner
und löschen nichts voneinander (`dangerous-clean-slate: false`).

## Bilder

Teils selbst erzeugt, teils gestellt. Für echte Kundenseiten gilt: Bilder
stellt der Kunde und sichert die Rechte daran zu (ORDÉ-AGB § 7).

Neue Bilder vor dem Einbauen nach WebP wandeln und verkleinern. Die Demos
waren einmal 20 MB schwer und die Seite dadurch unbenutzbar.
