/**
 * Nimbe Deck Helpers — reusable JS for HTML slide decks.
 *
 * Provides three building blocks (all ADN of the Nimbe presentation system):
 *  1. setupOverlays()   — on-demand detail overlays (click trigger -> glass overlay)
 *  2. setupSidebar()    — left lexique nav with active-slide sync
 *  3. setupSlideNav()   — right nav-dots + progress bar synced via IntersectionObserver
 *
 * Usage : copy this file inline into a standalone deck OR <script src="..."></script>.
 * Designed to be idempotent : safe to call setup* multiple times (defensive).
 *
 * Conventions :
 *   - Slides : <section class="slide"> elements. First h1/h2/eyebrow text becomes the
 *     sidebar title (auto-extracted).
 *   - Overlay triggers : any element with [data-overlay-open="<id>"]. Auto-decorated
 *     with .expandable-trigger.
 *   - Overlay containers : <div class="overlay-glass" id="<id>" hidden>...</div> at
 *     end of <body>. Must contain a button.overlay-close and the content.
 *   - Sidebar : container <nav class="lex-sidebar"></nav> + toggle button .lex-sidebar-toggle.
 *     Items are auto-built from slides.
 *   - Nav dots : container <div class="nav-dots" id="navDots"></div> + progress bar
 *     <div class="progress-bar" id="progressBar"></div>. Dots auto-built.
 */

