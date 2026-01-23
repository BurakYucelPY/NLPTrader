import React, { createContext, useContext, useState, useEffect, useRef } from 'react'

const NewsContext = createContext()

export function NewsProvider({ children }) {
  const [haberler, setHaberler] = useState([])
  const [yukleniyor, setYukleniyor] = useState(true)
  const [toplamSkor, setToplamSkor] = useState(null)
  const skorlarRef = useRef([])
  const baglaniyor = useRef(false)

  useEffect(() => {
    // Zaten haberler yüklendiyse veya bağlantı kuruluyorsa tekrar çekme
    if (haberler.length > 0 || baglaniyor.current) {
      setYukleniyor(false)
      return
    }
    baglaniyor.current = true

    console.log("SSE bağlantısı kuruluyor...")

    // Server-Sent Events ile canlı haber akışı
    const eventSource = new EventSource("http://localhost:8000/piyasa-durumu-stream")
    
    eventSource.onmessage = (event) => {
      if (event.data === "[DONE]") {
        setYukleniyor(false)
        eventSource.close()
        return
      }
      
      try {
        const haber = JSON.parse(event.data)
        
        // Haberi listeye ekle
        setHaberler(onceki => {
          const yeniListe = [...onceki, haber]
          // Skora göre sırala (en etkili haberler üstte)
          return yeniListe.sort((a, b) => Math.abs(b.skor) - Math.abs(a.skor))
        })
        
        // Ortalama skoru güncelle
        skorlarRef.current.push(haber.skor)
        const toplam = skorlarRef.current.reduce((acc, s) => acc + s, 0)
        setToplamSkor(toplam / skorlarRef.current.length)
        
      } catch (e) {
        console.error("Haber parse hatası:", e)
      }
    }

    eventSource.onopen = () => {
      console.log("SSE bağlantısı açıldı")
    }
    
    eventSource.onerror = (err) => {
      console.error("SSE bağlantı hatası:", err)
      baglaniyor.current = false
      setYukleniyor(false)
      eventSource.close()
    }
    
    return () => {
      eventSource.close()
    }
  }, [])

  return (
    <NewsContext.Provider value={{ haberler, yukleniyor, toplamSkor }}>
      {children}
    </NewsContext.Provider>
  )
}

export function useNews() {
  const context = useContext(NewsContext)
  if (!context) {
    throw new Error('useNews must be used within a NewsProvider')
  }
  return context
}
