import React from 'react'

function AnalysisMetrics({ strateji }) {
  if (!strateji) return null;
  const { bilesenler, ham_veriler } = strateji;

  return (
    <div className="components-grid">
      
      {/* MACD KARTI */}
      <div className="component-card macd">
        <h3>📈 MACD (%50)</h3>
        <div className="component-score">
          {bilesenler.macd_puan}
        </div>
        <p>Histogram Gücü: {ham_veriler.macd_hist}</p>
      </div>

      {/* RSI KARTI */}
      <div className="component-card rsi">
        <h3>⚡ RSI (%30)</h3>
        <div className="component-score">
          {bilesenler.rsi_puan}
        </div>
        <p>RSI Değeri: {ham_veriler.rsi_degeri}</p>
      </div>

      {/* SENTIMENT KARTI */}
      <div className="component-card sentiment">
        <h3>📰 Haber (%20)</h3>
        <div className="component-score">
          {bilesenler.sentiment_puan}
        </div>
        <p>Kaynak: {ham_veriler.haber_kaynak}</p>
      </div>

    </div>
  )
}

export default AnalysisMetrics
