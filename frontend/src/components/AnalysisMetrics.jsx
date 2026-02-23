import React from 'react'

function AnalysisMetrics({ strateji, coinRenk = '#007bff' }) {
  if (!strateji) return null;
  const { bilesenler, ham_veriler } = strateji;

  const kartStil = {
    borderTop: `3px solid ${coinRenk}`,
  }

  const skorStil = {
    color: coinRenk,
  }

  return (
    <div className="components-grid">

      {/* MACD KARTI */}
      <div className="component-card" style={kartStil}>
        <h3>📈 MACD (%30)</h3>
        <div className="component-score" style={skorStil}>
          {bilesenler.macd_puan}
        </div>
        <p>Histogram: {ham_veriler.macd_hist}</p>
      </div>

      {/* RSI KARTI */}
      <div className="component-card" style={kartStil}>
        <h3>⚡ RSI (%20)</h3>
        <div className="component-score" style={skorStil}>
          {bilesenler.rsi_puan}
        </div>
        <p>RSI Değeri: {ham_veriler.rsi_degeri}</p>
      </div>

      {/* OBV KARTI */}
      <div className="component-card" style={kartStil}>
        <h3>📊 OBV (%15)</h3>
        <div className="component-score" style={skorStil}>
          {bilesenler.obv_puan}
        </div>
        <p>Hacim Trendi: {ham_veriler.obv_trend > 0 ? "Yükseliş" : "Düşüş"}</p>
      </div>

      {/* VOLATİLİTE KARTI */}
      <div className="component-card" style={kartStil}>
        <h3>📉 Volatilite (%15)</h3>
        <div className="component-score" style={skorStil}>
          {bilesenler.volatilite_puan}
        </div>
        <p>Yıllık: %{ham_veriler.volatilite_yillik}</p>
      </div>

      {/* SENTIMENT KARTI */}
      <div className="component-card" style={kartStil}>
        <h3>📰 Haber (%20)</h3>
        <div className="component-score" style={skorStil}>
          {bilesenler.sentiment_puan}
        </div>
        <p>Kaynak: {ham_veriler.haber_kaynak}</p>
      </div>

    </div>
  )
}

export default AnalysisMetrics
