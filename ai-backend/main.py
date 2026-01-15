from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI()

class VeriModeli(BaseModel):
    metin: str

@app.get("/")
def read_root():
    return {"Durum": "Calisiyor", "Servis": "AI Backend"}

@app.post("/analiz")
def analiz_yap(veri: VeriModeli):
    analiz = TextBlob(veri.metin)
    skor = analiz.sentiment.polarity
    
    karar = "Notr"
    if skor > 0.05:
        karar = "Olumlu"
    elif skor < -0.05:
        karar = "Olumsuz"

    return {"skor": skor, "karar": karar}