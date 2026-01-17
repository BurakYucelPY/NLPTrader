import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD
from .nlp import get_sentiment_data

def calculate_hybrid_strategy(sembol: str):
    try:
        # 1. FİYAT GEÇMİŞİNİ ÇEK
        ticker = f"{sembol.upper()}-USD"
        stock = yf.Ticker(ticker)
        # MACD için biraz geriye dönük veri lazım (6 ay)
        df = stock.history(period="6mo", interval="1d")

        if df.empty: return {"hata": "Fiyat verisi bulunamadı"}
        current_price = df['Close'].iloc[-1]

        # ---------------------------------------------------------
        # 2. MATEMATİKSEL FORMÜLLER (Senin Stratejin)
        # ---------------------------------------------------------

        # A) RSI (%30 Etki) -> Formül: (50 - RSI) / 50
        rsi_indicator = RSIIndicator(close=df['Close'], window=14)
        rsi_val = rsi_indicator.rsi().iloc[-1]
        p_rsi = (50 - rsi_val) / 50
        
        # B) MACD (%50 Etki) -> Formül: Hist / MaxHist
        macd_obj = MACD(close=df['Close'])
        macd_hist_series = macd_obj.macd_diff()
        current_hist = macd_hist_series.iloc[-1]
        
        # Son 100 mumun en büyük hareketine göre normalize et
        max_hist_recent = macd_hist_series.abs().rolling(window=100, min_periods=1).max().iloc[-1]
        if max_hist_recent == 0: max_hist_recent = 1
        
        p_macd = current_hist / max_hist_recent
        p_macd = max(min(p_macd, 1.0), -1.0) # Skoru -1 ile +1 arasına sabitle

        # C) SENTIMENT (%20 Etki) -> nlp.py dosyasından geliyor
        sent_score, kaynak, haber_detaylari = get_sentiment_data()
        p_sent = sent_score

        # ---------------------------------------------------------
        # 3. SKOR HESABI
        # ---------------------------------------------------------
        total_score = (p_macd * 0.50) + (p_rsi * 0.30) + (p_sent * 0.20)
        
        karar = "NÖTR / BEKLE"
        renk = "gray"
        
        # Karar Eşikleri
        if total_score >= 0.50:
            karar = "GÜÇLÜ AL 🚀"
            renk = "#00c853"
        elif 0.20 <= total_score < 0.50:
            karar = "AL 🌱"
            renk = "#69f0ae"
        elif -0.20 < total_score < 0.20:
            karar = "BEKLE 😐"
            renk = "#bdbdbd"
        elif -0.50 < total_score <= -0.20:
            karar = "SAT 🔻"
            renk = "#ffab91"
        elif total_score <= -0.50:
            karar = "GÜÇLÜ SAT 💀"
            renk = "#d50000"

        return {
            "sembol": sembol.upper(),
            "fiyat": round(current_price, 2),
            "strateji": {
                "toplam_skor": round(total_score, 3),
                "karar": karar,
                "karar_renk": renk,
                "bilesenler": {
                    "macd_puan": round(p_macd, 3),
                    "rsi_puan": round(p_rsi, 3),
                    "sentiment_puan": round(p_sent, 3)
                },
                "ham_veriler": {
                    "rsi_degeri": round(rsi_val, 2),
                    "macd_hist": round(current_hist, 4),
                    "haber_kaynak": kaynak
                }
            },
            "haberler": haber_detaylari
        }

    except Exception as e:
        return {"hata": str(e)}