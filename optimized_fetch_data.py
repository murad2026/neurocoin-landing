import requests
import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense

CACHE_TIME = 600  # кэш на 10 минут
cache = {}

def fetch_data(symbol='BTCUSDT', interval='1h', limit=1000):
    cache_key = f"{symbol}_{interval}_{limit}"
    if cache_key in cache and (time.time() - cache[cache_key]['time'] < CACHE_TIME):
        print(f"[{symbol}] Используется кэш")
        return cache[cache_key]['data']

    url = 'https://api.binance.com/api/v3/klines'
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Ошибка запроса: {response.json()}")

    data = response.json()
    df = pd.DataFrame(data, columns=[
        'time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_volume', 'taker_buy_quote_volume', 'ignore'
    ])

    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['close'] = df['close'].astype(float)
    df = df[['time', 'close']]

    cache[cache_key] = {'data': df, 'time': time.time()}

    return df

def load_model_and_predict(symbol, df):
    data = df['close'].values.reshape(-1, 1)
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

    last_60 = scaled_data[-60:].reshape(1, 60, 1)
    prediction_scaled = model.predict(last_60, verbose=0)
    prediction = scaler.inverse_transform(prediction_scaled)

    return float(prediction[0][0])

# Пример использования:
symbol = 'BTCUSDT'
df = fetch_data(symbol)

# Прогноз цены (при каждом вызове)
prediction = load_model_and_predict(symbol, df)
print(f"Прогноз следующей цены для {symbol}: {prediction}")
