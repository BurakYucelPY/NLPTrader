import { useState } from 'react'
import AnalysisTemplate from '../../components/AnalysisTemplate'

function ETHPage() {
  const [veri, setVeri] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(false)

  const analizBaslat = async () => {
    setYukleniyor(true)
    try {
      const cevap = await fetch("http://localhost:8000/fiyat/eth")
      const sonuc = await cevap.json()
      setVeri(sonuc)
    } catch (hata) {
      console.error("ETH Analiz hatası:", hata)
    } finally {
      setYukleniyor(false)
    }
  }

  return (
    <AnalysisTemplate
      baslik="Ξ Ethereum (ETH)"
      yukleniyor={yukleniyor}
      veri={veri}
      analizBaslatFn={analizBaslat}
    />
  )
}

export default ETHPage
