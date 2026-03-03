import React from 'react'

function AssetCard({
  sembol,        // Örn: "BTC"
  ad,            // Örn: "Bitcoin"
  ikon,          // Emoji veya ikon
  renk,          // Kart rengi
  basariVerisi,  // Backend'den gelen başarı oranı verisi
  onClick        // Tıklama callback
}) {
  // Başarı oranına göre renk belirle
  const getBasariRenk = (oran) => {
    if (oran === null || oran === undefined) return '#888'
    if (oran >= 60) return '#00c853'
    if (oran >= 40) return '#ffc107'
    return '#ff5252'
  }

  const basariOrani = basariVerisi?.basari_orani
  const basariRenk = getBasariRenk(basariOrani)

  return (
    <div
      className="asset-card"
      onClick={() => onClick && onClick({ sembol, ad, ikon, renk })}
      style={{ borderColor: renk }}
    >
      <div className="asset-icon">{ikon}</div>
      <h3 className="asset-symbol">{sembol}</h3>
      <p className="asset-name">{ad}</p>

      {/* Başarı Oranı Badge */}
      {basariVerisi && (
        <div className="asset-success-badge" style={{ color: basariRenk, borderColor: basariRenk + '44' }}>
          {basariOrani !== null ? (
            <>
              <span className="success-icon">{basariOrani >= 60 ? '🟢' : basariOrani >= 40 ? '🟡' : '🔴'}</span>
              <span className="success-rate">%{basariOrani}</span>
            </>
          ) : (
            <span className="success-waiting">⏳ Veri Bekleniyor</span>
          )}
        </div>
      )}

      <div className="asset-arrow">→</div>
    </div>
  )
}

export default AssetCard

