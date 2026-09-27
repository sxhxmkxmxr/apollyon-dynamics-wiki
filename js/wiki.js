/* Apollyon wiki: shell behaviour shared by every page.
   The wiki-map drawer on narrow screens, "On this page" scroll-spy, and
   full-screen figures. The markup comes from scripts/site_shell.py. */
(function () {
  var body = document.body;

  /* ── Wiki map as a drawer below 1020px ───────────────────────────── */
  var btn = document.querySelector('.topbar-menu');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    var scrim = document.createElement('div');
    scrim.className = 'nav-scrim';
    body.appendChild(scrim);
    var behind = function () {
      return document.querySelectorAll('.main, .toc, .site-footer, .skip, .crumbs, .brand');
    };
    var setOpen = function (open, restoreFocus) {
      body.classList.toggle('nav-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      Array.prototype.forEach.call(behind(), function (el) {
        if (open) el.setAttribute('inert', ''); else el.removeAttribute('inert');
      });
      if (open) {
        var first = nav.querySelector('a[aria-current="page"]') || nav.querySelector('a');
        if (first) first.focus();
      } else if (restoreFocus) {
        btn.focus();
      }
    };
    btn.addEventListener('click', function () { setOpen(!body.classList.contains('nav-open'), true); });
    scrim.addEventListener('click', function () { setOpen(false, true); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false, false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('nav-open')) setOpen(false, true);
    });
    // Widening the window past the drawer breakpoint must not leave the page inert.
    var wide = window.matchMedia('(min-width: 1020px)');
    var onWide = function () { if (wide.matches && body.classList.contains('nav-open')) setOpen(false, false); };
    if (wide.addEventListener) wide.addEventListener('change', onWide); else wide.addListener(onWide);
  }

  /* ── Keep the current page in view inside the wiki map ─────────── */
  var here = nav && nav.querySelector('a[aria-current="page"]');
  if (here && nav.scrollHeight > nav.clientHeight) {
    nav.scrollTop = Math.max(0, here.offsetTop - nav.clientHeight / 3);
  }

  /* ── "On this page": close the collapsed box after a jump ──────── */
  var pageToc = document.querySelector('.page-toc');
  if (pageToc) {
    pageToc.addEventListener('click', function (e) { if (e.target.closest('a')) pageToc.open = false; });
  }

  /* ── Scroll-spy for both "On this page" lists ───────────────────── */
  var links = Array.prototype.slice.call(
    document.querySelectorAll('.toc a[href^="#"]:not(.toc-top), .page-toc a[href^="#"]'));
  var targets = [];
  links.forEach(function (a) {
    var el = document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));
    if (el && targets.indexOf(el) < 0) targets.push(el);
  });
  var current = null;
  function mark(id) {
    if (id === current) return;
    current = id;
    links.forEach(function (a) {
      var on = a.getAttribute('href') === '#' + id;
      a.classList.toggle('on', on);
      if (on) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
    });
  }
  var ticking = false;
  function update() {
    ticking = false;
    if (!targets.length) return;
    var y = window.scrollY || window.pageYOffset;
    var max = document.documentElement.scrollHeight - window.innerHeight;
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
  if (!plates.length) return;
  var box = document.createElement('div');
  box.className = 'zoom';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.setAttribute('aria-label', 'Expanded figure');
  box.innerHTML = '<button class="zoom-close" type="button">Close</button><div class="zoom-stage"></div><div class="zoom-cap"></div>';
  body.appendChild(box);
  var stage = box.querySelector('.zoom-stage'), cap = box.querySelector('.zoom-cap');
  var closeBtn = box.querySelector('.zoom-close');
  var lastFocus = null;

  // The figure itself: the first visible svg or image that is not part of the
  // plate's header (some headers carry a small icon), so on a phone the
  // compact chart is expanded, not the hidden wide one.
  function mediaOf(plate) {
    var all = plate.querySelectorAll('svg, img');
    for (var i = 0; i < all.length; i++) {
      var m = all[i];
      if (m.closest('.blueprint-head, .fig-data')) continue;
      if (m.parentElement && m.parentElement.closest('svg')) continue;  // an svg nested in another
      if (m.getClientRects().length) return m;
    }
    return null;
  }
  function close() {
    box.classList.remove('open'); body.classList.remove('zoom-open');
    stage.innerHTML = ''; cap.innerHTML = '';
    if (lastFocus) lastFocus.focus();
  }
  function open(plate, trigger) {
    var media = mediaOf(plate);
    if (!media) return;
    var clone = media.cloneNode(true);
    clone.removeAttribute('width'); clone.removeAttribute('height'); clone.removeAttribute('loading');
    stage.appendChild(clone);
    var c = plate.querySelector('figcaption, .blueprint-cap') || plate.querySelector('.blueprint-head .title');
    if (c) cap.innerHTML = c.innerHTML;
    lastFocus = trigger;
    box.classList.add('open'); body.classList.add('zoom-open');
    closeBtn.focus();
  }
  Array.prototype.forEach.call(plates, function (plate) {
    if (plate.hasAttribute('data-nozoom') || !plate.querySelector('svg, img')) return;
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'zoom-btn'; b.textContent = 'Expand';
    b.setAttribute('aria-label', 'Expand figure');
    b.addEventListener('click', function (e) { e.stopPropagation(); open(plate, b); });
    var head = plate.querySelector('.blueprint-head');
    if (head) { head.appendChild(b); } else { plate.classList.add('zoomable'); plate.appendChild(b); }
  });
  box.addEventListener('click', function (e) { if (!e.target.closest('a')) close(); });
  document.addEventListener('keydown', function (e) {
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'Tab') { e.preventDefault(); closeBtn.focus(); }  // the dialog's only control
  });
})();
