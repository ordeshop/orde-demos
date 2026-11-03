"""Packt den gebauten Entwurf (site/) in EINE HTML-Datei zum Durchklicken.

Alle acht Seiten, Bilder, Schrift, CSS und JS stecken in der Datei. Sie läuft ohne
Internet und ohne Server: Doppelklick am Laptop, am Handy im Browser öffnen.
Die Seiten wechseln über die Adresse #/produkte, #/service/auftrag usw.

Aufruf (nach build.py):  python3 entwuerfe/veit/einzeldatei.py
Ergebnis: VEIT-Entwurf-klickbar.html
"""
import base64
import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent
SITE = HIER.parent.parent / "demos" / "entwuerfe" / "veit"
ZIEL = HIER / "VEIT-Entwurf-klickbar.html"
SEITEN = ["index", "produkte", "tunnelfinisher-tf-57", "anwendungen", "service", "unternehmen", "karriere", "kontakt"]
TYPEN = {".webp": "image/webp", ".svg": "image/svg+xml", ".woff2": "font/woff2"}


def daten_uri(pfad):
    p = SITE / pfad
    return f"data:{TYPEN[p.suffix]};base64," + base64.b64encode(p.read_bytes()).decode()


def links_umbiegen(html):
    """seite.html#anker -> #/seite/anker"""
    def ersetzen(m):
        seite, anker = m.group(1), m.group(2)
        return f'href="#/{seite}' + (f"/{anker}" if anker else "") + '"'
    return re.sub(r'href="([\w-]+)\.html(?:#([\w-]+))?"', ersetzen, html)


def ids_vorsetzen(html, seite):
    """IDs je Seite eindeutig machen, Bezüge innerhalb der Seite mitziehen."""
    ids = set(re.findall(r'\bid="([\w-]+)"', html))
    for i in ids:
        neu = f"{seite}-{i}"
        html = re.sub(rf'\bid="{i}"', f'id="{neu}"', html)
        html = re.sub(rf'\b(for|aria-labelledby|aria-controls)="{i}"', rf'\1="{neu}"', html)
        html = html.replace(f'href="#{i}"', f'href="#/{seite}/{i}"')
    return html


def main_inhalt(seite):
    t = (SITE / f"{seite}.html").read_text(encoding="utf-8")
    titel = re.search(r"<title>(.*?)</title>", t).group(1)
    inhalt = t.split('<main id="inhalt">', 1)[1].split("</main>", 1)[0]
    return titel, inhalt


def bauen():
    roh = (SITE / "index.html").read_text(encoding="utf-8")
    kopf, rest = roh.split('<main id="inhalt">', 1)
    fuss = rest.split("</main>", 1)[1]

    teile = []
    for s in SEITEN:
        titel, inhalt = main_inhalt(s)
        inhalt = links_umbiegen(ids_vorsetzen(inhalt, s))
        titel_attr = titel.replace('"', "&quot;")
        teile.append(f'<div class="seite" data-seite="{s}" data-titel="{titel_attr}"{"" if s == "index" else " hidden"}>{inhalt}</div>')

    kopf = kopf.replace(" aria-current=page", "")
    html = kopf + '<main id="inhalt">' + "\n".join(teile) + "</main>" + fuss
    html = links_umbiegen(html)
    html = html.replace("Gestaltungsentwurf für eine neue veit.de",
                        "Gestaltungsentwurf für eine neue veit.de zum Durchklicken")

    # CSS und JS einbetten, Schrift und Bilder als Daten-URI
    css = (SITE / "assets/style.css").read_text(encoding="utf-8")
    css = re.sub(r"url\((fonts/[^)]+|bilder/[^)]+)\)", lambda m: f"url({daten_uri('assets/' + m.group(1))})", css)
    css += "\n.seite[hidden] { display: none; }\n"
    js = (SITE / "assets/main.js").read_text(encoding="utf-8")
    html = re.sub(r'<link rel="preload"[^>]+>\n', "", html)
    html = re.sub(r'<link rel="stylesheet"[^>]+>', f"<style>{css}</style>", html)
    html = re.sub(r'<script src="assets/main.js[^"]*" defer></script>', "", html)
    html = re.sub(r'(src|href)="(assets/bilder/[^"]+)"', lambda m: f'{m.group(1)}="{daten_uri(m.group(2))}"', html)

    router = r"""<script>
/* Seitenwechsel in der Einzeldatei: #/seite oder #/seite/anker */
(() => {
  const ruhig = matchMedia('(prefers-reduced-motion: reduce)');
  const seiten = [...document.querySelectorAll('.seite')];
  const menue = document.getElementById('menue');
  const zeigen = () => {
    const h = location.hash;
    if (h && !h.startsWith('#/')) return;
    let [name, anker] = h.replace(/^#\/?/, '').split('/');
    if (!seiten.some(s => s.dataset.seite === name)) name = 'index';
    seiten.forEach(s => { s.hidden = s.dataset.seite !== name; });
    const aktiv = seiten.find(s => s.dataset.seite === name);
    document.title = aktiv.dataset.titel.replace(/&quot;/g, '"');
    document.querySelectorAll('.hauptnav a, .menue a').forEach(a => {
      if (a.getAttribute('href') === '#/' + name) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    if (menue && !menue.hidden) { menue.hidden = true; document.body.style.overflow = ''; document.querySelector('.menue-knopf').setAttribute('aria-expanded', 'false'); }
    const ziel = anker && document.getElementById(name + '-' + anker);
    if (ziel) ziel.scrollIntoView(); else scrollTo(0, 0);
    dispatchEvent(new Event('resize'));
  };
  const wechseln = () => (document.startViewTransition && !ruhig.matches) ? document.startViewTransition(zeigen) : zeigen();
  addEventListener('hashchange', wechseln);
  zeigen();
})();
</script>
"""
    html = html.replace("</body>", router + f"<script>{js}</script>\n</body>")
    ZIEL.write_text(html, encoding="utf-8")
    print(ZIEL.name, round(ZIEL.stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    bauen()
