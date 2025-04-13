import websocket
import json
import time
import sqlite3

# Binance WebSocket URL
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade/ethusdt@trade/ltcusdt@trade"

# SOCKS5 Proxy settings
PROXY_HOST = "brd.superproxy.io"
PROXY_PORT = 22228
PROXY_USER = "brd-customer-hl_79abd1a3-zone-datacenter_proxy1"
PROXY_PASS = "lsluijlu6c29"

# SQLite database setup
conn = sqlite3.connect('crypto_trades.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    price REAL,
                    trade_time TEXT
                )''')
conn.commit()

# WebSocket event handlers
def on_message(ws, message):
    data = json.loads(message)
    symbol = data['s']
    price = float(data['p'])
    event_time = data['E']
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(event_time/1000))

    print(f"{symbol}: ${price} at {formatted_time}")

    cursor.execute("INSERT INTO trades (symbol, price, trade_time) VALUES (?, ?, ?)",
                   (symbol, price, formatted_time))
    conn.commit()

def on_error(ws, error):
    print(f"Ошибка: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Соединение закрыто")
    conn.close()

def on_open(ws):
    print("Соединение установлено с Binance WebSocket")

# Run WebSocket connection
if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        BINANCE_WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever(
        http_proxy_host=PROXY_HOST,
        http_proxy_port=PROXY_PORT,
        proxy_type="socks5h",
        http_proxy_auth=(PROXY_USER, PROXY_PASS)
    )