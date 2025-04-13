import requests
import pandas as pd
import time

def fetch_data(symbol):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol.replace('USDT', '')}&tsym=USDT&limit=2000"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data['Response'] != 'Success':
            print(f"CryptoCompare API error: {data['Message']}")
            return None
        time.sleep(1)  # пауза для избежания лимитов
        return pd.DataFrame(data['Data']['Data'])
    except requests.RequestException as e:
        print(f"Error fetching data from CryptoCompare: {e}")
        return None
