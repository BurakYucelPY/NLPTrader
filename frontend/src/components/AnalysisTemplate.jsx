import React from 'react'
import { useNavigate } from 'react-router-dom'
import { ROUTES } from '../routes/AppRoutes.jsx'
import DecisionCard from './DecisionCard'
import AnalysisMetrics from './AnalysisMetrics'
import '../App.css'

function AnalysisTemplate({ 
  baslik,           // Örn: "BTC Analizi" veya "🤖 NLPTrader"
  yukleniyor,       // Yükleniyor durumu (true/false)
  veri,             // API'den dönen veri
  analizBaslatFn,   // Butona basınca çalışacak fonksiyon
  butonMetni = "Yapay Zeka Analiz Ediyor..." // Varsayılan loading metni
}) {
  const navigate = useNavigate()

  return (
    <div className="container">
      
      {/* Geri Butonu */}
      <button 
        onClick={() => navigate(ROUTES.HOME)} 
        className="back-btn"
      >
        ← Geri
      </button>

      {/* Başlık */}
      <h1 className="title">{baslik}</h1>
      
      {/* Analiz Butonu */}
      <div className="button-container">
        <button 
          onClick={analizBaslatFn}
          disabled={yukleniyor}
          className={`analiz-btn ${yukleniyor ? 'loading' : ''}`}
        >
          {yukleniyor ? butonMetni : "STRATEJİYİ ÇALIŞTIR 🚀"}
        </button>
      </div>

      {/* Sonuç Alanı */}
      {veri && veri.strateji ? (
        <div className="dashboard">
          
          <DecisionCard 
            data={veri.strateji} 
            sembol={veri.sembol} 
            fiyat={veri.fiyat} 
          />

          <AnalysisMetrics strateji={veri.strateji} />

        </div>
      ) : (
        !yukleniyor && <p className="placeholder-text">Analiz başlatmak için butona basın.</p>
      )}
    </div>
  )
}

export default AnalysisTemplate
