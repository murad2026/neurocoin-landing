import json
import pandas as pd
import numpy as np
import requests
import time
import os
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
from keras.losses import MeanSquaredError

proxies = {
    'http': 'http://brd-customer-hl_79abd1a3-zone-datacenter_proxy1:lsluijlu6c29@brd.superproxy.io:33335',
    'https': 'http://brd-customer-hl_79abd1a3-zone-datacenter_proxy1:lsluijlu6c29@brd.superproxy.io:33335'
}

def fetch_data(symbol):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol.replace('USDT', '')}&tsym=USDT&limit=2000"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data['Response'] != 'Success':
            print(f"CryptoCompare error: {data['Message']}")
            return None
        time.sleep(1)
        return pd.DataFrame(data['Data']['Data'])
    except requests.RequestException as e:
        print(f"Fetch data error: {e}")
        return None

def get_current_volume(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data['volume'])
    except requests.RequestException as e:
        print(f"Binance error: {e}")
        return None

def predict_next_period(df, symbol):
    model_path = f"{symbol}_model.h5"
    data = df['close'].dropna().values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    if os.path.exists(model_path):
        model = load_model(model_path)
    else:
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

        model.compile(loss=MeanSquaredError(), optimizer='adam')
        model.fit(X, y, epochs=5, batch_size=32)
        model.save(model_path)

    last_60 = scaled_data[-60:].reshape(1, 60, 1)
    prediction = scaler.inverse_transform(model.predict(last_60))
    return float(prediction[0][0])

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

def recommend_investment(historical_volume, current_volume):
    if current_volume is None:
        return 250  # default if current volume unavailable

    volume_ratio = current_volume / historical_volume
    if volume_ratio > 1.5:
        return 1000
    elif volume_ratio > 1.0:
        return 750
    elif volume_ratio > 0.5:
        return 500
    else:
        return 250

def prepare_predictions(symbol):
    df = fetch_data(symbol)
    if df is None:
        print(f"Failed to fetch data for {symbol}")
        return

    historical_volume = df['volumeto'].mean()
    current_volume = get_current_volume(symbol)

    prediction = predict_next_period(df, symbol)
    trend = calculate_trend(df)
    investment = recommend_investment(historical_volume, current_volume)

    results = {
        "symbol": symbol,
        "prediction": prediction,
        "trend": trend,
        "investment": investment
    }

    with open(f"{symbol}_predictions.json", "w") as file:
        json.dump(results, file)
    print(f"Predictions saved for {symbol}")

if __name__ == "__main__":
    symbols = ['BTCUSDT', 'ETHUSDT', 'LTCUSDT']
    for sym in symbols:
        prepare_predictions(sym)
