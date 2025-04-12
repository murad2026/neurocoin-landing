import requests
import time

symbol = 'BTCUSDT'

# Проверка CryptoCompare
start_time = time.time()
url_crypto = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol.replace('USDT', '')}&tsym=USDT&limit=2000"
response = requests.get(url_crypto)
print(f"CryptoCompare response: {response.status_code}, время: {time.time() - start_time:.2f}s")

# Проверка Binance
start_time = time.time()
url_binance = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
response = requests.get(url_binance)
print(f"Binance response: {response.status_code}, время: {time.time() - start_time:.2f}s")

