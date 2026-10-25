# Entwurf Spielcenter Dream 24 – Fassung 2 („Licht an“)

**Kopie** von `entwuerfe/spielcenter-dream-24/` vom 25.10.2026, neu gestaltet.
Die erste Fassung bleibt unverändert liegen (Link
https://ordeshop.github.io/orde-demos/spielcenter-dream-24/), damit wir jederzeit
zurückwechseln können. Diese Fassung: https://ordeshop.github.io/orde-demos/spielcenter-dream-24-v2/

Betrieb, Quellen der Angaben, offene Fragen an den Betreiber und Checkliste:
siehe `../spielcenter-dream-24/README.md`. Gilt hier genauso; die Standortdaten
in `build.py` sind dieselben.

## Stand

- 25.10.2026: Fassung 2 gebaut und geprüft (8 Seiten, 360/390/1440 px, Bewegung
  reduziert, axe-core ohne Befund, Tastatur), PDF `Entwurf-spielcenter-dream-24-v2.pdf`.
  Noch an niemanden verschickt. Artur entscheidet, welche Fassung der Betreiber sieht;
  die andere wird dann gelöscht (ein Kunde, ein Link).

## Bauen

    python3 entwuerfe/spielcenter-dream-24-v2/build.py          # Seiten nach demos/entwuerfe/spielcenter-dream-24-v2/
    python3 entwuerfe/pdf-erzeugen.py spielcenter-dream-24-v2   # PDF hier im Ordner

Inhalte in `seiten/`, Kopf, Fuß, Türen und Standorte (`STANDORTE`) in `build.py`.

## Warum neu

Die erste Fassung traf einen der drei KI-Standardlooks aus `ORDE-STIL.md`
(fast schwarz mit greller Akzentfarbe), hatte über jeder Überschrift ein
kleines Label, als zweite Sektion vier gleiche Icon-Karten, Leerformeln
(„Willkommen im Dream“, „Mehr als nur ein Spiel“) und auf jeder Sektion
dieselbe Einblende-Animation.

## Gestaltungsplan

**Worum es geht:** fünf Spielhallen zwischen Wiesbaden und Füssen, lange
offen. Gäste schauen meist abends am Handy nach: Welches Dream ist in meiner
Nähe, hat es gerade offen, wie komme ich hin? Daneben Bewerber und der
Spielerschutz, der rechtlich sichtbar sein muss.

**Farben** (aus dem Logo, also aus der Leuchtreklame des Betriebs):

| Name | Hex | Wofür |
|---|---|---|
| Fassade | `#D2121A` | ganze Flächen: Kopf jeder Seite, Jobs-Band. Weiß darauf 5,5 : 1 |
| Rot Text | `#C8101A` | Knöpfe und Links auf Weiß (5,9 : 1) |
| Tinte | `#2A0F12` | Text, Fuß (rotstichiges Schwarz statt #000) |
| Rauch | `#F6F0EE` | ruhige Zwischenfläche, Zeilen beim Darüberfahren |
| Glas | `#1B1518` | nur die Glastür |
| Glut / Sonne | `#FF8A1E` / `#FFD23A` | nur Leuchtschild, Neonschein und gelbe Platzhalter |

**Schriften** (lokal als `.woff2`, alle OFL):
- **Anybody** (variabel, Breite 50–150 %): Überschriften. Das Spiel mit der
  Breite ist die Typo-Idee: „Fünfmal Dream.“ extra breit wie Automaten-
  Schriftzüge, „Von Wiesbaden bis Füssen.“ schmal wie Klebebuchstaben auf
  Glas. Schmal auch für die Folienschrift auf den Türen.
- **Hanken Grotesk** (variabel): Fließtext.
- **Tilt Neon**: nur das Neon-Wort „offen“.
- **Lobster**: nur im Logo-Nachbau.

**Layout:** Der Kopf jeder Seite ist die rote Fassade, darunter beginnt der
weiße „Gehweg“. Auf der Startseite steht in der Fassade links die Überschrift,
rechts die Eingangstür eines Hauses. Danach alle Häuser als Zeilen (keine
Karten), das Angebot mit großem Bildplatz, ein rotes Jobs-Band, der
Spielerschutz mit der Hotline groß, Fuß in Tinte.

    ┌──────────── rote Fassade ─────────────────────────────┐
    │ dream-Schild      Standorte Angebot Jobs Schutz Kontakt│
    │                                    ( Ort wählen )      │
    │ FÜNFMAL DREAM.                     ┌──────────┐        │
    │ Von Wiesbaden bis Füssen.          │  ~offen~ │        │
    │ Text · [Alle Adressen und Zeiten]  │  Zeiten  │        │
    └────────────────────────────────────┴──────────┴────────┘
      Welches Dream liegt bei Ihnen?   (fünf Zeilen, Live-Status)
      Drinnen im Dream                  (Bildplatz + Text)
    ▓▓▓ Arbeiten, wenn andere ausgehen. (rotes Band) ▓▓▓▓▓▓▓▓▓▓
      Spielen hat bei uns Grenzen.      (Regeln + Hotline)

**Das eine Merkmal: die Eingangstür mit echtem Neon-Schild.** Jedes Haus
wird als seine Glastür gezeigt: Neon „offen“, Öffnungszeiten als
Klebebuchstaben, Altersgrenze, Pflichthinweis, Adresse auf dem Sockelblech.
Das Neon leuchtet nur, wenn das Haus nach deutscher Zeit wirklich geöffnet
hat; sonst bleibt die Röhre dunkel und darunter steht, wann es wieder
aufmacht. Beim Laden zündet die Röhre wie echtes Neon (einziger
Bewegungsmoment). Auf der Startseite wählt man das Haus, auf der Seite
„Standorte“ stehen am Desktop alle fünf Türen nebeneinander wie eine
Straße. Funktioniert ohne JavaScript (Auswahl per CSS `:has()`).

**Was die Seite bewusst nicht macht:**
- kein Casino-Look (Chips, Karten, Jackpot, Goldregen, „Gewinne“): Werbung
  für Spielhallen ist nach Glücksspielstaatsvertrag eng begrenzt, und die
  Seite soll informieren, nicht anheizen
- keine Labels über Überschriften, keine Icon-Karten, keine nummerierten
  Abschnitte (außer dem echten Ablauf der Bewerbung)
- keine Einblende-Animationen, kein GSAP mehr (Seite deutlich leichter)
- keine erfundenen Zahlen, Fotos oder Bewertungen; Fotos bleiben sichtbare Platzhalter

**Referenzen** (`awesome-claude-design`, `awesome-design-md`): Stilfamilie
„Playful Color“ in ernster Ausführung, ausdrücklich nicht „Cinematic Dark“.
Gelesen: `airbnb` (eine einzige Markenfarbe auf Weiß, 48-px-Knöpfe, 8 px
Radius), `wise` (schwere Display-Schrift, ein interaktives Element im Kopf
als Kern der Seite, bei Wise der Rechner, hier die Tür), `1win` (Casino:
übernommen nur die Disziplin, dass die lauten Farben im Inhalt stecken, hier
im Leuchtschild, nicht im Rahmen). Farben und Schriften kommen vom Betrieb,
nicht von diesen Marken.

**Gegenprüfung:** Würde eine andere Spielhalle dasselbe bekommen? Die Tür
vielleicht, aber nicht in Dream-Rot, mit diesem Schild, diesen Zeiten und
dieser Straße aus fünf Häusern. Der Standardentwurf der Branche ist schwarz
mit Gold oder Neon. Ähnlichkeit zu den ORDÉ-Demos (MØRK, Studio Nové, FORGE,
KOMLA, Praxis, Elektro): keine rote Vollfläche, keine Tür-Idee, keine
Breitenachse.

## Technik

Statisches HTML und CSS, ein kleines `main.js` (Menü, Live-Status, Neon,
gemerkte Hausauswahl, Formular-Attrappe). Kein Framework, kein CDN. Icons:
sechs Tabler-Icons (MIT) als Inline-SVG. Schriften aus Fontsource (OFL).
Lizenzen unter `demos/entwuerfe/spielcenter-dream-24-v2/assets/fonts/LIZENZEN.txt`.
