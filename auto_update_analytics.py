import requests
import pandas as pd
from datetime import datetime, timezone
from optimized_fetch_data import fetch_data, load_model_and_predict

# Функция calculate_trend
def calculate_trend(df):
    df['EMA'] = df['close'].ewm(span=24, adjust=False).mean()
    current_price = df['close'].iloc[-1]
    ema_price = df['EMA'].iloc[-1]

    if current_price > ema_price * 1.01:
        return "Bullish"
    elif current_price < ema_price * 0.99:
        return "Bearish"
    else:
        return "Neutral"

# Функция recommend_investment
def recommend_investment(historical_volume, current_volume):
    volume_ratio = current_volume / historical_volume
    if volume_ratio > 1.5:
        return 1000
    elif volume_ratio > 1.0:
        return 750
    elif volume_ratio > 0.5:
        return 500
    else:
        return 250

symbols = ['BTCUSDT', 'ETHUSDT', 'LTCUSDT']

for symbol in symbols:
    df = fetch_data(symbol)
    predicted_price = load_model_and_predict(symbol, df)
    trend = calculate_trend(df)
    historical_volume = df['close'].mean()
    current_volume = df['close'].iloc[-1]
    investment = recommend_investment(historical_volume, current_volume)

    current_hour = datetime.now(timezone.utc).hour
    entry_period = f"{current_hour}:00 – {current_hour}:30"

    data = {
        "entry_period": entry_period,
        "recommended_amount": investment,
        "predicted_accuracy": 85,
        "actual_accuracy": 0,
        "trend": trend,
        "safe_trade_window": round(current_volume * 0.02, 2),
        "user_confirmations": 0,
        "total_confirmed_amount": 0
    }

    response = requests.post('http://localhost:8200/analytics', json=data)

    if response.status_code == 201:
        print(f"✅ {symbol}: Аналитика добавлена.")
    else:
        print(f"❌ {symbol}: Ошибка при отправке - {response.text}")