// AI Security Corpus: hotkeys, client-side search, section rail, hero pause. No dependencies.
(function () {
  'use strict';
  var root = document.documentElement.getAttribute('data-root') || './';
  var q = document.getElementById('q');
  var box = document.getElementById('results');
  var prompt = q && q.closest('.prompt');
  var corpus = null, loading = null, timer = null, items = [], quiet = false;

  // the index has one search field, in the hero: the status line's 'search' link scrolls to it
  var find = document.querySelector('.topbar .find');
  if (find && q) {
    find.addEventListener('click', function (e) {
      e.preventDefault();
      q.scrollIntoView({ block: 'center' });
      q.focus({ preventScroll: true });
    });
  }

  // ---------- hotkeys: / focuses search, Esc clears it, 1-8 jump to a group ----------
  // The digit keys can be switched off (WCAG 2.1.4); the choice is remembered per browser.
  var digitsOn = true;
  try { digitsOn = localStorage.getItem('hotkeys') !== 'off'; } catch (err) {}
  var hk = document.querySelector('.hk');
  function paintHk() {
    if (!hk) return;
    hk.textContent = 'hotkeys ' + (digitsOn ? 'on' : 'off');
    hk.setAttribute('aria-pressed', String(digitsOn));
    document.querySelectorAll('.sysop kbd').forEach(function (k) { k.classList.toggle('off', !digitsOn); });
  }
  if (hk) {
    paintHk();
    hk.addEventListener('click', function () {
      digitsOn = !digitsOn;
      try { localStorage.setItem('hotkeys', digitsOn ? 'on' : 'off'); } catch (err) {}
      paintHk();
    });
  }
  document.addEventListener('keydown', function (e) {
    var el = document.activeElement, tag = el && el.tagName;
    var typing = /input|textarea|select/i.test(tag || '');
    if (e.key === '/' && !typing && q) { e.preventDefault(); q.focus(); q.select(); return; }
    if (e.key === 'Escape') {
      // refocusing the prompt must not reopen the list it just closed
      if (box && !box.hidden) { hide(); if (q) { quiet = true; q.focus(); quiet = false; } return; }
      if (typing) { el.blur(); return; }
    }
    if (typing || e.metaKey || e.ctrlKey || e.altKey || !digitsOn) return;
    if (box && !box.hidden && el && box.contains(el)) return;
    var t = /^[1-8]$/.test(e.key) && document.querySelector('[data-hotkey="' + e.key + '"]');
    if (t) {
      t.scrollIntoView({ block: 'start' });
      var a = t.querySelector('a');
      if (a) a.focus({ preventScroll: true });
    }
  });

  // ---------- search ----------
  function load() {
    // corpus.json is the whole site model; a title/url-only index would be only 3% smaller gzipped,
    // since titles and URLs are the bulk of it, so the one file serves both
    if (loading) return loading;
    loading = fetch(root + 'data/corpus.json').then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(function (d) {
      corpus = d;
      items = [];
      d.groups.forEach(function (g) {
        g.categories.forEach(function (c) {
          var cat = { g: g.name, gs: g.slug, n: c.label || c.name, h: catPath(g, c) };
          c.sections.forEach(function (s) {
            s.links.forEach(function (l) {
              items.push({ t: l.t, u: l.u, d: l.d, k: (l.t + ' ' + l.d).toLowerCase(), c: cat, href: root + cat.h });
            });
          });
        });
      });
      return d;
    });
    return loading;
  }
  function catPath(g, c) {
    var p = c.path.split('/');
    return (p.length === 3 ? p[0] + '/' + p[1] : g.slug + '/' + c.slug) + '/';
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (ch) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]; });
  }
  function hilite(s, terms) {
    // one pass over the escaped text with every term in a single alternation, so a later term can never
    // match inside a <mark> tag inserted by an earlier one
    var parts = terms.filter(function (t) { return t.length >= 2; })
      .map(function (t) { return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); });
    if (!parts.length) return esc(s);
    var re = new RegExp('(' + parts.join('|') + ')', 'ig');
    return esc(s).replace(re, '<mark>$1</mark>');
  }
  var live = document.getElementById('q-status');
  function announce(text) { if (live) live.textContent = text; }
  function show(html, foot) {
    box.innerHTML = '<div class="rl">' + html + '</div>' + (foot ? '<div class="rf">' + foot + '</div>' : '');
    box.hidden = false;
    // a list taller than the panel gets a fade at its bottom edge and a 'scroll for more' cue
    var rl = box.firstChild;
    box.classList.toggle('over', rl.scrollHeight > rl.clientHeight + 1);
  }
  function hide() {
    if (box) { box.hidden = true; box.innerHTML = ''; box.classList.remove('over'); }
    if (prompt) prompt.classList.remove('live');
    announce('');
  }
  function status(msg, spoken) {
    if (!box) return;
    show('<div class="rs">' + msg + '</div>');
    announce(spoken || msg);
  }
  function run() {
    var text = q.value.trim().toLowerCase();
    if (!text) { hide(); return; }
    if (prompt) prompt.classList.add('live');
    if (!corpus) {
      status('loading the corpus index ...');
      load().then(run, function () { status('could not load data/corpus.json; try the category pages instead'); });
      return;
    }
    var terms = text.split(/\s+/).filter(Boolean);
    var hits = [], cap = 120;
    for (var i = 0; i < items.length; i++) {
      var it = items[i], ok = true;
      for (var j = 0; j < terms.length; j++) { if (it.k.indexOf(terms[j]) < 0) { ok = false; break; } }
      if (ok) { hits.push(it); }
    }
    if (!hits.length) {
      status('no match for <b>' + esc(q.value.trim()) + '</b> in ' + fmt(items.length) + ' links',
        'No match for ' + q.value.trim() + ' in ' + fmt(items.length) + ' links');
      return;
    }
    var groups = [], byCat = {}, shown = Math.min(hits.length, cap);
    hits.slice(0, cap).forEach(function (h) {
      var key = h.c.h;
      if (!byCat[key]) { byCat[key] = { c: h.c, href: h.href, rows: [] }; groups.push(byCat[key]); }
      byCat[key].rows.push(h);
    });
    var tail = ' match' + (hits.length === 1 ? '' : 'es') + ' in ' + groups.length + ' categor' + (groups.length === 1 ? 'y' : 'ies');
    var summary = fmt(hits.length) + tail;
    var html = '<div class="rs"><span class="n">' + fmt(hits.length) + '</span>' + tail + '. Arrow keys move, Enter opens, Esc closes.</div>';
    groups.forEach(function (gr) {
      html += '<div class="rh" style="--gc:var(--c-' + gr.c.gs + ')"><a href="' + esc(gr.href) + '"><span class="g">' + esc(gr.c.g) + ' / </span>' +
        esc(gr.c.n) + '</a></div><ul aria-label="' + esc(gr.c.g + ' / ' + gr.c.n) + '">';
      gr.rows.forEach(function (r) {
        html += '<li><a href="' + esc(r.u) + '">' + hilite(r.t, terms) + '<i>' + hilite(r.d, terms) + '</i></a></li>';
      });
      html += '</ul>';
    });
    if (hits.length > cap) html += '<div class="more">showing the first ' + cap + '; add a word to narrow it down</div>';
    show(html, '<span><span class="n">' + shown + '</span> of ' + fmt(hits.length) + ' shown</span><span>Esc closes</span><span class="sc">scroll for more ▾</span>');
    announce(summary + (hits.length > cap ? ', showing the first ' + cap : ''));
  }
  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }

  if (q && box) {
    q.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(run, corpus ? 60 : 0);
    });
    q.addEventListener('focus', function () { if (!quiet && q.value.trim() && box.hidden) run(); });
    q.addEventListener('keydown', function (e) {
      // Enter and ArrowDown both step into the list; a second Enter on the focused row opens it
      if ((e.key === 'ArrowDown' || e.key === 'Enter') && !box.hidden) {
        var first = box.querySelector('li a');
        if (first) { e.preventDefault(); first.focus(); }
      }
    });
    box.addEventListener('keydown', function (e) {
      var links = Array.prototype.slice.call(box.querySelectorAll('li a'));
      var i = links.indexOf(document.activeElement);
      if (i < 0) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); (links[i + 1] || links[0]).focus(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); if (i === 0) q.focus(); else links[i - 1].focus(); }
      else if (e.key === 'Home') { e.preventDefault(); links[0].focus(); }
      else if (e.key === 'End') { e.preventDefault(); links[links.length - 1].focus(); }
    });
    document.addEventListener('click', function (e) {
      if (!box.hidden && !box.contains(e.target) && e.target !== q) hide();
    });
    var form = q.closest('form');
    if (form) form.addEventListener('submit', function (e) { e.preventDefault(); run(); });
    // Deep link from the site's SearchAction: ?q=term
    var m = /[?&]q=([^&]+)/.exec(location.search);
    if (m) { q.value = decodeURIComponent(m[1].replace(/\+/g, ' ')); q.focus(); run(); }
  }

  // ---------- category page: the sticky rail sits under the sticky bar, whatever height the bar is ----------
  var bar = document.querySelector('.topbar.sticky');
  function barH() { document.documentElement.style.setProperty('--topbar-h', bar.offsetHeight + 'px'); }
  if (bar) {
    barH();
    if ('ResizeObserver' in window) new ResizeObserver(barH).observe(bar);
    else window.addEventListener('resize', barH);
  }

  // ---------- category page: highlight the section in view in the rail ----------
  var rail = document.querySelector('.rail');
  if (rail && 'IntersectionObserver' in window) {
    var map = {}, list = rail.querySelector('ol');
    rail.querySelectorAll('a[href^="#"]').forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    // keep the current chip in view by scrolling the rail's own box only, never the document
    // (scrollIntoView also moves the page, which yanked phone readers back to the chip row)
    function reveal(a) {
      var r = a.getBoundingClientRect();
      if (list.scrollWidth > list.clientWidth + 1) {
        var lb = list.getBoundingClientRect();
        if (r.left < lb.left + 12 || r.right > lb.right - 60) list.scrollLeft += r.left - lb.left - 12;
      } else if (rail.scrollHeight > rail.clientHeight + 1) {
        var rb = rail.getBoundingClientRect();
        if (r.top < rb.top || r.bottom > rb.bottom) rail.scrollTop += r.top - rb.top - rb.height / 2;
      }
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          rail.querySelectorAll('a.on').forEach(function (a) { a.classList.remove('on'); });
          var a = map[en.target.id];
          if (a) { a.classList.add('on'); reveal(a); }
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('.section').forEach(function (s) { io.observe(s); });
  }

  // ---------- pause every infinite animation (prism breathe, ghost drift, caret blink) when the tab is hidden,
  // and the hero's when it has scrolled off-screen ----------
  document.addEventListener('visibilitychange', function () {
    document.documentElement.classList.toggle('hid', document.hidden);
  });
  var hero = document.querySelector('.hero');
  if (hero) {
    var seen = true;
    function sync() { hero.classList.toggle('paused', document.hidden || !seen); }
    document.addEventListener('visibilitychange', sync);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { seen = en[0].isIntersecting; sync(); }).observe(hero);
    }
  }
})();
