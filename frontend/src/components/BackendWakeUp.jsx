import { useState, useEffect } from 'react'
import { API_BASE } from '../config/api'
import './BackendWakeUp.css'

/**
 * Backend Wake-Up Overlay
 * Render free tier uyku modundan uyanana kadar
 * bulanık arka planlı loading ekranı gösterir.
 */
function BackendWakeUp() {
    const [backendHazir, setBackendHazir] = useState(false)
    const [fadeOut, setFadeOut] = useState(false)
    const [denemeSayisi, setDenemeSayisi] = useState(0)
    const [gizle, setGizle] = useState(false)

    useEffect(() => {
        let iptal = false
        let timer = null

        const kontrolEt = async () => {
            try {
                const cevap = await fetch(`${API_BASE}/health`, {
                    method: 'GET',
                    signal: AbortSignal.timeout(5000)
                })
                const veri = await cevap.json()

                if (!iptal && veri.status === 'ok') {
                    setBackendHazir(true)
                    setFadeOut(true)
                    // Fade-out animasyonu bittikten sonra DOM'dan kaldır
                    setTimeout(() => {
                        if (!iptal) setGizle(true)
                    }, 700)
                    return
                }
            } catch {
                // Backend henüz uyanmadı, tekrar dene
            }

            if (!iptal) {
                setDenemeSayisi(s => s + 1)
                timer = setTimeout(kontrolEt, 3000)
            }
        }

        kontrolEt()

        return () => {
            iptal = true
            if (timer) clearTimeout(timer)
        }
    }, [])

    // Backend zaten hazırsa veya animasyon bittiyse hiçbir şey gösterme
    if (gizle) return null

    return (
        <div className={`wakeup-overlay ${fadeOut ? 'fade-out' : ''}`}>
            <div className="wakeup-content">
                {/* NLPTrader Başlık */}
                <h1 className="home-title" style={{ marginBottom: '32px' }}>
                    <span className="home-title-accent">NLP</span>Trader
                </h1>

                {/* Arkadaki pulse halkası */}
                <div className="wakeup-pulse" />

                {/* Dönen spinner */}
                <div className="wakeup-spinner" />

                {/* Metin */}
                <p className="wakeup-title">
                    Sunucu başlatılıyor
                    <span className="wakeup-dots">
                        <span /><span /><span />
                    </span>
                </p>
                <p className="wakeup-subtitle">Ücretsiz sunucu kullanıldığı için uyanması biraz zaman alabilir</p>

                {/* İlerleme çubuğu */}
                <div className="wakeup-progress">
                    <div className="wakeup-progress-bar" />
                </div>


            </div>
        </div>
    )
}

export default BackendWakeUp
