import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface AnalyticsItem {
  id: string;
  entry_period: string | null;
  recommended_amount: number | null;
  predicted_accuracy: number | null;
  actual_accuracy: number | null;
  trend: string | null;
  safe_trade_window: number | null;
  user_confirmations: number | null;
  total_confirmed_amount: number | null;
}

const translations = {
  en: {
    title: 'NeuroCoin Analytics',
    loading: 'Loading analytics...',
    headers: [
      'Entry Period',
      'Trade Amount ($)',
      'Predicted Accuracy (%)',
      'Actual Accuracy (%)',
      'Trend',
      'Safe Trade Window ($)',
      'Confirmations',
      'Confirmed Amount ($)',
    ],
  },
  es: {
    title: 'Analítica de NeuroCoin',
    loading: 'Cargando analítica...',
    headers: [
      'Periodo de entrada',
      'Monto de operación ($)',
      'Precisión prevista (%)',
      'Precisión real (%)',
      'Tendencia',
      'Ventana segura ($)',
      'Confirmaciones',
      'Monto confirmado ($)',
    ],
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
      try {
        const response = await axios.get<AnalyticsItem[]>('https://neurocoin-ml-service.onrender.com/analytics');
        setAnalytics(response.data);
      } catch (error) {
        console.error('Error fetching analytics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return <div className="text-white">{t.loading}</div>;
  }

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4 text-white">{t.title}</h2>
      <table className="min-w-full bg-gray-800 text-white rounded shadow-xl overflow-hidden">
        <thead className="bg-gray-700">
          <tr>
            {t.headers.map((header, index) => (
              <th key={index} className="py-2 px-4 border-b">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {analytics.map((item) => (
            <tr key={item.id} className="hover:bg-gray-600">
              <td className="py-2 px-4 border-b">{item.entry_period || '–'}</td>
              <td className="py-2 px-4 border-b">{item.recommended_amount ?? '–'}</td>
              <td className="py-2 px-4 border-b">
                {item.predicted_accuracy !== null ? `${item.predicted_accuracy}%` : '–'}
              </td>
              <td className="py-2 px-4 border-b">
                {item.actual_accuracy !== null ? `${item.actual_accuracy}%` : '–'}
              </td>
              <td className="py-2 px-4 border-b">{item.trend || '–'}</td>
              <td className="py-2 px-4 border-b">{item.safe_trade_window ?? '–'}</td>
              <td className="py-2 px-4 border-b">{item.user_confirmations ?? '–'}</td>
              <td className="py-2 px-4 border-b">{item.total_confirmed_amount ?? '–'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AnalyticsTable;