import requests
import pandas as pd

def fetch_crypto_history(symbol='BTC', currency='USD', limit=2000, api_key=''):
    url = f'https://min-api.cryptocompare.com/data/v2/histohour'
    headers = {'authorization': f'Apikey {api_key}'}
    params = {
        'fsym': symbol,
        'tsym': currency,
        'limit': limit  # количество записей (2000 часов ≈ 83 дня)
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if data['Response'] != 'Success':
        raise Exception(f"Ошибка запроса: {data.get('Message', 'Неизвестная ошибка')}")

    df = pd.DataFrame(data['Data']['Data'])
    df['time'] = pd.to_datetime(df['time'], unit='s')

    # выбираем нужные колонки
    df = df[['time', 'open', 'high', 'low', 'close', 'volumeto']]
    
    df.to_csv(f'{symbol}{currency}_historical.csv', index=False)
    print(f"Данные сохранены в файл {symbol}{currency}_historical.csv")

# Запуск функции
if __name__ == '__main__':
    fetch_crypto_history(
        symbol='BTC',
        currency='USD',
        limit=2000,
        api_key='4f2226b147f9f76bba34df40bfa9ce20d1174457d63f74028f130264af19acea'
    )
