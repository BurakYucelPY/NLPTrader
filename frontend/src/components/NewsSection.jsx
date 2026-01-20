import React from 'react'

function NewsSection({ haberler }) {
  if (!haberler) return null;

  return (
    <div className="news-list">
      {haberler.map((haber, index) => (
        <div key={index} className="news-item">
          <p className="news-title">{haber.baslik}</p>
          <span className={`news-tag ${haber.skor > 0 ? 'pos' : 'neg'}`}>
            {haber.skor > 0 ? "Olumlu" : "Olumsuz"}
          </span>
        </div>
      ))}
    </div>
  )
}

export default NewsSection
