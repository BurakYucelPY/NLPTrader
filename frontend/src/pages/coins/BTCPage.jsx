import { useState } from 'react'
import AnalysisTemplate from '../../components/AnalysisTemplate'

function BTCPage() {
  const [veri, setVeri] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(false)

  const analizBaslat = async () => {
    setYukleniyor(true)
    try {
      const cevap = await fetch("http://localhost:5199/api/Finans/btc")
      const sonuc = await cevap.json()
      setVeri(sonuc)
    } catch (hata) {
      console.error("BTC Analiz hatası:", hata)
    } finally {
      setYukleniyor(false)
    }
  }

  return (
    <AnalysisTemplate
      baslik="₿ Bitcoin (BTC)"
      yukleniyor={yukleniyor}
      veri={veri}
      analizBaslatFn={analizBaslat}
    />
  )
}

export default BTCPage
