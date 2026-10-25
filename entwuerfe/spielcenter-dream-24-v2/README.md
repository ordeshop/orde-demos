# Entwurf Spielcenter Dream 24 – Fassung 2 („Nachtfassung“)

**Kopie** von `entwuerfe/spielcenter-dream-24/` vom 25.10.2026, neu gestaltet.
Die erste Fassung bleibt unverändert liegen (Link
https://ordeshop.github.io/orde-demos/spielcenter-dream-24/), damit wir jederzeit
zurückwechseln können. Diese Fassung: https://ordeshop.github.io/orde-demos/spielcenter-dream-24-v2/

Betrieb, Quellen der Angaben, offene Fragen an den Betreiber und Checkliste:
siehe `../spielcenter-dream-24/README.md`. Gilt hier genauso; die Standortdaten
in `build.py` sind dieselben.

## Stand

- 25.10.2026: erster Umbau „Licht an“ (rote Fassade, Glastür mit Neon) von Artur
  abgelehnt: zu viel Rot, Tür-Idee passt nicht, Gesamteindruck stimmt nicht.
  Gewünscht: **dunkel und edel**, Nachtstimmung, warmes Licht, echte Atmosphäre,
  hochwertiger als Fassung 1, aber nicht grell. Der Umbau steht in der Git-Historie.
- 25.10.2026: Nachtfassung gebaut und geprüft (8 Seiten, 360/390/1440 px, Bewegung
  reduziert, axe-core ohne Befund, Tastatur, Zeitlogik mit festen Uhrzeiten), PDF erzeugt.
  Noch an niemanden verschickt. Artur entscheidet,
  welche Fassung der Betreiber sieht; die andere wird dann gelöscht (ein Kunde, ein Link).

## Bauen

    python3 entwuerfe/spielcenter-dream-24-v2/build.py          # Seiten nach demos/entwuerfe/spielcenter-dream-24-v2/
    python3 entwuerfe/pdf-erzeugen.py spielcenter-dream-24-v2   # PDF hier im Ordner

Inhalte in `seiten/`, Kopf, Fuß, Zifferblätter und Standorte (`STANDORTE`) in `build.py`.

## Gestaltungsplan

**Worum es geht:** fünf Spielhallen zwischen Wiesbaden und Füssen, lange offen.
Gäste schauen meist abends am Handy nach: Welches Dream ist in meiner Nähe, hat
es gerade offen, wie komme ich hin? Daneben Bewerber und der Spielerschutz.

**Richtung (Arturs Vorgabe):** dunkel und edel. Das ist eigentlich einer der
Standardlooks aus `ORDE-STIL.md`, hier aber ausdrücklich gewünscht. Damit es
nicht der Durchschnitt „schwarz plus eine grelle Farbe“ wird: warmes Dunkel in
mehreren Stufen statt Schwarz, Licht als Verlauf aus dem Leuchtschild statt
einer Signalfarbe, Messing statt Neon, Rot nur noch im Logo.

| Name | Hex | Wofür |
|---|---|---|
| Nacht | `#110A0A` | Grund, rotstichiges Fast-Schwarz |
| Samt | `#1B1012` | ruhigere Flächen (Jobs, Spielerschutz) |
| Mahagoni | `#2A181B` | Bildplätze, Zeilen beim Darüberfahren |
| Messing | `#D9A65A` | Linien, Zifferblatt, Knöpfe (8,9 : 1 auf Nacht) |
| Elfenbein | `#F3E9DF` | Text |
| Rauchtext | `#BBA89E` | Nebentext (8,3 : 1) |
| Glut | `#FF9A3C` | nur als Lichtschein (Leuchtschild, Lampen) |

**Schriften** (lokal als `.woff2`, OFL): **Bodoni Moda** (variabel mit optischer
Größe) für Überschriften, kursiv für Hervorhebung; **Jost** (geometrisch, Futura-Art)
für Text, Menü und Zahlen; **Lobster** nur im Logo-Nachbau.

**Layout:** Kopf liegt über einer dunklen Bühne. Rechts hängt das Dream-Schild
und ist die Lichtquelle des Raums: Es wirft warmes Licht auf die Wand, dahinter
unscharfe Lichtpunkte wie von Geräten, darüber feines Korn. Links die
Überschrift in Bodoni. Danach die fünf Häuser als Zeilen mit kleinem
Zifferblatt, das Angebot mit großem Bildplatz, Jobs, Spielerschutz, Fuß.

    ┌────────────────────────── Nacht ──────────────────────────┐
    │ dream                Standorte Angebot Jobs Schutz Kontakt │
    │                                         (( dream ))  Licht │
    │ Fünfmal Dream.                       ·   ○        ·        │
    │ Von Wiesbaden bis Füssen.                    ○    ·        │
    │ [Standorte und Zeiten]  Jobs                               │
    └────────────────────────────────────────────────────────────┘
      Fünf Häuser       ◔ Kaufering   offen bis 3 Uhr   Route
      Drinnen im Dream  (Bildplatz + Text)
      Arbeiten, wenn andere ausgehen.
      Spielen hat bei uns Grenzen.

**Das eine Merkmal: Öffnungszeiten als 24-Stunden-Zifferblatt.** Mitternacht
oben, ein Messingbogen zeigt die heutigen Öffnungsstunden, ein Zeiger die
aktuelle Uhrzeit in Deutschland, in der Mitte steht die Uhrzeit. Liegt der Zeiger
im Bogen, ist offen. Weil die Häuser bis 3 Uhr nachts offen haben, läuft der
Bogen über Mitternacht. Groß bei jedem Haus auf der Seite „Standorte“, klein in
jeder Zeile der Startseite. Oben auf „Standorte“ eine große Uhr mit einem Ring je
Haus und einem Zeiger: Wo er einen Bogen kreuzt, ist offen. Die Namen stehen an
Hinweislinien rechts, durch die Stunden, in denen alle zu haben. Ohne JavaScript
zeigen die Blätter die Zeiten von Montag bis Samstag.

**Bewegung:** ein Moment beim Laden. Das Schild geht an, dann füllt sich der
Raum mit warmem Licht. Bei „Bewegung reduzieren“ ist es sofort hell.

**Was die Seite bewusst nicht macht:**
- kein Casino-Look (Chips, Karten, Jackpot, Goldregen, „Gewinne“): Werbung für
  Spielhallen ist nach Glücksspielstaatsvertrag eng begrenzt
- kein Rot als Fläche, kein Neon, keine Strahlen wie in Fassung 1
- keine Labels über Überschriften, keine Icon-Karten, keine nummerierten
  Abschnitte (außer dem echten Ablauf der Bewerbung), keine Einblende-Animationen
- keine erfundenen Zahlen, Fotos oder Bewertungen; Fotos bleiben sichtbare Platzhalter

**Referenzen** (`awesome-claude-design`, `awesome-design-md`): Familie
„Cinematic Dark“ auf ausdrücklichen Wunsch. Gelesen: `ferrari` (Fast-Schwarz,
Markenfarbe nur als Signal, viel Luft), `bugatti` (Zurückhaltung, große Typo,
Linien statt Kästen), `1win` (Casino: laute Farben nur im Inhalt, nicht im
Rahmen). Farben und Schriften kommen vom Betrieb und vom Material Messing, nicht
von diesen Marken.

**Gegenprüfung:** Der Standard der Branche ist schwarz mit Gold und Chips oder
Neon. Hier gibt es keine Spielsymbole, das Licht kommt aus dem echten Schild des
Betriebs, und das Zifferblatt zeigt die echten Zeiten. Ähnlichkeit zu den
ORDÉ-Demos: FORGE ist dunkel, aber kalt und hart; diese Seite ist warm, mit
Kontrastschrift und Messing.

## Technik

Statisches HTML und CSS, ein kleines `main.js` (Menü, Live-Status, Zifferblätter,
Formular-Attrappe). Kein Framework, kein CDN. Icons: Tabler (MIT) als Inline-SVG.
Lizenzen unter `demos/entwuerfe/spielcenter-dream-24-v2/assets/fonts/LIZENZEN.txt`.
