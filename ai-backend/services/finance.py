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
        # 3. GELİŞMİŞ SKORLAMA VE KARAR MEKANİZMASI
        # =============================================================
        
        # Tüm indikatörleri bir listeye al
        indicators = {
            'macd': {'value': p_macd, 'weight': 0.30},
            'rsi': {'value': p_rsi, 'weight': 0.20},
            'obv': {'value': p_obv, 'weight': 0.15},
            'volatility': {'value': p_volatility, 'weight': 0.15},
            'sentiment': {'value': p_sent, 'weight': 0.20}
        }
        
        # A) TEMEL AĞIRLIKLI SKOR
        total_score = sum(ind['value'] * ind['weight'] for ind in indicators.values())
        
        # ---------------------------------------------------------
        # B) KONSENSÜS SKORU (İndikatör Uyumu)
        # Kaç indikatör aynı yönde? Ne kadar uyumlular?
        # ---------------------------------------------------------
        values = [ind['value'] for ind in indicators.values()]
        
        # Pozitif ve negatif yönde olan indikatör sayısı
        bullish_count = sum(1 for v in values if v > 0.1)
        bearish_count = sum(1 for v in values if v < -0.1)
        neutral_count = len(values) - bullish_count - bearish_count
        
        # Konsensüs oranı: 0 (tam kararsızlık) ile 1 (tam uyum) arası
        max_agreement = max(bullish_count, bearish_count)
        consensus_ratio = max_agreement / len(values)
        
        # ---------------------------------------------------------
        # C) SİNYAL GÜCÜ (Magnitude)
        # İndikatörlerin ortalama şiddeti - zayıf mı güçlü mü?
        # ---------------------------------------------------------
        signal_magnitude = np.mean([abs(v) for v in values])
        
        # ---------------------------------------------------------
        # D) GÜVEN SKORU (Confidence)
        # Konsensüs * Sinyal Gücü = Ne kadar güvenilir bir sinyal?
        # ---------------------------------------------------------
        raw_confidence = consensus_ratio * signal_magnitude
        
        # Volatilite penaltisi: Yüksek volatilitede güven düşer
        vol_penalty = 1.0 - min(volatility_annual * 0.5, 0.4)  # Max %40 penaltı
        
        # Nihai güven skoru (0-1 arası, tanh ile yumuşatılmış)
        confidence = np.tanh(raw_confidence * 2) * vol_penalty
        
        # ---------------------------------------------------------
        # E) TREND TUTARLILIĞI (Directional Consistency)
        # İndikatörler hem yön hem de güç olarak ne kadar tutarlı?
        # ---------------------------------------------------------
        if total_score != 0:
            # Her indikatörün ana skorla aynı yönde olup olmadığını kontrol et
            direction = np.sign(total_score)
            aligned_weights = sum(
                ind['weight'] for ind in indicators.values() 
                if np.sign(ind['value']) == direction
            )
            trend_consistency = aligned_weights  # 0 ile 1 arası
        else:
            trend_consistency = 0.0
        
        # ---------------------------------------------------------
        # F) RİSK/ÖDÜL SKORU
        # Potansiyel kazanç vs potansiyel kayıp oranı
        # ---------------------------------------------------------
        # Z-score ile risk seviyesi (ortalamadan sapma = risk)
        risk_level = min(abs(z_score) / 2, 1.0)  # 0-1 arası
        
        # Momentuma göre ödül potansiyeli
        reward_potential = abs(total_score) * trend_consistency
        
        # Risk/Ödül oranı (1'den büyükse ödül > risk)
        if risk_level > 0:
            risk_reward_ratio = reward_potential / risk_level
        else:
            risk_reward_ratio = reward_potential * 2  # Düşük risk bonus
        
        risk_reward_score = np.tanh(risk_reward_ratio - 1)  # -1 ile 1 arası
        
        # ---------------------------------------------------------
        # G) NİHAİ KARAR MATRİSİ (Multi-Factor Decision)
        # Sadece skora değil, tüm faktörlere bakarak karar ver
        # ---------------------------------------------------------
        
        # Final skor: Temel skor + Güven bonusu/penaltısı
        # Güven yüksekse skor güçlenir, düşükse zayıflar
        confidence_multiplier = 0.7 + (confidence * 0.6)  # 0.7 ile 1.3 arası
        adjusted_score = total_score * confidence_multiplier
        
        # Dinamik eşikler: Volatiliteye göre ayarla
        # Yüksek volatilitede daha yüksek eşik (daha temkinli)
        base_strong = 0.45
        base_normal = 0.20
        vol_adjustment = volatility_annual * 0.3  # Volatilite etkisi
        
        threshold_strong = base_strong + vol_adjustment
        threshold_normal = base_normal + (vol_adjustment * 0.5)
        
        # ---------------------------------------------------------
        # H) KARAR AĞACI (Decision Tree)
        # ---------------------------------------------------------
        karar = "BEKLE 😐"
        renk = "#bdbdbd"
        karar_aciklama = ""
        
        abs_score = abs(adjusted_score)
        score_direction = "BUY" if adjusted_score > 0 else "SELL"
        
        # Güçlü Sinyal Koşulları
        strong_signal = (
            abs_score > threshold_strong and
            confidence > 0.4 and
            trend_consistency > 0.6 and
            consensus_ratio >= 0.6
        )
        
        # Normal Sinyal Koşulları
        normal_signal = (
            abs_score > threshold_normal and
            confidence > 0.25 and
            trend_consistency > 0.4
        )
        
        # Zayıf Sinyal Koşulları (dikkatli ol)
        weak_signal = (
            abs_score > threshold_normal * 0.7 and
            confidence > 0.15
        )
        
        if adjusted_score > 0:  # AL yönlü
            if strong_signal:
                karar = "GÜÇLÜ AL 🚀"
                renk = "#00c853"
                karar_aciklama = f"Yüksek güven ({confidence:.0%}), güçlü konsensüs ({consensus_ratio:.0%})"
            elif normal_signal:
                karar = "AL 🌱"
                renk = "#69f0ae"
                karar_aciklama = f"Orta güven ({confidence:.0%}), kabul edilebilir trend tutarlılığı"
            elif weak_signal:
                karar = "ZAYIF AL 🤔"
                renk = "#c8e6c9"
                karar_aciklama = f"Düşük güven ({confidence:.0%}), dikkatli pozisyon"
            else:
                karar = "BEKLE 😐"
                renk = "#bdbdbd"
                karar_aciklama = "Yetersiz sinyal gücü veya tutarsız indikatörler"
                
        elif adjusted_score < 0:  # SAT yönlü
            if strong_signal:
                karar = "GÜÇLÜ SAT 💀"
                renk = "#d50000"
                karar_aciklama = f"Yüksek güven ({confidence:.0%}), güçlü düşüş konsensüsü"
            elif normal_signal:
                karar = "SAT 🔻"
                renk = "#ffab91"
                karar_aciklama = f"Orta güven ({confidence:.0%}), satış baskısı mevcut"
            elif weak_signal:
                karar = "ZAYIF SAT 🤔"
                renk = "#ffccbc"
                karar_aciklama = f"Düşük güven ({confidence:.0%}), kısmi pozisyon azaltma"
            else:
                karar = "BEKLE 😐"
                renk = "#bdbdbd"
                karar_aciklama = "Yetersiz sinyal gücü veya tutarsız indikatörler"
        else:
            karar = "BEKLE 😐"
            renk = "#bdbdbd"
            karar_aciklama = "Nötr piyasa koşulları"

        # =============================================================
        # 4. ÇIKTI FORMATI
        # =============================================================
        return {
            "sembol": sembol.upper(),
            "fiyat": round(current_price, 2),
            "strateji": {
                "toplam_skor": round(float(total_score), 3),
                "ayarli_skor": round(float(adjusted_score), 3),
                "karar": karar,
                "karar_renk": renk,
                "karar_aciklama": karar_aciklama,
                "guven_metrikleri": {
                    "guven_skoru": round(float(confidence), 3),
                    "konsensus_orani": round(float(consensus_ratio), 3),
                    "sinyal_gucu": round(float(signal_magnitude), 3),
                    "trend_tutarliligi": round(float(trend_consistency), 3),
                    "risk_odul_skoru": round(float(risk_reward_score), 3)
                },
                "indikator_dagilimi": {
                    "yukselis_yonlu": bullish_count,
                    "dusus_yonlu": bearish_count,
                    "notr": neutral_count
                },
                "bilesenler": {
                    "macd_puan": round(float(p_macd), 3),
                    "rsi_puan": round(float(p_rsi), 3),
                    "obv_puan": round(float(p_obv), 3),
                    "volatilite_puan": round(float(p_volatility), 3),
                    "sentiment_puan": round(float(p_sent), 3)
                },
                "dinamik_esikler": {
                    "guclu_esik": round(float(threshold_strong), 3),
                    "normal_esik": round(float(threshold_normal), 3),
                    "volatilite_etkisi": round(float(vol_adjustment), 3)
                },
                "ham_veriler": {
                    "rsi_degeri": round(rsi_val, 2),
                    "rsi_momentum": round(rsi_momentum, 2),
                    "macd_hist": round(current_hist, 6),
                    "macd_hist_std": round(hist_std, 6),
                    "obv_egim": round(obv_slope * 100, 2),
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