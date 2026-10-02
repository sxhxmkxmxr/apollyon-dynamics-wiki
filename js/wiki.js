/* Apollyon Wiki — Vector 2022 behaviour, shared by every page.

   Dropdowns and pinnable menus (main menu, contents, tools, appearance),
   Appearance preferences stored the way MediaWiki stores clientprefs,
   contents scroll-spy, sticky header, typeahead search, page previews,
   media viewer, section [edit] links, navbox collapse, the ?action= views
   (view source, history, information, cite, what links here, talk) and the
   special pages (search, contents, recent changes, random).

   Data comes from js/wiki-map-data.js (always loaded) and, on demand,
   js/wiki-search-data.js and js/wiki-history-data.js. Everything works from
   file:// as well as over HTTP. */
(function () {
  'use strict';

  var doc = document, html = doc.documentElement, body = doc.body;
  var MAP = window.WIKI_MAP || { site: 'Apollyon Wiki', groups: [] };
  var SITE = MAP.site || 'Apollyon Wiki';
  var me = doc.querySelector('script[src$="js/wiki.js"]');
  var ROOT = me ? me.getAttribute('src').replace(/js\/wiki\.js$/, '') : '';
  var PAGE = body.getAttribute('data-page') || '';
  var SPECIAL = PAGE.indexOf('special/') === 0;
  var PARAMS = new URLSearchParams(location.search);
  var ACTION = PARAMS.get('action') || 'view';
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'];

  var PAGES = [];
  MAP.groups.forEach(function (g) {
    g.pages.forEach(function (p) { p.group = g.name; p.groupSlug = g.slug; p.index = PAGES.length; PAGES.push(p); });
  });
  var CURRENT = null;
  PAGES.forEach(function (p) { if (p.href === PAGE) CURRENT = p; });

  /* ── small helpers ─────────────────────────────────────────────────── */
  function $(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function el(tag, cls, htmlText) {
    var n = doc.createElement(tag);
    if (cls) n.className = cls;
    if (htmlText != null) n.innerHTML = htmlText;
    return n;
  }
  function icon(name) { return '<span class="vector-icon mw-ui-icon-' + name + '"></span>'; }
  function href(p) { return ROOT + p; }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function fmtTime(d) { return pad(d.getUTCHours()) + ':' + pad(d.getUTCMinutes()); }
  function fmtDay(d) { return d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()] + ' ' + d.getUTCFullYear(); }
  function fmtStamp(d) { return fmtTime(d) + ', ' + fmtDay(d); }
  function num(n) { return Number(n).toLocaleString('en-US'); }
  function pageUrl(p) { return new URL(href(p.href), location.href).href.split('#')[0]; }
  function selfUrl() { return location.href.split('#')[0].split('?')[0]; }
  function titleOf(p) { return p ? p.title : ''; }
  var scripts = {};
  function loadScript(src, done) {
    if (scripts[src] === true) { done(); return; }
    if (scripts[src]) { scripts[src].push(done); return; }
    scripts[src] = [done];
    var s = doc.createElement('script');
    s.src = href(src);
    s.onload = s.onerror = function () {
      var q = scripts[src]; scripts[src] = true;
      q.forEach(function (f) { f(); });
    };
    doc.head.appendChild(s);
  }

  /* ── client preferences (MediaWiki's clientprefs) ──────────────────── */
  var PREF_KEY = 'mwclientpreferences';
  function getPref(feature) {
    var m = html.className.match(new RegExp('(?:^|\\s)' + feature + '-clientpref-(\\w+)(?=\\s|$)'));
    return m ? m[1] : null;
  }
  function setPref(feature, value) {
    var re = new RegExp('(^|\\s)' + feature + '-clientpref-\\w+(?=\\s|$)');
    var cls = feature + '-clientpref-' + value;
    html.className = re.test(html.className) ? html.className.replace(re, '$1' + cls) : html.className + ' ' + cls;
    var stored = {};
    try {
      (localStorage.getItem(PREF_KEY) || '').split(',').forEach(function (v) {
        if (v) stored[v.replace(/-clientpref-\w+$/, '')] = v;
      });
      stored[feature] = cls;
      localStorage.setItem(PREF_KEY, Object.keys(stored).map(function (k) { return stored[k]; }).join(','));
    } catch (e) { /* private mode: the choice lasts for this page only */ }
    prefListeners.forEach(function (f) { f(feature, value); });
  }
  var prefListeners = [];

  /* ── notifications ─────────────────────────────────────────────────── */
  function notify(text) {
    var area = $('.mw-notification-area');
    if (!area) { area = el('div', 'mw-notification-area'); area.setAttribute('aria-live', 'polite'); body.appendChild(area); }
    var n = el('div', 'mw-notification', esc(text));
    area.appendChild(n);
    var gone = function () { if (n.parentNode) n.parentNode.removeChild(n); };
    n.addEventListener('click', gone);
    setTimeout(gone, 5000);
  }
  function copy(text, message) {
    var done = function () { notify(message); };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text); done(); });
    } else { fallbackCopy(text); done(); }
  }
  function fallbackCopy(text) {
    var t = el('textarea'); t.value = text; t.style.position = 'fixed'; t.style.opacity = '0';
    body.appendChild(t); t.select();
    try { doc.execCommand('copy'); } catch (e) { /* nothing more to try */ }
    body.removeChild(t);
  }

  /* ── dropdowns (checkbox hack + outside click + Escape) ────────────── */
  var dropdowns = $$('.vector-dropdown');
  function syncDropdown(d) {
    var cb = $('.vector-dropdown-checkbox', d);
    if (cb) cb.setAttribute('aria-expanded', cb.checked ? 'true' : 'false');
  }
  function closeDropdowns(except) {
    dropdowns.forEach(function (d) {
      var cb = $('.vector-dropdown-checkbox', d);
      if (d !== except && cb && cb.checked) {
        cb.checked = false; syncDropdown(d);
        cb.dispatchEvent(new Event('change'));
      }
    });
  }
  dropdowns.forEach(function (d) {
    var cb = $('.vector-dropdown-checkbox', d);
    if (!cb) return;
    syncDropdown(d);
    cb.addEventListener('change', function () {
      if (cb.checked) closeDropdowns(d);
      syncDropdown(d);
    });
  });
  doc.addEventListener('click', function (e) {
    var open = e.target.closest && e.target.closest('.vector-dropdown');
    closeDropdowns(open);
    if (open && e.target.closest('.vector-dropdown-content a[href^="#"]')) closeDropdowns(null);
  });
  doc.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = dropdowns.filter(function (d) { var cb = $('.vector-dropdown-checkbox', d); return cb && cb.checked; })[0];
    if (open) { closeDropdowns(null); $('.vector-dropdown-checkbox', open).focus(); }
  });

  /* ── pinnable menus ────────────────────────────────────────────────── */
  var desktop = window.matchMedia('(min-width: 1120px)');
  var PINNABLES = [
    { name: 'main-menu', el: '#vector-main-menu', pinned: '#vector-main-menu-pinned-container', unpinned: '#vector-main-menu-unpinned-container' },
    { name: 'toc', el: '#vector-toc', pinned: '#vector-toc-pinned-container', unpinned: '#vector-page-titlebar-toc-unpinned-container' },
    { name: 'page-tools', el: '#vector-page-tools', pinned: '#vector-page-tools-pinned-container', unpinned: '#vector-page-tools-unpinned-container' },
    { name: 'appearance', el: '#vector-appearance', pinned: '#vector-appearance-pinned-container', unpinned: '#vector-appearance-unpinned-container' }
  ];
  function isPinned(p) { return getPref('vector-feature-' + p.name + '-pinned') === '1' && desktop.matches; }
  function place(p) {
    var node = $(p.el);
    if (!node) return;
    var pinned = isPinned(p);
    var target = $(pinned ? p.pinned : p.unpinned);
    if (target && node.parentNode !== target) target.appendChild(node);
    var hdr = $('.vector-pinnable-header', node);
    if (hdr) hdr.classList.toggle('vector-pinnable-header-pinned', pinned);
  }
  function placeAll() { PINNABLES.forEach(place); }
  PINNABLES.forEach(function (p) {
    var node = $(p.el);
    if (!node) return;
    var pin = $('.vector-pinnable-header-pin-button', node);
    var unpin = $('.vector-pinnable-header-unpin-button', node);
    if (pin) pin.addEventListener('click', function (e) {
      e.stopPropagation();
      setPref('vector-feature-' + p.name + '-pinned', '1');
      closeDropdowns(null); place(p);
    });
    if (unpin) unpin.addEventListener('click', function (e) {
      e.stopPropagation();
      setPref('vector-feature-' + p.name + '-pinned', '0');
      place(p);
    });
  });
  placeAll();
  if (desktop.addEventListener) desktop.addEventListener('change', placeAll);
  // The contents opened from the sticky header travel with it.
  ['#vector-page-titlebar-toc', '#vector-sticky-header-toc'].forEach(function (sel) {
    var d = $(sel);
    var cb = d && $('.vector-dropdown-checkbox', d);
    if (!cb) return;
    cb.addEventListener('change', function () {
      var toc = $('#vector-toc');
      if (!toc) return;
      if (cb.checked) $('.vector-unpinned-container', d).appendChild(toc);
      else place(PINNABLES[1]);
    });
  });

  /* ── appearance ────────────────────────────────────────────────────── */
  $$('[data-clientpref]').forEach(function (group) {
    var feature = group.getAttribute('data-clientpref');
    $$('input', group).forEach(function (inp) {
      inp.checked = getPref(feature) === inp.value;
      inp.addEventListener('change', function () { if (inp.checked) setPref(feature, inp.value); });
    });
  });
  // Wikipedia's floating "toggle limited content width" button on very wide screens
  var wide = window.matchMedia('(min-width: 1600px)');
  var widthBtn = el('button', 'cdx-button cdx-button--icon-only vector-limited-width-toggle', icon('fullScreen') + '<span>Toggle limited content width</span>');
  widthBtn.type = 'button';
  widthBtn.title = 'Toggle limited content width';
  widthBtn.addEventListener('click', function () {
    var v = getPref('vector-feature-limited-width') === '1' ? '0' : '1';
    setPref('vector-feature-limited-width', v);
    $$('[data-clientpref="vector-feature-limited-width"] input').forEach(function (i) { i.checked = i.value === v; });
    notify(v === '1' ? 'Content width restored.' : 'Content is now as wide as your browser window.');
  });
  body.appendChild(widthBtn);
  function syncWide() { widthBtn.hidden = !wide.matches; }
  syncWide();
  if (wide.addEventListener) wide.addEventListener('change', syncWide);

  /* ── sticky header ─────────────────────────────────────────────────── */
  var sticky = $('.vector-sticky-header-container');
  var heading = $('#firstHeading');
  var stickyAllowed = window.matchMedia('(min-width: 720px)');
  function setSticky(on) {
    on = on && stickyAllowed.matches;
    if (!sticky) return;
    sticky.classList.toggle('vector-sticky-header-visible', on);
    html.style.setProperty('--sticky-offset', on ? '3.125rem' : '0px');
    if (!on) {
      sticky.classList.remove('vector-sticky-header-search-active');
      var cb = $('#vector-sticky-header-toc-checkbox');
      if (cb && cb.checked) { cb.checked = false; cb.dispatchEvent(new Event('change')); }
    }
  }
  if (sticky && heading && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      var e = entries[0];
      setSticky(!e.isIntersecting && e.boundingClientRect.top < 0);
    }).observe(heading);
  }
  var stickySearchToggle = $('.vector-sticky-header-search-toggle');
  if (stickySearchToggle) {
    stickySearchToggle.addEventListener('click', function () {
      sticky.classList.add('vector-sticky-header-search-active');
      var inp = $('.vector-sticky-header-search input', sticky);
      if (inp) inp.focus();
    });
    var stickySearch = $('.vector-sticky-header-search');
    stickySearch.addEventListener('focusout', function (e) {
      if (!stickySearch.contains(e.relatedTarget)) {
        setTimeout(function () {
          if (!stickySearch.contains(doc.activeElement)) sticky.classList.remove('vector-sticky-header-search-active');
        }, 150);
      }
    });
  }
  // Narrow screens: the header search is an icon that expands in place
  var searchBox = $('#p-search');
  var searchToggle = searchBox && $('.search-toggle', searchBox);
  if (searchToggle) {
    searchToggle.addEventListener('click', function (e) {
      e.preventDefault();
      searchBox.classList.add('vector-search-box-expanded');
      $('input', searchBox).focus();
    });
    searchBox.addEventListener('focusout', function (e) {
      if (!searchBox.contains(e.relatedTarget)) {
        setTimeout(function () {
          if (!searchBox.contains(doc.activeElement)) searchBox.classList.remove('vector-search-box-expanded');
        }, 150);
      }
    });
  }

  /* ── typeahead search ──────────────────────────────────────────────── */
  function norm(s) { return String(s || '').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, ''); }
  function suggest(q) {
    q = norm(q.trim());
    if (!q) return [];
    var out = [];
    PAGES.forEach(function (p) {
      var t = norm(p.title), h = norm(p.heading), d = norm(p.description), score = 0;
      if (t.indexOf(q) === 0) score = 100;
      else if (h.indexOf(q) === 0) score = 90;
      else if ((' ' + t).indexOf(' ' + q) >= 0) score = 80;
      else if ((' ' + h).indexOf(' ' + q) >= 0) score = 70;
      else if (t.indexOf(q) >= 0 || h.indexOf(q) >= 0) score = 60;
      else if (d.indexOf(q) >= 0) score = 25;
      if (score) out.push({ score: score, page: p, label: p.title, href: p.href, description: p.description || p.group });
      p.sections.forEach(function (s) {
        var list = [s].concat(s.subs || []);
        list.forEach(function (x) {
          var l = norm(x.label);
          var sc = l.indexOf(q) === 0 ? 45 : (' ' + l).indexOf(' ' + q) >= 0 ? 35 : 0;
          if (sc) out.push({ score: sc, page: p, label: x.label, href: p.href + '#' + x.id, description: p.title + ' § ' + x.label, section: true });
        });
      });
    });
    out.sort(function (a, b) { return b.score - a.score || a.page.index - b.page.index; });
    return out.slice(0, 10);
  }
  function highlight(label, q) {
    var i = norm(label).indexOf(norm(q.trim()));
    if (i < 0 || !q.trim()) return esc(label);
    var n = q.trim().length;
    return esc(label.slice(0, i)) + '<span class="cdx-search-result-title__match">' + esc(label.slice(i, i + n)) + '</span>' + esc(label.slice(i + n));
  }
  function searchUrl(q, fulltext) {
    return href('special/search.html') + '?search=' + encodeURIComponent(q) + (fulltext ? '&fulltext=1' : '');
  }
  function exactPage(q) {
    var n = norm(q.trim());
    return PAGES.filter(function (p) { return norm(p.title) === n || norm(p.heading) === n; })[0] || null;
  }
  $$('.cdx-typeahead-search').forEach(function (box) {
    var form = $('form', box), input = $('input', box);
    var menu = el('div', 'cdx-menu');
    menu.hidden = true;
    menu.setAttribute('role', 'listbox');
    box.appendChild(menu);
    var items = [], active = -1;
    input.setAttribute('role', 'combobox');
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-expanded', 'false');
    function setActive(i) {
      active = i;
      items.forEach(function (a, j) { a.classList.toggle('cdx-menu-item--highlighted', j === i); a.setAttribute('aria-selected', j === i ? 'true' : 'false'); });
    }
    function close() { menu.hidden = true; input.setAttribute('aria-expanded', 'false'); active = -1; }
    function render() {
      var q = input.value;
      if (!q.trim()) { close(); return; }
      var res = suggest(q);
      var rows = res.map(function (r) {
        var thumb = r.page.thumb && !r.section
          ? '<span class="cdx-thumbnail" style="background-image:url(\'' + esc(href(r.page.thumb)) + '\')"></span>'
          : '<span class="cdx-thumbnail cdx-thumbnail--placeholder"></span>';
        return '<a class="cdx-menu-item" role="option" href="' + esc(href(r.href)) + '">' + thumb +
          '<span class="cdx-menu-item__text"><span class="cdx-menu-item__text__label">' + highlight(r.label, q) + '</span>' +
          '<span class="cdx-menu-item__text__description">' + esc(r.description) + '</span></span></a>';
      });
      rows.push('<a class="cdx-menu-item cdx-typeahead-search__search-footer" role="option" href="' + esc(searchUrl(q, true)) + '">' +
        '<span class="cdx-thumbnail cdx-thumbnail--placeholder cdx-thumbnail--search"></span>' +
        '<span class="cdx-typeahead-search__search-footer__text">Search for pages containing <strong>' + esc(q.trim()) + '</strong></span></a>');
      menu.innerHTML = '<div class="cdx-menu__listbox">' + rows.join('') + '</div>';
      items = $$('.cdx-menu-item', menu);
      menu.hidden = false;
      input.setAttribute('aria-expanded', 'true');
      setActive(-1);
    }
    input.addEventListener('input', render);
    input.addEventListener('focus', function () { if (input.value.trim()) render(); });
    input.addEventListener('keydown', function (e) {
      if (menu.hidden) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); setActive((active + 1) % items.length); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(active <= 0 ? items.length - 1 : active - 1); }
      else if (e.key === 'Escape') { close(); }
      else if (e.key === 'Enter' && active >= 0) { e.preventDefault(); location.href = items[active].href; }
    });
    box.addEventListener('focusout', function (e) {
      if (!box.contains(e.relatedTarget)) setTimeout(function () { if (!box.contains(doc.activeElement)) close(); }, 150);
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = input.value.trim();
      var p = q && exactPage(q);
      location.href = p ? href(p.href) : searchUrl(q, !!q);
    });
  });

  /* ── contents: scroll-spy, toggles ─────────────────────────────────── */
  var toc = $('#vector-toc');
  var userToggled = {};
  function tocItems() { return toc ? $$('.vector-toc-list-item', toc) : []; }
  function expand(li, open) {
    li.classList.toggle('vector-toc-list-item-expanded', open);
    var b = $('.vector-toc-toggle', li);
    if (b) b.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  if (toc) {
    $$('.vector-toc-toggle', toc).forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        var li = b.parentNode;
        var open = !li.classList.contains('vector-toc-list-item-expanded');
        userToggled[li.id] = open;
        expand(li, open);
      });
      expand(b.parentNode, false);
    });
  }
  var spyTargets = [];
  tocItems().forEach(function (li) {
    var a = $('.vector-toc-link', li);
    var id = a && decodeURIComponent(a.getAttribute('href').slice(1));
    var t = id && doc.getElementById(id);
    if (t) spyTargets.push({ el: t, li: li });
  });
  var activeLi = null;
  function markToc(li) {
    if (li === activeLi) return;
    activeLi = li;
    tocItems().forEach(function (x) {
      x.classList.remove('vector-toc-list-item-active', 'vector-toc-level-1-active');
    });
    var top = $('#toc-mw-content-text');
    var level1 = null;
    if (!li) { if (top) top.classList.add('vector-toc-list-item-active'); }
    else {
      li.classList.add('vector-toc-list-item-active');
      level1 = li.classList.contains('vector-toc-level-1') ? li : li.parentNode.closest('.vector-toc-level-1');
      if (level1 && level1 !== li) level1.classList.add('vector-toc-level-1-active');
    }
    $$('.vector-toc-level-1', toc).forEach(function (x) {
      if (!$('.vector-toc-list', x)) return;
      var want = x.id in userToggled ? userToggled[x.id] : x === level1;
      expand(x, want);
    });
  }
  var ticking = false;
  function spy() {
    ticking = false;
    if (!spyTargets.length) return;
    var line = (parseFloat(getComputedStyle(html).getPropertyValue('--sticky-offset')) || 0) * 16 + 24;
    var cur = null;
    for (var i = 0; i < spyTargets.length; i++) {
      if (spyTargets[i].el.getBoundingClientRect().top - line <= 0) cur = spyTargets[i].li; else break;
    }
    var max = doc.documentElement.scrollHeight - window.innerHeight;
    if (max - (window.scrollY || 0) < 4 && spyTargets.length) cur = spyTargets[spyTargets.length - 1].li;
    markToc(cur);
  }
  if (toc && ACTION === 'view') {
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(spy); } }, { passive: true });
    window.addEventListener('resize', spy);
    spy();
  }

  /* ── section [edit] links ──────────────────────────────────────────── */
  var sourceSnapshot = null;
  var parser = $('.mw-parser-output');
  if (parser) sourceSnapshot = parser.innerHTML;
  if (!SPECIAL && ACTION === 'view' && parser) {
    $$('section[id] > h2, section[id] > h3[id]', parser).forEach(function (h, i) {
      var label = h.textContent.replace(/\s+/g, ' ').trim();
      var span = el('span', 'mw-editsection',
        '<span class="mw-editsection-bracket">[</span><a href="?action=edit&amp;section=' + (i + 1) +
        '" title="Edit section: ' + esc(label) + '"><span>edit</span></a><span class="mw-editsection-bracket">]</span>');
      h.appendChild(span);
    });
  }

  /* ── navbox [hide]/[show] ──────────────────────────────────────────── */
  $$('.navbox').forEach(function (nb) {
    var th = $('.navbox-title', nb);
    if (!th) return;
    var t = el('span', 'mw-collapsible-toggle', '<button type="button" aria-expanded="true">hide</button>');
    th.insertBefore(t, th.firstChild);
    var b = $('button', t);
    b.addEventListener('click', function () {
      var c = nb.classList.toggle('mw-collapsed');
      b.textContent = c ? 'show' : 'hide';
      b.setAttribute('aria-expanded', c ? 'false' : 'true');
    });
  });

  /* ── footer: last edited, print URL ────────────────────────────────── */
  var lastmod = $('#footer-info-lastmod');
  if (lastmod && CURRENT && CURRENT.lastmod) {
    var d = new Date(CURRENT.lastmod);
    lastmod.innerHTML = 'This page was last edited on ' + fmtDay(d) + ', at ' + fmtTime(d) + '<span class="anonymous-show">&#160;(UTC)</span>.';
  }
  $$('.printfooter a').forEach(function (a) { a.href = selfUrl(); a.textContent = selfUrl(); });

  /* ── tool actions ──────────────────────────────────────────────────── */
  doc.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-action]');
    if (!a) return;
    var act = a.getAttribute('data-action');
    if (act === 'print') { e.preventDefault(); closeDropdowns(null); window.print(); }
    else if (act === 'permalink') {
      e.preventDefault();
      loadScript('js/wiki-history-data.js', function () {
        var revs = (window.WIKI_HISTORY || {})[PAGE] || [];
        location.href = revs.length ? '?oldid=' + revs[0].h.slice(0, 10) : '?';
      });
    } else if (act === 'copyurl') { e.preventDefault(); copy(selfUrl(), 'Link to this page copied to the clipboard.'); }
  });

  /* ── page previews ─────────────────────────────────────────────────── */
  var byPath = {};
  PAGES.forEach(function (p) { byPath[new URL(href(p.href), location.href).pathname] = p; });
  function pageForLink(a) {
    if (!a.href || a.target === '_blank') return null;
    var u;
    try { u = new URL(a.href, location.href); } catch (e) { return null; }
    if (u.origin !== location.origin && location.protocol !== 'file:') return null;
    if (u.search) return null;
    var p = byPath[u.pathname];
    if (!p || p.href === PAGE) return null;
    return { page: p, hash: u.hash.slice(1) };
  }
  var hover = window.matchMedia('(hover: hover) and (pointer: fine)');
  var card = null, showTimer = null, hideTimer = null, cardFor = null;
  function hideCard() {
    clearTimeout(showTimer);
    if (card && card.parentNode) card.parentNode.removeChild(card);
    card = null; cardFor = null;
  }
  function sectionLabel(p, id) {
    var found = null;
    p.sections.forEach(function (s) {
      if (s.id === id) found = s.label;
      (s.subs || []).forEach(function (x) { if (x.id === id) found = x.label; });
    });
    return found;
  }
  function showCard(a, hit) {
    hideCard();
    var p = hit.page;
    var sec = hit.hash && sectionLabel(p, hit.hash);
    card = el('div', 'mwe-popups' + (p.thumb ? ' has-thumb' : ''));
    card.setAttribute('role', 'tooltip');
    card.innerHTML =
      '<a class="mwe-popups-container" href="' + esc(a.href) + '">' +
      (p.thumb ? '<img class="mwe-popups-thumbnail" src="' + esc(href(p.thumb)) + '" alt="">' : '') +
      '<div class="mwe-popups-extract">' +
      '<b>' + esc(p.title) + (sec ? ' § ' + esc(sec) : '') + '</b>' +
      (p.description ? '<span class="mwe-popups-description">' + esc(p.description) + '</span>' : '<br>') +
      esc(p.extract) + '</div></a>' +
      '<footer class="mwe-popups-footer"><small>' + esc(p.group) + ' · ' + num(p.words) + ' words</small>' +
      '<button type="button" class="cdx-button cdx-button--weight-quiet cdx-button--icon-only mwe-popups-settings-button" title="Change preview settings">' +
      icon('settings') + '<span>Change preview settings</span></button></footer>';
    body.appendChild(card);
    cardFor = a;
    var rects = Array.prototype.slice.call(a.getClientRects());
    var r = rects.filter(function (x) { return lastMouse.y >= x.top - 2 && lastMouse.y <= x.bottom + 2; })[0] || rects[0] || a.getBoundingClientRect();
    var w = card.offsetWidth, h = card.offsetHeight;
    var left = Math.min(Math.max(8, r.left), doc.documentElement.clientWidth - w - 8);
    var below = r.bottom + 12 + h < window.innerHeight || r.top < h + 12;
    card.classList.toggle('flipped', !below);
    card.style.left = (left + window.scrollX) + 'px';
    card.style.top = ((below ? r.bottom + 10 : r.top - h - 10) + window.scrollY) + 'px';
    var arrow = Math.max(8, Math.min(w - 24, r.left - left + 4));
    card.style.setProperty('--arrow', arrow + 'px');
    card.querySelector('.mwe-popups-settings-button').addEventListener('click', function (e) { e.preventDefault(); hideCard(); previewSettings(); });
    card.addEventListener('mouseenter', function () { clearTimeout(hideTimer); });
    card.addEventListener('mouseleave', function () { hideTimer = setTimeout(hideCard, 300); });
  }
  function previewSettings() {
    var on = getPref('vector-feature-page-previews') !== '0';
    var bd = el('div', 'cdx-dialog-backdrop',
      '<div class="cdx-dialog" role="dialog" aria-modal="true" aria-labelledby="pp-title">' +
      '<h2 id="pp-title">Reading preferences</h2>' +
      '<p>Page previews show a summary of an article when you hover over a link to it.</p>' +
      '<div class="cdx-radio"><input class="cdx-radio__input" type="radio" name="pp" id="pp-on" value="1"' + (on ? ' checked' : '') + '><span class="cdx-radio__icon"></span><label class="cdx-radio__label" for="pp-on">Enable page previews</label></div>' +
      '<div class="cdx-radio"><input class="cdx-radio__input" type="radio" name="pp" id="pp-off" value="0"' + (on ? '' : ' checked') + '><span class="cdx-radio__icon"></span><label class="cdx-radio__label" for="pp-off">Disable page previews</label></div>' +
      '<div class="cdx-dialog-footer"><button type="button" class="cdx-button" data-x="cancel">Cancel</button>' +
      '<button type="button" class="cdx-button cdx-button--action-progressive cdx-button--weight-primary" data-x="save">Save</button></div></div>');
    body.appendChild(bd);
    var shut = function () { if (bd.parentNode) bd.parentNode.removeChild(bd); doc.removeEventListener('keydown', onKey); };
    var onKey = function (e) { if (e.key === 'Escape') shut(); };
    doc.addEventListener('keydown', onKey);
    bd.addEventListener('click', function (e) {
      var x = e.target.getAttribute('data-x');
      if (e.target === bd || x === 'cancel') shut();
      if (x === 'save') {
        var v = $('input[name="pp"]:checked', bd).value;
        setPref('vector-feature-page-previews', v);
        shut();
        notify(v === '1' ? 'Page previews are on.' : 'Page previews are off. Turn them back on from any preview’s settings, or clear this site’s data.');
      }
    });
    $('[data-x="save"]', bd).focus();
  }
  var lastMouse = { x: 0, y: 0 };
  if (hover.matches) {
    doc.addEventListener('mousemove', function (e) { lastMouse.x = e.clientX; lastMouse.y = e.clientY; }, { passive: true });
    doc.addEventListener('mouseover', function (e) {
      var a = e.target.closest && e.target.closest('.vector-body a[href]');
      if (!a || a === cardFor || getPref('vector-feature-page-previews') === '0') return;
      if (a.closest('.mwe-popups, .vector-toc, .mw-editsection, .navbar')) return;
      var hit = pageForLink(a);
      if (!hit) return;
      clearTimeout(hideTimer); clearTimeout(showTimer);
      showTimer = setTimeout(function () { showCard(a, hit); }, 500);
      a.addEventListener('mouseleave', function out() {
        a.removeEventListener('mouseleave', out);
        clearTimeout(showTimer);
        if (cardFor === a) hideTimer = setTimeout(hideCard, 300);
      });
    });
    window.addEventListener('scroll', function () { if (card && !card.matches(':hover')) hideCard(); }, { passive: true });
  }

  /* ── media viewer ──────────────────────────────────────────────────── */
  var media = parser ? $$('figure > img, .hero-plate > img, .blueprint-body > svg, .blueprint-body > img, .pp-body > svg', parser) : [];
  var mmv = null, mmvIndex = -1, mmvPushed = false, mmvReturn = null;
  function fileName(m) {
    if (m.tagName.toLowerCase() === 'img') return decodeURIComponent(m.getAttribute('src').split('/').pop());
    var label = m.getAttribute('aria-label') || 'Diagram';
    return label.split(/[:;—–]/)[0].trim().replace(/\s+/g, '_').replace(/[^\w\-().]/g, '').slice(0, 80) + '.svg';
  }
  function captionOf(m) {
    var host = m.closest('figure, .blueprint-plate, .hero-plate, .plate-paper');
    var c = host && $('figcaption, .blueprint-cap, .infobox-caption, .pp-cap', host);
    if (c) return c.innerHTML;
    var t = host && $('.blueprint-head .title, .pp-head', host);
    return t ? t.innerHTML : esc(m.getAttribute('alt') || m.getAttribute('aria-label') || '');
  }
  function buildViewer() {
    mmv = el('div', 'mw-mmv-wrapper');
    mmv.hidden = true;
    mmv.setAttribute('role', 'dialog');
    mmv.setAttribute('aria-modal', 'true');
    mmv.setAttribute('aria-label', 'Media viewer');
    mmv.innerHTML =
      '<div class="mw-mmv-image-wrapper"><div class="mw-mmv-image"></div>' +
      '<button type="button" class="cdx-button cdx-button--weight-quiet cdx-button--icon-only mw-mmv-nav mw-mmv-prev" title="Previous image">' + icon('previous') + '<span>Previous image</span></button>' +
      '<button type="button" class="cdx-button cdx-button--weight-quiet cdx-button--icon-only mw-mmv-nav mw-mmv-next" title="Next image">' + icon('next') + '<span>Next image</span></button>' +
      '<div class="mw-mmv-controls">' +
      '<button type="button" class="cdx-button cdx-button--weight-quiet cdx-button--icon-only mw-mmv-fullscreen" title="View in full-screen mode">' + icon('fullScreen') + '<span>Full screen</span></button>' +
      '<button type="button" class="cdx-button cdx-button--weight-quiet cdx-button--icon-only mw-mmv-close" title="Close this tool (Esc)">' + icon('close') + '<span>Close</span></button>' +
      '</div></div>' +
      '<div class="mw-mmv-post-image"><div><h2 class="mw-mmv-title"></h2><div class="mw-mmv-caption"></div></div>' +
      '<div class="mw-mmv-meta"><a class="cdx-button cdx-button--action-progressive cdx-button--weight-primary mw-mmv-details">More details</a>' +
      '<span class="mw-mmv-position"></span></div></div>';
    body.appendChild(mmv);
    $('.mw-mmv-close', mmv).addEventListener('click', closeViewer);
    $('.mw-mmv-prev', mmv).addEventListener('click', function () { showMedia(mmvIndex - 1); });
    $('.mw-mmv-next', mmv).addEventListener('click', function () { showMedia(mmvIndex + 1); });
    $('.mw-mmv-fullscreen', mmv).addEventListener('click', function () {
      if (doc.fullscreenElement) doc.exitFullscreen(); else if (mmv.requestFullscreen) mmv.requestFullscreen();
    });
    $('.mw-mmv-image-wrapper', mmv).addEventListener('click', function (e) { if (e.target === this || e.target.classList.contains('mw-mmv-image')) closeViewer(); });
    doc.addEventListener('keydown', function (e) {
      if (mmv.hidden) return;
      if (e.key === 'Escape') closeViewer();
      else if (e.key === 'ArrowLeft') showMedia(mmvIndex - 1);
      else if (e.key === 'ArrowRight') showMedia(mmvIndex + 1);
    });
  }
  function showMedia(i) {
    if (!media.length) return;
    mmvIndex = (i + media.length) % media.length;
    var m = media[mmvIndex];
    var stage = $('.mw-mmv-image', mmv);
    stage.innerHTML = '';
    var clone = m.cloneNode(true);
    clone.removeAttribute('width'); clone.removeAttribute('height'); clone.removeAttribute('loading');
    clone.removeAttribute('tabindex'); clone.removeAttribute('role'); clone.classList.remove('mw-file-clickable');
    if (m.tagName.toLowerCase() === 'svg') clone.setAttribute('role', 'img');
    stage.appendChild(clone);
    var name = fileName(m);
    $('.mw-mmv-title', mmv).textContent = 'File:' + name;
    $('.mw-mmv-caption', mmv).innerHTML = captionOf(m);
    $('.mw-mmv-position', mmv).textContent = (mmvIndex + 1) + ' of ' + media.length;
    var det = $('.mw-mmv-details', mmv);
    if (m.tagName.toLowerCase() === 'img') {
      det.textContent = 'More details'; det.href = m.src; det.target = '_blank'; det.rel = 'noopener'; det.removeAttribute('download');
    } else {
      var blob = new Blob(['<?xml version="1.0" encoding="UTF-8"?>\n' + m.outerHTML], { type: 'image/svg+xml' });
      det.textContent = 'Download'; det.href = URL.createObjectURL(blob); det.setAttribute('download', name); det.removeAttribute('target');
    }
    $$('.mw-mmv-nav', mmv).forEach(function (b) { b.hidden = media.length < 2; });
    var hash = '#/media/File:' + encodeURIComponent(name);
    if (mmvPushed) history.replaceState({ mmv: true }, '', hash);
  }
  function openViewer(i, fromHash) {
    if (!mmv) buildViewer();
    mmvReturn = doc.activeElement;
    mmv.hidden = false;
    body.classList.add('mw-mmv-lightbox-open');
    hideCard();
    if (!fromHash) { history.pushState({ mmv: true }, '', '#'); mmvPushed = true; }
    else mmvPushed = true;
    showMedia(i);
    $('.mw-mmv-close', mmv).focus();
  }
  function closeViewer() {
    if (!mmv || mmv.hidden) return;
    mmv.hidden = true;
    body.classList.remove('mw-mmv-lightbox-open');
    if (doc.fullscreenElement) doc.exitFullscreen();
    if (mmvPushed && history.state && history.state.mmv) { mmvPushed = false; history.back(); }
    else if (/^#\/media\//.test(location.hash)) history.replaceState(null, '', location.pathname + location.search);
    mmvPushed = false;
    if (mmvReturn && mmvReturn.focus) mmvReturn.focus();
  }
  window.addEventListener('popstate', function () {
    if (mmv && !mmv.hidden && !/^#\/media\//.test(location.hash)) { mmvPushed = false; closeViewer(); }
  });
  media.forEach(function (m, i) {
    m.classList.add('mw-file-clickable');
    m.setAttribute('tabindex', '0');
    m.setAttribute('role', m.tagName.toLowerCase() === 'svg' ? 'img' : 'button');
    if (m.tagName.toLowerCase() === 'img') m.setAttribute('aria-label', 'View image: ' + (m.getAttribute('alt') || fileName(m)));
    m.addEventListener('click', function (e) { if (!e.target.closest('a')) openViewer(i); });
    m.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openViewer(i); }
    });
  });
  if (/^#\/media\/File:/.test(location.hash) && media.length) {
    var want = decodeURIComponent(location.hash.replace(/^#\/media\/File:/, ''));
    media.forEach(function (m, i) { if (fileName(m) === want) openViewer(i, true); });
  }

  /* ── page actions: ?action=… ───────────────────────────────────────── */
  var content = $('#mw-content-text');
  var sub = $('#mw-content-subtitle');
  var titleMain = heading && $('.mw-page-title-main', heading);
  var pageTitle = CURRENT ? CURRENT.title : (titleMain ? titleMain.textContent : '');
  function actionPage(opts) {
    body.classList.remove('action-view');
    body.classList.add('action-' + opts.action);
    html.classList.remove('vector-toc-available');
    html.classList.add('vector-toc-not-available');
    doc.title = opts.docTitle + ' - ' + SITE;
    if (titleMain) titleMain.innerHTML = opts.heading;
    $$('.vector-sticky-header-context-bar-primary .mw-page-title-main').forEach(function (s) { s.innerHTML = opts.heading; });
    $$('#p-views .mw-list-item, #p-associated-pages .mw-list-item, .vector-page-tools .mw-list-item').forEach(function (li) { li.classList.remove('selected'); });
    (opts.tabs || []).forEach(function (id) { $$('#' + id).forEach(function (li) { li.classList.add('selected'); }); });
    var siteSub = $('#siteSub');
    if (siteSub) siteSub.style.display = 'none';
    var ind = $('.vector-body-before-content .mw-indicators');
    if (ind && opts.action !== 'view') ind.style.display = opts.keepIndicators ? '' : 'none';
    if (sub) sub.innerHTML = opts.sub || '';
    var cat = $('#catlinks');
    if (cat) cat.style.display = 'none';
    content.innerHTML = '<div class="mw-body-content mw-content-ltr mw-parser-output" lang="en" dir="ltr">' + opts.body + '</div>';
    window.scrollTo(0, 0);
  }
  var backlink = CURRENT ? '← <a href="' + esc(PAGE.split('/').pop()) + '" title="' + esc(pageTitle) + '">' + esc(pageTitle) + '</a>' : '';
  var selfName = PAGE.split('/').pop();

  function sourceFor(section, done) {
    var full = function (src) {
      var m = src.match(/<!-- article:start -->\n?([\s\S]*?)\n?<!-- article:end -->/);
      return m ? m[1] : src;
    };
    var pick = function (src) {
      if (!section) return src;
      var box = el('div'); box.innerHTML = src;
      var hs = $$('section[id] > h2, section[id] > h3[id]', box);
      var h = hs[section - 1];
      if (!h) return src;
      if (h.tagName === 'H2') return h.parentNode.outerHTML;
      var out = [h.outerHTML], n = h.nextElementSibling;
      while (n && !/^H[23]$/.test(n.tagName)) { out.push(n.outerHTML); n = n.nextElementSibling; }
      return out.join('\n');
    };
    if (location.protocol !== 'file:' && window.fetch) {
      fetch(location.pathname, { cache: 'no-cache' }).then(function (r) { return r.text(); })
        .then(function (t) { done(pick(full(t))); }, function () { done(pick(sourceSnapshot || '')); });
    } else done(pick(full(sourceSnapshot || '')));
  }

  function viewSource() {
    var section = parseInt(PARAMS.get('section') || '0', 10) || 0;
    actionPage({
      action: 'edit', docTitle: 'View source for ' + pageTitle,
      heading: 'View source for ' + esc(pageTitle), sub: backlink, tabs: ['ca-viewsource', 'ca-nstab-main'],
      body: '<div class="mw-message-box mw-message-box-warning"><p>You do not have permission to edit this page, for the following reason:</p>' +
        '<p><b>This page is protected.</b> Apollyon Wiki is published from HTML files in its repository. To change this article, edit the file <code>' +
        esc(PAGE) + '</code> between its <code>article:start</code> and <code>article:end</code> markers, then rebuild the wiki with <code>scripts/site_shell.py</code>.</p></div>' +
        '<p>You can view and copy the source of this page' + (section ? ' (section ' + section + ')' : '') + '.</p>' +
        '<textarea class="mw-source-textarea" readonly aria-label="Page source">Loading…</textarea>' +
        '<p>Return to <a href="' + esc(selfName) + '">' + esc(pageTitle) + '</a>.</p>'
    });
    sourceFor(section, function (src) { $('.mw-source-textarea').value = src.replace(/^\n+|\s+$/g, '') + '\n'; });
  }

  function historyView() {
    actionPage({
      action: 'history', docTitle: pageTitle + ': Revision history',
      heading: esc(pageTitle) + ': Revision history', sub: backlink, tabs: ['ca-history', 'ca-nstab-main', 'ca-more-history'],
      body: '<p class="mw-special-loading">Loading revisions…</p>'
    });
    loadScript('js/wiki-history-data.js', function () {
      var revs = (window.WIKI_HISTORY || {})[PAGE] || [];
      var box = $('.mw-parser-output', content);
      if (!revs.length) { box.innerHTML = '<p>No revisions are recorded for this page. The history is read from git when the wiki is built.</p>'; return; }
      var rows = revs.map(function (r, i) {
        var prev = revs[i + 1];
        var delta = r.b != null && prev && prev.b != null ? r.b - prev.b : r.b;
        var dcls = delta > 0 ? 'mw-plusminus-pos' : delta < 0 ? 'mw-plusminus-neg' : 'mw-plusminus-null';
        var big = Math.abs(delta) >= 500 ? ' big' : '';
        var d = new Date(r.d);
        return '<li' + (i === 0 ? ' class="selected"' : '') + '>' +
          '<span class="mw-history-histlinks mw-changeslist-links"><span>cur</span><span>prev</span></span> ' +
          '<span class="mw-changeslist-date" title="' + esc(r.h) + '">' + fmtStamp(d) + '</span> ' +
          '<span class="history-user"><bdi>' + esc(r.a) + '</bdi></span> ' +
          '<span class="mw-changeslist-separator"></span> ' +
          (r.b != null ? '<span class="history-size">' + num(r.b) + ' bytes</span> ' : '') +
          '<span class="' + dcls + big + '">' + (delta > 0 ? '+' : '') + num(delta || 0) + '</span> ' +
          '<span class="mw-changeslist-separator"></span> ' +
          '<span class="comment">' + esc(r.s) + '</span> <code>' + esc(r.h.slice(0, 7)) + '</code></li>';
      });
      box.innerHTML =
        '<p>Each revision is a commit to this page\'s source file. Size is the file size in bytes; the figure after it is the change from the revision before.</p>' +
        '<p class="mw-history-legend">Legend: (cur) = difference with latest revision, (prev) = difference with preceding revision.</p>' +
        '<p>(newest | oldest) View (newer 50 | older 50) (20 | 50 | 100 | 250 | 500)</p>' +
        '<ul id="pagehistory">' + rows.join('') + '</ul>' +
        '<p>(newest | oldest) View (newer 50 | older 50) (20 | 50 | 100 | 250 | 500)</p>';
    });
  }

  function infoView() {
    actionPage({
      action: 'info', docTitle: 'Information for "' + pageTitle + '"',
      heading: 'Information for "' + esc(pageTitle) + '"', sub: backlink, tabs: ['ca-nstab-main'],
      body: '<p class="mw-special-loading">Loading…</p>'
    });
    loadScript('js/wiki-history-data.js', function () {
      var revs = (window.WIKI_HISTORY || {})[PAGE] || [];
      var p = CURRENT;
      var snap = el('div'); snap.innerHTML = sourceSnapshot || '';
      var figures = $$('figure, .blueprint-plate', snap).length;
      var tables = $$('table', snap).length;
      var internal = $$('a[href]', snap).filter(function (a) { return !/^(https?:|mailto:|#)/.test(a.getAttribute('href')); }).length;
      var external = $$('a[href^="http"]', snap).length;
      var subs = p.sections.reduce(function (n, s) { return n + (s.subs || []).length; }, 0);
      var newest = revs[0], oldest = revs[revs.length - 1];
      var month = Date.now() - 30 * 864e5;
      var recent = revs.filter(function (r) { return new Date(r.d).getTime() >= month; });
      var authors = {};
      recent.forEach(function (r) { authors[r.a] = 1; });
      var row = function (k, v, id) { return '<tr' + (id ? ' id="' + id + '"' : '') + '><th>' + k + '</th><td>' + v + '</td></tr>'; };
      $('.mw-parser-output', content).innerHTML =
        '<h2 id="mw-pageinfo-header-basic">Basic information</h2><table class="wikitable mw-page-info">' +
        row('Display title', p.heading ? esc(p.heading) : esc(p.title)) +
        row('Default sort key', esc(p.title)) +
        row('Page length (in bytes)', num(p.bytes)) +
        row('Page content language', 'en - English') +
        row('Page content model', 'HTML, between <code>article:start</code> and <code>article:end</code>') +
        row('Indexing by robots', 'Allowed') +
        row('Number of redirects to this page', '0') +
        row('Counted as a content page', 'Yes') +
        row('Number of sections', p.sections.length + ' (and ' + subs + ' subsections)') +
        row('Number of words', num(p.words)) +
        row('Number of figures', num(figures)) +
        row('Number of tables', num(tables)) +
        row('Links to other pages', num(internal) + ' internal, ' + num(external) + ' external') +
        row('Pages that link here', '<a href="?action=whatlinkshere">' + num((p.links || []).length) + '</a>') +
        row('Category', '<a href="' + esc(href('special/contents.html#' + p.groupSlug)) + '">' + esc(p.group) + '</a>') +
        row('Reading order', (p.index + 1) + ' of ' + PAGES.length) +
        (p.thumb ? row('Page image', '<a href="' + esc(href(p.thumb)) + '"><img src="' + esc(href(p.thumb)) + '" alt="" style="width:120px;height:auto"></a>') : '') +
        '</table>' +
        '<h2 id="mw-pageinfo-restrictions">Page protection</h2><table class="wikitable mw-page-info">' +
        row('Edit', 'Allow only repository maintainers (infinite)') +
        row('Move', 'Allow only repository maintainers (infinite)') +
        '</table>' +
        '<h2 id="mw-pageinfo-header-edits">Edit history</h2><table class="wikitable mw-page-info">' +
        (oldest ? row('Page creator', esc(oldest.a)) + row('Date of page creation', fmtStamp(new Date(oldest.d))) : '') +
        (newest ? row('Latest editor', esc(newest.a)) + row('Date of latest edit', fmtStamp(new Date(newest.d))) : '') +
        row('Total number of edits', '<a href="?action=history">' + num(revs.length) + '</a>') +
        row('Recent number of edits (within past 30 days)', num(recent.length)) +
        row('Recent number of distinct authors', num(Object.keys(authors).length)) +
        '</table>' +
        '<h2 id="mw-pageinfo-header-properties">Page properties</h2><table class="wikitable mw-page-info">' +
        row('Transcluded templates (4)', 'Template:Navbox &middot; Template:Succession box &middot; Template:Category handler &middot; Template:Pp-protected') +
        '</table>';
      if (location.hash) { var t = doc.getElementById(location.hash.slice(1)); if (t) t.scrollIntoView(); }
    });
  }

  function citeView() {
    actionPage({
      action: 'cite', docTitle: 'Cite this page: ' + pageTitle,
      heading: 'Cite this page', sub: backlink, tabs: ['ca-nstab-main'],
      body: '<p class="mw-special-loading">Loading…</p>'
    });
    loadScript('js/wiki-history-data.js', function () {
      var revs = (window.WIKI_HISTORY || {})[PAGE] || [];
      var rev = revs[0];
      var last = rev ? new Date(rev.d) : new Date();
      var now = new Date();
      var link = selfUrl();
      var y = last.getUTCFullYear(), mon = MONTHS[last.getUTCMonth()], day = last.getUTCDate();
      var shortMon = function (d) { return MONTHS[d.getUTCMonth()].slice(0, 3); };
      var key = 'wiki:' + (rev ? rev.h.slice(0, 10) : 'current');
      var t = esc(pageTitle);
      var tagline = SITE + ', The Neo-Prime Encyclopedia';
      $('.mw-parser-output', content).innerHTML =
        '<div class="mw-cite-styles">' +
        '<h2>Bibliographic details for "' + t + '"</h2><ul>' +
        '<li>Page name: ' + t + '</li>' +
        '<li>Author: Apollyon Dynamics</li>' +
        '<li>Publisher: <i>' + esc(tagline) + '</i>.</li>' +
        '<li>Date of last revision: ' + fmtDay(last) + ' ' + fmtTime(last) + ' UTC</li>' +
        '<li>Date retrieved: ' + fmtDay(now) + ' ' + fmtTime(now) + ' UTC</li>' +
        '<li>Permanent URL: <a href="' + esc(link) + '">' + esc(link) + '</a></li>' +
        (rev ? '<li>Page Version ID: <code>' + esc(rev.h.slice(0, 10)) + '</code></li>' : '') +
        '</ul><p>Check your style guide, or your editor\'s, for the exact syntax to suit your needs.</p>' +
        '<h2>Citation styles for "' + t + '"</h2>' +
        '<h3>APA style</h3><p>' + t + '. (' + y + ', ' + mon + ' ' + day + '). In <i>' + esc(SITE) + '</i>. Retrieved ' + fmtTime(now) + ', ' + MONTHS[now.getUTCMonth()] + ' ' + now.getUTCDate() + ', ' + now.getUTCFullYear() + ', from ' + esc(link) + '</p>' +
        '<h3>MLA style</h3><p>"' + t + '." <i>' + esc(tagline) + '</i>. ' + day + ' ' + shortMon(last) + '. ' + y + '. Web. ' + now.getUTCDate() + ' ' + shortMon(now) + '. ' + now.getUTCFullYear() + '.</p>' +
        '<h3>MHRA style</h3><p>Apollyon Dynamics, \'' + t + '\', <i>' + esc(tagline) + ',</i> ' + fmtDay(last) + ', ' + fmtTime(last) + ' UTC, &lt;' + esc(link) + '&gt; [accessed ' + fmtDay(now) + ']</p>' +
        '<h3>Chicago style</h3><p>Apollyon Dynamics, "' + t + '," <i>' + esc(tagline) + ',</i> ' + esc(link) + ' (accessed ' + MONTHS[now.getUTCMonth()] + ' ' + now.getUTCDate() + ', ' + now.getUTCFullYear() + ').</p>' +
        '<h3>CBE/CSE style</h3><p>Apollyon Dynamics. ' + t + ' [Internet]. ' + esc(tagline) + '; ' + y + ' ' + shortMon(last) + ' ' + day + ', ' + fmtTime(last) + ' UTC [cited ' + now.getUTCFullYear() + ' ' + shortMon(now) + ' ' + now.getUTCDate() + ']. Available from: ' + esc(link) + '.</p>' +
        '<h3>Bluebook style</h3><p>' + t + ', ' + esc(link) + ' (last visited ' + MONTHS[now.getUTCMonth()] + ' ' + now.getUTCDate() + ', ' + now.getUTCFullYear() + ').</p>' +
        '<h3>AMA style</h3><p>Apollyon Dynamics. ' + t + '. ' + esc(tagline) + '. ' + mon + ' ' + day + ', ' + y + ', ' + fmtTime(last) + ' UTC. Available at: ' + esc(link) + '. Accessed ' + MONTHS[now.getUTCMonth()] + ' ' + now.getUTCDate() + ', ' + now.getUTCFullYear() + '.</p>' +
        '<h3>BibTeX entry</h3><pre>@misc{ ' + esc(key) + ',\n  author = "Apollyon Dynamics",\n  title = "' + t + ' --- {' + esc(SITE) + '}{,} The Neo-Prime Encyclopedia",\n  year = "' + y + '",\n  url = "' + esc(link) + '",\n  note = "[Online; accessed ' + now.getUTCDate() + '-' + MONTHS[now.getUTCMonth()] + '-' + now.getUTCFullYear() + ']"\n}</pre>' +
        '<p>When using the LaTeX package url (<code>\\usepackage{url}</code> somewhere in the preamble) which tends to give much more nicely formatted web addresses, the following may be preferred:</p>' +
        '<pre>@misc{ ' + esc(key) + ',\n  author = "Apollyon Dynamics",\n  title = "' + t + ' --- {' + esc(SITE) + '}{,} The Neo-Prime Encyclopedia",\n  year = "' + y + '",\n  url = "\\url{' + esc(link) + '}",\n  note = "[Online; accessed ' + now.getUTCDate() + '-' + MONTHS[now.getUTCMonth()] + '-' + now.getUTCFullYear() + ']"\n}</pre>' +
        '</div>';
    });
  }

  function linksView() {
    var links = (CURRENT && CURRENT.links) || [];
    var items = links.map(function (h) {
      var p = PAGES.filter(function (x) { return x.href === h; })[0];
      if (!p) return '';
      return '<li><a href="' + esc(href(p.href)) + '">' + esc(p.title) + '</a> ‎ (<a href="' + esc(href(p.href)) + '?action=whatlinkshere">← links</a> | <a href="' + esc(href(p.href)) + '?action=edit">edit</a>)</li>';
    });
    actionPage({
      action: 'whatlinkshere', docTitle: 'Pages that link to "' + pageTitle + '"',
      heading: 'Pages that link to "' + esc(pageTitle) + '"', sub: backlink, tabs: ['ca-nstab-main'],
      body: (items.length
        ? '<p>The following pages link to <a href="' + esc(selfName) + '">' + esc(pageTitle) + '</a>:</p>' +
          '<p>View (previous 50 | next 50) (20 | 50 | 100 | 250 | 500)</p><ul id="mw-whatlinkshere-list">' + items.join('') + '</ul>' +
          '<p>View (previous 50 | next 50) (20 | 50 | 100 | 250 | 500)</p>'
        : '<p>No pages link to <a href="' + esc(selfName) + '">' + esc(pageTitle) + '</a>.</p>')
    });
  }

  function talkView() {
    actionPage({
      action: 'talk', docTitle: 'Talk:' + pageTitle,
      heading: '<span class="mw-page-title-namespace">Talk</span><span class="mw-page-title-separator">:</span>' + esc(pageTitle),
      sub: '', tabs: ['ca-talk', 'ca-view'],
      body: '<div class="mw-message-box"><p><b>' + esc(SITE) + ' does not have a talk page with this exact name.</b> ' +
        'Discussion of this article happens with the people who wrote it.</p><ul>' +
        '<li>Questions, corrections and evaluation requests go to <a href="' + esc(href('about/history.html#contact')) + '">Apollyon Dynamics</a>.</li>' +
        '<li>Return to the article: <a href="' + esc(selfName) + '">' + esc(pageTitle) + '</a>.</li>' +
        '<li><a href="' + esc(searchUrl(pageTitle, true)) + '">Search for "' + esc(pageTitle) + '"</a> in existing pages.</li>' +
        '<li>See the <a href="' + esc(href('special/recent-changes.html')) + '">recent changes</a> to the wiki.</li></ul></div>'
    });
  }

  function oldidNotice() {
    loadScript('js/wiki-history-data.js', function () {
      var revs = (window.WIKI_HISTORY || {})[PAGE] || [];
      var want = PARAMS.get('oldid');
      var match = revs.filter(function (r) { return r.h.indexOf(want) === 0; })[0];
      var box = el('div', 'mw-message-box');
      if (match && match === revs[0]) {
        var d = new Date(match.d);
        box.innerHTML = 'This is the <b>current revision</b> of this page, as edited by <bdi>' + esc(match.a) + '</bdi> at ' +
          fmtTime(d) + ', ' + fmtDay(d) + ' (<code>' + esc(match.h.slice(0, 10)) + '</code>). The present address (URL) is a permanent link to this version.';
      } else {
        box.innerHTML = 'Revision <code>' + esc(want) + '</code> of this page is not published here. What follows is the current revision; ' +
          'see the <a href="?action=history">revision history</a>.';
      }
      if (sub) sub.parentNode.insertBefore(box, sub.nextSibling);
    });
  }

  if (!SPECIAL && CURRENT && content) {
    if (ACTION === 'edit') viewSource();
    else if (ACTION === 'history') historyView();
    else if (ACTION === 'info') infoView();
    else if (ACTION === 'cite') citeView();
    else if (ACTION === 'whatlinkshere') linksView();
    else if (ACTION === 'talk') talkView();
    else if (PARAMS.get('oldid')) oldidNotice();
  }

  /* ── special pages ─────────────────────────────────────────────────── */
  var special = $('#mw-special-root');
  var kind = special && special.getAttribute('data-special');
  var siteSubEl = $('#siteSub');
  if (special && siteSubEl) siteSubEl.style.display = 'none';

  if (kind === 'random') {
    var ref = doc.referrer ? new URL(doc.referrer).pathname : '';
    var pool = PAGES.filter(function (p) { return byPath[ref] !== p; });
    var pick = pool[Math.floor(Math.random() * pool.length)];
    if (pick) location.replace(href(pick.href));
  }

  if (kind === 'contents') {
    var filter = el('div', 'mw-contents-filter cdx-text-input cdx-text-input--has-start-icon',
      '<input class="cdx-text-input__input" type="search" placeholder="Filter pages and sections" aria-label="Filter pages and sections">' +
      '<span class="cdx-text-input__icon cdx-text-input__start-icon"></span>');
    special.insertBefore(filter, special.children[1] || null);
    var f = $('input', filter);
    f.addEventListener('input', function () {
      var q = norm(f.value.trim()), any = false;
      $$('.mw-contents-page', special).forEach(function (li) {
        li.hidden = !!q && norm(li.getAttribute('data-text')).indexOf(q) < 0;
        if (!li.hidden) any = true;
      });
      $$('[data-group]', special).forEach(function (g) { g.hidden = !$('.mw-contents-page:not([hidden])', g); });
      $('.mw-contents-none', special).hidden = any;
    });
  }

  if (kind === 'recentchanges') {
    loadScript('js/wiki-history-data.js', function () {
      var H = window.WIKI_HISTORY || {};
      var rows = [];
      PAGES.forEach(function (p) {
        (H[p.href] || []).forEach(function (r, i, arr) {
          var prev = arr[i + 1];
          rows.push({ p: p, r: r, delta: r.b != null && prev && prev.b != null ? r.b - prev.b : r.b, created: !prev });
        });
      });
      rows.sort(function (a, b) { return new Date(b.r.d) - new Date(a.r.d); });
      var out = [], day = null;
      rows.slice(0, 250).forEach(function (x) {
        var d = new Date(x.r.d), k = fmtDay(d);
        if (k !== day) { if (day) out.push('</ul>'); out.push('<h4 class="mw-changeslist-day">' + k + '</h4><ul class="special">'); day = k; }
        var dcls = x.delta > 0 ? 'mw-plusminus-pos' : x.delta < 0 ? 'mw-plusminus-neg' : 'mw-plusminus-null';
        var big = Math.abs(x.delta) >= 500 ? ' big' : '';
        out.push('<li><span class="mw-changeslist-links"><span>diff</span><span><a href="' + esc(href(x.p.href)) + '?action=history">hist</a></span></span> ' +
          '<span class="mw-changeslist-separator"></span> ' + (x.created ? '<abbr class="newpage" title="This edit created a new page">N</abbr>&nbsp;' : '') +
          '<a href="' + esc(href(x.p.href)) + '"><b>' + esc(x.p.title) + '</b></a>; <span class="mw-changeslist-date">' + fmtTime(d) + '</span> ' +
          '<span class="mw-changeslist-separator"></span> <span class="' + dcls + big + '">(' + (x.delta > 0 ? '+' : '') + num(x.delta || 0) + ')</span> ' +
          '<span class="mw-changeslist-separator"></span> <bdi>' + esc(x.r.a) + '</bdi> <span class="comment">' + esc(x.r.s) + '</span></li>');
      });
      if (day) out.push('</ul>');
      special.innerHTML =
        '<p>Track the most recent changes to ' + esc(SITE) + ' on this page. Each line is a commit that touched an article; times are UTC.</p>' +
        '<p>Show last 50 | 100 | 250 | 500 changes in last 1 | 3 | 7 | 14 | 30 days</p>' +
        (rows.length ? out.join('') : '<p>No changes are recorded. The list is read from git when the wiki is built.</p>');
    });
  }

  if (kind === 'search') {
    var q = (PARAMS.get('search') || '').trim();
    $$('.cdx-typeahead-search input').forEach(function (i) { if (!i.closest('.vector-sticky-header')) i.value = q; });
    special.innerHTML =
      '<form class="mw-search-form" action="search.html"><div class="cdx-text-input cdx-text-input--has-start-icon">' +
      '<input class="cdx-text-input__input" type="search" name="search" value="' + esc(q) + '" aria-label="Search ' + esc(SITE) + '" autofocus>' +
      '<span class="cdx-text-input__icon cdx-text-input__start-icon"></span></div>' +
      '<input type="hidden" name="fulltext" value="1"><button class="cdx-button">Search</button></form><div class="mw-search-out"></div>';
    var out = $('.mw-search-out', special);
    if (!q) { out.innerHTML = '<p>Enter words to search every article. Pages whose title matches go to the top.</p>'; }
    else {
      doc.title = q + ' - Search results - ' + SITE;
      out.innerHTML = '<p class="mw-special-loading">Searching…</p>';
      loadScript('js/wiki-search-data.js', function () {
        var terms = norm(q).split(/[^\p{L}\p{N}]+/u).filter(function (t) { return t.length > 1 || /\d/.test(t); });
        var data = window.WIKI_SEARCH || [];
        var results = [];
        data.forEach(function (doc_) {
          var p = PAGES.filter(function (x) { return x.href === doc_.href; })[0];
          if (!p) return;
          var all = norm(doc_.title + ' ' + doc_.sections.map(function (s) { return s.h + ' ' + s.t; }).join(' '));
          if (!terms.every(function (t) { return all.indexOf(t) >= 0; })) return;
          var score = 0, best = null, bestHits = -1;
          terms.forEach(function (t) { if (norm(doc_.title).indexOf(t) >= 0) score += 50; });
          doc_.sections.forEach(function (s) {
            var text = norm(s.h + ' ' + s.t), hits = 0;
            terms.forEach(function (t) {
              var i = -1; while ((i = text.indexOf(t, i + 1)) >= 0) hits++;
              if (norm(s.h).indexOf(t) >= 0) hits += 5;
            });
            score += hits;
            if (hits > bestHits) { bestHits = hits; best = s; }
          });
          results.push({ p: p, score: score, section: best });
        });
        results.sort(function (a, b) { return b.score - a.score || a.p.index - b.p.index; });
        var exact = exactPage(q);
        var mark = function (text) {
          var t = esc(text);
          terms.forEach(function (term) {
            t = t.replace(new RegExp('(' + term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'), '<span class="searchmatch">$1</span>');
          });
          return t;
        };
        var snippet = function (s) {
          var text = s.t, n = norm(text), at = -1;
          terms.forEach(function (t) { var i = n.indexOf(t); if (i >= 0 && (at < 0 || i < at)) at = i; });
          if (at < 0) return mark(text.slice(0, 180)) + '…';
          var start = Math.max(0, text.lastIndexOf(' ', Math.max(0, at - 70)));
          var end = Math.min(text.length, at + 150);
          return (start > 0 ? '… ' : '') + mark(text.slice(start, end).trim()) + (end < text.length ? ' …' : '');
        };
        var list = results.map(function (r) {
          var s = r.section;
          var sec = s && s.id ? ' <span class="mw-search-result-section">(section <a href="' + esc(href(r.p.href)) + '#' + esc(s.id) + '">' + esc(s.h) + '</a>)</span>' : '';
          var d = r.p.lastmod ? new Date(r.p.lastmod) : null;
          return '<li class="mw-search-result"><div class="mw-search-result-heading"><a href="' + esc(href(r.p.href)) + '">' + mark(r.p.title) + '</a>' + sec + '</div>' +
            '<div class="searchresult">' + (s ? snippet(s) : '') + '</div>' +
            '<div class="mw-search-result-data">' + Math.round(r.p.bytes / 1024) + ' KB (' + num(r.p.words) + ' words)' + (d ? ' - ' + fmtStamp(d) : '') + '</div></li>';
        });
        out.innerHTML =
          (exact ? '<p class="mw-search-exists">There is a page named "<a href="' + esc(href(exact.href)) + '"><b>' + esc(exact.title) + '</b></a>" on this wiki.</p>' : '') +
          (list.length
            ? '<div class="results-info">Results 1 – ' + list.length + ' of ' + list.length + '</div><ul class="mw-search-results">' + list.join('') + '</ul>'
            : '<p class="mw-search-nonefound">There were no results matching the query.</p><p>Try fewer words, or browse the <a href="contents.html">Contents</a>.</p>');
      });
    }
  }
})();
