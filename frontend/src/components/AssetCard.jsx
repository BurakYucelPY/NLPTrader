import React from 'react'

function AssetCard({
  sembol,        // Örn: "BTC"
  ad,            // Örn: "Bitcoin"
  ikon,          // Emoji veya ikon
  renk,          // Kart rengi
  onClick        // Tıklama callback
}) {
  return (
    <div
      className="asset-card"
      onClick={() => onClick && onClick({ sembol, ad, ikon, renk })}
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
