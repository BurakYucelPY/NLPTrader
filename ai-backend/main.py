from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Durum": "Calisiyor", "Servis": "AI Backend"}