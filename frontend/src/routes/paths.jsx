// Route path sabitleri
export const ROUTES = {
  HOME: '/',
  COIN: '/:coinId',
}

// Desteklenen tüm kripto paralar
export const KRIPTO_LISTESI = [
  { sembol: 'BTC', ad: 'Bitcoin', ikon: '₿', renk: '#f7931a', rota: '/btc' },
  { sembol: 'ETH', ad: 'Ethereum', ikon: 'Ξ', renk: '#627eea', rota: '/eth' },
  { sembol: 'BNB', ad: 'Binance Coin', ikon: '🔶', renk: '#f3ba2f', rota: '/bnb' },
  { sembol: 'SOL', ad: 'Solana', ikon: '◎', renk: '#14f195', rota: '/sol' },
  { sembol: 'XRP', ad: 'Ripple', ikon: '✕', renk: '#23292f', rota: '/xrp' },
  { sembol: 'DOGE', ad: 'Dogecoin', ikon: '🐕', renk: '#c2a633', rota: '/doge' },
  { sembol: 'ADA', ad: 'Cardano', ikon: '🔵', renk: '#0033ad', rota: '/ada' },
  { sembol: 'AVAX', ad: 'Avalanche', ikon: '🔺', renk: '#e84142', rota: '/avax' },
  { sembol: 'SHIB', ad: 'Shiba Inu', ikon: '🐶', renk: '#ffa409', rota: '/shib' },
  { sembol: 'TRX', ad: 'Tron', ikon: '⚡', renk: '#ff0013', rota: '/trx' },
  { sembol: 'DOT', ad: 'Polkadot', ikon: '●', renk: '#e6007a', rota: '/dot' },
  { sembol: 'LINK', ad: 'Chainlink', ikon: '⬡', renk: '#2a5ada', rota: '/link' },
  { sembol: 'LTC', ad: 'Litecoin', ikon: 'Ł', renk: '#bfbbbb', rota: '/ltc' },
  { sembol: 'BCH', ad: 'Bitcoin Cash', ikon: '₿', renk: '#8dc351', rota: '/bch' },
  { sembol: 'NEAR', ad: 'Near Protocol', ikon: 'Ⓝ', renk: '#00c1de', rota: '/near' },
  { sembol: 'FET', ad: 'Fetch.ai', ikon: '🤖', renk: '#1d2951', rota: '/fet' },
]
