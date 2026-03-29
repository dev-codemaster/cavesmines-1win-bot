const socket = io();
let grid = [];

socket.on('init', s => updateState(s));
socket.on('game', s => {updateState(s); renderGrid();});
socket.on('bet', b => document.getElementById('bet').textContent = b.amount.toFixed(2));
socket.on('cashout', s => updateState(s));
socket.on('safe', c => document.querySelector(`[data-r="${c.r}"][data-c="${c.c}"]`).classList.add('safe'));
socket.on('boom', c => {document.querySelector(`[data-r="${c.r}"][data-c="${c.c}"]`).classList.add('boom');});

function updateState(s) {
  document.getElementById('balance').textContent = s.balance.toFixed(2);
  document.getElementById('bet').textContent = s.bet.toFixed(2);
  document.getElementById('confidence').textContent = s.conf.toFixed(0)+'%';
  document.getElementById('histCount').textContent = s.history.length;
  grid = s.grid; renderHistory(s.history);
}

function renderGrid() {
  const g = document.getElementById('grid');
  g.innerHTML = '';
  for(let r=0;r<5;r++) for(let c=0;c<5;c++) {
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.dataset.r = r; cell.dataset.c = c;
    cell.onclick = () => socket.emit('click', {r,c});
    g.appendChild(cell);
  }
}

function placeBet() {
  const amt = parseFloat(document.getElementById('betInput').value);
  fetch('/api/bet', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({amount:amt})});
}

function cashout() { window.location.href = '/api/cashout'; }

function renderHistory(h) {
  document.getElementById('historyList').innerHTML = h.slice(-5).map(i => 
    `<div class="hist-item">ID: ${i.id.slice(-8)} <span style="color:#00ff88">+$${i.profit.toFixed(2)}</span></div>`
  ).join('');
}

renderGrid();
