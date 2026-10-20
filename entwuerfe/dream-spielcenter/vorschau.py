"""Baut dream-demo.html: alle Seiten in einer Datei, zum Ansehen am Handy.

Schriften, Icons und Skripte werden eingebettet, Links wie "jobs.html#bewerben"
werden zu "#jobs/bewerben", und ein kleiner Router zeigt jeweils eine Seite.
Aufruf (nach build.py):  python3 entwuerfe/dream-spielcenter/vorschau.py
Die Datei landet hier im Quellordner, nicht im hochgeladenen Ordner.
"""
import base64
import json
import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent
ROOT = HIER.parent.parent / "demos" / "entwuerfe" / "dream-spielcenter"
SEITEN = ["index", "angebot", "standorte", "jobs", "spielerschutz", "kontakt", "impressum", "datenschutz"]


def b64(pfad):
    return base64.b64encode((ROOT / pfad).read_bytes()).decode()


def links(html):
    def ersetze(m):
        seite, anker = m.group(1), m.group(2)
        return f'href="#{seite}{"/" + anker if anker else ""}"'
    return re.sub(r'href="(\w+)\.html(?:#([\w-]+))?"', ersetze, html)


def main():
    erste = (ROOT / "index.html").read_text()
    kopf, rest = erste.split("<main id=\"inhalt\">", 1)
    fuss = rest.split("</main>", 1)[1]

    seiten, titel = [], {}
    for name in SEITEN:
        html = (ROOT / f"{name}.html").read_text()
        titel[name] = re.search(r"<title>(.*?)</title>", html).group(1)
        inhalt = html.split("<main id=\"inhalt\">", 1)[1].split("</main>", 1)[0]
        # Anker innerhalb einer Seite (#bewerben) an die Seite binden
        inhalt = re.sub(r'<a ([^>]*)href="#([\w-]+)"', lambda m: f'<a {m.group(1)}href="#{name}/{m.group(2)}"', inhalt)
        seiten.append(f'<div data-page="{name}" hidden>{links(inhalt)}</div>')

    css = (ROOT / "assets/css/style.css").read_text()
    css = re.sub(r"url\(\.\./fonts/([^)]+)\)", lambda m: f"url(data:font/woff2;base64,{b64('assets/fonts/' + m.group(1))})", css)

    icons = (ROOT / "assets/icons/tabler-icons.min.css").read_text()
    alles = "".join(seiten) + kopf + fuss
    benutzt = set(re.findall(r"\bti-[a-z0-9-]+", alles))
    regeln = "".join(m.group(0) for m in re.finditer(r"\.(ti-[a-z0-9-]+):before\{[^}]*\}", icons) if m.group(1) in benutzt)
    icon_css = ('@font-face{font-family:"tabler-icons";font-display:block;src:url(data:font/woff2;base64,'
                + b64("assets/icons/fonts/tabler-icons.woff2") + ') format("woff2")}'
                + re.search(r"\.ti\{[^}]*\}", icons).group(0) + regeln)

    kopf = kopf.replace('<link rel="stylesheet" href="assets/icons/tabler-icons.min.css">', f"<style>{icon_css}</style>")
    kopf = kopf.replace('<link rel="stylesheet" href="assets/css/style.css">', f"<style>{css}</style>")
    kopf = kopf.replace('<a class="skip" href="#inhalt">', '<a class="skip" href="#inhalt" onclick="document.getElementById(\'inhalt\').focus();return false">')

    skripte = "".join(f"<script>{(ROOT / 'assets/js' / js).read_text()}</script>" for js in ["gsap.min.js", "ScrollTrigger.min.js"])
    router = """<script>
const TITEL = %s;
function zeige() {
  const [seite, anker] = (location.hash.slice(1) || 'index').split('/');
  const ziel = document.querySelector(`[data-page="${seite}"]`) ? seite : 'index';
  document.querySelectorAll('[data-page]').forEach(p => p.hidden = p.dataset.page !== ziel);
  document.querySelectorAll('.menu a').forEach(a => a.getAttribute('href') === '#' + ziel ? a.setAttribute('aria-current', 'page') : a.removeAttribute('aria-current'));
  document.title = TITEL[ziel];
  const el = anker && document.getElementById(anker);
  el ? el.scrollIntoView() : window.scrollTo(0, 0);
  window.ScrollTrigger && ScrollTrigger.refresh();
}
addEventListener('hashchange', zeige);
document.addEventListener('click', e => { if (e.target.closest('a[href="#"]')) e.preventDefault(); });
zeige();
</script>""" % json.dumps(titel, ensure_ascii=False)

    fuss = fuss.replace('<script src="assets/js/gsap.min.js"></script>\n<script src="assets/js/ScrollTrigger.min.js"></script>\n', skripte)
    fuss = fuss.replace('<script src="assets/js/main.js"></script>', router + f"<script>{(ROOT / 'assets/js/main.js').read_text()}</script>")

    html = links(kopf) + '<main id="inhalt" tabindex="-1">' + "".join(seiten) + "</main>" + links(fuss)
    assert "assets/" not in html, "Verweis auf assets/ übrig"
    (HIER / "dream-demo.html").write_text(html)
    print("dream-demo.html", round(len(html.encode()) / 1024), "KB,", len(benutzt), "Icons")


if __name__ == "__main__":
    main()
