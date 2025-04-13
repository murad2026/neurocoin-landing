import websocket
import json
import time

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade/ethusdt@trade/ltcusdt@trade"

PROXY_HOST = "brd.superproxy.io"
PROXY_PORT = 22228  # ✅ теперь правильный порт SOCKS5 от BrightData
PROXY_USER = "brd-customer-hl_79abd1a3-zone-datacenter_proxy1"
PROXY_PASS = "lsluijlu6c29"

def on_message(ws, message):
    data = json.loads(message)
    symbol = data['s']
    price = data['p']
    event_time = data['E']

    print(f"{symbol}: ${price} at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(event_time/1000))}")

def on_error(ws, error):
    print(f"Ошибка: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Соединение закрыто")

def on_open(ws):
    print("Соединение установлено с Binance WebSocket")

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
