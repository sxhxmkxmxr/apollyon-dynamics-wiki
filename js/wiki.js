/* Apollyon wiki — shell behaviour shared by every page.
   Mobile menu drawer, "On this page" scroll-spy, reading progress,
   full-screen figures, and the Wiki map (tab + side panel). */
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
  /* ── Wiki map: every group, page and section, from wiki-map-data.js ── */
  var MAP = window.WIKI_MAP;
  var me = document.querySelector('script[src$="js/wiki.js"]');
  var root = me ? me.getAttribute('src').replace(/js\/wiki\.js$/, '') : '';
  function norm(path) { return path.replace(/\/$/, '/index.html'); }
  var herePath = norm(location.pathname);

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function buildMap() {
    var wrap = el('div', 'wmap');
    var search = el('input', 'wmap-filter');
    search.type = 'search';
    search.placeholder = 'Filter pages and sections';
    search.setAttribute('aria-label', 'Filter pages and sections');
    wrap.appendChild(search);

    var pagesTotal = 0, sectionsTotal = 0, rows = [];
    MAP.groups.forEach(function (g, gi) {
      var grp = el('div', 'wmap-group');
      var h = el('div', 'wmap-gh');
      h.appendChild(el('span', 'n', (gi < 9 ? '0' : '') + (gi + 1)));
      h.appendChild(document.createTextNode(g.name));
      grp.appendChild(h);
      var ul = el('ul', 'wmap-pages');
      g.pages.forEach(function (pg) {
        pagesTotal++; sectionsTotal += pg.sections.length;
        var url = root + pg.href;
        var isHere = norm(new URL(url, location.href).pathname) === herePath;
        var li = el('li', 'wmap-page' + (isHere ? ' here' : ''));
        var det = el('details');
        if (isHere) det.open = true;
        var sum = el('summary');
        var a = el('a', null, pg.title);
        a.href = url;
        if (pg.heading) a.title = pg.heading;
        if (isHere) a.setAttribute('aria-current', 'page');
        sum.appendChild(a);
        if (pg.sections.length) sum.appendChild(el('span', 'wmap-count', String(pg.sections.length)));
        det.appendChild(sum);
        var sl = el('ul', 'wmap-sections');
        pg.sections.forEach(function (sec) {
          var si = el('li');
          var sa = el('a', null, sec.label);
          sa.href = isHere ? '#' + sec.id : url + '#' + sec.id;
          si.appendChild(sa);
          sl.appendChild(si);
          rows.push({ li: si, text: sec.label.toLowerCase(), page: li });
        });
        det.appendChild(sl);
        li.appendChild(det);
        ul.appendChild(li);
        li._det = det; li._grp = grp;
        li._text = (pg.title + ' ' + pg.heading).toLowerCase();
        li._secs = rows.slice(rows.length - pg.sections.length);
      });
      grp.appendChild(ul);
      wrap.appendChild(grp);
    });
    var foot = el('p', 'wmap-foot', pagesTotal + ' pages · ' + sectionsTotal + ' sections');
    wrap.appendChild(foot);
    var none = el('p', 'wmap-none', 'Nothing matches.');
    none.hidden = true;
    wrap.appendChild(none);

    search.addEventListener('input', function () {
      var q = search.value.trim().toLowerCase(), any = false;
      Array.prototype.forEach.call(wrap.querySelectorAll('.wmap-page'), function (li) {
        var pageHit = !q || li._text.indexOf(q) >= 0, secHit = false;
        li._secs.forEach(function (r) {
          var hit = !q || pageHit || r.text.indexOf(q) >= 0;
          r.li.hidden = !hit;
          if (q && r.text.indexOf(q) >= 0) secHit = true;
        });
        li.hidden = !(pageHit || secHit);
        if (q) li._det.open = secHit; else li._det.open = li.classList.contains('here');
        if (!li.hidden) any = true;
      });
      Array.prototype.forEach.call(wrap.querySelectorAll('.wmap-group'), function (g) {
        g.hidden = !g.querySelector('.wmap-page:not([hidden])');
      });
      none.hidden = any;
    });
    return wrap;
  }

  if (MAP && MAP.groups) {
    /* Right-hand panel tabs */
    var tabPage = document.getElementById('tab-page'), tabMap = document.getElementById('tab-map');
    var panePage = document.getElementById('toc-page'), paneMap = document.getElementById('toc-map');
    if (tabPage && tabMap && panePage && paneMap) {
      var built = false;
      var show = function (which, remember) {
        var map = which === 'map';
        if (map && !built) { paneMap.appendChild(buildMap()); built = true; }
        tabPage.setAttribute('aria-selected', map ? 'false' : 'true');
        tabMap.setAttribute('aria-selected', map ? 'true' : 'false');
        panePage.hidden = map; paneMap.hidden = !map;
        if (remember) { try { localStorage.setItem('wiki-panel', which); } catch (e) {} }
      };
      tabPage.addEventListener('click', function () { show('page', true); });
      tabMap.addEventListener('click', function () { show('map', true); });
      [tabPage, tabMap].forEach(function (t) {
        t.addEventListener('keydown', function (e) {
          if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
            var other = t === tabPage ? tabMap : tabPage;
            other.click(); other.focus();
          }
        });
      });
      var saved = null;
      try { saved = localStorage.getItem('wiki-panel'); } catch (e) {}
      var hasSections = !!panePage.querySelector('ul');
      show(saved === 'map' || !hasSections ? 'map' : 'page', false);
    }

    /* Narrower screens: the right panel is hidden, so the map opens as a sheet */
    if (nav) {
      var openBtn = el('button', 'map-open', 'Wiki map');
      openBtn.type = 'button';
      nav.appendChild(openBtn);
      var sheet = el('div', 'map-sheet');
      sheet.setAttribute('role', 'dialog');
      sheet.setAttribute('aria-modal', 'true');
      sheet.setAttribute('aria-label', 'Wiki map');
      var head = el('div', 'map-sheet-head');
      head.appendChild(el('span', null, 'Wiki map'));
      var closeBtn = el('button', 'map-sheet-close', 'Close \u00d7');
      closeBtn.type = 'button';
      head.appendChild(closeBtn);
      sheet.appendChild(head);
      var sheetBody = el('div', 'map-sheet-body');
      sheet.appendChild(sheetBody);
      body.appendChild(sheet);
      var sheetBuilt = false;
      var setSheet = function (open) {
        if (open && !sheetBuilt) { sheetBody.appendChild(buildMap()); sheetBuilt = true; }
        sheet.classList.toggle('open', open);
        body.classList.toggle('map-sheet-open', open);
        if (open) { body.classList.remove('nav-open'); closeBtn.focus(); } else openBtn.focus();
      };
      openBtn.addEventListener('click', function (e) { e.stopPropagation(); setSheet(true); });
      closeBtn.addEventListener('click', function () { setSheet(false); });
      sheet.addEventListener('click', function (e) {
        if (e.target === sheet) setSheet(false);
        else if (e.target.closest('a')) sheet.classList.remove('open'), body.classList.remove('map-sheet-open');
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && sheet.classList.contains('open')) setSheet(false);
      });
    }
  }
})();
