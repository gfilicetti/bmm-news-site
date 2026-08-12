/**
 * BMM News - Custom Agent Search Widget & Modal (Option B)
 * Live Agent Search API Integration (discoveryengine.googleapis.com)
 * Data Store ID: bmm-site-1_1785864019095
 * Project ID: bmm-news-site
 */

(function () {
  'use strict';

  function createModalDOM() {
    if (document.getElementById('bmm-search-modal')) return;

    const modalHTML = `
      <div id="bmm-search-modal" class="bmm-search-modal" aria-hidden="true" role="dialog" aria-modal="true">
        <div class="bmm-search-backdrop"></div>
        <div class="bmm-search-container">
          <div class="bmm-search-header">
            <span class="bmm-search-icon">🔍</span>
            <input type="text" id="bmm-search-input" class="bmm-search-input" placeholder="Search news via Agent Search..." autocomplete="off" spellcheck="false" focus>
            <button id="bmm-search-close" class="bmm-search-close" aria-label="Close Search">&times;</button>
          </div>
          <div class="bmm-search-subhead">
            <span class="bmm-search-badge"><span class="pulse-dot"></span>Live Search</span>
            <span class="bmm-search-shortcut"><kbd>ESC</kbd> to exit</span>
          </div>
          <div id="bmm-search-body" class="bmm-search-body">
            <div id="bmm-ai-answer" class="bmm-ai-answer" style="display:none;"></div>
            <div id="bmm-search-results" class="bmm-search-results">
              <div class="bmm-search-placeholder"></div>
            </div>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);
    bindModalEvents();
  }

  function bindModalEvents() {
    const modal = document.getElementById('bmm-search-modal');
    const input = document.getElementById('bmm-search-input');
    const closeBtn = document.getElementById('bmm-search-close');
    const backdrop = modal.querySelector('.bmm-search-backdrop');

    // Header Trigger
    document.querySelectorAll('#searchWidgetTrigger, .search-trigger, [href="#search"]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    });

    // Keybindings (Cmd+K, Ctrl+K, /)
    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        openModal();
      } else if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault();
        openModal();
      } else if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
      }
    });

    closeBtn.addEventListener('click', closeModal);
    backdrop.addEventListener('click', closeModal);

    // Input Debounced API Calls
    let debounceTimer;
    input.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      const query = e.target.value.trim();
      debounceTimer = setTimeout(() => {
        performLiveAgentSearch(query);
      }, 300);
    });
  }

  function openModal() {
    const modal = document.getElementById('bmm-search-modal');
    const input = document.getElementById('bmm-search-input');
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    setTimeout(() => input.focus(), 50);
  }

  function closeModal() {
    const modal = document.getElementById('bmm-search-modal');
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  // Live Agent Search API Call
  async function performLiveAgentSearch(query) {
    const aiAnswerEl = document.getElementById('bmm-ai-answer');
    const resultsEl = document.getElementById('bmm-search-results');

    if (!query || query.length === 0) {
      aiAnswerEl.style.display = 'none';
      resultsEl.innerHTML = '<div class="bmm-search-placeholder"></div>';
      return;
    }

    // Show Loading State
    aiAnswerEl.style.display = 'none';
    resultsEl.innerHTML = `
      <div class="bmm-search-placeholder">
        <p>⏳ Querying Agent Search API...</p>
      </div>
    `;

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      renderApiResults(data, query);
    } catch (err) {
      console.error('Agent Search Live API Error:', err);
      resultsEl.innerHTML = `
        <div class="bmm-no-results">
          <p>⚠️ Failed to reach Agent Search API (${escapeHTML(err.message)})</p>
        </div>
      `;
    }
  }

  function renderApiResults(data, query) {
    const aiAnswerEl = document.getElementById('bmm-ai-answer');
    const resultsEl = document.getElementById('bmm-search-results');

    // 1. Render Real Agent Search Generative Summary Answer
    const summaryText = data.summary?.summaryText;
    if (summaryText) {
      aiAnswerEl.style.display = 'block';
      aiAnswerEl.innerHTML = `
        <div class="ai-header">
          <span class="ai-sparkle">✨</span>
          <strong>AI Summary</strong>
        </div>
        <p class="ai-text">${escapeHTML(summaryText)}</p>
      `;
    } else {
      aiAnswerEl.style.display = 'none';
    }

    // 2. Render Real Discovery Engine Search Results
    const results = data.results || [];
    if (results.length === 0) {
      resultsEl.innerHTML = `
        <div class="bmm-no-results">
          <p>No results found for "<strong>${escapeHTML(query)}</strong>".</p>
        </div>
      `;
      return;
    }

    resultsEl.innerHTML = results.map(item => {
      const struct = item.document?.derivedStructData || {};
      const title = struct.title || item.document?.name || 'Untitled Article';
      const link = struct.link || '#';
      const snippets = struct.snippets || [];
      const snippetText = snippets.length > 0 ? snippets[0].snippet : (struct.pagemap?.metatags?.[0]?.['og:description'] || '');

      return `
        <a href="${escapeHTML(link)}" class="bmm-result-card">
          <div class="result-header">
            <span class="result-category">Agent Search Match</span>
          </div>
          <h4 class="result-title">${escapeHTML(title)}</h4>
          <p class="result-excerpt">${snippetText ? snippetText : 'Click to view story details.'}</p>
        </a>
      `;
    }).join('');
  }

  function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createModalDOM);
  } else {
    createModalDOM();
  }
})();
