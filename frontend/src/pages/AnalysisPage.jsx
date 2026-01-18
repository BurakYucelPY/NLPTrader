import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ROUTES } from '../routes/AppRoutes.jsx'
import '../App.css'

function AnalysisPage() {
  const navigate = useNavigate()
  const [veri, setVeri] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(false)

  const analizBaslat = async () => {
    setYukleniyor(true)
    try {
      const cevap = await fetch("http://localhost:5199/api/Finans/btc")
      const sonuc = await cevap.json()
      
      console.log("Gelen Veri:", sonuc)
      setVeri(sonuc)
    } catch (hata) {
      console.log("Hata:", hata)
    } finally {
      setYukleniyor(false)
    }
  }

  return (
    <div className="container">
      
      <button 
        onClick={() => navigate(ROUTES.HOME)} 
        className="back-btn"
        style={{ 
          position: 'absolute', 
          top: '20px', 
          left: '20px',
          background: 'rgba(255,255,255,0.1)',
          border: '1px solid rgba(255,255,255,0.2)',
          color: '#fff',
          padding: '10px 20px',
          borderRadius: '8px',
          cursor: 'pointer',
          fontSize: '14px'
        }}
      >
        ← Geri
      </button>

      <h1 className="title">🤖 NLPTrader</h1>
      
      <div className="button-container">
        <button 
          onClick={analizBaslat}
          disabled={yukleniyor}
          className={`analiz-btn ${yukleniyor ? 'loading' : ''}`}
        >
          {yukleniyor ? "Yapay Zeka Analiz Ediyor..." : "STRATEJİYİ ÇALIŞTIR 🚀"}
        </button>
      </div>

      {veri && veri.strateji ? (
        <div className="dashboard">
          
          {/* 1. NİHAİ KARAR KARTI */}
          <div className="decision-card" style={{ borderColor: veri.strateji.karar_renk, boxShadow: `0 0 20px ${veri.strateji.karar_renk}40` }}>
            <h2>NİHAİ KARAR ({veri.sembol})</h2>
            <div className="decision-text" style={{ color: veri.strateji.karar_renk }}>
              {veri.strateji.karar}
            </div>
            <div className="score-info">
              Skor: <strong>{veri.strateji.toplam_skor}</strong> | Fiyat: <strong>${veri.fiyat}</strong>
            </div>
          </div>

          {/* 2. BİLEŞENLER (MACD - RSI - HABER) */}
          <div className="components-grid">
            
            {/* MACD KARTI */}
            <div className="component-card macd">
              <h3>📈 MACD (%50)</h3>
              <div className="component-score">
                {veri.strateji.bilesenler.macd_puan}
              </div>
              <p>Histogram Gücü: {veri.strateji.ham_veriler.macd_hist}</p>
            </div>

            {/* RSI KARTI */}
            <div className="component-card rsi">
              <h3>⚡ RSI (%30)</h3>
              <div className="component-score">
                {veri.strateji.bilesenler.rsi_puan}
              </div>
              <p>RSI Değeri: {veri.strateji.ham_veriler.rsi_degeri}</p>
            </div>

            {/* SENTIMENT KARTI */}
            <div className="component-card sentiment">
              <h3>📰 Haber (%20)</h3>
              <div className="component-score">
                {veri.strateji.bilesenler.sentiment_puan}
              </div>
              <p>Kaynak: {veri.strateji.ham_veriler.haber_kaynak}</p>
            </div>

          </div>

          {/* 3. HABER LİSTESİ */}
          <div className="news-section">
            <h4>Analiz Edilen Son Haberler</h4>
            {veri.haberler && veri.haberler.map((haber, index) => (
              <div key={index} className="news-item">
                <span className="news-title">{haber.baslik.substring(0, 100)}...</span>
                <span className={`news-tag ${haber.skor > 0 ? 'pos' : 'neg'}`}>
                  {haber.skor > 0 ? "Olumlu" : "Olumsuz"}
                </span>
              </div>
            ))}
          </div>

        </div>
      ) : (
        !yukleniyor && <p className="placeholder-text">Analiz başlatmak için butona basın.</p>
      )}
    </div>
  )
}

export default AnalysisPage
