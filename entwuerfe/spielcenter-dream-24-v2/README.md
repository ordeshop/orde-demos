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
- 25.10.2026: Farben der Originalseite übernommen, Zifferblätter durch Zeitstrahl ersetzt
  (beides Arturs Wunsch).
- 25.10.2026: Feinschliff „Luxus“ (siehe unten) gebaut und geprüft: 360/390/1024/1440 px,
  axe-core ohne Befund, Live-Zeile und Zeitstrahl mit fünf festen Uhrzeiten getestet.
- 25.10.2026: Kursive getauscht, Arturs Wunsch (die Bodoni-Kursive gefiel ihm nicht):
  jetzt **Spectral kursiv**. 25 Schriften verglichen, auf der echten Seite in engerer Wahl
  Spectral, Brygada 1918, Libre Baskerville, Castoro, Unna und Yellowtail (Schreibschrift).
  Spectral, weil die Haarstriche auf Schwarz nicht wegbrechen, w und D ohne Schnörkel sind,
  sie bis 17 px gut lesbar bleibt und „Fünfmal Dream.“ am Handy einzeilig bleibt. Ersatz,
  falls gewünscht: Brygada 1918 (wärmer) oder Unna (leichter). Geprüft: 360/390/1440 px,
  axe-core ohne Befund, keine vom Browser schräggestellte Bodoni mehr.

## Bauen

    python3 entwuerfe/spielcenter-dream-24-v2/build.py          # Seiten nach demos/entwuerfe/spielcenter-dream-24-v2/
    python3 entwuerfe/pdf-erzeugen.py spielcenter-dream-24-v2   # PDF hier im Ordner

Inhalte in `seiten/`, Kopf, Fuß, Zeitstrahl und Standorte (`STANDORTE`) in `build.py`.

## Gestaltungsplan

**Worum es geht:** fünf Spielhallen zwischen Wiesbaden und Füssen, lange offen.
Gäste schauen meist abends am Handy nach: Welches Dream ist in meiner Nähe, hat
es gerade offen, wie komme ich hin? Daneben Bewerber und der Spielerschutz.

**Richtung (Arturs Vorgabe):** dunkel und edel, mit den **Farben der Originalseite**
(Fassung 1, Arturs Wunsch vom 25.10.2026, nachdem eine Messing-Variante gezeigt war).
Dunkel mit greller Akzentfarbe ist eigentlich einer der Standardlooks aus
`ORDE-STIL.md`, hier aber ausdrücklich gewünscht und durch das Logo des Betriebs
begründet. Edel wird es über Schrift, Luft, feine Linien und Licht statt über
laute Flächen: Der Marken-Verlauf steht nur auf dem hervorgehobenen Wort der
Überschrift, auf den Balken im Zeitstrahl und auf dem Hauptknopf.

| Name | Hex | Wofür |
|---|---|---|
| Schwarz | `#050505` | Grund |
| Kohle | `#0E0E0F` | ruhigere Flächen (Drinnen, Spielerschutz, Fuß) |
| Stahl | `#18181B` | Bildplätze |
| Rot → Orange → Gelb | `#E3171B` → `#F6731F` → `#FFC928` | Marken-Verlauf wie im Logo: hervorgehobene Wörter (nur große Schrift), Balken im Zeitstrahl; Hauptknopf Orange → Gelb mit schwarzer Schrift (7,4 : 1) |
| Orange | `#F6731F` | Links, Linien, Icons (7,2 : 1) |
| Gelb | `#FFC928` | Fokus, „heute“, Platzhalter |
| Grün | `#38D27A` / Text `#7BE3A2` | „Jetzt geöffnet“, wie in Fassung 1 |
| Text / Grau | `#E9E7E4` / `#A4A19C` | Text und Nebentext (7,9 : 1) |

**Schriften** (lokal als `.woff2`, OFL): **Bodoni Moda** (variabel mit optischer
Größe) für Überschriften; **Spectral kursiv** für alles Kursive (hervorgehobene Wörter,
Pausenzeile, Bildideen, Zusatz unter den Häusern); **Jost** (geometrisch, Futura-Art)
für Text, Menü und Zahlen; **Lobster** nur im Logo-Nachbau.

**Layout:** Kopf liegt über einer dunklen Bühne. Rechts hängt das Dream-Schild
und ist die Lichtquelle des Raums: Es wirft warmes Licht auf die Wand, dahinter
unscharfe Lichtpunkte wie von Geräten, darüber feines Korn. Links die
Überschrift in Bodoni. Danach die fünf Häuser als Zeilen mit kleinem
Zeitstrahl, das Angebot mit großem Bildplatz, Jobs, Spielerschutz, Fuß.

    ┌────────────────────────── Nacht ──────────────────────────┐
    │ dream                Standorte Angebot Jobs Schutz Kontakt │
    │                                         (( dream ))  Licht │
    │ Fünfmal Dream.                       ·   ○        ·        │
    │ Von Wiesbaden bis Füssen.                    ○    ·        │
    │ [Standorte und Zeiten]  Jobs                               │
    └────────────────────────────────────────────────────────────┘
      Fünf Häuser       Kaufering  ▬▬▬▬▬|▬  offen bis 3 Uhr   Route
      Drinnen im Dream  (Bildplatz + Text)
      Arbeiten, wenn andere ausgehen.
      Spielen hat bei uns Grenzen.

