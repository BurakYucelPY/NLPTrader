import { useState } from 'react'
import AnalysisTemplate from '../components/AnalysisTemplate'

function PEPEPage() {
  const [veri, setVeri] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(false)

  const analizBaslat = async () => {
    setYukleniyor(true)
    try {
      const cevap = await fetch("http://localhost:5199/api/Finans/pepe")
      const sonuc = await cevap.json()
      setVeri(sonuc)
    } catch (hata) {
      console.error("PEPE Analiz hatası:", hata)
    } finally {
      setYukleniyor(false)
    }
  }

  return (
    <AnalysisTemplate
      baslik="🐸 Pepe (PEPE)"
      yukleniyor={yukleniyor}
      veri={veri}
      analizBaslatFn={analizBaslat}
    />
  )
}

export default PEPEPage
