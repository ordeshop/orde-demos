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
  document.querySelectorAll('[data-plan-jetzt]').forEach(strich => {
    strich.style.setProperty('--x', stelle(z.h) + '%');
    strich.querySelector('[data-uhrzeit]').textContent = z.uhr;
    strich.classList.add('lebt');
  });
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
