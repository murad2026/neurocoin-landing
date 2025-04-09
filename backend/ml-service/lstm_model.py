import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

df = pd.read_csv('BTCUSDT_historical.csv')
data = df['close'].values.reshape(-1, 1)

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# Подготовка данных
X, y = [], []
for i in range(60, len(scaled_data)):
    X.append(scaled_data[i-60:i, 0])
    y.append(scaled_data[i, 0])

X, y = np.array(X), np.array(y)
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# Создание модели
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X, y, epochs=10, batch_size=32)

# Тестовое предсказание
last_60 = scaled_data[-60:]
last_60 = np.reshape(last_60, (1, 60, 1))
pred_price = model.predict(last_60)
pred_price = scaler.inverse_transform(pred_price)
print(f'Прогнозируемая цена BTC на следующий час: {pred_price[0][0]}')
