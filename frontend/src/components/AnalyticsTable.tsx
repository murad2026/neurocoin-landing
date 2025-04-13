import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface AnalyticsItem {
  currency: string;
  predicted_price: number;
  recommended_investment: number;
  trend: string;
  entry_period: string;
  predicted_accuracy: number;
  safe_trade_window: number;
}

const translations = {
  en: {
    title: 'NeuroCoin Analytics',
    loading: 'Loading analytics...',
    headers: ['Currency', 'Entry Period', 'Predicted Price ($)', 'Recommended Investment ($)', 'Trend', 'Predicted Accuracy (%)', 'Safe Trade Window ($)'],
  },
  es: {
    title: 'Analítica de NeuroCoin',
    loading: 'Cargando analítica...',
    headers: ['Moneda', 'Período de entrada', 'Precio Predicho ($)', 'Inversión Recomendada ($)', 'Tendencia', 'Precisión Pronosticada (%)', 'Ventana Segura ($)'],
  },
};

const AnalyticsTable = () => {
  const [analytics, setAnalytics] = useState<AnalyticsItem[]>([]);
  const [loading, setLoading] = useState(true);

  const getDefaultLang = (): 'en' | 'es' => {
    if (typeof navigator !== 'undefined') {
      return navigator.language.startsWith('es') ? 'es' : 'en';
    }
    return 'en';
  };

  const [lang] = useState(getDefaultLang());
  const t = translations[lang];

  useEffect(() => {
    const fetchAnalytics = async () => {
      const symbols = ['BTCUSDT', 'ETHUSDT', 'LTCUSDT'];
      const results: AnalyticsItem[] = [];

      for (const symbol of symbols) {
        try {
          const { data } = await axios.get(`http://localhost:8103/predict/${symbol}`);
          results.push({
            currency: symbol.replace('USDT', ''),
            entry_period: data.entry_period,
            predicted_price: data.predicted_price,
            recommended_investment: data.recommended_investment,
            trend: data.trend,
            predicted_accuracy: data.predicted_accuracy,
            safe_trade_window: data.safe_trade_window,
          });
        } catch (error) {
          console.error('Error fetching analytics:', error);
        }
      }

      setAnalytics(results);
      setLoading(false);
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return <div className="text-white">{t.loading}</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-gray-800 text-white rounded shadow-xl overflow-hidden">
        <thead className="bg-gray-700">
          <tr>
            {t.headers.map((header, index) => (
              <th key={index} className="py-2 px-4 border-b whitespace-nowrap">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {analytics.map((item, index) => (
            <tr key={index} className="hover:bg-gray-600">
              <td className="py-2 px-4 border-b">{item.currency}</td>
              <td className="py-2 px-4 border-b">{item.entry_period}</td>
              <td className="py-2 px-4 border-b">${item.predicted_price.toFixed(2)}</td>
              <td className="py-2 px-4 border-b">${item.recommended_investment}</td>
              <td className="py-2 px-4 border-b">{item.trend}</td>
              <td className="py-2 px-4 border-b">{item.predicted_accuracy}%</td>
              <td className="py-2 px-4 border-b">${item.safe_trade_window}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AnalyticsTable;
