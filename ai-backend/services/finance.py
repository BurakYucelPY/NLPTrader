import yfinance as yf
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volume import OnBalanceVolumeIndicator
from .nlp import get_sentiment_data

def calculate_hybrid_strategy(sembol: str):
    """
    Non-Linear Tanh (Hiperbolik Tanjant) ve Momentum (Türev) tabanlı
    profesyonel hibrit strateji hesaplama fonksiyonu.
    
    Tüm indikatörler -1 ile +1 arasında normalize edilir.
    Tanh fonksiyonu uç değerlerde sertleşme sağlar (sigmoid benzeri).
    """
    try:
        # =============================================================
        # 1. VERİ HAZIRLIĞI
        # =============================================================
        ticker = f"{sembol.upper()}-USD"
        stock = yf.Ticker(ticker)
        # Türev (momentum) hesabı için 6 aylık geçmiş veri
        df = stock.history(period="6mo", interval="1d")

        if df.empty: 
            return {"hata": "Fiyat verisi bulunamadı"}
        
        current_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2] if len(df) > 1 else current_price

        # =============================================================
        # 2. İNDİKATÖR HESAPLAMALARI VE NON-LINEAR NORMALİZASYON
        # =============================================================

        # ---------------------------------------------------------
        # A) RSI (%20 Ağırlık) - Tanh + Momentum Bonusu
        # ---------------------------------------------------------
        rsi_indicator = RSIIndicator(close=df['Close'], window=14)
        rsi_series = rsi_indicator.rsi()
        rsi_val = rsi_series.iloc[-1]
        rsi_prev = rsi_series.iloc[-2] if len(rsi_series) > 1 else rsi_val
        
        # Tanh normalizasyonu: 50 merkezli, uçlarda sertleşen eğri
        # RSI > 50 ise negatif (sat yönlü), RSI < 50 ise pozitif (al yönlü)
        rsi_base = -np.tanh((rsi_val - 50) / 10)
        
        # Momentum bonusu: RSI'ın türevi (değişim hızı)
        rsi_momentum = (rsi_val - rsi_prev)
        rsi_momentum_normalized = np.clip(rsi_momentum / 10, -1, 1)  # -1 ile 1 arası
        
        # %80 base + %20 momentum
        p_rsi = np.clip(rsi_base * 0.80 + rsi_momentum_normalized * 0.20, -1, 1)

        # ---------------------------------------------------------
        # B) MACD (%30 Ağırlık) - Histogram / StdDev + Tanh
        # ---------------------------------------------------------
        macd_obj = MACD(close=df['Close'])
        macd_hist_series = macd_obj.macd_diff()
        current_hist = macd_hist_series.iloc[-1]
        
        # Son 100 periyodun standart sapması ile normalize et
        hist_std = macd_hist_series.tail(100).std()
        if hist_std == 0 or np.isnan(hist_std): 
            hist_std = 1
        
        # Tanh normalizasyonu: değer ne kadar büyükse o kadar 1'e veya -1'e yaklaşır
        p_macd = np.tanh(current_hist / hist_std)

        # ---------------------------------------------------------
        # C) OBV (%15 Ağırlık) - Eğim (Slope) + Tanh
        # ---------------------------------------------------------
        obv_indicator = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume'])
        obv_series = obv_indicator.on_balance_volume()
        
        # Son 5 günlük OBV değişim yüzdesi (eğim/slope)
        obv_current = obv_series.iloc[-1]
        obv_5_days_ago = obv_series.iloc[-6] if len(obv_series) >= 6 else obv_series.iloc[0]
        
        if obv_5_days_ago != 0:
            obv_slope = (obv_current - obv_5_days_ago) / abs(obv_5_days_ago)
        else:
            obv_slope = 0.0
        
        # Eğim küçük çıkacağı için 20x çarpanla genişlet ve tanh uygula
        p_obv = np.tanh(obv_slope * 20)

        # ---------------------------------------------------------
        # D) Volatilite / Z-Score (%15 Ağırlık) - Mean Reversion
        # ---------------------------------------------------------
        # 20 günlük SMA ve Standart Sapma
        sma_20 = df['Close'].rolling(window=20).mean().iloc[-1]
        std_20 = df['Close'].rolling(window=20).std().iloc[-1]
        
        # Z-Score hesabı: Fiyatın ortalamadan kaç std sapma uzakta olduğu
        if std_20 != 0 and not np.isnan(std_20):
            z_score = (current_price - sma_20) / std_20
        else:
            z_score = 0.0
        
        # Ters işlem mantığı: Fiyat ortalamadan çok saptıysa geri dönüş beklenir
        # Z-score pozitifse (fiyat yüksekte) sat yönlü, negatifse al yönlü
        p_volatility = -np.tanh(z_score)
        
        # Yıllık volatilite hesabı (bilgi amaçlı)
        returns = df['Close'].pct_change().dropna()
        volatility_annual = returns.rolling(window=20).std().iloc[-1] * np.sqrt(252)

        # ---------------------------------------------------------
        # E) Sentiment (%20 Ağırlık) - Tanh ile güçlendirilmiş
        # ---------------------------------------------------------
        sent_score, kaynak, haber_detaylari = get_sentiment_data()
        
        # Sentiment skorunu 2x çarpanla güçlendir ve tanh uygula
        p_sent = np.tanh(sent_score * 2)

        # =============================================================
        # 3. SKORLAMA VE KARAR
        # =============================================================
        # Ağırlıklar: MACD(%30) + RSI(%20) + OBV(%15) + Volatilite(%15) + Sentiment(%20)
        total_score = (
            (p_macd * 0.30) + 
            (p_rsi * 0.20) + 
            (p_obv * 0.15) + 
            (p_volatility * 0.15) + 
            (p_sent * 0.20)
        )
        
        # Karar Eşikleri (Thresholds)
        karar = "BEKLE 😐"
        renk = "#bdbdbd"
        
        if total_score > 0.60:
            karar = "GÜÇLÜ AL 🚀"
            renk = "#00c853"
        elif 0.25 <= total_score <= 0.60:
            karar = "AL 🌱"
            renk = "#69f0ae"
        elif -0.25 < total_score < 0.25:
            karar = "BEKLE 😐"
            renk = "#bdbdbd"
        elif -0.60 <= total_score <= -0.25:
            karar = "SAT 🔻"
            renk = "#ffab91"
        elif total_score < -0.60:
            karar = "GÜÇLÜ SAT 💀"
            renk = "#d50000"

        # =============================================================
        # 4. ÇIKTI FORMATI
        # =============================================================
        return {
            "sembol": sembol.upper(),
            "fiyat": round(current_price, 2),
            "strateji": {
                "toplam_skor": round(total_score, 3),
                "karar": karar,
                "karar_renk": renk,
                "bilesenler": {
                    "macd_puan": round(float(p_macd), 3),
                    "rsi_puan": round(float(p_rsi), 3),
                    "obv_puan": round(float(p_obv), 3),
                    "volatilite_puan": round(float(p_volatility), 3),
                    "sentiment_puan": round(float(p_sent), 3)
                },
                "ham_veriler": {
                    "rsi_degeri": round(rsi_val, 2),
                    "rsi_momentum": round(rsi_momentum, 2),
                    "macd_hist": round(current_hist, 6),
                    "macd_hist_std": round(hist_std, 6),
                    "obv_egim": round(obv_slope * 100, 2),  # Yüzde olarak
                    "z_score": round(z_score, 3),
                    "volatilite_yillik": round(volatility_annual * 100, 1) if not np.isnan(volatility_annual) else 0,
                    "fiyat_onceki": round(prev_price, 2),
                    "sma_20": round(sma_20, 2),
                    "haber_kaynak": kaynak
                }
            },
            "haberler": haber_detaylari
        }

    except Exception as e:
        return {"hata": str(e)}