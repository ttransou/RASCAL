const state = {
  activeView: 'chat',
  activeCategory: 'all',
  searchQuery: '',
  wikiDocs: [],
  faqData: null,
  themeMode: localStorage.getItem('uiThemeMode') || 'default',
  messages: [],
  currentTrace: null,
};

const categoryOrder = ['all', 'policy', 'concept', 'primary-source'];

function init() {
  bindEvents();
  applyTheme();
  loadHealth();
  loadWikiIndex();
  loadFaq();
  renderConversation();
}

function bindEvents() {
  document.getElementById('askForm').addEventListener('submit', handleAskSubmit);
  document.getElementById('themeToggle').addEventListener('click', toggleTheme);
  document.getElementById('searchInput').addEventListener('input', (event) => {
    state.searchQuery = event.target.value.trim().toLowerCase();
    renderCatalog();
  });
  document.querySelectorAll('[data-view]').forEach((button) => {
    button.addEventListener('click', () => switchView(button.dataset.view));
  });
  document.getElementById('closeModal').addEventListener('click', closeModal);
  document.getElementById('wikiModal').addEventListener('click', (event) => {
    if (event.target.id === 'wikiModal') closeModal();
  });
  document.getElementById('conversation').addEventListener('click', handleMessageActions);
  document.getElementById('catalogList').addEventListener('click', handleCatalogClick);
}

function applyTheme() {
  document.body.classList.toggle('light', state.themeMode === 'light');
  document.body.classList.toggle('dark', state.themeMode === 'dark');
  const label = state.themeMode === 'default' ? '🌓 Theme' : state.themeMode === 'light' ? '☀️ Theme' : '🌙 Theme';
  document.getElementById('themeToggle').textContent = label;
}

function toggleTheme() {
  const modes = ['default', 'light', 'dark'];
  const next = modes[(modes.indexOf(state.themeMode) + 1) % modes.length];
  state.themeMode = next;
  localStorage.setItem('uiThemeMode', next);
  applyTheme();
}

function switchView(view) {
  state.activeView = view;
  document.querySelectorAll('.view-pane').forEach((pane) => pane.classList.add('hidden'));
  document.querySelectorAll('.tab-btn, .nav-btn').forEach((button) => button.classList.toggle('active', button.dataset.view === view));
  document.getElementById(`${view}View`).classList.remove('hidden');
}

async function loadHealth() {
  try {
    const response = await fetch('/health');
    const payload = await response.json();
    document.getElementById('healthPill').textContent = payload.status || 'healthy';
    document.getElementById('healthPill').className = `pill ${payload.status === 'healthy' ? 'healthy' : 'warning'}`;
    document.getElementById('healthSummary').textContent = payload.summary || 'The current local shell is live.';
    document.getElementById('modeBadge').textContent = `mode: ${payload.mode || 'local'}`;
    document.getElementById('groundingBadge').textContent = `grounding: ${payload.grounding || 'wiki-first'}`;
  } catch (error) {
    document.getElementById('healthPill').textContent = 'offline';
    document.getElementById('healthPill').className = 'pill warning';
    document.getElementById('healthSummary').textContent = 'The local API is unavailable. Refresh after the server starts.';
  }
}

async function loadWikiIndex() {
  try {
    const response = await fetch('/wiki_index');
    const payload = await response.json();
    state.wikiDocs = payload.documents || [];
    renderCategoryFilters();
    renderCatalog();
  } catch (error) {
    state.wikiDocs = [];
    renderCatalog();
  }
}

async function loadFaq() {
  try {
    const response = await fetch('/faq.json');
    const payload = await response.json();
    state.faqData = payload;
    renderFaq();
  } catch (error) {
    state.faqData = { sections: [] };
    renderFaq();
  }
}

async function handleAskSubmit(event) {
  event.preventDefault();
  const input = document.getElementById('questionInput');
  const question = input.value.trim();
  if (!question) return;

  state.messages.push({ role: 'user', text: question, id: crypto.randomUUID() });
  renderConversation();
  input.value = '';

  try {
    const response = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    const payload = await response.json();
    const assistantMessage = {
      role: 'assistant',
      text: payload.answer || 'No answer was returned.',
      id: crypto.randomUUID(),
      trace: payload.trace || null,
      citations: payload.citations || [],
    };
    state.messages.push(assistantMessage);
    state.currentTrace = assistantMessage.trace;
    renderConversation();
    renderTrace();
  } catch (error) {
    state.messages.push({ role: 'assistant', text: 'The assistant could not reach the local API. Please verify the server.', id: crypto.randomUUID() });
    renderConversation();
  }
}

