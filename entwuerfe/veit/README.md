# VEIT GmbH – Entwurf für einen Relaunch von veit.de

Stand 04.11.2026. **Vorschau: https://ordeshop.github.io/orde-demos/veit/komplett/**
(die ganze Seite in neuer Gestaltung, Deutsch und Englisch, ein Link mit Sprachwahl).

**Abgelöst:** Der erste Entwurf mit acht Seiten (Quelle `seiten/`, `build.py`) ist
durch die komplette Vorschau ersetzt. `demos/entwuerfe/veit/*.html` leiten nur noch
auf die passende Seite in `komplett/` weiter. `build.py` würde diese Weiterleitungen
überschreiben und bricht deshalb ab; `seiten/` bleibt als Gestaltungsquelle stehen.

Gestaltungsvorschlag vor einem Auftrag, `noindex`, Formulare sind Attrappen.
Betrieb: VEIT GmbH, Landsberg am Lech, Bügel-, Fixier- und Finishtechnik.
Bestehende Seite: www.veit.de (WordPress, rund 1.750 Adressen). Der Entwurf
zeigt acht Seiten: Start, Produkte, Tunnelfinisher TF 57, Anwendungen,
Service, Unternehmen, Karriere, Kontakt.

```bash
python3 entwuerfe/veit/build.py --alt  # nur noch bewusst: seiten/ -> demos/entwuerfe/veit/
```

Relaunch-Plan, Inventar der alten Adressen und Weiterleitungen liegen nicht hier.

## Quellen

Alle Inhalte stammen von www.veit.de (abgerufen 03.11.2026): Startseite,
Unternehmen/Portrait, Meilensteine, Globale Präsenz, Strategie, Management,
Referenzen, Produkte und Produktseiten (TF 57, 8363, SG 66, 2129, SF 27),
Anwendungen, Services/Support, Wartungsvertrag, Karriere, Auszubildende,
Kontakt. Bilder ebenfalls von veit.de (Fassade, Teamfoto 2015, Maschinenfotos,
Drei-Generationen-Foto, historische Aufnahmen). **Keine KI-Bilder.** Die
blaue Stofffläche im Bewegungsmoment ist eine berechnete Grafik
(`stoff-knitter.webp`, Python), sie zeigt nichts Echtes.

Nicht übernommen: Fotos, die nach Bildagentur aussehen (Fotolia-Dateinamen:
Krawatte, Hemden auf Bügeln, Autositz, Frau mit blauem Stoff, Silhouetten,
Schülergruppe). Ob VEIT sie im neuen Auftritt weiter nutzen darf, hängt an den
Lizenzen.

## Gelb markiert = noch zu prüfen

- „18 eigene Gesellschaften“ (Globale Präsenz) gegen „Teams in 18 Ländern“
  (Strategie): Was stimmt?
- „Seit über 60 Jahren“ steht noch auf veit.de, Gründung war 1956. Im Entwurf
  steht deshalb nur „seit 1956“.
- Bildunterschrift Drei-Generationen-Foto (wer steht wo)
- Technische Daten TF 57 (Maße, Anschlusswerte): stehen nicht auf veit.de
- Stellenangebote: kommen heute aus coveto, im Entwurf Platzhalter
- Vertriebspartner-Suche: im Entwurf Attrappe, im echten Auftritt aus der
  bestehenden Datenbank (255 Einträge)
- Impressum, Datenschutz, AGB: unverändert von VEIT übernehmen

## Gestaltungsplan

Nach `ORDE-STIL.md` und `werkzeuge/website/BAUKASTEN.md`.

**Drei Dinge, die es bei VEIT wirklich gibt:** das Typenschild an der Maschine
(Modellnummer: 2129, SG 66, 8363, TF 57), der Dampf, das Blau der
Maschinenverkleidung neben Edelstahl und hellgrauem Lack.

**Die eine Hauptaktion:** Ansprechpartner finden bzw. Anfrage stellen (B2B,
weltweit über Vertriebspartner). Für Bestandskunden: Service-Hotline und
Ersatzteil-Shop, deshalb immer im Kopf erreichbar.

