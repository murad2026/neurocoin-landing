import json
import pandas as pd
import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense

def fetch_data(symbol):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol.replace('USDT', '')}&tsym=USDT&limit=2000"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['Data']['Data'])
    return df

def predict_next_period(df):
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

def get_current_volume(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return float(data['volume'])

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

def prepare_predictions(symbol):
    df = fetch_data(symbol)
    historical_volume = df['volumeto'].mean()
    current_volume = get_current_volume(symbol)

    prediction = predict_next_period(df)
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

# Example usage
symbols = ['BTCUSDT', 'ETHUSDT', 'LTCUSDT']
for sym in symbols:
    prepare_predictions(sym)

