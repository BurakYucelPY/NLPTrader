import React from 'react'

function NewsSection({ haberler }) {
  if (!haberler) return null;

  return (
    <div className="news-section">
      <h4>Analiz Edilen Son Haberler</h4>
      {haberler.map((haber, index) => (
        <div key={index} className="news-item">
          <span className="news-title">{haber.baslik.substring(0, 100)}...</span>
          <span className={`news-tag ${haber.skor > 0 ? 'pos' : 'neg'}`}>
            {haber.skor > 0 ? "Olumlu" : "Olumsuz"}
          </span>
        </div>
      ))}
    </div>
  )
}

export default NewsSection
