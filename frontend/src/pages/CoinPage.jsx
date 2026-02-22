import { useState, useEffect } from 'react'
import { useParams, Navigate } from 'react-router-dom'
import AnalysisTemplate from '../components/AnalysisTemplate'
import { KRIPTO_LISTESI } from '../routes/paths.jsx'

function CoinPage() {
    const { coinId } = useParams()
    const [veri, setVeri] = useState(null)
    const [yukleniyor, setYukleniyor] = useState(false)

    // URL'deki coinId'ye göre kripto bilgisini bul
    const kripto = KRIPTO_LISTESI.find(
        (k) => k.sembol.toLowerCase() === coinId?.toLowerCase()
    )

    useEffect(() => {
        if (!kripto) return

        const analizBaslat = async () => {
            setYukleniyor(true)
            try {
                const cevap = await fetch(`http://localhost:5199/api/Finans/${kripto.sembol.toLowerCase()}`)
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
        />
    )
}

export default CoinPage
