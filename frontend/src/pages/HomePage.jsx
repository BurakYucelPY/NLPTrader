import React, { useState, useMemo, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import AssetCard from '../components/AssetCard'
import NewsSection from '../components/NewsSection'
import PixelBlast from '../components/PixelBlast'
import { KRIPTO_LISTESI } from '../routes/paths.jsx'
import { useNews } from '../context/NewsContext.jsx'
import '../App.css'

function HomePage() {
  const navigate = useNavigate()
  const { haberler, yukleniyor, toplamSkor } = useNews()

  // Overlay state (sadece yükleme ekranı)
  const [secilenCoin, setSecilenCoin] = useState(null)

  // Parçacıklar (overlay arka planı için)
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

  // Coin tıklama — overlay aç, analiz et, bitince sayfaya yönlendir
  const coinTiklandi = useCallback(async (coin) => {
    setSecilenCoin(coin)

    try {
      const cevap = await fetch(`http://localhost:5199/api/Finans/${coin.sembol.toLowerCase()}`)
      const sonuc = await cevap.json()
      // Analiz bitti — coin sayfasına yönlendir, veriyi state ile taşı
      navigate(`/${coin.sembol.toLowerCase()}`, { state: { analizVeri: sonuc } })
    } catch (hata) {
      console.error(`${coin.sembol} Analiz hatası:`, hata)
    } finally {
      setSecilenCoin(null)
    }
  }, [navigate])

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

      {/* PixelBlast Tüm Ekran Arka Plan */}
      <div className="pixel-blast-bg">
        <PixelBlast
          variant="square"
          pixelSize={4}
          color="#B19EEF"
          patternScale={2}
          patternDensity={1}
          pixelSizeJitter={0}
          enableRipples
          rippleSpeed={0.4}
          rippleThickness={0.12}
          rippleIntensityScale={1.5}
          liquid={false}
          liquidStrength={0.12}
          liquidRadius={1.2}
          liquidWobbleSpeed={5}
          speed={0.5}
          edgeFade={0.25}
          transparent
        />
      </div>

      {/* SOL TARAF: Coinler */}
      <div className="coins-panel">

        <div className="home-hero" style={{ position: 'relative', zIndex: 2 }}>
          <h1 className="home-title">
            <span className="home-title-accent">NLP</span>Trader
          </h1>
          <p className="home-subtitle">Yapay zeka destekli kripto analiz platformu</p>
        </div>

        <div className="assets-grid" style={{ position: 'relative', zIndex: 2 }}>
          {KRIPTO_LISTESI.map((varlik) => (
            <AssetCard
              key={varlik.sembol}
              sembol={varlik.sembol}
              ad={varlik.ad}
              ikon={varlik.ikon}
              renk={varlik.renk}
              onClick={coinTiklandi}
            />
          ))}
        </div>
      </div>

      {/* SAĞ TARAF: Haber Paneli */}
      <div className="news-panel">
        <div className="news-header">
          <h3 className="news-panel-title">Piyasa Gündemi</h3>
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

      {/* ========== YÜKLEME OVERLAY (Sadece analiz sırasında) ========== */}
      {secilenCoin && (
        <div className="coin-overlay">
          <div
            className="coin-overlay-content"
            style={{
              background: `
                radial-gradient(ellipse at 20% 0%, ${secilenCoin.renk}18 0%, transparent 50%),
                radial-gradient(ellipse at 80% 100%, ${secilenCoin.renk}12 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, ${secilenCoin.renk}08 0%, transparent 70%),
                linear-gradient(180deg, #1a1a2e 0%, #16162a 100%)
              `,
            }}
          >
            {/* Üst Glow Çizgisi */}
            <div
              className="coin-glow-line"
              style={{
                background: `linear-gradient(90deg, transparent 0%, ${secilenCoin.renk} 50%, transparent 100%)`,
              }}
            />

            {/* Watermark */}
            <div className="coin-watermark" style={{ color: secilenCoin.renk }}>
              {secilenCoin.ikon}
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
                  backgroundColor: p.isSembol ? undefined : secilenCoin.renk,
                  color: p.isSembol ? secilenCoin.renk : undefined,
                  opacity: p.opacity,
                }}
              >
                {p.isSembol ? secilenCoin.ikon : ''}
              </div>
            ))}

            {/* Corner Glows */}
            <div
              className="coin-corner-glow coin-corner-glow-tl"
              style={{ background: `radial-gradient(circle, ${secilenCoin.renk}15 0%, transparent 70%)` }}
            />
            <div
              className="coin-corner-glow coin-corner-glow-br"
              style={{ background: `radial-gradient(circle, ${secilenCoin.renk}10 0%, transparent 70%)` }}
            />

            {/* Loading İçerik */}
            <h1 className="overlay-title">
              {secilenCoin.ikon} {secilenCoin.ad} ({secilenCoin.sembol})
            </h1>

            <div className="overlay-loading">
              <div className="overlay-spinner" style={{ borderTopColor: secilenCoin.renk }}>
                <span className="overlay-spinner-icon">{secilenCoin.ikon}</span>
              </div>
              <p className="overlay-loading-text">
                Yapay Zeka <strong style={{ color: secilenCoin.renk }}>{secilenCoin.sembol}</strong> Analiz Ediyor...
              </p>
              <div className="overlay-loading-bar">
                <div className="overlay-loading-bar-fill" style={{ background: `linear-gradient(90deg, ${secilenCoin.renk}, ${secilenCoin.renk}66)` }} />
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  )
}

export default HomePage
