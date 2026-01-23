import React from 'react'
import AssetCard from '../components/AssetCard'
import NewsSection from '../components/NewsSection'
import { KRIPTO_LISTESI } from '../routes/paths.jsx'
import { useNews } from '../context/NewsContext.jsx'
import '../App.css'

function HomePage() {
  // Context'ten haberleri al - artık her sayfa değişiminde yeniden çekilmeyecek
  const { haberler, yukleniyor, toplamSkor } = useNews()

  // Genel sentiment durumu
  const getSentimentDurum = () => {
    if (toplamSkor === null) return { text: 'Analiz ediliyor...', renk: '#888', emoji: '🔄' }
    if (toplamSkor > 0.1) return { text: 'Piyasa Pozitif', renk: '#00c853', emoji: '🟢' }
    if (toplamSkor < -0.1) return { text: 'Piyasa Negatif', renk: '#ff5252', emoji: '🔴' }
    return { text: 'Piyasa Nötr', renk: '#ffc107', emoji: '🟡' }
  }

  const sentiment = getSentimentDurum()

  return (
    <div className="home-container">
      
      {/* SOL TARAF: Coinler */}
      <div className="coins-panel">
        <h1 className="title" style={{ textAlign: 'left', marginBottom: '10px' }}>🤖 NLPTrader</h1>
        <p style={{ color: '#aaa', marginBottom: '40px', fontSize: '1rem' }}>
          Yapay zeka analizini başlatmak için bir varlık seçin.
        </p>

        <div className="assets-grid">
          {KRIPTO_LISTESI.map((varlik) => (
            <AssetCard
              key={varlik.sembol}
              sembol={varlik.sembol}
              ad={varlik.ad}
              ikon={varlik.ikon}
              renk={varlik.renk}
              rotaYolu={varlik.rota}
            />
          ))}
        </div>
      </div>

      {/* SAĞ TARAF: Haber Paneli */}
      <div className="news-panel">
        {/* Üst Kısım: Skor */}
        <div className="news-header">
          <h3>📢 Piyasa Gündemi</h3>
          <div className="sentiment-badge" style={{ background: sentiment.renk + '22', borderColor: sentiment.renk }}>
            <span className="sentiment-emoji">{sentiment.emoji}</span>
            <span className="sentiment-text" style={{ color: sentiment.renk }}>{sentiment.text}</span>
            {toplamSkor !== null && (
              <span className="sentiment-score" style={{ color: sentiment.renk }}>
                {(toplamSkor * 100).toFixed(1)}%
              </span>
            )}
          </div>
          <p className="news-subtitle">
            {haberler.length > 0 ? `${haberler.length} haber analiz edildi` : 'Haberler yükleniyor...'}
          </p>
        </div>

        {/* Alt Kısım: Scrollable Haber Listesi */}
        <div className="news-scroll-container">
          {yukleniyor && haberler.length === 0 ? (
            <div className="news-loading">
              <div className="loading-spinner">⏳</div>
              <p>Yapay zeka haberleri tarıyor...</p>
            </div>
          ) : (
            <NewsSection haberler={haberler} />
          )}
        </div>
      </div>

    </div>
  )
}

export default HomePage
