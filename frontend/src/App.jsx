import { useState } from 'react'

function App() {
  // Verileri tutacağımız kutular
  const [fiyat, setFiyat] = useState("Yükleniyor...")
  const [analiz, setAnaliz] = useState(null)

  // C#'tan veriyi çeken fonksiyon
  const veriCek = async () => {
    try {
      setFiyat("Güncelleniyor...")
      
      // Backend'e istek atıyoruz (5199 portuna)
      const cevap = await fetch("http://localhost:5199/api/Finans/btc")
      const veri = await cevap.json()

      // Gelen veriyi kutulara koyuyoruz
      setFiyat(veri.fiyat)
      setAnaliz(veri.teknik_analiz)
      
    } catch (hata) {
      console.log("Hata oluştu:", hata)
      setFiyat("Hata! Backend çalışıyor mu?")
    }
  }

  return (
    <div style={{ padding: "50px", fontFamily: "sans-serif" }}>
      <h1>Borsa Paneli Test</h1>
      
      <div style={{ border: "1px solid #ddd", padding: "20px", borderRadius: "10px", maxWidth: "400px" }}>
        <h2>Bitcoin (BTC)</h2>
        <h3 style={{ color: "green" }}>${fiyat}</h3>

        {analiz && (
          <div style={{ background: "#f9f9f9", padding: "10px", marginTop: "10px" }}>
            <p><strong>RSI:</strong> {analiz.rsi}</p>
            <p><strong>MACD:</strong> {analiz.macd_durum}</p>
            <p><strong>Sinyal:</strong> {analiz.sinyal}</p>
          </div>
        )}

        <button 
          onClick={veriCek}
          style={{ 
            marginTop: "15px", 
            padding: "10px 20px", 
            background: "black", 
            color: "white", 
            border: "none", 
            cursor: "pointer" 
          }}
        >
          Veriyi Getir
        </button>
      </div>
    </div>
  )
}

export default App