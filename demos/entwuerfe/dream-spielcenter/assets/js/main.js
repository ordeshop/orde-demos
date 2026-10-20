// Menü am Handy
const burger = document.querySelector('.burger'), menu = document.getElementById('menu');
burger.addEventListener('click', () => {
  const open = burger.getAttribute('aria-expanded') !== 'true';
  burger.setAttribute('aria-expanded', open);
  burger.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
  menu.classList.toggle('open', open);
});
menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { if (menu.classList.contains('open')) burger.click(); }));

// Geöffnet/geschlossen live, Zeitzone Berlin.
// data-open: Öffnungsstunde Mo..So, data-close: Schluss am Folgetag (z. B. 3 = 3 Uhr nachts).
const fmt = new Intl.DateTimeFormat('de-DE', { timeZone: 'Europe/Berlin', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' }).formatToParts(new Date());
const day = { So: 0, Mo: 1, Di: 2, Mi: 3, Do: 4, Fr: 5, Sa: 6 }[fmt.find(p => p.type === 'weekday').value.replace('.', '')];
const now = +fmt.find(p => p.type === 'hour').value + fmt.find(p => p.type === 'minute').value / 60;
const idx = d => (d + 6) % 7;

function state(el) {
  const open = el.dataset.open.split(',').map(Number), close = +el.dataset.close;
  return { isOpen: now < close || now >= open[idx(day)], opens: open[idx(day)], close, bizDay: now < close ? (day + 6) % 7 : day };
}

document.querySelectorAll('[data-open]').forEach(el => {
  const s = state(el);
  el.querySelectorAll('.status').forEach(st => {
    st.textContent = s.isOpen ? 'Jetzt geöffnet · bis ' + s.close + ':00 Uhr' : 'Geschlossen · öffnet um ' + s.opens + ':00 Uhr';
    st.classList.toggle('open', s.isOpen);
  });
  el.querySelector(`tr[data-d="${s.bizDay}"]`)?.classList.add('today');
  const big = el.querySelector('.now-big'), sub = el.querySelector('.now-sub');
  if (big) big.innerHTML = s.isOpen ? 'Jetzt <span>geöffnet</span>' : 'Ab <span>' + s.opens + ' Uhr</span>';
  if (sub) sub.textContent = s.isOpen ? 'Heute Nacht bis ' + s.close + ':00 Uhr.' : 'Heute wieder ab ' + s.opens + ':00 Uhr für Sie da.';
});

// Formulare sind im Entwurf nur Attrappen
document.querySelectorAll('form[data-demo]').forEach(f => f.addEventListener('submit', e => {
  e.preventDefault();
  f.querySelector('[role=status]').textContent = 'Demo: Im fertigen Projekt wird die Nachricht jetzt verschickt.';
}));

document.querySelectorAll('.year').forEach(y => y.textContent = new Date().getFullYear());

// Animationen mit GSAP – nur wenn Bewegung erlaubt ist
if (window.gsap && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  gsap.registerPlugin(ScrollTrigger);
  gsap.from('.h-a', { y: 40, opacity: 0, duration: 1, ease: 'power3.out', stagger: .12 });
  gsap.from('.hero-logo', { scale: .85, rotate: -4, duration: 1.4, ease: 'elastic.out(1,.6)' });
  gsap.utils.toArray('.rv').forEach(el => gsap.from(el, { y: 50, opacity: 0, duration: .9, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%' } }));
  gsap.to('.top', { '--p': 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: true } });
}
