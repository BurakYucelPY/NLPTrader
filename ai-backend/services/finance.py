import yfinance as yf

def fiyat_getir(sembol: str):
    """
    Sembolün (BTC, THY) son fiyatını getirir.
    """
    try:
        if sembol.lower() in ["btc", "eth", "sol", "avax"]:
            arama_kodu = f"{sembol.upper()}-USD"
        else:
            arama_kodu = f"{sembol.upper()}.IS"

        hisse = yf.Ticker(arama_kodu)
        # Sadece son 1 günün verisini al
        bilgi = hisse.history(period="1d")
        
        if bilgi.empty:
            return {"hata": "Veri bulunamadi", "sembol": sembol}

        son_fiyat = bilgi['Close'].iloc[-1]
        
        return {
            "sembol": arama_kodu,
            "fiyat": round(son_fiyat, 2),
            "para_birimi": "USD" if "-USD" in arama_kodu else "TRY"
        }
        
    except Exception as e:
        return {"hata": str(e)}