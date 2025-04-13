from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('crypto_trades.db', check_same_thread=False)

def find_optimal_trade_window(symbol, interval_minutes=15, analysis_period_hours=4):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(trade_time) FROM trades WHERE symbol = ?", (symbol,))
    last_time_str = cursor.fetchone()[0]

    if not last_time_str:
        return None

    end_time = datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
    start_time = end_time - timedelta(hours=analysis_period_hours)

    query = """
    SELECT trade_time, price FROM trades
    WHERE symbol = ? AND trade_time BETWEEN ? AND ?
    ORDER BY trade_time ASC
    """

    df = pd.read_sql_query(query, conn, params=(symbol, start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')))

    if df.empty:
        return None

    df['trade_time'] = pd.to_datetime(df['trade_time'])
    df.set_index('trade_time', inplace=True)

    df['returns'] = df['price'].pct_change()
    volatility = df['returns'].rolling(window=interval_minutes).std()

    volatility.dropna(inplace=True)

    if volatility.empty:
        return None

    optimal_time = volatility.idxmin()  # Ищем минимальную волатильность как наиболее стабильный момент

    optimal_start = optimal_time
    optimal_end = optimal_start + timedelta(minutes=interval_minutes)

    return {
        'symbol': symbol,
        'optimal_start_utc': optimal_start.strftime('%Y-%m-%d %H:%M:%S'),
        'optimal_end_utc': optimal_end.strftime('%Y-%m-%d %H:%M:%S'),
        'timezone': 'UTC'
    }

@app.route('/optimal_window/<symbol>', methods=['GET'])
def optimal_window(symbol):
    window = find_optimal_trade_window(symbol)

    if window:
        return jsonify(window)
    else:
        return jsonify({'error': 'No optimal window found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8105, debug=True)
