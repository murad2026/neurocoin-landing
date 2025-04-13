import requests
from datetime import datetime, timezone

data = {
    "entry_period": "21:00 – 21:30",
    "recommended_amount": 750,
    "predicted_accuracy": 85,
    "actual_accuracy": 0,
    "trend": "Bullish",
    "safe_trade_window": 1708.8,
    "user_confirmations": 0,
    "total_confirmed_amount": 0
}

response = requests.post('https://neurocoin-ml-service.onrender.com/analytics', json=data)

print(response.status_code, response.json())
