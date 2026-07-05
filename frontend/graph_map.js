const state = {
  themeMode: localStorage.getItem('uiThemeMode') || 'default',
  preset: 'document-only',
  filter: 'all',
  nodes: [],
  edges: [],
};

function init() {
  bindEvents();
  applyTheme();
  loadGraph();
}

function bindEvents() {
  document.getElementById('themeToggle').addEventListener('click', toggleTheme);
  document.getElementById('presetSelect').addEventListener('change', (event) => {
    state.preset = event.target.value;
    renderGraph();
  });
  document.getElementById('filterSelect').addEventListener('change', (event) => {
    state.filter = event.target.value;
    renderGraph();
  });
}

function applyTheme() {
  document.body.classList.toggle('light', state.themeMode === 'light');
  document.body.classList.toggle('dark', state.themeMode === 'dark');
}

function toggleTheme() {
  const modes = ['default', 'light', 'dark'];
  const next = modes[(modes.indexOf(state.themeMode) + 1) % modes.length];
  state.themeMode = next;
  localStorage.setItem('uiThemeMode', next);
  applyTheme();
}

async function loadGraph() {
  try {
    const response = await fetch('/graph_map_data');
    const payload = await response.json();
    state.nodes = payload.nodes || [];
    state.edges = payload.edges || [];
    renderGraph();
  } catch (error) {
    state.nodes = [
      { id: 'doc-1', label: 'Policy Handbook', group: 'policy' },
      { id: 'doc-2', label: 'Review Workflow', group: 'concept' },
      { id: 'doc-3', label: 'Escalation Ladder', group: 'policy' },
    ];
    state.edges = [
      { from: 'doc-1', to: 'doc-2', type: 'depends_on' },
      { from: 'doc-2', to: 'doc-3', type: 'related_to' },
    ];
    renderGraph();
  }
}

function renderGraph() {
  const visibleNodes = state.nodes.filter((node) => state.filter === 'all' || node.group === state.filter);
  const visibleEdges = state.edges.filter((edge) => visibleNodes.some((node) => node.id === edge.from) && visibleNodes.some((node) => node.id === edge.to));
  const canvas = document.getElementById('graphCanvas');
  const width = 900;
  const height = 420;
  const nodePositions = {
    'doc-1': { x: 150, y: 180 },
    'doc-2': { x: 430, y: 120 },
    'doc-3': { x: 710, y: 220 },
  };

  const svg = `
    <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="${width}" height="${height}" rx="24" fill="transparent"></rect>
      ${visibleEdges.map((edge) => {
        const from = nodePositions[edge.from] || { x: 120, y: 120 };
        const to = nodePositions[edge.to] || { x: 300, y: 220 };
        return `<line x1="${from.x}" y1="${from.y}" x2="${to.x}" y2="${to.y}" stroke="#f59e0b" stroke-width="2" stroke-dasharray="6 4"></line>`;
      }).join('')}
      ${visibleNodes.map((node) => {
        const position = nodePositions[node.id] || { x: 140, y: 140 };
        const fill = node.group === 'policy' ? '#5eead4' : '#8b5cf6';
        return `
          <g>
            <circle cx="${position.x}" cy="${position.y}" r="38" fill="${fill}" opacity="0.9"></circle>
            <text x="${position.x}" y="${position.y + 6}" text-anchor="middle" fill="#07111f" font-size="13" font-weight="600">${node.label}</text>
          </g>
        `;
      }).join('')}
    </svg>
  `;

  canvas.innerHTML = svg;
  document.getElementById('statusText').textContent = `${state.preset} • ${state.filter} • ${visibleNodes.length} nodes`;
}

document.addEventListener('DOMContentLoaded', init);
