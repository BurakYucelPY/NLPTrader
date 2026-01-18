import React from 'react'
import { useNavigate } from 'react-router-dom'

function AssetCard({ 
  sembol,        // Örn: "BTC"
  ad,            // Örn: "Bitcoin"
  ikon,          // Emoji veya ikon
  renk,          // Kart rengi
  rotaYolu       // Yönlendirilecek sayfa
}) {
  const navigate = useNavigate()

  return (
    <div 
      className="asset-card"
      onClick={() => navigate(rotaYolu)}
      style={{ borderColor: renk }}
    >
      <div className="asset-icon">{ikon}</div>
      <h3 className="asset-symbol">{sembol}</h3>
      <p className="asset-name">{ad}</p>
      <div className="asset-arrow">→</div>
    </div>
  )
}

export default AssetCard
