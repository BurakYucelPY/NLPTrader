import yfinance as yf
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volume import OnBalanceVolumeIndicator
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
        # 2. MATEMATİKSEL FORMÜLLER
        # Toplam %80 Teknik Analiz + %20 Sentiment = %100
        # ---------------------------------------------------------

        # A) RSI (%20 Etki) -> Formül: (50 - RSI) / 50
        # RSI 30 altı = aşırı satım (al sinyali), 70 üstü = aşırı alım (sat sinyali)
        rsi_indicator = RSIIndicator(close=df['Close'], window=14)
        rsi_val = rsi_indicator.rsi().iloc[-1]
        p_rsi = (50 - rsi_val) / 50
        
        # B) MACD (%30 Etki) -> Formül: Hist / MaxHist
        # Histogram pozitif = yükseliş trendi, negatif = düşüş trendi
        macd_obj = MACD(close=df['Close'])
        macd_hist_series = macd_obj.macd_diff()
        current_hist = macd_hist_series.iloc[-1]
        
        # Son 100 mumun en büyük hareketine göre normalize et
        max_hist_recent = macd_hist_series.abs().rolling(window=100, min_periods=1).max().iloc[-1]
        if max_hist_recent == 0: max_hist_recent = 1
        
        p_macd = current_hist / max_hist_recent
        p_macd = max(min(p_macd, 1.0), -1.0)

        # C) OBV - On Balance Volume (%15 Etki)
        # Hacim fiyatı teyit ediyor mu? OBV yükselirken fiyat yükseliyorsa güçlü trend
        obv_indicator = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume'])
        obv_series = obv_indicator.on_balance_volume()
        
        # OBV'nin son 20 günlük trendine bak
        obv_sma_short = obv_series.rolling(window=5).mean().iloc[-1]
        obv_sma_long = obv_series.rolling(window=20).mean().iloc[-1]
        
        # OBV trendi: kısa vadeli SMA uzun vadeli SMA'nın üstündeyse pozitif
        if obv_sma_long != 0:
            obv_trend = (obv_sma_short - obv_sma_long) / abs(obv_sma_long)
            p_obv = max(min(obv_trend * 10, 1.0), -1.0)  # Normalize et
        else:
            p_obv = 0.0

        # D) VOLATİLİTE - İstatistiksel Sınır (%15 Etki)
        # Bollinger Band genişliği ile volatilite ölç
        # Yüksek volatilite + düşük fiyat = fırsat, yüksek volatilite + yüksek fiyat = risk
        returns = df['Close'].pct_change().dropna()
        volatility = returns.rolling(window=20).std().iloc[-1] * np.sqrt(252)  # Yıllık volatilite
        
        # Bollinger Bands ile fiyatın konumu
        sma_20 = df['Close'].rolling(window=20).mean().iloc[-1]
        std_20 = df['Close'].rolling(window=20).std().iloc[-1]
        upper_band = sma_20 + (2 * std_20)
        lower_band = sma_20 - (2 * std_20)
        
        # Fiyat bandın neresinde? Alt banda yakınsa al, üst banda yakınsa sat
        if upper_band != lower_band:
            band_position = (current_price - lower_band) / (upper_band - lower_band)
            # 0 = alt band (al), 1 = üst band (sat), 0.5 = orta
            p_volatility = (0.5 - band_position)  # -0.5 ile +0.5 arası
            p_volatility = p_volatility * 2  # -1 ile +1 arası normalize
        else:
            p_volatility = 0.0

        # E) SENTIMENT (%20 Etki) -> nlp.py dosyasından geliyor
        sent_score, kaynak, haber_detaylari = get_sentiment_data()
        p_sent = sent_score

        # ---------------------------------------------------------
        # 3. SKOR HESABI
        # %80 Teknik: MACD(%30) + RSI(%20) + OBV(%15) + Volatilite(%15)
        # %20 Sentiment
        # ---------------------------------------------------------
        total_score = (p_macd * 0.30) + (p_rsi * 0.20) + (p_obv * 0.15) + (p_volatility * 0.15) + (p_sent * 0.20)
        
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
                    "obv_puan": round(p_obv, 3),
                    "volatilite_puan": round(p_volatility, 3),
                    "sentiment_puan": round(p_sent, 3)
                },
                "ham_veriler": {
                    "rsi_degeri": round(rsi_val, 2),
                    "macd_hist": round(current_hist, 4),
                    "obv_trend": round(p_obv, 3),
                    "volatilite_yillik": round(volatility * 100, 1),
                    "haber_kaynak": kaynak
                }
            },
            "haberler": haber_detaylari
        }

    except Exception as e:
        return {"hata": str(e)}