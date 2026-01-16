from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from textblob import TextBlob
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

app = FastAPI()

class AnalizIstegi(BaseModel):
    metin: str

@app.post("/analiz")
def analiz_et(istek: AnalizIstegi):
    blob = TextBlob(istek.metin)
    sentiment_score = blob.sentiment.polarity
    
    karar = "Notr"
    if sentiment_score > 0.1:
        karar = "Olumlu"
    elif sentiment_score < -0.1:
        karar = "Olumsuz"

    return {"skor": sentiment_score, "karar": karar}

@app.get("/fiyat/{sembol}")
def fiyat_getir(sembol: str):
    try:
        # 1. Geçmiş veriyi çek (Son 1 aylık veri, mum grafiği için)
        ticker = f"{sembol.upper()}-USD"
        stock = yf.Ticker(ticker)
        df = stock.history(period="1mo", interval="1d")

        if df.empty:
            return {"hata": "Veri bulunamadı"}

        current_price = df['Close'].iloc[-1]

        # 2. TEKNİK ANALİZ HESAPLAMALARI
        
        # RSI Hesapla (Göreceli Güç Endeksi)
        rsi_indicator = RSIIndicator(close=df['Close'], window=14)
        rsi_value = rsi_indicator.rsi().iloc[-1]

        # MACD Hesapla (Trend Takibi)
        macd = MACD(close=df['Close'])
        macd_diff = macd.macd_diff().iloc[-1] # MACD Histogramı

        # 3. Teknik Sinyal Üret (Basit bir algoritma)
        teknik_karar = "Bekle"
        
        # RSI 30'un altındaysa ve MACD pozitifse AL
        if rsi_value < 30 and macd_diff > 0:
            teknik_karar = "GUCLU AL"
        elif rsi_value < 40:
            teknik_karar = "AL"
        # RSI 70'in üstündeyse SAT
        elif rsi_value > 70:
            teknik_karar = "SAT"
        
        return {
            "sembol": sembol.upper(),
            "fiyat": round(current_price, 2),
            "teknik_analiz": {
                "rsi": round(rsi_value, 2),
                "macd_durum": "Pozitif" if macd_diff > 0 else "Negatif",
                "sinyal": teknik_karar
            }
        }

    except Exception as e:
        return {"hata": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)