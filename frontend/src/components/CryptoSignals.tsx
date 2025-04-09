import { useEffect, useState } from 'react';
import axios from 'axios';

interface Signal {
  interval: string;
  prediction: string;
  probability: number;
  currentPrice: number;
}

interface SignalsData {
  [currency: string]: Signal[];
}

interface Props {
  lang?: 'en' | 'es';
}

const texts = {
  en: { price: 'Price', prediction: 'Prediction', rise: '📈 Rise', fall: '📉 Fall', probability: 'Probability' },
  es: { price: 'Precio', prediction: 'Predicción', rise: '📈 Subirá', fall: '📉 Bajará', probability: 'Probabilidad' },
};

export default function CryptoSignals({ lang = 'en' }: Props) {
  const [signals, setSignals] = useState<SignalsData>({});
  const [selectedCurrency, setSelectedCurrency] = useState('BTC');
  const coins = ['BTC', 'ETH', 'DOGE'];

  useEffect(() => {
    axios.get('https://neurocoin-backend.onrender.com/api/signals')
      .then(response => setSignals(response.data.signals))
      .catch(error => console.error('Error:', error));
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
            {coin}
          </button>
        ))}
      </div>

      <div className="space-y-4">
        {(signals[selectedCurrency] || []).map((signal, index) => (
          <div key={index} className="p-4 bg-gray-800 rounded-xl shadow-md">
            <p><strong>{selectedCurrency}</strong> ({signal.interval})</p>
            <p>{t.price}: ${signal.currentPrice.toFixed(2)}</p>
            <p>
              {t.prediction}: {signal.prediction === 'rise' ? t.rise : t.fall} ({t.probability}: {signal.probability}%)
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
