# Bewegung – Motion Design zum Scrollen

Beispiel von ORDÉ, kein echter Betrieb. Eine HTML-Datei, ein WebGL2-Bild, keine Fotos, kein Film.

## Die Idee in einem Satz

Die Seite ist ein Motion-Design-Programm: Scrollen spult die Zeitleiste, und auf der Bühne wird aus einem einzigen
Keyframe Schritt für Schritt ein fertiger Film.

Merkmal: Die Werkzeuge sind echt. Kurveneditor, Verschluss (Bewegungsunschärfe) und Zellen reagieren sofort.

## Gestaltungsplan

- **Richtung:** Stil-Bibliothek Nr. 10 (Swiss / Raster-Systeme) mit einem Moment aus Nr. 1 (Formkette).
  Vorbild Handwerk: Studio Dumbar (jede Form bleibt in ihrer Rasterzelle), Dropbox Brand (Regeln als Regler).
- **Bewegungsgrammatik:** Alles bewegt sich nur innerhalb seiner Zelle und in Vierteldrehungen.
  Kurven: rein `cubic-bezier(.65,0,.35,1)`, raus `(.16,1,.3,1)`, Einrasten mit Überschwingen.
- **Farben:** Kreide `#ECEDE8`, Tinte `#141518`, Editor `#17181B`, Signal Blau `#2F5BFF` (nur Werkzeuge),
  Farbe als Ereignis ab Kapitel 6: Rot `#FF3D2E`, Gelb `#FFC21A`, Blau.
- **Schriften:** Instrument Sans (variabel, wird beim schnellen Scrollen schmaler), Space Mono (Werte, Zeitcode).
- **Layout:** Editor mit Bühne, Inspektor rechts (Handy: unten) und Zeitleiste; im letzten Kapitel fällt der
  Editor weg und der Film steht allein.
- **Bewusst nicht:** keine Fotos, kein Film, kein Glitch, keine Überblendungen.

## Kapitel

| # | Kapitel | Was entsteht | Interaktion |
|---|---|---|---|
| 0 | Laden | Raster zeichnet sich, Renderbalken läuft | – |
| 1 | Keyframe | Punkt läuft linear von A nach B, Geisterbilder zeigen gleiche Abstände | – |
| 2 | Kurve | Abstände verdichten sich an den Enden | Griffe ziehen, Vorgaben |
| 3 | Gewicht | Fallen, Stauchen, Nachfedern, echte Bewegungsunschärfe aus 8 Unterbildern | Verschluss 0–360° |
| 4 | Raster | 19 Formen rasten vom Punkt aus ein, drehen sich im Takt (93 BPM) | Maus/Tipp: Vierteldrehung |
| 5 | Schrift | BEWEGUNG füllt acht Zellen | – |
| 6 | Farbe | Farbe kommt per Blende aus der Zellecke | Klick: neue Farbe |
| 7 | Render | Editor verschwindet, der fertige Film läuft | Leertaste/▶: alles abspielen |

Versteckt: Bühne gedrückt halten = Zeitlupe.
