from fastapi import FastAPI
from services.finance import calculate_hybrid_strategy

app = FastAPI()

@app.get("/fiyat/{sembol}")
def get_analysis(sembol: str):
    # Tüm hesaplamayı finance.py yapıyor, biz sadece sonucu iletiyoruz
    return calculate_hybrid_strategy(sembol)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)