import { useState } from 'react'
import AnalysisTemplate from '../../components/AnalysisTemplate'

function LINKPage() {
  const [veri, setVeri] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(false)

  const analizBaslat = async () => {
    setYukleniyor(true)
    try {
      const cevap = await fetch("http://localhost:8000/fiyat/link")
      const sonuc = await cevap.json()
      setVeri(sonuc)
    } catch (hata) {
      console.error("LINK Analiz hatası:", hata)
    } finally {
      setYukleniyor(false)
    }
  }

  return (
    <AnalysisTemplate
      baslik="⬡ Chainlink (LINK)"
      yukleniyor={yukleniyor}
      veri={veri}
      analizBaslatFn={analizBaslat}
    />
  )
}

export default LINKPage
