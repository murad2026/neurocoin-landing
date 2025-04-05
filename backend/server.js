const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));


const CMC_API_KEY = process.env.CMC_API_KEY;
const coins = ['BTC', 'ETH', 'DOGE'];

app.get('/api/signals', async (req, res) => {
  try {
    const response = await axios.get(
      'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',
      {
        headers: { 'X-CMC_PRO_API_KEY': CMC_API_KEY },
        params: { symbol: coins.join(','), convert: 'USDT' },
      }
    );

    const intervals = ['15m', '1h', '4h', '1d'];
    const signals = {};

    coins.forEach(coin => {
      const price = response.data.data[coin].quote.USDT.price;
      signals[coin] = intervals.map(interval => ({
        interval,
        prediction: Math.random() > 0.5 ? 'rise' : 'fall',
        probability: (Math.random() * (80 - 60) + 60).toFixed(1),
        currentPrice: price,
      }));
    });

    res.json({ signals });
  } catch (error) {
    console.error(error.response ? error.response.data : error.message);
    res.status(500).json({ error: 'Ошибка получения данных' });
  }
});

app.listen(5000, () => {
  console.log('NeuroCoin Analytics API (расширенный) на порту 5000 🚀');
});
