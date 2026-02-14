from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from services.finance import calculate_hybrid_strategy
from services.nlp import get_sentiment_data, stream_news_data
from services.chatbot import chat_with_groq
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)