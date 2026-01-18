import { useState } from 'react'
import AnalysisTemplate from '../components/AnalysisTemplate'

function ADAPage() {
  const [veri, setVeri] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(false)

  const analizBaslat = async () => {
    setYukleniyor(true)
    try {
      const cevap = await fetch("http://localhost:5199/api/Finans/ada")
      const sonuc = await cevap.json()
      setVeri(sonuc)
    } catch (hata) {
      console.error("ADA Analiz hatası:", hata)
    } finally {
      setYukleniyor(false)
    }
  }

  return (
    <AnalysisTemplate
      baslik="🔵 Cardano (ADA)"
      yukleniyor={yukleniyor}
      veri={veri}
      analizBaslatFn={analizBaslat}
    />
  )
}

export default ADAPage
