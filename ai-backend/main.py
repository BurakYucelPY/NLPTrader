from fastapi import FastAPI
from services.finance import calculate_hybrid_strategy
from services.nlp import get_sentiment_data

app = FastAPI()

@app.get("/piyasa-durumu")
def get_market_news():
    # Sadece haberleri ve sentiment sonuçlarını döndürür
    _, _, haberler = get_sentiment_data()
    return {"haberler": haberler}

@app.get("/fiyat/{sembol}")
def get_analysis(sembol: str):
    # Tüm hesaplamayı finance.py yapıyor, biz sadece sonucu iletiyoruz
    return calculate_hybrid_strategy(sembol)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)