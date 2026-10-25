// Dream Spielcenter, Entwurf Fassung 2. Ohne Bibliotheken.

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
    timeZone: 'Europe/Berlin', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23',
  }).formatToParts(new Date()).map(p => [p.type, p.value]));
  return { tag: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].indexOf(t.weekday), h: +t.hour + t.minute / 60 };
}

// data-open: Öffnungsstunde Mo..So, data-close: Schluss am Folgetag (0 = Mitternacht)
function lage(el, z) {
  const auf = el.dataset.open.split(',').map(Number);
  const zu = +el.dataset.close;
  const nachMitternacht = zu > 0 && z.h < zu;
  const offen = nachMitternacht || z.h >= auf[z.tag];
  return {
    offen,
    bis: zu === 0 ? 'Mitternacht' : zu + ' Uhr',
    ab: auf[z.tag] + ' Uhr',
    geschaeftstag: nachMitternacht ? (z.tag + 6) % 7 : z.tag,
  };
}

const ruhig = matchMedia('(prefers-reduced-motion: reduce)');

function zuenden(haus) {
  if (ruhig.matches || haus.dataset.state !== 'offen' || !haus.offsetParent) return;
  haus.classList.remove('zuendet');
  void haus.offsetWidth; // Animation neu starten
  haus.classList.add('zuendet');
}

function aktualisieren(erstesMal) {
  const z = jetzt();
  document.querySelectorAll('[data-open]').forEach(el => {
    const l = lage(el, z);
    const vorher = el.dataset.state;
    el.dataset.state = l.offen ? 'offen' : 'zu';
    const istTuer = el.classList.contains('haus');
    el.querySelectorAll('[data-status]').forEach(s => {
      s.textContent = istTuer
        ? (l.offen ? 'Geöffnet bis ' + l.bis : 'Geschlossen · ab ' + l.ab)
        : (l.offen ? 'Jetzt offen · bis ' + l.bis : 'Geschlossen · öffnet um ' + l.ab);
    });
    const heute = String((l.geschaeftstag + 1) % 7); // JS-Wochentag, So = 0
    el.querySelectorAll('tr[data-d]').forEach(tr => tr.classList.toggle('heute', tr.dataset.d.split(' ').includes(heute)));
    if (istTuer && (erstesMal || vorher !== el.dataset.state)) zuenden(el);
  });
}

// Hausauswahl: merken und beim Wechsel die Röhre zünden
const SCHLUESSEL = 'dream-haus';
let gemerkt = null;
try { gemerkt = localStorage.getItem(SCHLUESSEL); } catch (e) { /* ohne Speicher geht es auch */ }
document.querySelectorAll('[data-merken]').forEach(fenster => {
  const wahl = gemerkt && fenster.querySelector(`input[value="${gemerkt}"]`);
  if (wahl) wahl.checked = true;
  fenster.addEventListener('change', e => {
    if (e.target.type !== 'radio') return;
    try { localStorage.setItem(SCHLUESSEL, e.target.value); } catch (err) { /* egal */ }
    zuenden(fenster.querySelector(`.haus[data-ort="${e.target.value}"]`));
  });
});

aktualisieren(true);
setInterval(() => aktualisieren(false), 60000);

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
        ? 'Ein Feld fehlt noch oder stimmt nicht. Es ist rot markiert.'
        : falsch.length + ' Felder fehlen noch oder stimmen nicht. Sie sind rot markiert.';
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
