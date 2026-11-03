/* VEIT – Entwurf. Menü, die Presse, Hinweise für Attrappen. */
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

  /* Hinweis bei Attrappen */
  let toastZeit;
  const toast = (text) => {
    let t = document.querySelector('.toast');
    if (!t) { t = document.createElement('p'); t.className = 'toast'; t.setAttribute('role', 'status'); document.body.append(t); }
    t.textContent = text; t.hidden = false;
    clearTimeout(toastZeit); toastZeit = setTimeout(() => { t.hidden = true; }, 4200);
  };
  document.querySelectorAll('[data-attrappe-link]').forEach((a) => a.addEventListener('click', (e) => {
    e.preventDefault(); toast('Im Entwurf noch ohne Ziel. Im fertigen Auftritt führt der Link auf die echte Seite.');
  }));
  document.querySelectorAll('form[data-attrappe]').forEach((f) => f.addEventListener('submit', (e) => {
    e.preventDefault();
    const erg = f.querySelector('.partner-ergebnis, .formular-ergebnis');
    const text = f.classList.contains('partner')
      ? 'Entwurf: Hier erscheinen im fertigen Auftritt Name, Telefon und E-Mail des zuständigen Vertriebspartners aus der VEIT-Datenbank.'
      : 'Entwurf: Das Formular ist noch nicht angeschlossen. Im fertigen Auftritt geht die Anfrage an VEIT.';
    if (erg) { erg.hidden = false; erg.textContent = text; } else { toast(text); }
  }));

  /* Die Presse: Fortschritt 0..1 über den Abschnitt, nur transform/opacity */
  const presse = document.querySelector('.presse');
  if (!presse) return;
  const kopf = presse.querySelector('.pressenkopf');
  const text = presse.querySelector('.presse-text');
  const wolken = [...presse.querySelectorAll('.dampf span')];
  const knitter = presse.querySelector('.stoff-knitter');
  const buehne = presse.querySelector('.presse-buehne');
  const tisch = presse.querySelector('.tisch');
  const clamp = (v) => Math.min(1, Math.max(0, v));
  const ease = (t) => 1 - Math.pow(1 - t, 3);
  let sichtbar = false, laeuft = false;

  const zeichnen = () => {
    laeuft = false;
    const r = presse.getBoundingClientRect();
    const weg = presse.offsetHeight - innerHeight;
    const p = clamp(-r.top / weg);
    // Hub: 0 = oben, 1 = aufgesetzt
    let hub;
    if (p < .4) hub = ease(p / .4);
    else if (p < .55) hub = 1;
    else hub = 1 - ease(clamp((p - .55) / .25));
    // Kopf fährt von oberhalb der Bühne bis auf die Oberkante des Stoffs
    const H = buehne.clientHeight, kh = kopf.offsetHeight, kontakt = H - tisch.offsetHeight + 10 - kh;
    const oben = -kh * 1.05;
    kopf.style.transform = `translateY(${oben + hub * (kontakt - oben)}px)`;
    knitter.style.opacity = String(1 - clamp((p - .4) / .15));
    wolken.forEach((w, i) => {
      const s = clamp((p - .42 - (i % 3) * .02) / .32);
      w.style.opacity = String(s < .35 ? s / .35 : (1 - s) / .65);
      w.style.transform = `translateY(${-s * 34}vh) scale(${.5 + s * .9})`;
    });
    const t = ease(clamp((p - .72) / .14));
    text.style.opacity = String(t);
    text.style.transform = `translateY(${(1 - t) * 24}px)`;
  };
  const anfordern = () => { if (sichtbar && !laeuft) { laeuft = true; requestAnimationFrame(zeichnen); } };

  const einrichten = () => {
    if (ruhig.matches) { presse.classList.add('ruhig'); kopf.style.transform = ''; text.style.cssText = ''; return; }
    presse.classList.remove('ruhig');
    zeichnen();
  };
  new IntersectionObserver((e) => { sichtbar = e[0].isIntersecting; anfordern(); }).observe(presse);
  addEventListener('scroll', () => { if (!ruhig.matches) anfordern(); }, { passive: true });
  addEventListener('resize', () => { if (!ruhig.matches) anfordern(); });
  ruhig.addEventListener('change', einrichten);
  einrichten();
})();
