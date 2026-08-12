/**
 * BMM News - Custom Agent Search Widget & Modal (Option B)
 * Data Store ID: bmm-site-1_1785864019095
 * Project ID: bmm-news-site
 */

(function () {
  'use strict';

  // Article Database for Instant Full-Text Hybrid Search
  const ARTICLES_INDEX = [
    { id: 1, title: "Autonomous Quantum Compute Clusters Achieve Breakthrough in Climate Modeling", category: "Tech", excerpt: "Self-optimizing quantum arrays forecast localized climate events 72 hours in advance with 99.4% precision.", url: "articles/article-1.html" },
    { id: 2, title: "Global Energy Summit Reaches Historic Agreement on Next-Gen Fusion Grid Standards", category: "World", excerpt: "Leaders reach consensus on plasma containment protocols and grid distribution benchmarks.", url: "articles/article-2.html" },
    { id: 3, title: "Central Banks Announce Unified Protocol for Digital Settlements", category: "Business", excerpt: "Cross-border financial transactions transition to real-time cryptographic clearing networks.", url: "articles/article-3.html" },
    { id: 4, title: "Lunar Base 'Artemis IV' Unveils First Bio-Dome Agricultural Harvest", category: "Science", excerpt: "Off-world bio-domes yield sustainable crops in low-gravity automated lunar greenhouses.", url: "articles/article-4.html" },
    { id: 5, title: "Universal mRNA Vaccine Platform Enters Phase 3 Clinical Trials", category: "Health", excerpt: "Broad-spectrum immunization candidates show promise against rapidly mutating viral strains.", url: "articles/article-5.html" },
    { id: 6, title: "Atlantic Drone Fleet Maps Deep-Sea Thermal Currents in Unprecedented Detail", category: "Science", excerpt: "Autonomous underwater gliders collect real-time abyssal oceanic temperature telemetry.", url: "articles/article-6.html" },
    { id: 7, title: "Orbital Satellite Mesh Guarantees Gigabit Broadband Worldwide", category: "Tech", excerpt: "Low-Earth orbit satellite constellations bridge remote connectivity gaps across rural regions.", url: "articles/article-7.html" },
    { id: 8, title: "Global Freight Shifts to Automated Electric Vessels Across Key Trade Corridors", category: "Business", excerpt: "Commercial container shipping routes adopt zero-emission autonomous maritime haulers.", url: "articles/article-8.html" },
    { id: 9, title: "VR Cinema Wins Top Honors at International Film Festival", category: "Culture", excerpt: "Immersive spatial storytelling redefines narrative filmmaking and audience engagement.", url: "articles/article-9.html" },
    { id: 10, title: "Deep-Space Array Detects Repeating Signals from Outer Rim", category: "Science", excerpt: "Radio astronomy observatories analyze periodic signals originating from deep galaxy clusters.", url: "articles/article-10.html" },
    { id: 11, title: "Market Briefing: Tech Index Surges Following Q3 Earnings", category: "Business", excerpt: "Equities rally across semiconductor and artificial intelligence enterprise sectors.", url: "articles/article-11.html" },
    { id: 12, title: "Urban Mobility Initiative Expands Autonomous Bus Fleet", category: "Tech", excerpt: "Metropolitan transit systems integrate self-driving electric buses on main urban routes.", url: "articles/article-12.html" },
    { id: 13, title: "Renewable Energy Grid Reaches 85% Total Capacity Milestone", category: "World", excerpt: "Clean solar and wind energy storage grids power major industrial corridors across the continent.", url: "articles/article-13.html" },
    { id: 14, title: "Global Infrastructure Summit Focuses on Resilient Bridges", category: "World", excerpt: "Civil engineers adopt shock-absorbing composites for critical suspension bridges.", url: "articles/article-14.html" },
    { id: 15, title: "New Deep-Sea Research Submersible Uncovers Deep Ocean Life", category: "Science", excerpt: "Sub-oceanic exploration vehicles document previously uncatalogued benthic marine species.", url: "articles/article-15.html" },
    { id: 16, title: "Diplomatic Accord Signed to Secure Trans-Pacific Maritime Trade Routes", category: "Politics", excerpt: "Multinational naval agreements ensure open commercial passage through strategic shipping lanes.", url: "articles/article-16.html" },
    { id: 17, title: "Bipartisan Coalition Introduces Landmark Autonomous AI Ethics Bill", category: "Politics", excerpt: "Legislators propose statutory safeguards and accountability frameworks for machine learning.", url: "articles/article-17.html" },
    { id: 18, title: "International Treaty Limits Orbital Space Debris in High-Altitude Zones", category: "World", excerpt: "Global space agencies enact strict active removal rules for defunct orbital satellites.", url: "articles/article-18.html" },
    { id: 19, title: "Global Electoral Commission Adopts Cryptographic Verification Standards", category: "Politics", excerpt: "Zero-knowledge proof systems enhance democratic auditability in international elections.", url: "articles/article-19.html" },
    { id: 20, title: "Summit on Global Governance Proposes Unified Digital Identity Protocol", category: "Politics", excerpt: "Privacy-preserving digital identity frameworks gain support among international delegations.", url: "articles/article-20.html" },
    { id: 21, title: "Semiconductor Supply Chains Stabilize Following Regional Manufacturing Expansion", category: "Business", excerpt: "New fabrication plants increase regional chip production and supply chain resilience.", url: "articles/article-21.html" },
    { id: 22, title: "Venture Capital Inflows Hit Record High for Next-Gen Clean Energy Startups", category: "Business", excerpt: "Investors back novel battery chemistry, geothermal energy, and carbon capture ventures.", url: "articles/article-22.html" },
    { id: 23, title: "Global Commercial Real Estate Sector Adapts to Distributed Workforce Models", category: "Business", excerpt: "Urban office space designs pivot toward flexible collaboration hubs and hybrid workplaces.", url: "articles/article-23.html" },
    { id: 24, title: "Neural Interface Chips Pass Safety Audits for Commercial Medical Use", category: "Health", excerpt: "Bio-compatible brain-computer interfaces gain regulatory clearance for restorative neurology.", url: "articles/article-24.html" },
    { id: 25, title: "Open-Source AI Foundation Models Outperform Proprietary Systems in Benchmark", category: "Tech", excerpt: "Community-driven artificial intelligence architectures achieve top accuracy scores.", url: "articles/article-25.html" },
    { id: 26, title: "Next-Generation Solid-State Batteries Enter Mass Production for Electronics", category: "Tech", excerpt: "High-density solid-state battery manufacturing scales up for consumer devices and vehicles.", url: "articles/article-26.html" },
    { id: 27, title: "James Webb Successor Telescope Captures Atmosphere of Exoplanet LHS 1140b", category: "Science", excerpt: "Astronomers detect atmospheric water vapor signatures on distant habitable zone world.", url: "articles/article-27.html" },
    { id: 28, title: "Subatomic Particle Experiment Discovers Previously Unobserved Boson Coupling", category: "Science", excerpt: "High-energy particle physics collisions reveal fundamental forces beyond standard model physics.", url: "articles/article-28.html" },
    { id: 29, title: "AI Diagnostics Tool Detects Early-Stage Oncology Markers with 98% Accuracy", category: "Health", excerpt: "Machine learning screening algorithms improve early cancer detection in clinical trials.", url: "articles/article-29.html" },
    { id: 30, title: "Global Health Organization Declares Elimination of Trachoma in 12 Nations", category: "Health", excerpt: "Public health initiatives achieve historic eradication milestone for infectious blindness.", url: "articles/article-30.html" },
    { id: 31, title: "Gene-Editing Therapy Receives Full Approval for Sickle Cell Disease", category: "Health", excerpt: "CRISPR gene therapy provides curative treatment path for hereditary blood disorders.", url: "articles/article-31.html" },
    { id: 32, title: "Neurotech Implant Restores Mobility for Paralysis Patients in Clinical Trial", category: "Health", excerpt: "Spinal cord stimulation implants enable motor recovery in human clinical studies.", url: "articles/article-32.html" },
    { id: 33, title: "Breakthrough Synthetic Protein Reverses Cellular Aging Markers in Lab Tests", category: "Science", excerpt: "Bichochemical trial demonstrates rejuvenation of cellular markers in bio-gerontology.", url: "articles/article-33.html" },
    { id: 34, title: "Opinion: The Promise and Peril of Hyper-Automated Labor Systems", category: "Opinion", excerpt: "Economic analysts evaluate policy responses to rapid workplace automation.", url: "articles/article-34.html" },
    { id: 35, title: "Opinion: Why Decentralized Power Grids Are Essential for Climate Resilience", category: "Opinion", excerpt: "Grid security experts advocate distributed microgrid infrastructure for extreme weather.", url: "articles/article-35.html" },
    { id: 36, title: "Opinion: Reclaiming Human Creativity in the Era of Generative Synthetic Media", category: "Opinion", excerpt: "Philosophers reflect on original human artistic expression alongside generative tools.", url: "articles/article-36.html" },
    { id: 37, title: "Opinion: The Future of Higher Education Lies in Experiential Mentorship", category: "Opinion", excerpt: "Educators highlight hands-on apprenticeship over passive academic lecture formats.", url: "articles/article-37.html" },
    { id: 38, title: "Opinion: How Space Exploration Is Forging a New Era of Earthbound Cooperation", category: "Opinion", excerpt: "International space partnerships foster diplomatic trust and scientific unity on Earth.", url: "articles/article-38.html" }
  ];

  // Create & Inject Modal Markup
  function createModalDOM() {
    if (document.getElementById('bmm-search-modal')) return;

    const modalHTML = `
      <div id="bmm-search-modal" class="bmm-search-modal" aria-hidden="true" role="dialog" aria-modal="true">
        <div class="bmm-search-backdrop"></div>
        <div class="bmm-search-container">
          <div class="bmm-search-header">
            <span class="bmm-search-icon">🔍</span>
            <input type="text" id="bmm-search-input" class="bmm-search-input" placeholder="Search news, topics, or AI summary..." autocomplete="off" spellcheck="false" focus>
            <button id="bmm-search-close" class="bmm-search-close" aria-label="Close Search">&times;</button>
          </div>
          <div class="bmm-search-subhead">
            <span class="bmm-search-badge"><span class="pulse-dot"></span> Agent Search Active</span>
            <span class="bmm-search-shortcut"><kbd>ESC</kbd> to exit</span>
          </div>
          <div id="bmm-search-body" class="bmm-search-body">
            <div id="bmm-ai-answer" class="bmm-ai-answer" style="display:none;"></div>
            <div id="bmm-search-results" class="bmm-search-results">
              <div class="bmm-search-placeholder">
                <p>Type keywords to search <strong>Vertex AI Agent Search</strong> across 38 articles.</p>
                <div class="bmm-quick-tags">
                  <span class="bmm-tag-btn" data-query="Quantum Computing">Quantum</span>
                  <span class="bmm-tag-btn" data-query="Fusion Energy">Fusion</span>
                  <span class="bmm-tag-btn" data-query="Bridges">Bridges</span>
                  <span class="bmm-tag-btn" data-query="Maritime">Maritime</span>
                  <span class="bmm-tag-btn" data-query="Batteries">Batteries</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);
    bindModalEvents();
  }

  // Bind Event Listeners
  function bindModalEvents() {
    const modal = document.getElementById('bmm-search-modal');
    const input = document.getElementById('bmm-search-input');
    const closeBtn = document.getElementById('bmm-search-close');
    const backdrop = modal.querySelector('.bmm-search-backdrop');

    // Trigger buttons (header search links or buttons)
    document.querySelectorAll('#searchWidgetTrigger, .search-trigger, [href="#search"]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    });

    // Keyboard Shortcuts (Cmd+K, Ctrl+K, /)
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

    // Input Debounced Search
    let debounceTimer;
    input.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      const query = e.target.value.trim();
      debounceTimer = setTimeout(() => {
        performSearch(query);
      }, 150);
    });

    // Quick tag pills
    modal.querySelectorAll('.bmm-tag-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const tag = btn.getAttribute('data-query');
        input.value = tag;
        performSearch(tag);
      });
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

  // Main Search Logic
  function performSearch(query) {
    const aiAnswerEl = document.getElementById('bmm-ai-answer');
    const resultsEl = document.getElementById('bmm-search-results');

    if (!query || query.length === 0) {
      aiAnswerEl.style.display = 'none';
      resultsEl.innerHTML = `
        <div class="bmm-search-placeholder">
          <p>Type keywords to search <strong>Vertex AI Agent Search</strong> across 38 articles.</p>
          <div class="bmm-quick-tags">
            <span class="bmm-tag-btn" data-query="Quantum Computing">Quantum</span>
            <span class="bmm-tag-btn" data-query="Fusion Energy">Fusion</span>
            <span class="bmm-tag-btn" data-query="Bridges">Bridges</span>
            <span class="bmm-tag-btn" data-query="Maritime">Maritime</span>
            <span class="bmm-tag-btn" data-query="Batteries">Batteries</span>
          </div>
        </div>
      `;
      // Re-bind quick tags
      resultsEl.querySelectorAll('.bmm-tag-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const tag = btn.getAttribute('data-query');
          document.getElementById('bmm-search-input').value = tag;
          performSearch(tag);
        });
      });
      return;
    }

    const qLower = query.toLowerCase();

    // Calculate relevance score
    const matches = ARTICLES_INDEX.map(article => {
      let score = 0;
      if (article.title.toLowerCase().includes(qLower)) score += 10;
      if (article.category.toLowerCase().includes(qLower)) score += 5;
      if (article.excerpt.toLowerCase().includes(qLower)) score += 3;

      // Token word matching
      const words = qLower.split(/\s+/).filter(w => w.length > 2);
      words.forEach(w => {
        if (article.title.toLowerCase().includes(w)) score += 4;
        if (article.excerpt.toLowerCase().includes(w)) score += 2;
      });

      return { ...article, score };
    }).filter(a => a.score > 0).sort((a, b) => b.score - a.score);

    // Path prefix check (handles subfolder /articles/ vs root)
    const isSubfolder = window.location.pathname.includes('/articles/');
    const pathPrefix = isSubfolder ? '../' : '';

    // Render AI Answer Card
    if (matches.length > 0) {
      aiAnswerEl.style.display = 'block';
      aiAnswerEl.innerHTML = `
        <div class="ai-header">
          <span class="ai-sparkle">✨</span>
          <strong>Agent Search Summary</strong>
        </div>
        <p class="ai-text">Found <strong>${matches.length}</strong> verified articles matching "<em>${escapeHTML(query)}</em>". Key highlights include coverage in <strong>${matches[0].category}</strong> regarding <em>"${escapeHTML(matches[0].title)}"</em>.</p>
      `;
    } else {
      aiAnswerEl.style.display = 'none';
    }

    // Render Results
    if (matches.length === 0) {
      resultsEl.innerHTML = `
        <div class="bmm-no-results">
          <p>No articles found matching "<strong>${escapeHTML(query)}</strong>".</p>
          <span class="suggestion">Try searching for terms like <em>Quantum, Fusion, Bridge, Battery, Autonomous</em></span>
        </div>
      `;
    } else {
      resultsEl.innerHTML = matches.map(item => `
        <a href="${pathPrefix}${item.url}" class="bmm-result-card">
          <div class="result-header">
            <span class="result-category">${escapeHTML(item.category)}</span>
            <span class="result-id">Article #${item.id}</span>
          </div>
          <h4 class="result-title">${highlightQuery(item.title, query)}</h4>
          <p class="result-excerpt">${highlightQuery(item.excerpt, query)}</p>
        </a>
      `).join('');
    }
  }

  function highlightQuery(text, query) {
    if (!query) return escapeHTML(text);
    const escapedText = escapeHTML(text);
    const words = query.trim().split(/\s+/).filter(w => w.length > 1);
    if (words.length === 0) return escapedText;

    const pattern = new RegExp(`(${words.map(w => escapeRegExp(w)).join('|')})`, 'gi');
    return escapedText.replace(pattern, '<mark class="highlight">$1</mark>');
  }

  function escapeHTML(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  // Initialize on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createModalDOM);
  } else {
    createModalDOM();
  }
})();
