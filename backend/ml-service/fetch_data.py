import requests
import pandas as pd

def get_binance_data(symbol='BTCUSDT', interval='1h', limit=1000):
    url = 'https://api.binance.com/api/v3/klines'
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Ошибка запроса:", response.json())
        return

    data = response.json()
    if not data:
        print("Получен пустой ответ от Binance!")
        return

    df = pd.DataFrame(data, columns=[
        'time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_volume', 'taker_buy_quote_volume', 'ignore'
    ])

    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['close'] = df['close'].astype(float)
    df = df[['time', 'close']]

    df.to_csv(f'{symbol}_historical.csv', index=False)
    print(f"Файл {symbol}_historical.csv создан, строк: {len(df)}")

get_binance_data('BTCUSDT')
