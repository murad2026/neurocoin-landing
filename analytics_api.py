import sqlite3
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = 'analytics.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id TEXT PRIMARY KEY,
            entry_period TEXT,
            recommended_amount REAL,
            predicted_accuracy REAL,
            actual_accuracy REAL,
            trend TEXT,
            safe_trade_window REAL,
            user_confirmations INTEGER,
            total_confirmed_amount REAL,
            timestamp TEXT
        )''')
        db.commit()

@app.route('/analytics', methods=['POST'])
def add_analytics():
    data = request.json
    entry_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    new_entry = (
        entry_id,
        data.get("entry_period"),
        data.get("recommended_amount"),
        data.get("predicted_accuracy"),
        data.get("actual_accuracy"),
        data.get("trend"),
        data.get("safe_trade_window"),
        data.get("user_confirmations"),
        data.get("total_confirmed_amount"),
        timestamp
    )

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO analytics (
            id, entry_period, recommended_amount, predicted_accuracy, actual_accuracy,
            trend, safe_trade_window, user_confirmations, total_confirmed_amount, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', new_entry)
    db.commit()

    return jsonify({
        "id": entry_id,
        "entry_period": data.get("entry_period"),
        "recommended_amount": data.get("recommended_amount"),
        "predicted_accuracy": data.get("predicted_accuracy"),
        "actual_accuracy": data.get("actual_accuracy"),
        "trend": data.get("trend"),
        "safe_trade_window": data.get("safe_trade_window"),
        "user_confirmations": data.get("user_confirmations"),
        "total_confirmed_amount": data.get("total_confirmed_amount"),
        "timestamp": timestamp
    }), 201

@app.route('/analytics', methods=['GET'])
def get_analytics():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM analytics')
    rows = cursor.fetchall()

    analytics = []
    for row in rows:
        analytics.append({
            "id": row[0],
            "entry_period": row[1],
            "recommended_amount": row[2],
            "predicted_accuracy": row[3],
            "actual_accuracy": row[4],
            "trend": row[5],
            "safe_trade_window": row[6],
            "user_confirmations": row[7],
            "total_confirmed_amount": row[8],
            "timestamp": row[9]
        })

    return jsonify(analytics), 200

@app.route('/analytics/<entry_id>', methods=['GET'])
def get_single_analytics(entry_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM analytics WHERE id = ?', (entry_id,))
    row = cursor.fetchone()
    if row:
        entry = {
            "id": row[0],
            "entry_period": row[1],
            "recommended_amount": row[2],
            "predicted_accuracy": row[3],
            "actual_accuracy": row[4],
            "trend": row[5],
            "safe_trade_window": row[6],
            "user_confirmations": row[7],
            "total_confirmed_amount": row[8],
            "timestamp": row[9]
        }
        return jsonify(entry), 200
    return jsonify({"error": "Entry not found"}), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