function renderConversation() {
  const container = document.getElementById('conversation');
  if (!state.messages.length) {
    container.innerHTML = '<p class="empty-state">Start with a question to see an answer, citations, and traceability.</p>';
    return;
  }

  container.innerHTML = state.messages.map((message) => {
    const bubble = message.role === 'assistant' ? renderMarkdown(message.text) : escapeHtml(message.text);
    return `
      <article class="message ${message.role}">
        <div class="message-bubble">
          <div class="message-meta">${message.role === 'assistant' ? 'Assistant' : 'You'}</div>
          <div>${bubble}</div>
          ${message.role === 'assistant' ? `
            <div class="feedback-row">
              <button class="feedback-btn good" type="button" data-action="feedback" data-rating="up" data-id="${message.id}">👍 Helpful</button>
              <button class="feedback-btn bad" type="button" data-action="feedback" data-rating="down" data-id="${message.id}">👎 Needs work</button>
              <button class="feedback-btn" type="button" data-action="save" data-id="${message.id}">📝 Save to wiki</button>
            </div>` : ''}
        </div>
      </article>`;
  }).join('');
}

function handleMessageActions(event) {
  const button = event.target.closest('button[data-action]');
  if (!button) return;
  const action = button.dataset.action;
  const message = state.messages.find((entry) => entry.id === button.dataset.id);
  if (!message) return;

  if (action === 'feedback') {
    sendFeedback(button.dataset.rating, message);
  } else if (action === 'save') {
    saveToWiki(message);
  }
}

async function sendFeedback(rating, message) {
  try {
    await fetch('/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rating, question: message.text, cited_docs: state.currentTrace?.retrieved_docs || [] }),
    });
    message.feedbackSent = true;
    renderConversation();
  } catch (error) {
    console.error(error);
  }
}

async function saveToWiki(message) {
  try {
    const response = await fetch('/wiki', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: `Analysis: ${message.text.slice(0, 48)}`, content: message.text }),
    });
    const payload = await response.json();
    alert(payload.message || 'Saved to wiki.');
  } catch (error) {
    console.error(error);
  }
}

function renderTrace() {
  const container = document.getElementById('traceContent');
  if (!state.currentTrace) {
    container.innerHTML = '<p class="empty-state">Ask a question to inspect retrieved wiki chunks, scores, and citations.</p>';
    return;
  }

  const cards = (state.currentTrace.retrieved_docs || []).map((doc) => `
    <article class="trace-card">
      <h4>${escapeHtml(doc.title || doc.doc_id || 'Wiki evidence')}</h4>
      <div class="meta">
        <span>${escapeHtml(doc.type || 'document')}</span>
        <span>${escapeHtml(doc.doc_id || '')}</span>
        <span>score ${Number(doc.combined_score || doc.score || 0).toFixed(2)}</span>
      </div>
      <p class="excerpt">${escapeHtml(doc.excerpt || doc.summary || 'No excerpt provided yet.')}</p>
    </article>
  `).join('');

  const citations = (state.currentTrace.citations || []).map((citation) => `
    <article class="trace-card">
      <h4>${escapeHtml(citation.doc_id || citation.source_file || 'Citation')}</h4>
      <div class="meta">
        <span>${escapeHtml(citation.type || 'source')}</span>
        <span>${escapeHtml(citation.confidence || 'medium')}</span>
      </div>
      <p class="excerpt">${renderCitationSource(citation)}</p>
    </article>
  `).join('');

  container.innerHTML = `
    <div class="trace-card">
      <h4>Answer summary</h4>
      <p>${escapeHtml(state.currentTrace.summary || 'The response used curated wiki evidence and traceable citations.')}</p>
    </div>
    ${cards}
    ${citations}
  `;
}

function renderCategoryFilters() {
  const container = document.getElementById('categoryFilters');
  const categories = ['all', ...new Set(state.wikiDocs.map((doc) => normalizeCategory(doc.category)))].filter(Boolean);
  container.innerHTML = categories.map((category) => `
    <button class="category-chip ${state.activeCategory === category ? 'active' : ''}" type="button" data-category="${category}">${labelForCategory(category)}</button>
  `).join('');
  container.querySelectorAll('[data-category]').forEach((button) => {
    button.addEventListener('click', () => {
      state.activeCategory = button.dataset.category;
      renderCategoryFilters();
      renderCatalog();
    });
  });
}

