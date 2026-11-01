# app.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, emit
import sqlite3
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cyber_titan_secret_2026'
socketio = SocketIO(app, cors_allowed_origins="*")

# ==========================================
# 1. قاعدة البيانات (تم تحسين نظام الحفظ)
# ==========================================
def get_db_connection():
    conn = sqlite3.connect('cyber_web.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     username TEXT UNIQUE, credits INTEGER, xp INTEGER, upgrades TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 2. مسارات الموقع (Web Routes)
# ==========================================
@app.route('/')
def index():
    # الواجهة الرئيسية للموقع
    return render_template('index.html')

# ==========================================
# 3. إصلاح أخطاء المتجر (Shop API Fixes)
# ==========================================
HARDWARE_SHOP = {
    "cpu": {"base_cost": 150, "max_tier": 5},
    "firewall": {"base_cost": 150, "max_tier": 5},
    "ai_bot": {"base_cost": 250, "max_tier": 3}
}

@app.route('/api/buy_upgrade', methods=['POST'])
def buy_upgrade():
    data = request.json
    username = data.get('username')
    item_key = data.get('item_key')

    if item_key not in HARDWARE_SHOP:
        return jsonify({"status": "error", "message": "عنصر غير موجود!"}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if not user:
        return jsonify({"status": "error", "message": "المستخدم غير موجود!"}), 404

    upgrades = json.loads(user['upgrades']) if user['upgrades'] else {}
    current_tier = upgrades.get(item_key, 0)
    
    # إصلاح المشكلة 1: منع تجاوز الحد الأقصى للمستوى
    if current_tier >= HARDWARE_SHOP[item_key]['max_tier']:
        return jsonify({"status": "error", "message": "وصلت للحد الأقصى لهذا التطوير!"}), 400

    # إصلاح المشكلة 2: حساب التكلفة والتحقق الأمني في السيرفر وليس واجهة المستخدم
    cost = HARDWARE_SHOP[item_key]['base_cost'] * (current_tier + 1)
    
    if user['credits'] < cost:
        return jsonify({"status": "error", "message": "رصيدك غير كافٍ!"}), 400

    # تنفيذ عملية الشراء
    new_credits = user['credits'] - cost
    upgrades[item_key] = current_tier + 1
    
    conn.execute('UPDATE users SET credits = ?, upgrades = ? WHERE username = ?',
                 (new_credits, json.dumps(upgrades), username))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "new_credits": new_credits, "new_tier": upgrades[item_key]})

# ==========================================
# 4. نظام اللعب الجماعي (Multiplayer System)
# ==========================================
@socketio.on('join_match')
def handle_join(data):
    room = data['match_id']
    username = data['username']
    role = data['role'] # 'Red Team' أو 'Blue Team'
    
    join_room(room)
    # إرسال إشعار لجميع اللاعبين في نفس الغرفة
    emit('match_notification', {'message': f'{username} انضم كـ {role}!'}, room=room)

@socketio.on('attack_node')
def handle_attack(data):
    room = data['match_id']
    node_id = data['node_id']
    attacker = data['username']
    
    # إبلاغ الخصم في نفس اللحظة بالهجوم (Real-time synchronization)
    emit('node_under_attack', {
        'node_id': node_id,
        'attacker': attacker,
        'message': f'تحذير! العقدة {node_id} تتعرض لهجوم من {attacker}!'
    }, room=room)

if __name__ == '__main__':
    # تشغيل السيرفر مع دعم الـ WebSockets
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)