# =========================================
# path: app.py
# =========================================
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from db_config import get_db_connection  # stellt Verbindung zu deiner budget_tracker-DB her
from typing import Tuple, Any

app = Flask(__name__)
app.secret_key = "CHANGE_ME"  # TODO: per ENV setzen

# ---------------- Helpers ----------------
def require_login():
    if 'user_id' not in session:
        return jsonify({"message": "Please login first"}), 401
    return None

def run_query(sql: str, params: Tuple[Any, ...] = (), fetch: bool = False, one: bool = False):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = None
    if fetch:
        rows = cur.fetchone() if one else cur.fetchall()
    conn.commit()
    conn.close()
    return rows if fetch else cur.lastrowid

# --------------- API: Auth ----------------
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json(force=True)
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()
    if not username or not password:
        return jsonify({"message": "username/password required"}), 400
    try:
        hashed = generate_password_hash(password)
        run_query('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed))
        return jsonify({"message": "User registered successfully!"}), 201
    except Error as e:
        return jsonify({"message": "Registration failed", "detail": str(e)}), 400  # :contentReference[oaicite:5]{index=5}

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(force=True)
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()
    row = run_query('SELECT id, username, password FROM users WHERE username=%s', (username,), fetch=True, one=True)
    if row and check_password_hash(row[2], password):
        session['user_id'] = row[0]
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials"}), 401  # :contentReference[oaicite:6]{index=6}

# ----------- API: Categories --------------
@app.route('/api/categories', methods=['GET'])
def list_categories():
    if (resp := require_login()) is not None: return resp
    uid = session['user_id']
    rows = run_query('SELECT id,name,color FROM categories WHERE user_id=%s ORDER BY name', (uid,), fetch=True)
    return jsonify([{"id": r[0], "name": r[1], "color": r[2]} for r in rows])

@app.route('/api/categories', methods=['POST'])
def add_category():
    if (resp := require_login()) is not None: return resp
    uid = session['user_id']
    data = request.get_json(force=True)
    name = (data.get('name') or '').strip()
    color = (data.get('color') or '#999999').strip()
    if not name:
        return jsonify({"message": "Name required"}), 400
    try:
        cat_id = run_query('INSERT INTO categories (user_id,name,color) VALUES (%s,%s,%s)', (uid, name, color))
        return jsonify({"id": cat_id, "name": name, "color": color}), 201
    except Error as e:
        return jsonify({"message": "Could not add category", "detail": str(e)}), 400

@app.route('/api/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id: int):
    if (resp := require_login()) is not None: return resp
    uid = session['user_id']
    # Kategorie entkoppeln und löschen
    run_query('UPDATE transactions SET category_id=NULL WHERE user_id=%s AND category_id=%s', (uid, cat_id))
    run_query('DELETE FROM categories WHERE user_id=%s AND id=%s', (uid, cat_id))
    return jsonify({"message": "Category deleted"})

# ----------- API: Transactions ------------
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    if (resp := require_login()) is not None: return resp
    uid = session['user_id']
    rows = run_query(
        '''
        SELECT t.id, t.amount, t.type, t.description, t.date, t.category_id, c.name, c.color
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.user_id=%s
        ORDER BY t.date DESC, t.id DESC
        ''', (uid,), fetch=True
    )
    return jsonify([{
        "id": r[0],
        "amount": float(r[1]),
        "type": r[2],
        "description": r[3],
        "date": r[4].isoformat() if hasattr(r[4], 'isoformat') else str(r[4]),
        "category_id": r[5],
        "category_name": r[6],
        "category_color": r[7],
    } for r in rows]), 200  # :contentReference[oaicite:7]{index=7}

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    if (resp := require_login()) is not None: return resp
    uid = session['user_id']
    data = request.get_json(force=True)

    try:
        amount = float(data.get('amount'))
    except Exception:
        return jsonify({"message": "Invalid amount"}), 400
    if amount <= 0:
        return jsonify({"message": "Amount must be > 0"}), 400

    type_ = data.get('type')
    if type_ not in ('income', 'expense'):
        return jsonify({"message": "type must be income/expense"}), 400

    description = (data.get('description') or '').strip()
    cat_id = data.get('category_id')
    date_str = (data.get('date') or '').strip()
    tx_date = datetime.utcnow()
    if date_str:
        try:
            tx_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except Exception:
            return jsonify({"message": "date must be ISO-8601"}), 400

    if cat_id is not None:
        owns = run_query('SELECT 1 FROM categories WHERE id=%s AND user_id=%s', (cat_id, uid), fetch=True, one=True)
        if not owns:
            return jsonify({"message": "Category not found"}), 404

    run_query(
        'INSERT INTO transactions (user_id, amount, type, description, date, category_id) VALUES (%s,%s,%s,%s,%s,%s)',
        (uid, amount, type_, description, tx_date, cat_id)
    )
    return jsonify({"message": "Transaction added successfully!"}), 201  # :contentReference[oaicite:8]{index=8}

@app.route('/api/transactions/<int:tx_id>', methods=['DELETE'])
def delete_transaction(tx_id: int):
    if (resp := require_login()) is not None: return resp
    uid = session['user_id']
    run_query('DELETE FROM transactions WHERE id=%s AND user_id=%s', (tx_id, uid))
    return jsonify({"message": "Transaction deleted"})

# --------------- API: Summary -------------
@app.route('/api/summary', methods=['GET'])
def summary():
    if (resp := require_login()) is not None: return resp
    uid = session['user_id']

    rows_month = run_query(
        """
        SELECT DATE_FORMAT(date,'%Y-%m') as ym,
               SUM(CASE WHEN type='income' THEN amount ELSE 0 END) as income,
               SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) as expense
        FROM transactions
        WHERE user_id=%s
        GROUP BY ym
        ORDER BY ym
        """, (uid,), fetch=True
    )
    by_month = [{"month": r[0], "income": float(r[1] or 0), "expense": float(r[2] or 0)} for r in rows_month]

    rows_cat = run_query(
        """
        SELECT COALESCE(c.name,'—') as name, COALESCE(c.color,'#999999') as color,
               SUM(CASE WHEN t.type='income' THEN t.amount ELSE 0 END) as income,
               SUM(CASE WHEN t.type='expense' THEN t.amount ELSE 0 END) as expense
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.user_id=%s
        GROUP BY name,color
        ORDER BY name
        """, (uid,), fetch=True
    )
    by_category = [{"name": r[0], "color": r[1], "income": float(r[2] or 0), "expense": float(r[3] or 0)} for r in rows_cat]
    return jsonify({"by_month": by_month, "by_category": by_category})

# ---------------- Pages -------------------
@app.route('/')
def index():  # für index.html (url_for('register')/('login')) :contentReference[oaicite:9]{index=9}
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():  # Template postet an url_for('login') :contentReference[oaicite:10]{index=10}
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()
        row = run_query('SELECT id, username, password FROM users WHERE username=%s', (username,), fetch=True, one=True)
        if row and check_password_hash(row[2], password):
            session['user_id'] = row[0]
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Ungültige Anmeldedaten")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():  # Links zeigen auf url_for('register') :contentReference[oaicite:11]{index=11}
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()
        if not username or not password:
            return render_template('register.html', error="Felder sind erforderlich")
        try:
            hashed = generate_password_hash(password)
            run_query('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed))
            return redirect(url_for('login'))
        except Error:
            return render_template('register.html', error="Benutzer existiert bereits?")
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')  # nutzt die Fetch-APIs + Charts :contentReference[oaicite:12]{index=12}

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

