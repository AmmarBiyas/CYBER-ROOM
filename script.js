// static/script.js
const socket = io();

// --- نظام اللعب الجماعي (Multiplayer) ---
socket.on('connect', () => {
    logToTerminal('متصل بسيرفر اللعب الجماعي.', 'success');
});

socket.on('match_notification', (data) => {
    logToTerminal(`[إشعار] ${data.message}`, 'info');
});

socket.on('node_under_attack', (data) => {
    logToTerminal(`[تحذير رادار] ${data.message}`, 'error');
});

function joinMatch() {
    const username = document.getElementById('username').value;
    const matchId = document.getElementById('match_id').value;
    const role = document.getElementById('role').value;
    
    if(!username || !matchId) {
        alert("يرجى إدخال اسم المستخدم ورقم الغرفة!");
        return;
    }
    socket.emit('join_match', { username: username, match_id: matchId, role: role });
    logToTerminal(`جاري الانضمام للغرفة ${matchId}...`, 'info');
}

function attackNode() {
    const username = document.getElementById('username').value;
    const matchId = document.getElementById('match_id').value;
    const nodeId = document.getElementById('target_node').value;
    
    if(!username || !matchId || !nodeId) {
        alert("تأكد من الانضمام لغرفة وإدخال اسم العقدة!");
        return;
    }
    socket.emit('attack_node', { username: username, match_id: matchId, node_id: nodeId });
    logToTerminal(`إطلاق هجوم على العقدة ${nodeId}...`, 'warning');
}

// --- نظام المتجر المصلح (Shop API) ---
function buyItem(itemKey) {
    const username = document.getElementById('username').value || "Guest";
    
    fetch('/api/buy_upgrade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, item_key: itemKey })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('credits_display').innerText = data.new_credits;
            logToTerminal(`✅ تمت الترقية بنجاح! المستوى الجديد: ${data.new_tier}`, 'success');
        } else {
            logToTerminal(`❌ فشل الشراء: ${data.message}`, 'error');
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        logToTerminal('خطأ في الاتصال بالخادم.', 'error');
    });
}

// --- واجهة الطرفية الوهمية (Terminal Logging) ---
function logToTerminal(message, type='info') {
    const term = document.getElementById('battle_log');
    const time = new Date().toLocaleTimeString();
    let colorClass = '';
    
    if(type === 'error') colorClass = 'error';
    if(type === 'warning') colorClass = 'highlight';
    
    term.innerHTML += `<div><span style="color:#888;">[${time}]</span> <span class="${colorClass}">${message}</span></div>`;
    term.scrollTop = term.scrollHeight;
}
