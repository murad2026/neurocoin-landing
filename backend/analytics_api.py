from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

analytics_db = []

@app.route('/analytics', methods=['POST'])
def add_analytics():
    data = request.json

    required_fields = [
        "entry_period", "recommended_amount", "predicted_accuracy",
        "actual_accuracy", "trend", "safe_trade_window",
        "user_confirmations", "total_confirmed_amount"
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

   new_entry = {
    "id": str(uuid.uuid4()),
    "currency": data.get("currency"),
    "entry_period": data.get("entry_period"),
    "recommended_amount": data.get("recommended_amount"),
    "predicted_accuracy": data.get("predicted_accuracy"),
    "actual_accuracy": data.get("actual_accuracy"),
    "trend": data.get("trend"),
    "safe_trade_window": data.get("safe_trade_window"),
    "user_confirmations": data.get("user_confirmations"),
    "total_confirmed_amount": data.get("total_confirmed_amount"),
    "timestamp": datetime.utcnow().isoformat()
}

    analytics_db.append(new_entry)
    return jsonify(new_entry), 201

@app.route('/analytics', methods=['GET'])
def get_analytics():
    return jsonify(analytics_db), 200

@app.route('/analytics/<entry_id>', methods=['GET'])
def get_single_analytics(entry_id):
    entry = next((item for item in analytics_db if item['id'] == entry_id), None)
    if entry:
        return jsonify(entry), 200
    return jsonify({"error": "Entry not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
