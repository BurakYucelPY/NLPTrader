import React from 'react'
import AssetCard from '../components/AssetCard'
import { KRIPTO_LISTESI } from '../routes/paths.jsx'
import '../App.css'

function HomePage() {
  return (
    <div className="container" style={{ justifyContent: 'flex-start', paddingTop: '40px' }}>
      <h1 className="title">🤖 NLPTrader</h1>
      <p style={{ color: '#aaa', marginBottom: '40px', fontSize: '1.1rem' }}>
        Yapay zeka destekli kripto analizi • {KRIPTO_LISTESI.length} Kripto Para
      </p>
      
      <div className="assets-grid">
        {KRIPTO_LISTESI.map((varlik) => (
          <AssetCard
            key={varlik.sembol}
            sembol={varlik.sembol}
            ad={varlik.ad}
            ikon={varlik.ikon}
            renk={varlik.renk}
            rotaYolu={varlik.rota}
          />
        ))}
      </div>
    </div>
  )
}

export default HomePage
