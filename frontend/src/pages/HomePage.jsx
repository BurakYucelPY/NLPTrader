import { useNavigate } from 'react-router-dom'
import { ROUTES } from '../routes/AppRoutes.jsx'
import '../App.css'

function HomePage() {
  const navigate = useNavigate()

  const handleAssetClick = (asset) => {
    navigate(ROUTES.ANALYSIS)
  }

  return (
    <div className="container" style={{ justifyContent: 'center' }}>
      <h1 className="title">🤖 NLPTrader</h1>
      <button 
        className="analiz-btn" 
        onClick={() => handleAssetClick('BTC')}
        style={{ padding: '20px 60px', fontSize: '24px' }}
      >
        BTC
      </button>
    </div>
  )
}

export default HomePage
