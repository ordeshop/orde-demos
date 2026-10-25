// Dream Spielcenter, Entwurf Fassung 2 (Nachtfassung). Ohne Bibliotheken.

// Menü am Handy
const burger = document.querySelector('.burger');
const menu = document.getElementById('menu');
if (burger && menu) {
  burger.addEventListener('click', () => {
    const auf = burger.getAttribute('aria-expanded') !== 'true';
    burger.setAttribute('aria-expanded', String(auf));
    menu.classList.toggle('offen', auf);
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') { burger.click(); burger.focus(); }
  });
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
  const tag = nachMitternacht ? (z.tag + 6) % 7 : z.tag; // Geschäftstag
  return {
    offen: nachMitternacht || z.h >= auf[z.tag],
    auf: auf[tag],
    zu,
    bis: zu === 0 ? 'Mitternacht' : zu + ' Uhr',
    ab: auf[z.tag] + ' Uhr',
    tag,
  };
}

// Zifferblatt: 24 Stunden, Mitternacht oben, im Uhrzeigersinn
function punkt(h, r) {
  const w = h / 24 * 2 * Math.PI;
  return [100 + r * Math.sin(w), 100 - r * Math.cos(w)];
}
function bogen(auf, zu, r = 84) {
  const ende = zu === 0 ? 24 : 24 + zu;
  const [x1, y1] = punkt(auf, r);
  const [x2, y2] = punkt(ende, r);
  return `M${x1.toFixed(2)} ${y1.toFixed(2)}A${r} ${r} 0 ${ende - auf > 12 ? 1 : 0} 1 ${x2.toFixed(2)} ${y2.toFixed(2)}`;
}

function aktualisieren() {
  const z = jetzt();
  document.querySelectorAll('[data-open]').forEach(el => {
    const l = lage(el, z);
    el.dataset.state = l.offen ? 'offen' : 'zu';
    el.querySelectorAll('[data-status]').forEach(s => {
      s.textContent = l.offen ? 'Jetzt geöffnet · bis ' + l.bis : 'Geschlossen · öffnet um ' + l.ab;
    });
    if (el.classList.contains('ring')) el.querySelector('[data-bogen]').setAttribute('d', bogen(l.auf, l.zu, +el.dataset.r));
    el.querySelectorAll('.blatt').forEach(blatt => {
      blatt.querySelector('[data-bogen]').setAttribute('d', bogen(l.auf, l.zu));
      const [x, y] = punkt(z.h, 84);
      const marke = blatt.querySelector('[data-jetzt]');
      marke.setAttribute('cx', x.toFixed(2));
      marke.setAttribute('cy', y.toFixed(2));
      const zeit = blatt.querySelector('[data-uhrzeit]');
      if (zeit) zeit.textContent = z.uhr;
      const text = blatt.querySelector('[data-blatt-text]');
      if (text) text.textContent = l.offen ? 'offen bis ' + (l.zu === 0 ? 24 : l.zu) + ' Uhr' : 'zu · ab ' + l.ab;
      blatt.classList.add('lebt');
    });
    const heute = String((l.tag + 1) % 7); // JS-Wochentag, So = 0
    el.querySelectorAll('tr[data-d]').forEach(tr => tr.classList.toggle('heute', tr.dataset.d.split(' ').includes(heute)));
  });
}

// Große Uhr: Zeiger und Uhrzeit
function uhrStellen() {
  const z = jetzt();
  document.querySelectorAll('.uhr').forEach(uhr => {
    uhr.querySelector('[data-zeiger]').setAttribute('transform', `rotate(${(z.h / 24 * 360).toFixed(2)} 100 100)`);
    uhr.querySelector('[data-uhrzeit]').textContent = z.uhr;
    uhr.classList.add('lebt');
  });
}

function alles() { aktualisieren(); uhrStellen(); }
alles();
setInterval(alles, 30000);

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
