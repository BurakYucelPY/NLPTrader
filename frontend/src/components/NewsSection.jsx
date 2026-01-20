import React from 'react'

function NewsSection({ haberler }) {
  if (!haberler || haberler.length === 0) return null;

  const getSkorRenk = (skor) => {
    if (skor > 0.2) return '#00c853'
    if (skor > 0) return '#69f0ae'
    if (skor < -0.2) return '#ff5252'
    if (skor < 0) return '#ffab91'
    return '#888'
  }

  return (
    <div className="news-list">
      {haberler.map((haber, index) => (
        <div 
          key={index} 
          className="news-item"
          style={{ 
            animationDelay: `${index * 0.05}s`,
            borderLeft: `3px solid ${getSkorRenk(haber.skor)}`
          }}
        >
          <div className="news-content">
            <p className="news-title">{haber.baslik}</p>
            <div className="news-meta">
              <span 
                className="news-score"
                style={{ color: getSkorRenk(haber.skor) }}
              >
                {haber.skor > 0 ? '+' : ''}{(haber.skor * 100).toFixed(0)}%
              </span>
              <span className={`news-tag ${haber.skor > 0 ? 'pos' : (haber.skor < 0 ? 'neg' : 'neutral')}`}>
                {haber.skor > 0 ? "Olumlu" : (haber.skor < 0 ? "Olumsuz" : "Nötr")}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default NewsSection
