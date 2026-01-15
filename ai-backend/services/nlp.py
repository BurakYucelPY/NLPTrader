from textblob import TextBlob

def metni_analiz_et(metin: str):
    """
    Verilen metnin duygu analizini yapar.
    Return: Sözlük {skor, karar}
    """
    analiz = TextBlob(metin)
    skor = analiz.sentiment.polarity
    
    karar = "Notr"
    if skor > 0.05:
        karar = "Olumlu"
    elif skor < -0.05:
        karar = "Olumsuz"
        
    return {"skor": skor, "karar": karar}