import { useState } from 'react'
import AnalysisTemplate from '../components/AnalysisTemplate'

function BTCPage() {
  const [veri, setVeri] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(false)

  const btcAnaliziniBaslat = async () => {
    setYukleniyor(true)
    try {
      const cevap = await fetch("http://localhost:5199/api/Finans/btc")
      const sonuc = await cevap.json()
      
      console.log("BTC Verisi alındı:", sonuc)
      setVeri(sonuc)
    } catch (hata) {
      console.error("BTC Analiz hatası:", hata)
    } finally {
      setYukleniyor(false)
    }
  }

  return (
    <AnalysisTemplate
      baslik="🤖 NLPTrader (BTC)"
      yukleniyor={yukleniyor}
      veri={veri}
      analizBaslatFn={btcAnaliziniBaslat}
    />
  )
}

export default BTCPage
