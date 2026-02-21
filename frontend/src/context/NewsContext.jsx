import React, { createContext, useContext, useState, useEffect, useRef, useCallback } from 'react'

const NewsContext = createContext()

export function NewsProvider({ children }) {
  const [haberler, setHaberler] = useState([])
  const [yukleniyor, setYukleniyor] = useState(true)
  const [toplamSkor, setToplamSkor] = useState(null)
  const [hata, setHata] = useState(false)
  const skorlarRef = useRef([])
  const retryCountRef = useRef(0)
  const maxRetry = 3

  const baglan = useCallback(() => {
    setYukleniyor(true)
    setHata(false)

    console.log("SSE bağlantısı kuruluyor... (deneme:", retryCountRef.current + 1, ")")

    const eventSource = new EventSource("http://localhost:5199/api/Haber/stream")

    eventSource.onmessage = (event) => {
      if (event.data === "[DONE]") {
        setYukleniyor(false)
        eventSource.close()
        return
      }

      try {
        const haber = JSON.parse(event.data)

        setHaberler(onceki => {
          const yeniListe = [...onceki, haber]
          return yeniListe.sort((a, b) => Math.abs(b.skor) - Math.abs(a.skor))
        })

        skorlarRef.current.push(haber.skor)
        const toplam = skorlarRef.current.reduce((acc, s) => acc + s, 0)
        setToplamSkor(toplam / skorlarRef.current.length)

      } catch (e) {
        console.error("Haber parse hatası:", e)
      }
    }

    eventSource.onopen = () => {
      console.log("SSE bağlantısı açıldı")
      retryCountRef.current = 0
    }

    eventSource.onerror = (err) => {
      console.error("SSE bağlantı hatası:", err)
      eventSource.close()

      // Retry mekanizması
      if (retryCountRef.current < maxRetry) {
        retryCountRef.current += 1
        console.log(`${3} saniye sonra tekrar deneniyor...`)
        setTimeout(() => baglan(), 3000)
      } else {
        setYukleniyor(false)
        setHata(true)
      }
    }

    return eventSource
  }, [])

  useEffect(() => {
    if (haberler.length > 0) {
      setYukleniyor(false)
      return
    }

    const es = baglan()
    return () => { if (es) es.close() }
  }, [])

  // Manuel yeniden deneme
  const yenidenDene = useCallback(() => {
    retryCountRef.current = 0
    skorlarRef.current = []
    setHaberler([])
    setToplamSkor(null)
    baglan()
  }, [baglan])

  return (
    <NewsContext.Provider value={{ haberler, yukleniyor, toplamSkor, hata, yenidenDene }}>
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
