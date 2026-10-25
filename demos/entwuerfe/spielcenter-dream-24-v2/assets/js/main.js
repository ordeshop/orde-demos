// Dream Spielcenter, Entwurf Fassung 2 (Nachtfassung). Ohne Bibliotheken.

// Menü am Handy
const burger = document.querySelector('.burger');
const menu = document.getElementById('menu');
if (burger && menu) {
  burger.addEventListener('click', () => {
    const auf = burger.getAttribute('aria-expanded') !== 'true';
    burger.setAttribute('aria-expanded', String(auf));
    menu.classList.toggle('offen', auf);
    document.querySelector('[data-kopf]')?.classList.toggle('menue-offen', auf);
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') { burger.click(); burger.focus(); }
  });
}

// Kopf: wird beim Scrollen mattes Glas. Auf der Startseite erscheint das Logo darin
// erst, wenn der Automat aus dem Bild ist (dort steht das Schild schon fünfmal).
const kopf = document.querySelector('[data-kopf]');
const automat = document.querySelector('[data-automat]');
if (kopf) {
  const fest = () => kopf.classList.toggle('fest', window.scrollY > 8);
  fest();
  addEventListener('scroll', fest, { passive: true });
  if (automat && 'IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => kopf.classList.toggle('logo-aus', e.isIntersecting), { rootMargin: '-84px 0px 0px 0px' }).observe(automat);
  }
}

// Intro der Startseite: Das Kopfskript hat .intro gesetzt (einmal je Besuch, nicht bei
// „Bewegung reduzieren“). Die Walzen drehen und bleiben von links nach rechts auf dem
// Dream-Schild stehen, beim Treffer laufen die Lampen, dann gleitet der Automat an seinen
// Platz. Tippen, eine Taste oder Scrollen beendet es sofort.
const wurzel = document.documentElement;
if (wurzel.classList.contains('intro')) {
  clearTimeout(window.dreamNotaus);
  try { sessionStorage.setItem('dream-intro', '1'); } catch (e) { /* ohne Speicher kommt das Intro eben jedes Mal */ }
  // Kein Intro, wenn die Seite im Hintergrund lädt, schon gescrollt ist oder zu lange gebraucht hat
  if (!automat || document.hidden || window.scrollY > 0 || performance.now() > 2500) wurzel.classList.remove('intro');
  else intro();
}

function intro() {
  const r = automat.getBoundingClientRect();
  automat.style.setProperty('--intro-y', Math.round(innerHeight / 2 - (r.top + r.height / 2)) + 'px');
  automat.style.setProperty('--intro-s', Math.min(1.15, innerWidth * .94 / r.width).toFixed(3));
  requestAnimationFrame(() => wurzel.classList.toggle('intro-an', wurzel.classList.contains('intro')));

  // Jede Walze läuft nach unten und bleibt mit einem kleinen Ruck auf der Zielzelle stehen
  const laeufe = [...automat.querySelectorAll('[data-streifen]')].map((streifen, j) => {
    const n = +streifen.dataset.n;
    const ziel = +streifen.dataset.ziel;
    const lage = k => `translateY(${(-(k - .8) / n * 100).toFixed(3)}%)`; // wie in build.py: oben 0,8 Zellen angeschnitten
    return streifen.animate([
      { transform: lage(ziel + 14 + 4 * j), filter: 'blur(3px)' },
      { transform: lage(ziel - .12), filter: 'blur(0px)', offset: .92, easing: 'cubic-bezier(.3, .7, .4, 1)' },
      { transform: lage(ziel), filter: 'blur(0px)' },
    ], { duration: 1000 + 280 * j, delay: 350, fill: 'both' });
  });
  const stopp = 350 + 1000 + 280 * (laeufe.length - 1);
  const uhren = [
    setTimeout(() => wurzel.classList.add('intro-gewinn'), stopp),
    setTimeout(ende, stopp + 1150),
  ];
  const abbruch = ['pointerdown', 'keydown', 'wheel', 'touchstart'];
  abbruch.forEach(t => addEventListener(t, ende, { passive: true }));

  function ende() {
    if (!wurzel.classList.contains('intro')) return;
    uhren.forEach(clearTimeout);
    abbruch.forEach(t => removeEventListener(t, ende));
    laeufe.forEach(a => a.finish());
    wurzel.classList.remove('intro', 'intro-an');
    wurzel.classList.add('intro-aus');
    setTimeout(() => wurzel.classList.remove('intro-aus', 'intro-gewinn'), 1900);
  }
}

// Uhrzeit in Deutschland, egal in welcher Zeitzone das Gerät steht. tag: 0 = Montag
function jetzt() {
  const t = Object.fromEntries(new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Europe/Berlin', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
  }).formatToParts(new Date()).map(p => [p.type, p.value]));
  return {
    tag: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].indexOf(t.weekday),
    h: +t.hour + t.minute / 60,
    uhr: t.hour + ':' + t.minute,
  };
}

// data-open: Öffnungsstunde Mo..So, data-close: Schluss am Folgetag (0 = Mitternacht)
function lage(el, z) {
  const auf = el.dataset.open.split(',').map(Number);
  const zu = +el.dataset.close;
  const nachMitternacht = zu > 0 && z.h < zu;
  return {
    offen: nachMitternacht || z.h >= auf[z.tag],
    bis: zu === 0 ? 'Mitternacht' : zu + ' Uhr',
    ab: auf[z.tag] + ' Uhr',
    tag: nachMitternacht ? (z.tag + 6) % 7 : z.tag, // Geschäftstag
  };
}

