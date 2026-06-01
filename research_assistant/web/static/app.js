/* ═══════════════════════════════════════════════════════════════════════════
   Research Assistant — Theme & UI Helpers
   ═══════════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── Theme management ─────────────────────────────────────────────────── */
  const THEME_KEY = 'ra-theme';

  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function getTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored === 'light' || stored === 'dark') return stored;
    if (stored === 'system') return getSystemTheme();
    return getSystemTheme(); // default to system
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    updateToggleUI(localStorage.getItem(THEME_KEY) || 'system');
  }

  function setTheme(mode) {
    localStorage.setItem(THEME_KEY, mode);
    const resolved = mode === 'system' ? getSystemTheme() : mode;
    applyTheme(resolved);
  }

  function updateToggleUI(mode) {
    document.querySelectorAll('.theme-toggle-btn').forEach(function (btn) {
      var val = btn.getAttribute('data-theme-value');
      btn.classList.toggle('active', val === mode);
      btn.setAttribute('aria-pressed', val === mode ? 'true' : 'false');
    });
  }

  // Initialize theme immediately (before paint)
  var storedMode = localStorage.getItem(THEME_KEY) || 'system';
  var initialTheme = storedMode === 'system' ? getSystemTheme() : storedMode;
  document.documentElement.setAttribute('data-theme', initialTheme);

  // Listen for system theme changes when in system mode
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
    if (localStorage.getItem(THEME_KEY) === 'system') {
      applyTheme(getSystemTheme());
    }
  });

  // Expose for inline onclick handlers
  window.setTheme = setTheme;
  window.updateToggleUI = updateToggleUI;

  /* ── Tab switching ────────────────────────────────────────────────────── */
  window.switchTab = function (groupId, tabId) {
    var bar = document.getElementById(groupId + '-bar');
    if (!bar) return;

    // Update tab buttons
    bar.querySelectorAll('.tab-btn').forEach(function (btn) {
      var isActive = btn.getAttribute('data-tab') === tabId;
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    // Update tab panels
    var panels = document.querySelectorAll('[id^="' + groupId + '-"]');
    panels.forEach(function (panel) {
      if (panel.id === groupId + '-' + tabId) {
        panel.classList.add('active');
      } else if (panel.getAttribute('role') === 'tabpanel') {
        panel.classList.remove('active');
      }
    });
  };

  /* ── Copy diagnostics ─────────────────────────────────────────────────── */
  window.copyDiagnostics = function (btn) {
    var pre = btn.closest('.state-box') ? btn.parentElement.parentElement.querySelector('pre') : null;
    if (!pre) pre = document.getElementById('diagnostics');
    if (!pre) return;

    var text = pre.textContent;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(function () {
          btn.textContent = 'Copy';
          btn.classList.remove('copied');
        }, 2000);
      });
    } else {
      // Fallback
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(function () {
        btn.textContent = 'Copy';
        btn.classList.remove('copied');
      }, 2000);
    }
  };

  /* ── Sidebar toggle (mobile) ──────────────────────────────────────────── */
  window.toggleSidebar = function () {
    var sidebar = document.querySelector('.app-sidebar');
    var overlay = document.querySelector('.sidebar-overlay');
    if (!sidebar) return;
    sidebar.classList.toggle('open');
    if (overlay) overlay.classList.toggle('open');
  };

  /* ── Advanced settings toggle ─────────────────────────────────────────── */
  document.addEventListener('click', function (e) {
    var toggle = e.target.closest('.advanced-toggle');
    if (toggle) {
      toggle.classList.toggle('open');
      var panel = toggle.nextElementSibling;
      if (panel) panel.classList.toggle('open');
      toggle.setAttribute('aria-expanded', panel && panel.classList.contains('open') ? 'true' : 'false');
    }
  });

  /* ── Initialize toggle UI on DOM ready ────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', function () {
    updateToggleUI(storedMode);
  });

  /* ── Right control panel ─────────────────────────────────────────────── */
  var panelState = { open: false, currentTab: 'status', loadedTabs: {} };

  window.togglePanel = function () {
    var panel = document.querySelector('.control-panel');
    var overlay = document.querySelector('.panel-overlay');
    var trigger = document.querySelector('.panel-trigger');
    if (!panel || !overlay) return;

    panelState.open = !panelState.open;
    panel.classList.toggle('open', panelState.open);
    overlay.classList.toggle('open', panelState.open);
    if (trigger) trigger.classList.toggle('active', panelState.open);
    document.body.style.overflow = panelState.open ? 'hidden' : '';

    // Lazy-load first tab content on first open
    if (panelState.open && !panelState.loadedTabs[panelState.currentTab]) {
      openPanelTab(panelState.currentTab);
    }
  };

  window.closePanel = function () {
    var panel = document.querySelector('.control-panel');
    var overlay = document.querySelector('.panel-overlay');
    var trigger = document.querySelector('.panel-trigger');
    if (!panel) return;

    panelState.open = false;
    panel.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    if (trigger) trigger.classList.remove('active');
    document.body.style.overflow = '';
  };

  window.openPanelTab = function (tabId) {
    panelState.currentTab = tabId;

    // Update tab buttons
    document.querySelectorAll('.panel-tab-btn').forEach(function (btn) {
      var isActive = btn.getAttribute('data-panel-tab') === tabId;
      btn.classList.toggle('active', isActive);
    });

    // Show the correct tab panel
    document.querySelectorAll('.panel-tab-panel').forEach(function (panel) {
      panel.classList.toggle('active', panel.id === 'panel-tab-' + tabId);
    });

    // HTMX-load content if first time
    if (!panelState.loadedTabs[tabId]) {
      var target = document.getElementById('panel-tab-' + tabId);
      if (!target) return;

      var url;
      switch (tabId) {
        case 'status':     url = '/panel/status'; break;
        case 'settings':   url = '/panel/settings'; break;
        case 'providers':  url = '/panel/providers'; break;
        default: return;
      }

      target.innerHTML = '<div style="display:flex;justify-content:center;padding:2rem;"><span class="spinner"></span></div>';
      target.setAttribute('hx-get', url);
      target.setAttribute('hx-trigger', 'load');
      htmx.process(target);
      panelState.loadedTabs[tabId] = true;
    }
  };

  // Overlay click to close
  document.addEventListener('click', function (e) {
    if (e.target.classList.contains('panel-overlay')) {
      closePanel();
    }
  });

  // Keyboard shortcuts
  document.addEventListener('keydown', function (e) {
    // Escape closes the panel
    if (e.key === 'Escape' && panelState.open) {
      closePanel();
      e.preventDefault();
    }
    // Ctrl+\ toggles the panel
    if ((e.ctrlKey || e.metaKey) && e.key === '\\') {
      togglePanel();
      e.preventDefault();
    }
  });

  // Close sidebar on Escape (moved to panel handler above — keep both working)
  // The earlier Escape handler in base.html inline script handles sidebar.

  /* ── Provider test debounce ─────────────────────────────────────────────── */
  var _providerTestTimer = null;

  window.testAllProviders = function () {
    var btn = document.querySelector('[onclick="testAllProviders()"]');
    if (!btn || btn.disabled) return;

    btn.disabled = true;
    btn.textContent = 'Testing…';

    var forms = document.querySelectorAll('form[hx-post="/providers/test"]');
    forms.forEach(function (form, i) {
      setTimeout(function () {
        htmx.trigger(form, 'submit');
      }, i * 350); // stagger by 350ms to avoid rate-limit storms
    });

    // Re-enable after all requests have had time to complete
    setTimeout(function () {
      btn.disabled = false;
      btn.textContent = 'Test all providers';
    }, forms.length * 350 + 15000);
  };

  // Debounce individual provider test clicks (HTMX submit)
  document.addEventListener('htmx:beforeRequest', function (e) {
    var el = e.detail.elt;
    if (el.getAttribute('hx-post') !== '/providers/test') return;

    var btn = el.querySelector('button[type="submit"]');
    if (!btn) return;

    if (btn.disabled) {
      e.preventDefault();
      return;
    }

    btn.disabled = true;
    var origText = btn.textContent;
    btn.textContent = 'Testing…';

    // Re-enable after a reasonable timeout
    setTimeout(function () {
      btn.disabled = false;
      btn.textContent = origText;
    }, 20000);
  });

})();
