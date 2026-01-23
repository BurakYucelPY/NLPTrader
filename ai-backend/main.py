from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from services.finance import calculate_hybrid_strategy
from services.nlp import get_sentiment_data, stream_news_data
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)