// Zeitstrahl: ein Tag läuft von 6 Uhr morgens bis 6 Uhr am nächsten Morgen
const TAG_BEGINN = 6;
const stelle = h => ((h - TAG_BEGINN + 24) % 24) / 24 * 100;

function aktualisieren() {
  const z = jetzt();
  const bandTag = z.h < TAG_BEGINN ? (z.tag + 6) % 7 : z.tag; // der Tag, in dem „jetzt“ auf dem Strahl liegt
  document.querySelectorAll('[data-open]').forEach(el => {
    const l = lage(el, z);
    el.dataset.state = l.offen ? 'offen' : 'zu';
    el.querySelectorAll('[data-status]').forEach(s => {
      s.textContent = l.offen ? 'Jetzt geöffnet · bis ' + l.bis : 'Geschlossen · öffnet um ' + l.ab;
    });
    const auf = el.dataset.open.split(',').map(Number)[bandTag];
    const zu = +el.dataset.close;
    const ende = zu === 0 ? 24 : 24 + zu;
    el.querySelectorAll('.zeitband').forEach(band => {
      const balken = band.querySelector('[data-balken]');
      balken.style.left = (auf - TAG_BEGINN) / 24 * 100 + '%';
      balken.style.width = (ende - auf) / 24 * 100 + '%';
      band.querySelector('[data-jetzt]').style.left = stelle(z.h) + '%';
      band.classList.add('lebt');
    });
    const heute = String((l.tag + 1) % 7); // JS-Wochentag, So = 0
    el.querySelectorAll('tr[data-d]').forEach(tr => tr.classList.toggle('heute', tr.dataset.d.split(' ').includes(heute)));
  });
  concierge(z);
  document.querySelectorAll('[data-plan-jetzt]').forEach(strich => {
    strich.style.setProperty('--x', stelle(z.h) + '%');
    strich.querySelector('[data-uhrzeit]').textContent = z.uhr;
    strich.classList.add('lebt');
  });
}

// Live-Zeile auf der Bühne: welche Häuser gerade geöffnet sind
const ZAHLWORTE = { 2: 'zwei', 3: 'drei', 4: 'vier', 5: 'fünf', 6: 'sechs', 7: 'sieben', 8: 'acht' };
const aufzaehlen = namen => namen.length < 2 ? namen.join('') : namen.slice(0, -1).join(', ') + ' und ' + namen[namen.length - 1];
function concierge(z) {
  const text = document.querySelector('[data-concierge]');
  if (!text) return;
  const haeuser = [...document.querySelectorAll('.zeile[data-name]')];
  const offen = haeuser.filter(h => h.dataset.state === 'offen').map(h => h.dataset.name);
  document.querySelector('[data-concierge-lampe]')?.classList.toggle('an', offen.length > 0);
  if (offen.length === haeuser.length) {
    text.textContent = 'Jetzt sind alle ' + (ZAHLWORTE[haeuser.length] || haeuser.length) + ' Häuser geöffnet.';
  } else if (offen.length) {
    text.textContent = 'Jetzt geöffnet in ' + aufzaehlen(offen) + '.';
  } else {
    const naechstes = haeuser
      .map(h => ({ name: h.dataset.name, ab: h.dataset.open.split(',').map(Number)[z.tag] }))
      .sort((a, b) => a.ab - b.ab)[0];
    text.textContent = 'Gerade sind alle Häuser geschlossen. ' + naechstes.name + ' öffnet um ' + naechstes.ab + ' Uhr.';
  }
}

aktualisieren();
setInterval(aktualisieren, 30000);

// Formulare sind im Entwurf Attrappen: prüfen, aber nichts verschicken
document.querySelectorAll('form[data-demo]').forEach(form => {
  const meldung = form.querySelector('.formular-meldung');
  form.addEventListener('submit', e => {
    e.preventDefault();
    const falsch = [...form.querySelectorAll('[required]')].filter(f => !f.checkValidity());
    form.querySelectorAll('[required]').forEach(f => f.setAttribute('aria-invalid', String(falsch.includes(f))));
    if (falsch.length) {
      meldung.className = 'formular-meldung voll fehler';
      meldung.textContent = falsch.length === 1
        ? 'Ein Feld fehlt noch oder stimmt nicht. Es ist markiert.'
        : falsch.length + ' Felder fehlen noch oder stimmen nicht. Sie sind markiert.';
      falsch[0].focus();
      return;
    }
    meldung.className = 'formular-meldung voll ok';
    meldung.textContent = 'Danke. Im fertigen Projekt geht die Nachricht jetzt an das Dream. Im Entwurf wird nichts verschickt.';
    form.reset();
  });
  form.addEventListener('input', e => {
    if (e.target.getAttribute('aria-invalid') === 'true' && e.target.checkValidity()) e.target.setAttribute('aria-invalid', 'false');
  });
});

document.querySelectorAll('.jahr').forEach(j => { j.textContent = new Date().getFullYear(); });
