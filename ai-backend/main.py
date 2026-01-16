from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
import feedparser

app = FastAPI()

class AnalizIstegi(BaseModel):
    metin: str

# 1. MANUEL ANALİZ (Senin elinle yazdığın)
@app.post("/analiz")
def analiz_et(istek: AnalizIstegi):
    blob = TextBlob(istek.metin)
    return {"skor": blob.sentiment.polarity, "karar": "Olumlu" if blob.sentiment.polarity > 0 else "Olumsuz"}

# 2. OTOMATİK HABER ANALİZİ (YENİ)
@app.get("/piyasa-durumu")
def piyasa_durumu():
    # Cointelegraph Bitcoin RSS Beslemesi
    rss_url = "https://cointelegraph.com/rss/tag/bitcoin"
    feed = feedparser.parse(rss_url)
    
    toplam_skor = 0
    haber_sayisi = 0
    analiz_edilenler = []

    # İlk 5 haberi çek ve analiz et
    for entry in feed.entries[:5]:
        baslik = entry.title
        blob = TextBlob(baslik)
        skor = blob.sentiment.polarity
        
        toplam_skor += skor
        haber_sayisi += 1
        
        analiz_edilenler.append({
            "baslik": baslik,
            "skor": skor,
            "karar": "Olumlu" if skor > 0 else "Nötr/Olumsuz"
        })

    # Genel ortalamayı al
    ortalama_skor = toplam_skor / haber_sayisi if haber_sayisi > 0 else 0
    
    genel_karar = "Nötr"
    if ortalama_skor > 0.05: genel_karar = "Piyasa Çoşkulu (Boğa)"
    elif ortalama_skor < -0.05: genel_karar = "Piyasa Tedirgin (Ayı)"

    return {
        "genel_skor": round(ortalama_skor, 3),
        "genel_karar": genel_karar,
        "kaynak": "Cointelegraph RSS",
        "detaylar": analiz_edilenler
    }

# 3. FİYAT VE TEKNİK ANALİZ
@app.get("/fiyat/{sembol}")
def fiyat_getir(sembol: str):
    try:
        ticker = f"{sembol.upper()}-USD"
        stock = yf.Ticker(ticker)
        df = stock.history(period="1mo", interval="1d")

        if df.empty: return {"hata": "Veri bulunamadı"}

        current_price = df['Close'].iloc[-1]
        
        # Teknik Göstergeler
        rsi = RSIIndicator(close=df['Close'], window=14).rsi().iloc[-1]
        macd = MACD(close=df['Close']).macd_diff().iloc[-1]

        sinyal = "Bekle"
        if rsi < 30 and macd > 0: sinyal = "GUCLU AL"
        elif rsi < 40: sinyal = "AL"
        elif rsi > 70: sinyal = "SAT"
        
        return {
            "sembol": sembol.upper(),
            "fiyat": round(current_price, 2),
            "teknik_analiz": {
                "rsi": round(rsi, 2),
                "macd_durum": "Pozitif" if macd > 0 else "Negatif",
                "sinyal": sinyal
            }
        }
    except Exception as e:
        return {"hata": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)