from fastapi import FastAPI
from pydantic import BaseModel

from services.nlp import metni_analiz_et
from services.finance import fiyat_getir

app = FastAPI()

class VeriModeli(BaseModel):
    metin: str

@app.get("/")
def read_root():
    return {"Durum": "Calisiyor", "Servis": "AI Backend"}

@app.post("/analiz")
def analiz_yap(veri: VeriModeli):
    sonuc = metni_analiz_et(veri.metin)
    return sonuc

@app.get("/fiyat/{sembol}")
def fiyat_sorgula(sembol: str):
    sonuc = fiyat_getir(sembol)
    return sonuc