| Achse | Wahl |
|---|---|
| A Schrift | Instrument Sans als einzige Familie, aber in zwei Extremen: Überschriften und Modellnummern schmal (`font-stretch: 75%`) und fett, ein Wort kursiv geneigt wie das Logo („Gemischt“); Fließtext normalbreit 400. Zahlen tabellarisch. 57 + 62 KB. |
| B Farbe | „Maschinenlack“: hellgrauer Stahl `#EEF1F4` und Weiß als Grund, VEIT-Blau `#005CA9` als Volltonfläche (Service-Band, Presse) und für Links, Tinte `#0D1B2A` für Text, Blech `#CBD3DC` für Linien, Rot `#E30613` nur im Logo. |
| C Layout | Datenblatt und Typenschild: Produkte mit großer Modellnummer und echten Werten in Tabellen. Formensprache: eckig, eine schräge Kante (14 px, aus der alten Seite und der Logo-Neigung) an Knöpfen und Bildausschnitten, Haarlinien, keine Schatten. |
| D Kopf | Geteilt: links Satz und zwei Knöpfe auf Weiß, rechts das Foto der Fassade mit dem großen VEIT-Schriftzug, schräg angeschnitten. |
| E Bewegung | **Die Presse:** Beim Scrollen senkt sich ein Pressenkopf auf zerknitterten blauen Stoff, Dampf steigt, der Kopf hebt ab, der Stoff ist glatt und „Pressing for Excellence.“ steht da. Nur transform und opacity. |
| F Kleinteile | Typenschild-Karten in wachsender Breite (die Breite zeigt die Größe der Maschine), Hotline-Liste mit Ländervorwahl, Partnersuche mit zwei Auswahlfeldern. |
| G Navigation | Kopfzeile mit fünf Punkten, rechts Shop, Sprache, Kontakt. Am Handy Vollbild-Menü mit Service-Hotline oben. |
| I Seitenwechsel | `@view-transition` Überblendung. |

**Das eine Merkmal:** die Presse, die den Stoff glättet, und die Modellnummern
als Typenschild.

**Was die Seite bewusst nicht macht:** kein Bildschirm-Slider, keine Stockfotos,
keine Icons aus einer Schriftart (Font Awesome lädt heute von fremdem Server),
kein Cookie-Banner nötig (keine externen Dienste, YouTube nur als Link),
keine Einblende-Animation auf jeder Sektion, keine Kästen in Kästen.

**Bewegungs-Steckbrief Presse:** Auslöser Scrollen durch einen 230 vh hohen
Abschnitt, die Bühne klebt. 0–40 %: Pressenkopf fährt ein. 40–55 %: Kopf
liegt auf, Dampfwolken steigen, Knitter blendet aus. 55–80 %: Kopf hebt ab.
Ab 70 %: Satz erscheint. Handy: gleiche Folge, Abschnitt 200 vh. „Bewegung
reduzieren“: kein Kleben, Endbild (glatter Stoff, Satz sichtbar, Kopf oben).

**Gegenprüfung:** Ein anderer Maschinenbauer bekäme „Blau-Grau mit Produktbild“
auch. Eigen für VEIT sind: Modellnummer als Typenschild, Breite nach
Maschinengröße, die Presse mit Dampf, die schräge Kante aus dem bisherigen
Auftritt (Wiedererkennung), die Kundenliste als Textwand. Gegen das Register
in `BAUKASTEN.md`: Kopf „Geteilt“ und Instrument Sans gab es noch nicht.

**Stilfamilie und Referenzen** (`awesome-claude-design`, `awesome-design-md`):
Familie „Data-Dense Pro“ (scan-lastig, Einkäufer in Betrieben), zurückhaltend.
Als Referenz gelesen: SpaceX (karg, das Bild der Maschine trägt den Abschnitt,
ein Hauptknopf je Band) und Uber (strenge Zweifarbigkeit bei Text, wenig
Schmuck). Übernommen: je Abschnitt höchstens ein Hauptknopf, Maschinenfoto
statt Dekoration, Text nur in Tinte und Blau. Nicht übernommen: Versalien-
Labels über Überschriften (SpaceX), Pillenknöpfe (Uber), Farben und Schriften
dieser Marken.

## Checkliste (aus `ABLAUF-KUNDENAUFTRAG.md`)

```
- [x] 1  Anfrage: Markt DE (Seite DE/EN), Unternehmen, Prüfung erledigt, Slug veit
- [x] 2  Entwurf: gebaut, geprüft (Desktop/Handy), PDF, Link
- [ ] 3  Angebot raus (mit AGB); Umfang sprengt die ORDÉ-Pakete, eigenes Angebot
- [ ] 4  Zusage, Auftragsbestätigung mit Briefing-Link
- [ ] 5  Anzahlung da
- [ ] 6  Briefing vollständig
- [ ] 7  Repo angelegt, gebaut, geprüft
- [ ] 8  Vorschau gezeigt, Korrekturrunde erledigt
- [ ] 9  Fall B (Relaunch): Bestandsaufnahme, Sicherung, Weiterleitungen, umgeschaltet, getestet
- [ ] 10 Abnahme, Schlussrechnung bezahlt
- [ ] 11 Live, Vorschau-Ordner gelöscht, Übergabe, Referenz erfragt
- [ ] 12 Betreuung bis: TT.MM.JJJJ
```
