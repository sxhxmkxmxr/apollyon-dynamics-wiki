/* Apollyon wiki — shell behaviour shared by every page.
   Mobile menu drawer, "On this page" scroll-spy, reading progress. */
(function () {
  var body = document.body;

  /* ── Mobile menu ─────────────────────────────────────────────────── */
  var btn = document.querySelector('.rail-menu');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    var scrim = document.createElement('div');
    scrim.className = 'nav-scrim';
    body.appendChild(scrim);
    var setOpen = function (open) {
      body.classList.toggle('nav-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    btn.addEventListener('click', function () { setOpen(!body.classList.contains('nav-open')); });
    scrim.addEventListener('click', function () { setOpen(false); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  }

  /* ── Keep the current page in view inside the sidebar ────────────── */
  var here = nav && nav.querySelector('li.here');
  if (here && nav.scrollHeight > nav.clientHeight) {
    nav.scrollTop = Math.max(0, here.offsetTop - nav.clientHeight / 3);
  }

  /* ── Scroll-spy for both tables of contents ──────────────────────── */
  var links = Array.prototype.slice.call(
    document.querySelectorAll('.toc a[href^="#"]:not(.toc-top), .nav-toc a[href^="#"]'));
  var targets = [];
  links.forEach(function (a) {
    var el = document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));
    if (el && targets.indexOf(el) < 0) targets.push(el);
  });
  var current = null;
  function mark(id) {
    if (id === current) return;
    current = id;
    links.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + id); });
  }

  /* ── Reading progress (thin rule under the rail) ─────────────────── */
  var bar = document.querySelector('.rail-progress i');

  var ticking = false;
  function update() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
    if (!targets.length) return;
    var line = 120, id = targets[0].id;
    for (var i = 0; i < targets.length; i++) {
      if (targets[i].getBoundingClientRect().top - line <= 0) id = targets[i].id; else break;
    }
    if (max - y < 4) id = targets[targets.length - 1].id;
    mark(id);
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }, { passive: true });
  window.addEventListener('resize', update);
  update();
  /* ── Figures open full-screen (diagram labels are small in-column) ── */
  var plates = document.querySelectorAll('.main .blueprint-plate, .main figure, .main .hero-plate');
  if (plates.length) {
    var box = document.createElement('div');
    box.className = 'zoom';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Expanded figure');
    box.innerHTML = '<button class="zoom-close" type="button">Close &times;</button><div class="zoom-stage"></div><div class="zoom-cap"></div>';
    body.appendChild(box);
    var stage = box.querySelector('.zoom-stage'), cap = box.querySelector('.zoom-cap');
    var lastFocus = null;
    var close = function () {
      box.classList.remove('open'); body.classList.remove('zoom-open');
      stage.innerHTML = ''; cap.innerHTML = '';
      if (lastFocus) lastFocus.focus();
    };
    var open = function (plate, trigger) {
      var media = plate.querySelector('.blueprint-body svg, .blueprint-body img, :scope > img, :scope > svg, img, svg');
      if (!media) return;
      var clone = media.cloneNode(true);
      clone.removeAttribute('width'); clone.removeAttribute('height'); clone.removeAttribute('loading');
      stage.appendChild(clone);
      var c = plate.querySelector('figcaption, .blueprint-cap, .blueprint-head .title');
      if (c) cap.innerHTML = c.innerHTML;
      lastFocus = trigger;
      box.classList.add('open'); body.classList.add('zoom-open');
      box.querySelector('.zoom-close').focus();
    };
    Array.prototype.forEach.call(plates, function (plate) {
      var media = plate.querySelector('svg, img');
      if (!media || plate.closest('.aside, .toc')) return;
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'zoom-btn'; b.textContent = 'Expand';
      b.setAttribute('aria-label', 'Expand figure');
      b.addEventListener('click', function (e) { e.stopPropagation(); open(plate, b); });
      var host = plate.querySelector('.blueprint-body') || plate;
      host.classList.add('zoomable');
      host.appendChild(b);
    });
    box.addEventListener('click', function (e) { if (!e.target.closest('a')) close(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && box.classList.contains('open')) close();
    });
  }
})();
