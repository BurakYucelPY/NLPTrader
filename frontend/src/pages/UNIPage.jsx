import { useState } from 'react'
import AnalysisTemplate from '../components/AnalysisTemplate'

function UNIPage() {
  const [veri, setVeri] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(false)

  const analizBaslat = async () => {
    setYukleniyor(true)
    try {
      const cevap = await fetch("http://localhost:5199/api/Finans/uni")
      const sonuc = await cevap.json()
      setVeri(sonuc)
    } catch (hata) {
      console.error("UNI Analiz hatası:", hata)
    } finally {
      setYukleniyor(false)
    }
  }

  return (
    <AnalysisTemplate
      baslik="🦄 Uniswap (UNI)"
      yukleniyor={yukleniyor}
      veri={veri}
      analizBaslatFn={analizBaslat}
    />
  )
}

export default UNIPage
