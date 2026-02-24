from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from services.finance import calculate_hybrid_strategy
from services.nlp import get_sentiment_data, stream_news_data
from services.chatbot import chat_with_groq
import yfinance as yf
import json

app = FastAPI()

# CORS - Frontend'in erişebilmesi için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/piyasa-durumu")
def get_market_news():
    # Sadece haberleri ve sentiment sonuçlarını döndürür
    _, _, haberler = get_sentiment_data()
    return {"haberler": haberler}

@app.get("/piyasa-durumu-stream")
def get_market_news_stream():
    """Haberleri tek tek stream olarak gönderir"""
    def generate():
        for haber in stream_news_data():
            yield f"data: {json.dumps(haber, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )

@app.get("/fiyat/{sembol}")
def get_analysis(sembol: str):
    # Tüm hesaplamayı finance.py yapıyor, biz sadece sonucu iletiyoruz
    return calculate_hybrid_strategy(sembol)

@app.post("/chatbot")
async def chatbot_endpoint(request: Request):
    """Chatbot endpoint: analiz verisini bağlam olarak kullanarak sohbet eder"""
    body = await request.json()
    sembol = body.get("sembol", "")
    mesaj = body.get("mesaj", "")
    gecmis = body.get("gecmis", [])
    
    # Seçilen coin için analiz verisini çek
    analiz_verisi = {}
    if sembol:
        analiz_verisi = calculate_hybrid_strategy(sembol)
    
    # Groq ile sohbet et
    cevap = chat_with_groq(analiz_verisi, mesaj, gecmis)
    
    return {"cevap": cevap}

@app.get("/grafik/{sembol}")
def get_chart_data(sembol: str, periyot: str = Query("6mo")):
    """Coin için geçmiş fiyat verilerini döndürür (grafik için)"""
    try:
        ticker = f"{sembol.upper()}-USD"
        stock = yf.Ticker(ticker)
        
        # Periyoda göre uygun interval seç
        interval_map = {
            "1d": "15m",
            "5d": "1h",
            "1mo": "1d",
            "6mo": "1d",
            "1y": "1wk",
            "max": "1mo"
        }
        interval = interval_map.get(periyot, "1d")
        
        df = stock.history(period=periyot, interval=interval)
        
        if df.empty:
            return {"hata": "Grafik verisi bulunamadı"}
        
        # Lightweight Charts formatında veri döndür
        veri = []
        for tarih, satir in df.iterrows():
            veri.append({
                "time": int(tarih.timestamp()),
                "open": round(float(satir['Open']), 2),
                "high": round(float(satir['High']), 2),
                "low": round(float(satir['Low']), 2),
                "close": round(float(satir['Close']), 2),
                "volume": round(float(satir['Volume']), 2)
            })
        
        # Güncel fiyat ve değişim hesapla
        son_fiyat = veri[-1]["close"] if veri else 0
        ilk_fiyat = veri[0]["open"] if veri else 0
        degisim = son_fiyat - ilk_fiyat
        degisim_yuzde = (degisim / ilk_fiyat * 100) if ilk_fiyat != 0 else 0
        
        return {
            "sembol": sembol.upper(),
            "periyot": periyot,
            "fiyat": round(son_fiyat, 2),
            "degisim": round(degisim, 2),
            "degisim_yuzde": round(degisim_yuzde, 2),
            "veri": veri
        }
    except Exception as e:
        return {"hata": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)