function renderCatalog() {
  const container = document.getElementById('catalogList');
  const docs = state.wikiDocs.filter((doc) => {
    const categoryMatches = state.activeCategory === 'all' || normalizeCategory(doc.category) === state.activeCategory;
    const searchMatches = !state.searchQuery || [doc.title, doc.type, doc.summary, doc.key_points?.join(' ')].join(' ').toLowerCase().includes(state.searchQuery);
    return categoryMatches && searchMatches;
  });

  if (!docs.length) {
    container.innerHTML = '<p class="empty-state">Nothing matches the current filters yet.</p>';
    return;
  }

  container.innerHTML = docs.map((doc) => `
    <button class="catalog-item" type="button" data-doc-id="${doc.id}">
      <span>
        <strong>${escapeHtml(doc.title)}</strong>
        <span class="muted">${escapeHtml(doc.type || 'document')} • ${escapeHtml(doc.summary || 'Curated wiki content')}</span>
      </span>
      <span class="pill">${escapeHtml(labelForCategory(normalizeCategory(doc.category)))}</span>
    </button>
  `).join('');
}

function handleCatalogClick(event) {
  const button = event.target.closest('button[data-doc-id]');
  if (!button) return;
  const doc = state.wikiDocs.find((entry) => entry.id === button.dataset.docId);
  if (!doc) return;
  openWikiModal(doc);
}

async function openWikiModal(doc) {
  try {
    const response = await fetch(`/wiki/${doc.id}`);
    const payload = await response.json();
    document.getElementById('wikiModalContent').innerHTML = `
      <h3>${escapeHtml(payload.title || doc.title)}</h3>
      <p class="muted">${escapeHtml(payload.summary || doc.summary || '')}</p>
      <pre>${escapeHtml(payload.content || 'No detailed content is available yet.')}</pre>
    `;
  } catch (error) {
    document.getElementById('wikiModalContent').innerHTML = `
      <h3>${escapeHtml(doc.title)}</h3>
      <p class="muted">${escapeHtml(doc.summary || '')}</p>
      <pre>${escapeHtml('Preview content is not available in the local scaffold yet.')}</pre>
    `;
  }
  document.getElementById('wikiModal').classList.remove('hidden');
  document.getElementById('wikiModal').setAttribute('aria-hidden', 'false');
}

function closeModal() {
  document.getElementById('wikiModal').classList.add('hidden');
  document.getElementById('wikiModal').setAttribute('aria-hidden', 'true');
}

function renderFaq() {
  const container = document.getElementById('faqContent');
  if (!state.faqData?.sections?.length) {
    container.innerHTML = '<p class="empty-state">The FAQ content is still being staged.</p>';
    return;
  }

  container.innerHTML = state.faqData.sections.map((section) => `
    <section class="faq-section">
      <h3>${escapeHtml(section.title)}</h3>
      ${(section.entries || []).map((entry) => `
        <div class="faq-entry">
          <strong>${escapeHtml(entry.question)}</strong>
          <span>${escapeHtml(entry.answer)}</span>
        </div>
      `).join('')}
    </section>
  `).join('');
}

function normalizeCategory(category) {
  if (!category) return 'concept';
  const lowered = category.toLowerCase();
  if (lowered.includes('policy')) return 'policy';
  if (lowered.includes('source') || lowered.includes('reference')) return 'primary-source';
  return 'concept';
}

function labelForCategory(category) {
  const labels = {
    all: 'All',
    policy: 'Policies',
    concept: 'Concepts',
    'primary-source': 'Primary Sources',
  };
  return labels[category] || category;
}

function renderCitationSource(citation) {
  if (citation.source_url && /^https?:\/\//i.test(citation.source_url)) {
    return `<a href="${escapeHtml(citation.source_url)}" target="_blank" rel="noreferrer">Source document</a>`;
  }
  return escapeHtml(citation.source_file || 'Internal wiki citation');
}

function renderMarkdown(text) {
  return text
    .split('\n\n')
    .map((block) => {
      if (/^###\s/.test(block)) return `<h3>${escapeHtml(block.replace(/^###\s/, ''))}</h3>`;
      if (/^##\s/.test(block)) return `<h2>${escapeHtml(block.replace(/^##\s/, ''))}</h2>`;
      if (/^[-*]\s/.test(block)) {
        const items = block.split('\n').map((line) => `<li>${escapeHtml(line.replace(/^[-*]\s/, ''))}</li>`).join('');
        return `<ul>${items}</ul>`;
      }
      return `<p>${escapeHtml(block)}</p>`;
    })
    .join('');
}

function escapeHtml(text) {
  return String(text)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

document.addEventListener('DOMContentLoaded', init);
