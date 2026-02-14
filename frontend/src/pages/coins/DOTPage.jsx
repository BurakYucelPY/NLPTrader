import { useState } from 'react'
import AnalysisTemplate from '../../components/AnalysisTemplate'

function DOTPage() {
  const [veri, setVeri] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(false)

  const analizBaslat = async () => {
    setYukleniyor(true)
    try {
      const cevap = await fetch("http://localhost:8000/fiyat/dot")
      const sonuc = await cevap.json()
      setVeri(sonuc)
    } catch (hata) {
      console.error("DOT Analiz hatası:", hata)
    } finally {
      setYukleniyor(false)
    }
  }

  return (
    <AnalysisTemplate
      baslik="● Polkadot (DOT)"
      yukleniyor={yukleniyor}
      veri={veri}
      analizBaslatFn={analizBaslat}
    />
  )
}

export default DOTPage
