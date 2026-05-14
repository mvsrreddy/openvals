/**
 * OpenVals Documentation — App Logic
 */
(function () {
  'use strict';

  // ── Theme ──────────────────────────────────────────────
  const toggle = document.querySelector('.theme-toggle');
  const stored = localStorage.getItem('ov-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', stored);
  setIcon(stored);

  toggle.addEventListener('click', () => {
    const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('ov-theme', next);
    setIcon(next);
  });

  function setIcon(t) { toggle.textContent = t === 'dark' ? '☀' : '☽'; }

  // ── Mobile Menu ────────────────────────────────────────
  const burger = document.querySelector('.hamburger');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');

  if (burger) burger.addEventListener('click', openSidebar);
  if (overlay) overlay.addEventListener('click', closeSidebar);

  function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.add('active');
  }
  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
  }

  // ── Sidebar Sections ───────────────────────────────────
  document.querySelectorAll('.sidebar-section-title').forEach(el => {
    el.addEventListener('click', () => el.parentElement.classList.toggle('collapsed'));
  });

  // ── Table of Contents ──────────────────────────────────
  const tocList = document.querySelector('.toc-list');
  const headings = document.querySelectorAll('.content h2, .content h3');

  if (tocList && headings.length) {
    headings.forEach(h => {
      if (!h.id) {
        h.id = h.textContent.trim().toLowerCase()
          .replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
      }
      const a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.firstChild.textContent.trim();
      a.className = h.tagName === 'H3' ? 'toc-h3' : '';
      tocList.appendChild(a);

      // anchor link on heading
      const anchor = document.createElement('a');
      anchor.className = 'anchor-link';
      anchor.href = '#' + h.id;
      anchor.textContent = '#';
      h.appendChild(anchor);
    });

    // scroll spy
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          let current = '';
          headings.forEach(h => {
            if (window.scrollY >= h.offsetTop - 80) current = h.id;
          });
          tocList.querySelectorAll('a').forEach(a => {
            a.classList.toggle('active', a.getAttribute('href') === '#' + current);
          });
          ticking = false;
        });
        ticking = true;
      }
    });
  }

  // ── Syntax Highlighting ────────────────────────────────
  function highlight(code) {
    // Order matters: comments & strings first to avoid keyword matches inside them
    const tokens = [];
    let i = 0;
    const src = code;

    while (i < src.length) {
      // Line comment
      if (src[i] === '#') {
        const end = src.indexOf('\n', i);
        const slice = end === -1 ? src.slice(i) : src.slice(i, end);
        tokens.push('<span class="tok-cmt">' + esc(slice) + '</span>');
        i += slice.length;
        continue;
      }
      // Strings
      if (src[i] === '"' || src[i] === "'") {
        const q = src.slice(i, i + 3) === '"""' || src.slice(i, i + 3) === "'''"
          ? src.slice(i, i + 3) : src[i];
        const end = src.indexOf(q, i + q.length);
        const slice = end === -1 ? src.slice(i) : src.slice(i, end + q.length);
        tokens.push('<span class="tok-str">' + esc(slice) + '</span>');
        i += slice.length;
        continue;
      }
      // Word
      if (/[a-zA-Z_]/.test(src[i])) {
        let w = '';
        while (i < src.length && /[\w]/.test(src[i])) { w += src[i]; i++; }
        const kw = ['def','class','if','else','elif','for','while','return','from',
          'import','as','try','except','finally','with','pass','in','is','and','or',
          'not','lambda','yield','async','await','None','True','False','raise','del','global','nonlocal','assert','break','continue'];
        const bi = ['print','len','range','enumerate','zip','dict','list','set','tuple',
          'int','str','float','bool','super','type','input','open','sum','min','max',
          'abs','round','sorted','map','filter','isinstance','hasattr','getattr','setattr'];
        if (w === 'self' || w === 'cls') tokens.push('<span class="tok-self">' + w + '</span>');
        else if (kw.includes(w)) tokens.push('<span class="tok-kw">' + w + '</span>');
        else if (bi.includes(w)) tokens.push('<span class="tok-bi">' + w + '</span>');
        else if (i < src.length && src[i] === '(') tokens.push('<span class="tok-fn">' + w + '</span>');
        else tokens.push(esc(w));
        continue;
      }
      // Numbers
      if (/\d/.test(src[i])) {
        let n = '';
        while (i < src.length && /[\d.]/.test(src[i])) { n += src[i]; i++; }
        tokens.push('<span class="tok-num">' + n + '</span>');
        continue;
      }
      // Decorator
      if (src[i] === '@' && (i === 0 || src[i - 1] === '\n')) {
        let d = '';
        while (i < src.length && /[\w@.]/.test(src[i])) { d += src[i]; i++; }
        tokens.push('<span class="tok-dec">' + esc(d) + '</span>');
        continue;
      }
      // Operators
      if ('=+-*/<>!&|%^~:'.includes(src[i])) {
        tokens.push('<span class="tok-op">' + esc(src[i]) + '</span>');
        i++;
        continue;
      }
      tokens.push(esc(src[i]));
      i++;
    }
    return tokens.join('');
  }

  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  document.querySelectorAll('pre code.language-python').forEach(block => {
    block.innerHTML = highlight(block.textContent);
  });

  // ── Copy Button ────────────────────────────────────────
  document.querySelectorAll('.code-block-wrapper').forEach(wrap => {
    const btn = wrap.querySelector('.copy-btn');
    const code = wrap.querySelector('code');
    if (!btn || !code) return;
    btn.addEventListener('click', () => {
      navigator.clipboard.writeText(code.textContent).then(() => {
        btn.textContent = '✓ Copied';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 1500);
      });
    });
  });

  // ── Search ─────────────────────────────────────────────
  const searchBtn = document.querySelector('.header-search-btn');
  const searchModal = document.querySelector('.search-modal');
  const searchInput = document.querySelector('.search-input');
  const searchResults = document.querySelector('.search-results');
  let focusIdx = -1;

  if (!searchBtn || !searchModal) return;

  searchBtn.addEventListener('click', openSearch);

  function openSearch() {
    searchModal.classList.add('active');
    searchInput.value = '';
    searchResults.innerHTML = '';
    focusIdx = -1;
    setTimeout(() => searchInput.focus(), 50);
  }

  function closeSearch() {
    searchModal.classList.remove('active');
  }

  searchModal.addEventListener('click', e => {
    if (e.target === searchModal) closeSearch();
  });

  // Keyboard: /, Esc, arrows, enter
  document.addEventListener('keydown', e => {
    if (e.key === '/' && !isInput(e.target)) {
      e.preventDefault();
      openSearch();
    }
    if (e.key === 'Escape') closeSearch();
  });

  searchInput.addEventListener('keydown', e => {
    const items = searchResults.querySelectorAll('.search-result-item');
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      focusIdx = Math.min(focusIdx + 1, items.length - 1);
      updateFocus(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      focusIdx = Math.max(focusIdx - 1, 0);
      updateFocus(items);
    } else if (e.key === 'Enter' && focusIdx >= 0 && items[focusIdx]) {
      e.preventDefault();
      window.location.href = items[focusIdx].getAttribute('href');
    }
  });

  function updateFocus(items) {
    items.forEach((el, i) => el.classList.toggle('focused', i === focusIdx));
    if (items[focusIdx]) items[focusIdx].scrollIntoView({ block: 'nearest' });
  }

  function isInput(el) {
    return el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.isContentEditable;
  }

  // Perform search on input
  searchInput.addEventListener('input', () => {
    const q = searchInput.value.trim();
    focusIdx = -1;

    if (!q) { searchResults.innerHTML = ''; return; }

    const results = typeof window.search === 'function' ? window.search(q) : [];

    if (!results.length) {
      searchResults.innerHTML = '<div class="search-empty">No results for "' + esc(q) + '"</div>';
      return;
    }

    searchResults.innerHTML = results.map(r => {
      const snippet = highlightMatch(r.content, q, 90);
      const tag = r.url.includes('api/') ? 'API' :
                  r.url.includes('guides/') ? 'Guide' : '';
      return `<a href="${r.url}" class="search-result-item">
        <div class="search-result-title">${r.title}${tag ? ' <span class="search-result-tag">' + tag + '</span>' : ''}</div>
        <div class="search-result-snippet">${snippet}</div>
      </a>`;
    }).join('');
  });

  function highlightMatch(text, query, maxLen) {
    const lower = text.toLowerCase();
    const qi = lower.indexOf(query.toLowerCase());
    if (qi === -1) return esc(text.slice(0, maxLen)) + '…';

    const start = Math.max(0, qi - 30);
    const end = Math.min(text.length, qi + query.length + (maxLen - 30));
    let snippet = (start > 0 ? '…' : '') + text.slice(start, end) + (end < text.length ? '…' : '');

    // Insert <mark> tags around the match
    const re = new RegExp('(' + query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
    return esc(snippet).replace(re, '<mark>$1</mark>');
  }

})();