(function (global) {
  'use strict';

  /* --------------------------------------------------------------------- */
  /* 1. Overlay pattern                                                    */
  /* --------------------------------------------------------------------- */
  function setupOverlays(opts) {
    var triggers = document.querySelectorAll('[data-overlay-open]');
    var overlays = document.querySelectorAll('.overlay-glass');
    var lastFocus = null;

    function open(id) {
      var overlay = document.getElementById(id);
      if (!overlay) return;
      lastFocus = document.activeElement;
      overlay.removeAttribute('hidden');
      requestAnimationFrame(function () { overlay.classList.add('open'); });
      document.body.classList.add('overlay-open');
      setTimeout(function () {
        var closeBtn = overlay.querySelector('.overlay-close');
        if (closeBtn) closeBtn.focus();
      }, 100);
    }
    function close(overlay) {
      overlay.classList.remove('open');
      document.body.classList.remove('overlay-open');
      setTimeout(function () {
        overlay.setAttribute('hidden', '');
        if (lastFocus && lastFocus.focus) lastFocus.focus();
      }, 350);
    }
    function closeAll() {
      document.querySelectorAll('.overlay-glass.open').forEach(close);
    }

    triggers.forEach(function (t) {
      if (t.__nimbeOverlayBound) return;
      t.__nimbeOverlayBound = true;
      t.classList.add('expandable-trigger');
      t.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        open(t.dataset.overlayOpen);
      });
    });

    overlays.forEach(function (o) {
      if (o.__nimbeOverlayBound) return;
      o.__nimbeOverlayBound = true;
      var closeBtn = o.querySelector('.overlay-close');
      if (closeBtn) closeBtn.addEventListener('click', function () { close(o); });
      o.addEventListener('click', function (e) {
        if (e.target === o) close(o);
      });
    });

    if (!setupOverlays.__keydownBound) {
      setupOverlays.__keydownBound = true;
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeAll();
      });
    }

    return { open: open, close: close, closeAll: closeAll };
  }

  /* --------------------------------------------------------------------- */
  /* 2. Sidebar lexique                                                    */
  /* --------------------------------------------------------------------- */
  function setupSidebar(opts) {
    opts = opts || {};
    var slidesSel = opts.slides || '.slide';
    var sidebarSel = opts.sidebar || '.lex-sidebar';
    var toggleSel = opts.toggle || '.lex-sidebar-toggle';
    var storageKey = opts.storageKey || 'nimbe-deck-sidebar';

    var sidebar = document.querySelector(sidebarSel);
    var toggle = document.querySelector(toggleSel);
    var slides = document.querySelectorAll(slidesSel);
    if (!sidebar || !slides.length) return null;

    var list = sidebar.querySelector('.lex-sidebar-list');
    if (!list) {
      list = document.createElement('ul');
      list.className = 'lex-sidebar-list';
      sidebar.appendChild(list);
    } else {
      list.innerHTML = '';
    }

    function extractTitle(slide) {
      var h1 = slide.querySelector('h1');
      if (h1 && h1.textContent.trim()) return h1.textContent.trim();
      var h2 = slide.querySelector('h2');
      if (h2 && h2.textContent.trim()) return h2.textContent.trim();
      var eb = slide.querySelector('.eyebrow');
      if (eb && eb.textContent.trim()) return eb.textContent.trim();
      return 'Slide ' + (Array.prototype.indexOf.call(slides, slide) + 1);
    }

    slides.forEach(function (slide, i) {
      var li = document.createElement('li');
      li.className = 'lex-item';
      li.dataset.slideIdx = i;
      li.innerHTML = '<span class="lex-item-num">' +
        String(i + 1).padStart(2, '0') + '</span>' +
        '<span class="lex-item-title">' + extractTitle(slide) + '</span>';
      li.addEventListener('click', function () {
        slide.scrollIntoView({ behavior: 'smooth' });
      });
      list.appendChild(li);
    });

    function applyState(collapsed) {
      sidebar.classList.toggle('collapsed', collapsed);
      try { localStorage.setItem(storageKey, collapsed ? '1' : '0'); } catch (e) {}
    }
    var saved = null;
    try { saved = localStorage.getItem(storageKey); } catch (e) {}
    var initialCollapsed = saved === null
      ? (window.innerWidth < 1280)
      : (saved === '1');
    applyState(initialCollapsed);

    if (toggle) {
      toggle.addEventListener('click', function () {
        applyState(!sidebar.classList.contains('collapsed'));
      });
    }

    return {
      setActive: function (idx) {
        var items = list.querySelectorAll('.lex-item');
        items.forEach(function (it, i) {
          it.classList.toggle('active', i === idx);
        });
      }
    };
  }

  /* --------------------------------------------------------------------- */
  /* 3. Slide nav (right dots + progress bar) via IntersectionObserver     */
  /* --------------------------------------------------------------------- */
  function setupSlideNav(opts) {
    opts = opts || {};
    var slidesSel = opts.slides || '.slide';
    var dotsSel = opts.dotsContainer || '#navDots';
    var progressSel = opts.progressBar || '#progressBar';
    var threshold = typeof opts.threshold === 'number' ? opts.threshold : 0.55;
    var onActive = opts.onActive || null;

    var slides = document.querySelectorAll(slidesSel);
    var dotsContainer = document.querySelector(dotsSel);
    var progressBar = document.querySelector(progressSel);
    if (!slides.length || !dotsContainer) return null;

    dotsContainer.innerHTML = '';
    slides.forEach(function (s, i) {
      var dot = document.createElement('div');
      dot.className = 'nav-dot';
      dot.title = 'Slide ' + (i + 1);
      dot.addEventListener('click', function () {
        s.scrollIntoView({ behavior: 'smooth' });
      });
      dotsContainer.appendChild(dot);
    });
    var dots = dotsContainer.querySelectorAll('.nav-dot');

    function setActive(idx) {
      dots.forEach(function (d, i) { d.classList.toggle('active', i === idx); });
      if (progressBar) {
        progressBar.style.width = ((idx + 1) / slides.length * 100) + '%';
      }
      if (onActive) onActive(idx);
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var idx = Array.prototype.indexOf.call(slides, e.target);
          if (idx >= 0) setActive(idx);
        }
      });
    }, { threshold: threshold, rootMargin: '0px' });
    slides.forEach(function (s) { io.observe(s); });

    setActive(0);

    return { setActive: setActive };
  }

  /* --------------------------------------------------------------------- */
  /* Public API                                                            */
  /* --------------------------------------------------------------------- */
  global.NimbeDeck = {
    setupOverlays: setupOverlays,
    setupSidebar: setupSidebar,
    setupSlideNav: setupSlideNav,
    /**
     * One-call init that wires sidebar + nav + overlays together.
     * Returns the three controllers : { overlays, sidebar, nav }.
     */
    init: function (opts) {
      opts = opts || {};
      var sidebar = setupSidebar(opts.sidebar);
      var nav = setupSlideNav({
        slides: (opts.nav && opts.nav.slides) || '.slide',
        dotsContainer: (opts.nav && opts.nav.dotsContainer) || '#navDots',
        progressBar: (opts.nav && opts.nav.progressBar) || '#progressBar',
        onActive: function (idx) { if (sidebar) sidebar.setActive(idx); }
      });
      var overlays = setupOverlays(opts.overlays);
      return { overlays: overlays, sidebar: sidebar, nav: nav };
    }
  };
})(typeof window !== 'undefined' ? window : this);
