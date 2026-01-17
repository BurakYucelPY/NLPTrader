from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
import feedparser
import requests # YENİ: Daha güçlü internet bağlantısı için

app = FastAPI()

class AnalizIstegi(BaseModel):
    metin: str

# 1. MANUEL METİN ANALİZİ
@app.post("/analiz")
def analiz_et(istek: AnalizIstegi):
    blob = TextBlob(istek.metin)
    skor = blob.sentiment.polarity
    karar = "Olumlu" if skor > 0 else "Olumsuz"
    return {"skor": skor, "karar": karar}

# 2. OTOMATİK HABER ANALİZİ (GÜÇLENDİRİLMİŞ VERSİYON)
@app.get("/piyasa-durumu")
def piyasa_durumu():
    # Haber Kaynakları (Biri çalışmazsa diğerini dener)
    kaynaklar = [
        "https://cointelegraph.com/rss/tag/bitcoin",
        "https://www.coindesk.com/arc/outboundfeeds/rss/"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    secilen_feed = None
    kullanilan_kaynak = ""

    # Sırayla kaynakları dene
    for url in kaynaklar:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                if feed.entries:
                    secilen_feed = feed
                    kullanilan_kaynak = "Cointelegraph" if "cointelegraph" in url else "CoinDesk"
                    break
        except Exception as e:
            print(f"Hata ({url}): {e}")
            continue

    if not secilen_feed:
        return {
            "genel_skor": 0,
            "genel_karar": "Veri Çekilemedi (Tüm Kaynaklar Engelledi)",
            "kaynak": "Yok",
            "detaylar": []
        }

    # Analiz Başlıyor
    toplam_skor = 0
    haber_sayisi = 0
    analiz_edilenler = []

    for entry in secilen_feed.entries[:5]:
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

    ortalama_skor = toplam_skor / haber_sayisi if haber_sayisi > 0 else 0
    
    genel_karar = "Nötr"
    if ortalama_skor > 0.05: genel_karar = "Piyasa Coşkulu (Boğa)"
    elif ortalama_skor < -0.05: genel_karar = "Piyasa Tedirgin (Ayı)"

    return {
        "genel_skor": round(ortalama_skor, 3),
        "genel_karar": genel_karar,
        "kaynak": kullanilan_kaynak,
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
        
        rsi_indicator = RSIIndicator(close=df['Close'], window=14)
        rsi = rsi_indicator.rsi().iloc[-1]
        
        macd_indicator = MACD(close=df['Close'])
        macd_diff = macd_indicator.macd_diff().iloc[-1]

        sinyal = "Bekle"
        if rsi < 30 and macd_diff > 0: sinyal = "GUCLU AL"
        elif rsi < 40: sinyal = "AL"
        elif rsi > 70: sinyal = "SAT"
        
        return {
            "sembol": sembol.upper(),
            "fiyat": round(current_price, 2),
            "teknik_analiz": {
                "rsi": round(rsi, 2),
                "macd_durum": "Pozitif" if macd_diff > 0 else "Negatif",
                "sinyal": sinyal
            }
        }
    except Exception as e:
        return {"hata": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)