import React from 'react'
import AssetCard from '../components/AssetCard'
import { ROUTES } from '../routes/AppRoutes.jsx'
import '../App.css'

function HomePage() {
  // İleride buraya yeni coinler eklenecek
  const varlıklar = [
    {
      sembol: 'BTC',
      ad: 'Bitcoin',
      ikon: '₿',
      renk: '#f7931a',
      rota: ROUTES.ANALYSIS
    },
    // İleride eklenecekler:
    // { sembol: 'ETH', ad: 'Ethereum', ikon: 'Ξ', renk: '#627eea', rota: '/eth' },
    // { sembol: 'SOL', ad: 'Solana', ikon: '◎', renk: '#14f195', rota: '/sol' },
  ]

  return (
    <div className="container" style={{ justifyContent: 'center' }}>
      <h1 className="title">🤖 NLPTrader</h1>
      <p style={{ color: '#aaa', marginBottom: '40px', fontSize: '1.1rem' }}>
        Yapay zeka destekli kripto analizi
      </p>
      
      <div className="assets-grid">
        {varlıklar.map((varlik) => (
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
