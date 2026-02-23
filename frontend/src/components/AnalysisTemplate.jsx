import React, { useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { ROUTES } from '../routes/AppRoutes.jsx'
import DecisionCard from './DecisionCard'
import AnalysisMetrics from './AnalysisMetrics'
import '../App.css'

function AnalysisTemplate({
  baslik,
  yukleniyor,
  veri,
  coinRenk = '#007bff',
  coinSembol = '●',
}) {
  const navigate = useNavigate()

  const parcaciklar = useMemo(() => {
    return Array.from({ length: 18 }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      delay: Math.random() * 8,
      duration: 6 + Math.random() * 10,
      size: 18 + Math.random() * 22,
      opacity: 0.06 + Math.random() * 0.14,
      isSembol: i < 5,
    }))
  }, [])

  return (
    <>
      {/* Geri Butonu — container dışında, fixed pozisyon */}
      <button
        onClick={() => navigate(ROUTES.HOME)}
        className="back-btn"
      >
        ← Geri
      </button>

      <div
        className="container coin-page-bg"
        style={{
          background: `
            radial-gradient(ellipse at 20% 0%, ${coinRenk}18 0%, transparent 50%),
            radial-gradient(ellipse at 80% 100%, ${coinRenk}12 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, ${coinRenk}08 0%, transparent 70%),
            linear-gradient(180deg, #1a1a2e 0%, #16162a 100%)
          `,
        }}
      >
        {/* Üst Glow Çizgisi */}
        <div
          className="coin-glow-line"
          style={{
            background: `linear-gradient(90deg, transparent 0%, ${coinRenk} 50%, transparent 100%)`,
          }}
        />

        {/* Watermark */}
        <div className="coin-watermark" style={{ color: coinRenk }}>
          {coinSembol}
        </div>

        {/* Yüzen Parçacıklar */}
        {parcaciklar.map((p) => (
          <div
            key={p.id}
            className="coin-particle"
            style={{
              left: `${p.left}%`,
              animationDelay: `${p.delay}s`,
              animationDuration: `${p.duration}s`,
              fontSize: p.isSembol ? `${p.size}px` : undefined,
              width: p.isSembol ? undefined : `${p.size}px`,
              height: p.isSembol ? undefined : `${p.size}px`,
              borderRadius: p.isSembol ? undefined : '50%',
              backgroundColor: p.isSembol ? undefined : coinRenk,
              color: p.isSembol ? coinRenk : undefined,
              opacity: p.opacity,
            }}
          >
            {p.isSembol ? coinSembol : ''}
          </div>
        ))}

        {/* Corner Glow Effects */}
        <div
          className="coin-corner-glow coin-corner-glow-tl"
          style={{ background: `radial-gradient(circle, ${coinRenk}15 0%, transparent 70%)` }}
        />
        <div
          className="coin-corner-glow coin-corner-glow-br"
          style={{ background: `radial-gradient(circle, ${coinRenk}10 0%, transparent 70%)` }}
        />

        {/* Başlık */}
        <h1 className="title">{baslik}</h1>

        {/* Sonuç Alanı */}
        {yukleniyor ? (
          <div className="button-container">
            <div
              className="analiz-btn loading"
              style={{
                background: `linear-gradient(45deg, ${coinRenk}, ${coinRenk}bb)`,
                boxShadow: `0 4px 25px ${coinRenk}55`,
              }}
            >
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
            <AnalysisMetrics strateji={veri.strateji} coinRenk={coinRenk} />
          </div>
        ) : null}
      </div>
    </>
  )
}

export default AnalysisTemplate
