import { useState, useEffect } from 'react'
import { useParams, useLocation, Navigate } from 'react-router-dom'
import AnalysisTemplate from '../components/AnalysisTemplate'
import { KRIPTO_LISTESI } from '../routes/paths.jsx'
import { API_BASE } from '../config/api'

function CoinPage() {
    const { coinId } = useParams()
    const location = useLocation()
    const [veri, setVeri] = useState(null)
    const [yukleniyor, setYukleniyor] = useState(false)

    // URL'deki coinId'ye göre kripto bilgisini bul
    const kripto = KRIPTO_LISTESI.find(
        (k) => k.sembol.toLowerCase() === coinId?.toLowerCase()
    )

    useEffect(() => {
        if (!kripto) return

        // Eğer HomePage'den veri ile geldiyse, direkt kullan
        if (location.state?.analizVeri) {
            setVeri(location.state.analizVeri)
            return
        }

        // Doğrudan URL'den geldiyse, API'den çek
        const analizBaslat = async () => {
            setYukleniyor(true)
            try {
                const cevap = await fetch(`${API_BASE}/fiyat/${kripto.sembol.toLowerCase()}`)
                const sonuc = await cevap.json()
                setVeri(sonuc)
            } catch (hata) {
                console.error(`${kripto.sembol} Analiz hatası:`, hata)
            } finally {
                setYukleniyor(false)
            }
        }

        analizBaslat()
    }, [coinId])

    // Geçersiz coin ise ana sayfaya yönlendir
    if (!kripto) {
        return <Navigate to="/" replace />
    }

    return (
        <AnalysisTemplate
            baslik={`${kripto.ikon} ${kripto.ad} (${kripto.sembol})`}
            yukleniyor={yukleniyor}
            veri={veri}
            coinRenk={kripto.renk}
            coinSembol={kripto.ikon}
            coinSembolStr={kripto.sembol}
        />
    )
}

export default CoinPage
