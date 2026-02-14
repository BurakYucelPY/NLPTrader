import { useState } from 'react'
import AnalysisTemplate from '../../components/AnalysisTemplate'

function AVAXPage() {
  const [veri, setVeri] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(false)

  const analizBaslat = async () => {
    setYukleniyor(true)
    try {
      const cevap = await fetch("http://localhost:8000/fiyat/avax")
      const sonuc = await cevap.json()
      setVeri(sonuc)
    } catch (hata) {
      console.error("AVAX Analiz hatası:", hata)
    } finally {
      setYukleniyor(false)
    }
  }

  return (
    <AnalysisTemplate
      baslik="🔺 Avalanche (AVAX)"
      yukleniyor={yukleniyor}
      veri={veri}
      analizBaslatFn={analizBaslat}
    />
  )
}

export default AVAXPage
