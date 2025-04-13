import { useEffect, useState } from 'react';
import axios from 'axios';

interface Signal {
  prediction: string;
  currentPrice: number;
  trend: string;
  recommendedInvestment: number;
}

interface SignalsData {
  [currency: string]: Signal;
}

interface Props {
  lang?: 'en' | 'es';
}

const texts = {
  en: { price: 'Price', prediction: 'Prediction', trend: 'Trend', investment: 'Investment ($)' },
  es: { price: 'Precio', prediction: 'Predicción', trend: 'Tendencia', investment: 'Inversión ($)' },
};

export default function CryptoSignals({ lang = 'en' }: Props) {
  const [signals, setSignals] = useState<SignalsData>({});
  const [selectedCurrency, setSelectedCurrency] = useState('BTCUSDT');
  const coins = ['BTCUSDT', 'ETHUSDT', 'LTCUSDT'];

  useEffect(() => {
    const fetchSignals = async () => {
      const newSignals: SignalsData = {};

      for (const coin of coins) {
        try {
          const response = await axios.get(`http://localhost:8103/predict/${coin}`);
          newSignals[coin] = {
            prediction: response.data.predicted_price.toFixed(2),
            currentPrice: response.data.current_price,  // <— Здесь правильное поле
            trend: response.data.trend,
            recommendedInvestment: response.data.recommended_investment,
          };          
        } catch (error) {
          console.error('Error fetching signal:', error);
        }
      }

      setSignals(newSignals);
    };

    fetchSignals();
  }, []);

  const t = texts[lang];

  return (
    <div className="text-center py-12">
      <div className="mb-6 flex justify-center gap-4">
        {coins.map((coin) => (
          <button
            key={coin}
            className={`px-4 py-2 rounded-xl ${selectedCurrency === coin ? 'bg-green-500' : 'bg-gray-700'}`}
            onClick={() => setSelectedCurrency(coin)}
          >
            {coin.replace('USDT', '')}
          </button>
        ))}
      </div>

      {signals[selectedCurrency] && (
        <div className="p-4 bg-gray-800 rounded-xl shadow-md inline-block">
          <p><strong>{selectedCurrency.replace('USDT', '')}</strong></p>
          <p>{t.price}: ${signals[selectedCurrency].currentPrice.toFixed(2)}</p>
          <p>{t.prediction}: ${signals[selectedCurrency].prediction}</p>
          <p>{t.trend}: {signals[selectedCurrency].trend}</p>
          <p>{t.investment}: ${signals[selectedCurrency].recommendedInvestment}</p>
        </div>
      )}
    </div>
  );
}