import React, { useState, useEffect } from 'react'
import AssetCard from '../components/AssetCard'
import NewsSection from '../components/NewsSection'
import { KRIPTO_LISTESI } from '../routes/paths.jsx'
import '../App.css'

function HomePage() {
  const [haberler, setHaberler] = useState(null)

  useEffect(() => {
    // Sayfa açıldığında genel piyasa haberlerini çek
    const haberGetir = async () => {
      try {
        const cevap = await fetch("http://localhost:5199/api/Haber/analiz")
        const sonuc = await cevap.json()
        if (sonuc.haberler) {
           setHaberler(sonuc.haberler)
        }
      } catch (hata) {
        console.error("Haberler çekilemedi:", hata)
      }
    }
    haberGetir()
  }, [])

  return (
    <div className="container-fluid" style={{ padding: 0, display: 'flex', minHeight: '100vh', background: '#1a1a2e' }}>
      
      {/* SOL TARAFLAR: Coinler */}
      <div style={{ flex: '1', padding: '40px', overflowY: 'auto' }}>
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

      {/* SAĞ TARAFLAR: Haber Paneli */}
      <div className="news-panel" style={{ width: '400px', flexShrink: 0, borderLeft: '1px solid #333', background: '#1e1e2d' }}>
        <div style={{ position: 'sticky', top: '40px' }}>
          <h3>📢 Piyasa Gündemi</h3>
          <p style={{ color: '#777', fontSize: '0.9rem', marginBottom: '30px' }}>
            CoinDesk ve Cointelegraph üzerinden anlık yapay zeka sentiment analizi.
          </p>

          {haberler ? (
            <NewsSection haberler={haberler} />
          ) : (
            <div style={{ textAlign: 'center', padding: '60px 0', color: '#666' }}>
              <div className="loading-spinner" style={{ marginBottom: '15px' }}>⏳</div>
              <p>Haber akışı taranıyor...</p>
            </div>
          )}
        </div>
      </div>

    </div>
  )
}

export default HomePage
