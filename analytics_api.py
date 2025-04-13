from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analytics.db'
db = SQLAlchemy(app)

class Analytics(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    entry_period = db.Column(db.String(50))
    recommended_amount = db.Column(db.Float)
    predicted_accuracy = db.Column(db.Float)
    actual_accuracy = db.Column(db.Float)
    trend = db.Column(db.String(20))
    safe_trade_window = db.Column(db.Float)
    user_confirmations = db.Column(db.Integer)
    total_confirmed_amount = db.Column(db.Float)
    timestamp = db.Column(db.String(50))

with app.app_context():
    db.create_all()

@app.route('/analytics', methods=['POST'])
def add_analytics():
    data = request.json
    new_entry = Analytics(
        id=str(uuid.uuid4()),
        entry_period=data.get("entry_period"),
        recommended_amount=data.get("recommended_amount"),
        predicted_accuracy=data.get("predicted_accuracy"),
        actual_accuracy=data.get("actual_accuracy"),
        trend=data.get("trend"),
        safe_trade_window=data.get("safe_trade_window"),
        user_confirmations=data.get("user_confirmations"),
        total_confirmed_amount=data.get("total_confirmed_amount"),
        timestamp=datetime.utcnow().isoformat()
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Created", "id": new_entry.id}), 201

@app.route('/analytics', methods=['GET'])
def get_analytics():
    entries = Analytics.query.all()
    return jsonify([{
        "id": entry.id,
        "entry_period": entry.entry_period,
        "recommended_amount": entry.recommended_amount,
        "predicted_accuracy": entry.predicted_accuracy,
        "actual_accuracy": entry.actual_accuracy,
        "trend": entry.trend,
        "safe_trade_window": entry.safe_trade_window,
        "user_confirmations": entry.user_confirmations,
        "total_confirmed_amount": entry.total_confirmed_amount,
        "timestamp": entry.timestamp
    } for entry in entries])

if __name__ == "__main__":
    app.run(debug=True)
