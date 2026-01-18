import React from 'react'

function DecisionCard({ data, sembol, fiyat }) {
  if (!data) return null;

  return (
    <div className="decision-card" style={{ 
      borderColor: data.karar_renk, 
      boxShadow: `0 0 20px ${data.karar_renk}40` 
    }}>
      <h2>NİHAİ KARAR ({sembol})</h2>
      <div className="decision-text" style={{ color: data.karar_renk }}>
        {data.karar}
      </div>
      <div className="score-info">
        Skor: <strong>{data.toplam_skor}</strong> | Fiyat: <strong>${fiyat}</strong>
      </div>
    </div>
  )
}

export default DecisionCard
