# ORDÉ Demos

Die sechs Beispielseiten, mit denen ORDÉ zeigt, wie eine Seite aussehen kann.

**Das sind keine echten Betriebe.** Jede Seite trägt unten einen Balken mit dem
Hinweis „Beispielseite · kein echter Betrieb" und einem Weg zurück zu ORDÉ.

| Ordner | Was es darstellt | Branche |
|---|---|---|
| `cafe/` | MØRK — Café, mehrseitig mit Karte und Über-uns | Restaurant, Café |
| `salon/` | Studio Nové — Friseursalon | Friseur |
| `fitness/` | FORGE — Fitnessstudio | Studio |
| `komla/` | KOMLA — Fotograf, Portfolio | Fotograf |
| `praxis/` | Praxisseite mit Sprechzeiten | Praxis |
| `elektro/` | Elektrobetrieb mit Leistungen | Handwerk |

## Aufbau

```
demos/           die sechs Seiten, je ein Ordner mit index.html
vorschau/        Screenshots, die die ORDÉ-Website anzeigt
vorschau-erzeugen.py
```

Jede Demo ist eine einzelne HTML-Datei mit eingebettetem CSS plus einem
Bilderordner. Kein Build, kein Framework. Zum Ansehen genügt ein Doppelklick
auf die `index.html`.

## Wo das online liegt

Auf dem Server unter **`/demos/`**, also `ordeshop.net/demos/cafe/` und so
weiter. Die ORDÉ-Website verlinkt dorthin und zeigt die Bilder aus
`vorschau/` unter `demos/vorschau/`.

Hochgeladen wird per FTP durch `.github/workflows/demos-hochladen.yml`.
Das ist ein **eigener Upload**, getrennt von der Website — beide schreiben in
verschiedene Ordner auf demselben Server und kommen sich nicht ins Gehege.

## Eine Demo ändern

1. Die `index.html` der Demo bearbeiten
2. **Vorschaubilder neu erzeugen** — sonst zeigt die Startseite den alten Stand:

```bash
python3 vorschau-erzeugen.py cafe      # nur diese eine
python3 vorschau-erzeugen.py           # alle sechs
```

3. Commit und Push — der Rest läuft von selbst

Voraussetzung für das Skript:

```bash
pip install playwright pillow --break-system-packages
playwright install chromium
```

Liegt Chromium schon irgendwo, kann der Pfad über die Umgebungsvariable
`PLAYWRIGHT_CHROMIUM` gesetzt werden.

## Eine neue Demo hinzufügen

1. Ordner unter `demos/` anlegen, `index.html` hineinlegen
2. Den Rückkehr-Balken unten einbauen — so wie in den anderen Demos, sonst
   kommt der Besucher nicht zurück zur ORDÉ-Seite
3. `python3 vorschau-erzeugen.py <name>` laufen lassen
4. In der ORDÉ-Website in `build.py` unter `BRANCHEN` die Demo eintragen,
   damit sie auf der Startseite und unter „Beispiele" erscheint

## Woher die Bilder stammen

Die Fotos in den Demos sind teils selbst erzeugt, teils vom Auftraggeber
gestellt. Für echte Kundenseiten gilt: Bilder stellt der Kunde, und er
sichert die Rechte daran zu — so steht es in den AGB, § 7.

## Verwandte Projekte

- **`orde-website`** — die eigene Website von ORDÉ, die hierher verlinkt
- **`orde-vorlage`** — Startgerüst für echte Kundenprojekte
