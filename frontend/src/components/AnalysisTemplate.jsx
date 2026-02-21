import React from 'react'
import { useNavigate } from 'react-router-dom'
import { ROUTES } from '../routes/AppRoutes.jsx'
import DecisionCard from './DecisionCard'
import AnalysisMetrics from './AnalysisMetrics'
import '../App.css'

function AnalysisTemplate({
  baslik,           // Örn: "₿ Bitcoin (BTC)"
  yukleniyor,       // Yükleniyor durumu (true/false)
  veri,             // API'den dönen veri
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

      {/* Sonuç Alanı */}
      {yukleniyor ? (
        <div className="button-container">
          <div className="analiz-btn loading">
            Yapay Zeka Analiz Ediyor...
          </div>
        </div>
      ) : veri && veri.strateji ? (
        <div className="dashboard">

          <DecisionCard
            data={veri.strateji}
            sembol={veri.sembol}
            fiyat={veri.fiyat}
          />

          <AnalysisMetrics strateji={veri.strateji} />

        </div>
      ) : null}
    </div>
  )
}

export default AnalysisTemplate

