from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import requests
import time
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense

app = Flask(__name__)
CORS(app)

# Cache dictionary
cache = {}
CACHE_TIMEOUT = 900  # 15 минут

# Загрузка исторических данных
def fetch_data(symbol):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol.replace('USDT', '')}&tsym=USDT&limit=2000"
    response = requests.get(url)
    data = response.json()
    if data['Response'] != 'Success':
        raise Exception('Ошибка при получении данных от CryptoCompare')
    df = pd.DataFrame(data['Data']['Data'])
    return df

# Получение текущего объёма с Binance
def get_current_volume(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return float(data['volume'])

# Прогноз цены следующего часа
def predict_next_hour(symbol):
    df = fetch_data(symbol)
    data = df['close'].dropna().values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i, 0])
        y.append(scaled_data[i, 0])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, y, epochs=5, batch_size=32, verbose=0)

    last_60 = scaled_data[-60:]
    last_60 = np.reshape(last_60, (1, 60, 1))
    pred_price = model.predict(last_60, verbose=0)
    pred_price = scaler.inverse_transform(pred_price)

    return float(pred_price[0][0])

# Рекомендация по сумме инвестиций на основе объёма
def recommend_investment(symbol):
    historical_df = fetch_data(symbol)
    historical_volume = historical_df['volumeto'].mean()
    current_volume = get_current_volume(symbol)
    volume_ratio = current_volume / historical_volume

    if volume_ratio > 1.5:
        return 1000
    elif volume_ratio > 1.0:
        return 750
    elif volume_ratio > 0.5:
        return 500
    else:
        return 250

# Определение текущего тренда с использованием EMA
def calculate_trend(symbol):
    df = fetch_data(symbol)
    df['EMA'] = df['close'].ewm(span=24, adjust=False).mean()
    current_price = df['close'].iloc[-1]
    ema_price = df['EMA'].iloc[-1]

    if current_price > ema_price * 1.01:
        return "Bullish"
    elif current_price < ema_price * 0.99:
        return "Bearish"
    else:
        return "Neutral"

@app.route('/predict/<symbol>', methods=['GET'])
def prediction(symbol):
    current_time = time.time()
    if symbol in cache and current_time - cache[symbol]['timestamp'] < CACHE_TIMEOUT:
        return jsonify(cache[symbol]['data'])

    price = predict_next_hour(symbol)
    investment = recommend_investment(symbol)
    trend = calculate_trend(symbol)

    data = {
        "symbol": symbol,
        "predicted_price": price,
        "recommended_investment": investment,
        "trend": trend
    }

    cache[symbol] = {'data': data, 'timestamp': current_time}
    return jsonify(data)

@app.route('/', methods=['GET'])
def home():
    return "NeuroCoin ML Service с прогнозами, аналитикой объёмов и трендов"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8103, debug=True)
