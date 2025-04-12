import json
import pandas as pd
import numpy as np
import requests
import time
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense

def fetch_data(symbol):
    start = time.time()
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol.replace('USDT', '')}&tsym=USDT&limit=2000"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['Data']['Data'])
    print(f"[{symbol}] fetch_data: {time.time() - start:.2f}s")
    return df

def predict_next_period(df, symbol):
    start = time.time()
    data = df['close'].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i, 0])
        y.append(scaled_data[i, 0])

    X, y = np.array(X), np.array(y)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(50))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, y, epochs=5, batch_size=32, verbose=0)

    last_60 = scaled_data[-60:].reshape(1, 60, 1)
    prediction = scaler.inverse_transform(model.predict(last_60, verbose=0))
    print(f"[{symbol}] predict_next_period: {time.time() - start:.2f}s")
    return float(prediction[0][0])

def calculate_trend(df, symbol):
    start = time.time()
    df['EMA'] = df['close'].ewm(span=24, adjust=False).mean()
    current_price = df['close'].iloc[-1]
    ema_price = df['EMA'].iloc[-1]

    if current_price > ema_price * 1.01:
        trend = "Bullish"
    elif current_price < ema_price * 0.99:
        trend = "Bearish"
    else:
        trend = "Neutral"
    print(f"[{symbol}] calculate_trend: {time.time() - start:.2f}s")
    return trend

def get_current_volume(symbol):
    start = time.time()
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    print(f"[{symbol}] get_current_volume: {time.time() - start:.2f}s")
    return float(data['volume'])

def recommend_investment(historical_volume, current_volume, symbol):
    start = time.time()
    volume_ratio = current_volume / historical_volume
    if volume_ratio > 1.5:
        inv = 1000
    elif volume_ratio > 1.0:
        inv = 750
    elif volume_ratio > 0.5:
        inv = 500
    else:
        inv = 250
    print(f"[{symbol}] recommend_investment: {time.time() - start:.2f}s")
    return inv

def prepare_predictions(symbol):
    total_start = time.time()
    df = fetch_data(symbol)
    historical_volume = df['volumeto'].mean()
    current_volume = get_current_volume(symbol)

    prediction = predict_next_period(df, symbol)
    trend = calculate_trend(df, symbol)
    investment = recommend_investment(historical_volume, current_volume, symbol)

    results = {
        "symbol": symbol,
        "prediction": prediction,
        "trend": trend,
        "investment": investment
    }

    with open(f"{symbol}_predictions.json", "w") as file:
        json.dump(results, file)

    print(f"[{symbol}] Всего заняло: {time.time() - total_start:.2f}s\n")

symbols = ['BTCUSDT', 'ETHUSDT', 'LTCUSDT']
for sym in symbols:
    prepare_predictions(sym)