**Das eine Merkmal: Öffnungszeiten als Zeitstrahl.** Ein Tag läuft von 6 Uhr
morgens bis 6 Uhr am nächsten Morgen, so bleibt „9 bis 3 Uhr nachts“ ein
durchgehender Balken im Marken-Verlauf. Ein weißer Strich zeigt die Uhrzeit
jetzt in Deutschland; steht er im Balken, ist offen (geschlossene Häuser:
gedimmter Balken). Klein in jeder Zeile der Startseite und bei jedem Haus, oben
auf „Standorte“ als Zeitplan aller Häuser untereinander mit einem gemeinsamen
Strich und der Uhrzeit. Ohne JavaScript zeigen die Balken die Zeiten von Montag.
(Vorher 24-Stunden-Zifferblätter; auf Arturs Wunsch vom 25.10.2026 ersetzt.)

**Bewegung:** ein Moment beim Laden. Das Schild geht an, dann füllt sich der
Raum mit warmem Licht. Bei „Bewegung reduzieren“ ist es sofort hell.

**Was die Seite bewusst nicht macht:**
- kein Casino-Look (Chips, Karten, Jackpot, Goldregen, „Gewinne“): Werbung für
  Spielhallen ist nach Glücksspielstaatsvertrag eng begrenzt
- kein Rot als Fläche, kein Neon, keine Strahlen und kein Laufband wie in Fassung 1
- keine Labels über Überschriften, keine Icon-Karten, keine nummerierten
  Abschnitte (außer dem echten Ablauf der Bewerbung), keine Einblende-Animationen
- keine erfundenen Zahlen, Fotos oder Bewertungen; Fotos bleiben sichtbare Platzhalter

**Referenzen** (`awesome-claude-design`, `awesome-design-md`): Familie
„Cinematic Dark“ auf ausdrücklichen Wunsch. Gelesen: `ferrari` (Fast-Schwarz,
Markenfarbe nur als Signal, viel Luft), `bugatti` (Zurückhaltung, große Typo,
Linien statt Kästen), `1win` (Casino: laute Farben nur im Inhalt, nicht im
Rahmen). Farben kommen aus der Originalseite und dem Logo, nicht von diesen Marken.

**Gegenprüfung:** Der Standard der Branche ist schwarz mit Gold und Chips oder
Neon. Hier gibt es keine Spielsymbole, das Licht kommt aus dem echten Schild des
Betriebs, und der Zeitstrahl zeigt die echten Zeiten. Ähnlichkeit zu den
ORDÉ-Demos: FORGE ist dunkel, aber kalt und hart; diese Seite ist warm, mit
Kontrastschrift und dem Verlauf aus dem Dream-Logo.

## Feinschliff „Luxus“ (25.10.2026)

Arturs Wunsch: noch luxuriöser und professioneller. Richtung, Farben, Schriften und
Zeitstrahl bleiben; geändert wird, was billig wirkte, und es kommen Details dazu, wie
sie Grandhotels und Spielbanken bei Nacht zeigen.

- **Bühne als Filmvorspann, auf der Mittelachse:** das Dream-Schild als Emblem mit
  Lichthof, einem feinen waagerechten Lichtstreif (wie ein anamorphotisches Objektiv)
  und einer Spiegelung wie auf schwarzem Glas. Die runden Lichtflecken entfallen
  (wirkten wie ein Effektfilter), es bleiben wenige winzige Funken. Unten eine
  Live-Zeile: welche Häuser gerade geöffnet sind.
- **Kopf:** bleibt beim Scrollen stehen und wird dann mattes Glas; auf der Startseite
  erscheint das Logo darin erst, wenn das große Schild aus dem Bild ist (kein
  doppeltes Logo).
- **Häuser von Norden nach Süden** (Wiesbaden, Heidenheim, Senden, Kaufering,
  Füssen), passend zu „Von Wiesbaden bis Füssen“. Größere Namen, feinerer Zeitstrahl.
- **Bildregie statt grauer Kästen:** Fotoplätze sind Rahmen mit Sucherecken und einer
  Bildidee samt Format („Gerätereihe im Halbdunkel, warmes Seitenlicht, Hochformat
  4 : 5“). So weiß der Betreiber, welches Foto er liefern soll.
- **Rhythmus:** eine große Schriftzeile als Pause zwischen den Abschnitten
  („Täglich geöffnet · Zutritt ab 18 · Nur mit Ausweis“), Spielerschutz als gerahmte
  Plakette, großer Fuß mit allen Häusern und Telefonnummern.
- **Zierde aus dem Logo:** der Stern des Dream-Logos als einziges Ornament (Trenner,
  Plakette), sparsam eingesetzt.
- **Details:** feines Filmkorn über der ganzen Seite, Lichtkante am Hauptknopf, Unterstrich
  der Navigation wächst aus der Mitte, ruhigere Platzhalter-Markierung, Favicon.
- Bewegung bleibt bei einem Moment: Beim Laden geht das Schild an, der Lichtstreif zieht
  auf, der Raum wird hell.

## Technik

Statisches HTML und CSS, ein kleines `main.js` (Menü, Live-Status, Zeitstrahl,
Formular-Attrappe). Kein Framework, kein CDN. Icons: Tabler (MIT) als Inline-SVG.
CSS und JS werden mit `?v=` und einem Prüfwert des Inhalts eingebunden (`build.py`),
damit nach einer Änderung kein Browser die alte Datei aus dem Zwischenspeicher zeigt.
Lizenzen unter `demos/entwuerfe/spielcenter-dream-24-v2/assets/fonts/LIZENZEN.txt`.
