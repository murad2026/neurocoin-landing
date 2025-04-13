import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface OptimalWindow {
  symbol: string;
  optimal_start_utc: string;
  optimal_end_utc: string;
  timezone: string;
}

const OptimalTradeWindow = ({ symbol }: { symbol: string }) => {
  const [window, setWindow] = useState<OptimalWindow | null>(null);
  const [userTimezone, setUserTimezone] = useState('');
  const [userCountry, setUserCountry] = useState('');

  useEffect(() => {
    const fetchOptimalWindow = async () => {
      try {
        const { data } = await axios.get(`http://localhost:8105/optimal_window/${symbol}`);
        setWindow(data);
      } catch (error) {
        console.error('Error fetching optimal window:', error);
      }
    };

    fetchOptimalWindow();

    // Определение таймзоны и страны браузера
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const country = Intl.DateTimeFormat(undefined, { timeZoneName: 'long' })
      .formatToParts(new Date())
      .find(part => part.type === 'timeZoneName')?.value;

    setUserTimezone(timezone);
    setUserCountry(country || '');
  }, [symbol]);

  if (!window) return <div className="text-white">Loading optimal trade window...</div>;

  const convertUTCToLocal = (utcTime: string) => {
    return new Date(utcTime + 'Z').toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    });
  };

  return (
    <div className="p-6 bg-gray-800 rounded-xl shadow-xl text-white">
      <h2 className="text-xl font-bold mb-4">🕒 Оптимальное время для входа ({symbol.replace('USDT', '')}):</h2>
      <p className="text-lg">
        📌 {convertUTCToLocal(window.optimal_start_utc)} - {convertUTCToLocal(window.optimal_end_utc)} (по вашему местному
        времени — {userCountry})
      </p>
      <div className="mt-4 bg-gray-700 p-2 rounded-md text-yellow-400">
        ⚠️ <strong>Важно:</strong> Убедитесь, что часы и часовой пояс вашего устройства ({userTimezone}) установлены
        правильно и соответствуют вашему реальному местоположению.
      </div>
    </div>
  );
};

export default OptimalTradeWindow;