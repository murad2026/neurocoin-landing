import React, { useState } from 'react';
import Head from 'next/head';
import Script from 'next/script';
import Link from 'next/link';
import { Card, CardContent } from '@/components/ui/card';

interface Translation {
  title: string;
  subtitle: string;
  features: string[];
  readyTitle: string;
  readySubtitle: string;
  botButton: string;
}

const translations: Record<'en' | 'es', Translation> = {
  en: {
    title: 'NeuroCoin',
    subtitle: 'Next-gen crypto analytics — Powered by AI.',
    features: ['AI trend analysis', 'Auto signals by coin', 'Twitter/news sentiment'],
    readyTitle: 'Ready to try?',
    readySubtitle: 'Join the bot and start for free.',
    botButton: 'Launch Bot',
  },
  es: {
    title: 'NeuroCoin',
    subtitle: 'Analítica cripto de próxima generación — Impulsada por IA.',
    features: ['Análisis de tendencias con IA', 'Señales automáticas por moneda', 'Sentimiento de Twitter/noticias'],
    readyTitle: '¿Listo para probar?',
    readySubtitle: 'Únete al bot y empieza gratis.',
    botButton: 'Lanzar Bot',
  },
};

export default function NeuroCoinLanding() {
  const getDefaultLang = (): 'en' | 'es' => {
    if (typeof navigator !== 'undefined') {
      return navigator.language.startsWith('es') ? 'es' : 'en';
    }
    return 'en';
  };

  const [lang] = useState(getDefaultLang());
  const t = translations[lang];

  return (
    <div>
      <Head>
        <title>NeuroCoin — AI-Powered Crypto Analytics</title>
        <meta
          name="description"
          content="Next-gen crypto analytics powered by AI. Real-time signals, market trends, and sentiment — all in one Telegram bot."
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Script
        defer
        data-domain="ncoin.cc"
        src="https://plausible.io/js/script.file-downloads.hash.outbound-links.pageview-props.revenue.tagged-events.js"
      />
      <Script
        id="plausible-init"
        dangerouslySetInnerHTML={{
          __html: `window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments); }`,
        }}
      />

      <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-gray-800 text-white p-6" id="top">
        <header className="flex flex-wrap items-center justify-between py-4 px-4 md:px-8">
          <Link href="#top" className="text-2xl font-bold text-green-400">
            NeuroCoin
          </Link>
          <nav className="space-x-4 text-sm md:text-base">
            <a href="#features" className="text-gray-300 hover:text-white">
              {lang === 'en' ? 'Features' : 'Características'}
            </a>
            <a href="#how" className="text-gray-300 hover:text-white">
              {lang === 'en' ? 'How It Works' : 'Cómo Funciona'}
            </a>
            <a href="#pricing" className="text-gray-300 hover:text-white">
              {lang === 'en' ? 'Pricing' : 'Precios'}
            </a>
            <a href="#login" className="text-green-400 font-semibold">
              {t.botButton}
            </a>
          </nav>
        </header>

        <section id="features" className="grid md:grid-cols-3 gap-6 py-12">
          {t.features.map((title: string, i: number) => (
            <Card key={i} className="bg-gray-900 rounded-2xl p-4">
              <CardContent>
                <h3 className="text-xl font-semibold mb-2">{title}</h3>
                <p className="text-gray-400">
                  AI scans real-time data and delivers ready-to-use signals in our Telegram bot.
                </p>
              </CardContent>
            </Card>
          ))}
        </section>

        <section id="login" className="text-center py-20">
          <h2 className="text-4xl font-bold mb-4">{t.readyTitle}</h2>
          <p className="text-gray-400 mb-6">{t.readySubtitle}</p>
          <a href="https://t.me/neurocoin_bot" target="_blank" rel="noopener noreferrer">
            <button className="text-lg px-6 py-3 rounded-2xl shadow-xl bg-green-500 hover:bg-green-600 text-white">
              {t.botButton}
            </button>
          </a>
        </section>
      </div>
    </div>
  );
}
