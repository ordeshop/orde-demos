/* VEIT-Theme: Menü am Handy und der Bewegungsmoment „Die Presse“. Keine Bibliothek. */
(() => {
  const ruhig = matchMedia('(prefers-reduced-motion: reduce)');

  /* Menü am Handy */
  const knopf = document.querySelector('.menue-knopf');
  const menue = document.getElementById('menue');
  if (knopf && menue) {
    const zu = menue.querySelector('.menue-zu');
    const auf = (offen) => {
      menue.hidden = !offen;
      knopf.setAttribute('aria-expanded', String(offen));
      document.body.style.overflow = offen ? 'hidden' : '';
      (offen ? zu : knopf).focus();
    };
    knopf.addEventListener('click', () => auf(true));
    zu.addEventListener('click', () => auf(false));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !menue.hidden) auf(false); });
  }

  /* Die Presse: Fortschritt 0..1 über die Strecke, in der die Bühne klebt. Nur transform/opacity.
     0–.18 Stoff wird aufgelegt · .18–.46 Kopf fährt herunter · .46–.70 Dampf, Stoff wird glatt · .70–.86 Kopf hoch · danach Glanz */
  const presse = document.querySelector('.presse');
  if (!presse) return;
  const $ = (s) => presse.querySelector(s);
  const kopf = $('.pressenkopf'), maschine = $('.maschine'), tisch = $('.tisch'), knitter = $('.stoff-knitter'),
    glatt = $('.stoff-glatt'), glanz = $('.glanz'), lampe = $('.lampe'), balken = $('.presse-fortschritt span');
  const wolken = [...presse.querySelectorAll('.dampf span')];
  const stangen = [...presse.querySelectorAll('.stange')];
  const schritte = [...presse.querySelectorAll('.presse-schritte li')];
  const clamp = (v) => Math.min(1, Math.max(0, v));
  const ease = (t) => 1 - Math.pow(1 - t, 3);
  const inout = (t) => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const ab = (p, von, bis) => clamp((p - von) / (bis - von));
  let sichtbar = false, laeuft = false;

  const zeichnen = () => {
    laeuft = false;
    const r = presse.getBoundingClientRect();
    const weg = presse.offsetHeight - innerHeight;
    const p = clamp(-r.top / weg);
    // 1. Stoff auflegen: der zerknitterte Stoff gleitet von links auf den Tisch
    const auf = ease(ab(p, 0, .18));
    knitter.style.transform = glatt.style.transform = `translateX(${(1 - auf) * -105}%)`;
    // 2. Kopf: oben in der Maschine → auf den Stoff → wieder hoch
    const hub = p < .46 ? inout(ab(p, .18, .46)) : p < .70 ? 1 : 1 - inout(ab(p, .70, .86));
    const kontakt = maschine.clientHeight - tisch.offsetHeight - knitter.offsetHeight * .35 - kopf.offsetHeight - kopf.offsetTop;
    kopf.style.transform = `translateY(${hub * kontakt}px)`;
    const luecke = kopf.offsetTop - stangen[0].offsetTop;
    stangen.forEach((st) => { st.style.transform = `scaleY(${(luecke + hub * kontakt) / 100})`; });
    lampe.style.opacity = String(.15 + .85 * (p > .44 && p < .72 ? 1 : 0));
    // 3. Dampf beim Aufsetzen, Stoff wird glatt
    knitter.style.opacity = String(1 - ab(p, .48, .66));
    wolken.forEach((w, i) => {
      const s = ab(p, .46 + (i % 3) * .025, .80);
      w.style.opacity = String(s <= 0 ? 0 : s < .3 ? s / .3 : (1 - s) / .7);
      w.style.transform = `translateY(${-s * 30}vh) scale(${.45 + s})`;
    });
    // 4. Glanz zieht über den glatten Stoff
    const g = ab(p, .84, 1);
    glanz.style.opacity = String(g > 0 && g < 1 ? 1 : 0);
    glanz.style.setProperty('--glanz', `${g * 440}%`);
    // Schritte und Balken
    const nr = p < .18 ? 0 : p < .78 ? 1 : 2;
    schritte.forEach((li, i) => li.classList.toggle('an', i === nr));
    balken.style.transform = `scaleX(${p})`;
  };
  const anfordern = () => { if (sichtbar && !laeuft) { laeuft = true; requestAnimationFrame(zeichnen); } };

  const einrichten = () => {
    if (ruhig.matches) {
      presse.classList.add('ruhig');
      [kopf, knitter, glatt, lampe, glanz, balken, ...wolken, ...stangen].forEach((el) => { el.style.cssText = ''; });
      schritte.forEach((li) => li.classList.add('an'));
      return;
    }
    presse.classList.remove('ruhig');
    zeichnen();
  };
  new IntersectionObserver((e) => { sichtbar = e[0].isIntersecting; anfordern(); }).observe(presse);
  addEventListener('scroll', () => { if (!ruhig.matches) anfordern(); }, { passive: true });
  addEventListener('resize', () => { if (!ruhig.matches) anfordern(); });
  ruhig.addEventListener('change', einrichten);
  einrichten();
})();
