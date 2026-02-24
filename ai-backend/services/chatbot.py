from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_system_prompt(analiz_verisi: dict) -> str:
    """
    Analiz verisini system prompt'a dönüştürür.
    Groq modeli bu bağlamla cevap verir.
    """
    if not analiz_verisi or "hata" in analiz_verisi:
        return """Sen NLPTrader asistanısın. Kripto para piyasaları hakkında yardımcı oluyorsun.
Şu anda analiz verisi mevcut değil. Kullanıcıya genel bilgiler verebilirsin ama
spesifik tahmin yapamayacağını belirt. Türkçe cevap ver. Kısa ve öz cevaplar ver."""

    s = analiz_verisi.get("strateji", {})
    b = s.get("bilesenler", {})
    g = s.get("guven_metrikleri", {})
    h = s.get("ham_veriler", {})
    d = s.get("dinamik_esikler", {})
    dag = s.get("indikator_dagilimi", {})

    return f"""Sen NLPTrader yapay zeka asistanısın. Kripto para analizi konusunda uzmanlaşmış bir yardımcısın.
Aşağıdaki CANLI ANALİZ VERİLERİ, NLPTrader sisteminin şu anda hesapladığı gerçek zamanlı verilerdir.
Bu verileri kullanarak kullanıcının sorularını yanıtla.

═══════════════════════════════════════
📊 ANALİZ EDİLEN VARLIK: {analiz_verisi.get('sembol', 'Bilinmiyor')}
💰 GÜNCEL FİYAT: ${analiz_verisi.get('fiyat', 'N/A')}
═══════════════════════════════════════

🎯 NİHAİ KARAR: {s.get('karar', 'N/A')}
📝 AÇIKLAMA: {s.get('karar_aciklama', 'N/A')}
📈 TOPLAM SKOR: {s.get('toplam_skor', 'N/A')} (ayarlı: {s.get('ayarli_skor', 'N/A')})

═══════════════════════════════════════
📐 İNDİKATÖR PUANLARI (her biri -1 ile +1 arası):
  • MACD  (%30 ağırlık): {b.get('macd_puan', 'N/A')}
  • RSI   (%20 ağırlık): {b.get('rsi_puan', 'N/A')}
  • OBV   (%15 ağırlık): {b.get('obv_puan', 'N/A')}
  • Volatilite (%15 ağırlık): {b.get('volatilite_puan', 'N/A')}
  • Sentiment  (%20 ağırlık): {b.get('sentiment_puan', 'N/A')}

📊 İNDİKATÖR DAĞILIMI:
  • Yükseliş yönlü: {dag.get('yukselis_yonlu', 'N/A')} gösterge
  • Düşüş yönlü: {dag.get('dusus_yonlu', 'N/A')} gösterge
  • Nötr: {dag.get('notr', 'N/A')} gösterge

🔬 HAM VERİLER:
  • RSI Değeri: {h.get('rsi_degeri', 'N/A')} (momentum: {h.get('rsi_momentum', 'N/A')})
  • MACD Histogram: {h.get('macd_hist', 'N/A')} (std: {h.get('macd_hist_std', 'N/A')})
  • OBV Eğimi: %{h.get('obv_egim', 'N/A')}
  • Z-Score: {h.get('z_score', 'N/A')}
  • Yıllık Volatilite: %{h.get('volatilite_yillik', 'N/A')}
  • SMA-20: ${h.get('sma_20', 'N/A')}
  • Önceki Fiyat: ${h.get('fiyat_onceki', 'N/A')}
  • Haber Kaynakları: {h.get('haber_kaynak', 'N/A')}

🛡️ GÜVEN METRİKLERİ:
  • Güven Skoru: {g.get('guven_skoru', 'N/A')}
  • Konsensüs Oranı: {g.get('konsensus_orani', 'N/A')}
  • Sinyal Gücü: {g.get('sinyal_gucu', 'N/A')}
  • Trend Tutarlılığı: {g.get('trend_tutarliligi', 'N/A')}
  • Risk/Ödül Skoru: {g.get('risk_odul_skoru', 'N/A')}

⚙️ DİNAMİK EŞİKLER:
  • Güçlü Eşik: {d.get('guclu_esik', 'N/A')}
  • Normal Eşik: {d.get('normal_esik', 'N/A')}
  • Volatilite Etkisi: {d.get('volatilite_etkisi', 'N/A')}
═══════════════════════════════════════

KURALLAR:
1. Her zaman Türkçe cevap ver.
2. Cevaplarını yukarıdaki gerçek verilere dayandır, uydurma bilgi verme.
3. Kısa ve öz cevaplar ver, gereksiz uzatma.
4. Kullanıcıya "bunlar tavsiye değil, yatırım kararlarını kendin ver" uyarısını uygun zamanlarda ekle.
5. Teknik terimleri basitçe açıkla, herkesin anlayacağı dilde konuş.
6. Eğer bir gösterge hakkında sorulursa, o göstergenin puanını, ham verisini ve ne anlama geldiğini açıkla.
7. Emoji kullanarak cevaplarını görsel olarak zenginleştir."""


def chat_with_groq(analiz_verisi: dict, mesaj: str, gecmis: list = None) -> str:
    """
    Groq API ile sohbet. Analiz verisini bağlam olarak kullanır.
    """
    system_prompt = build_system_prompt(analiz_verisi)
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Önceki konuşma geçmişini ekle
    if gecmis:
        for m in gecmis:
            messages.append({
                "role": m.get("role", "user"),
                "content": m.get("content", "")
            })
    
    # Kullanıcının yeni mesajını ekle
    messages.append({"role": "user", "content": mesaj})
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Bir hata oluştu: {str(e)}"


def generate_ai_commentary(analiz_verisi: dict) -> str:
    """
    Analiz verisini alır ve detaylı bir yapay zeka yorumu üretir.
    """
    if not analiz_verisi or "hata" in analiz_verisi:
        return "Analiz verisi bulunamadığı için yorum üretilemedi."

    s = analiz_verisi.get("strateji", {})
    b = s.get("bilesenler", {})
    g = s.get("guven_metrikleri", {})
    h = s.get("ham_veriler", {})

    system_prompt = f"""Sen profesyonel bir kripto para piyasa analistisin. Aşağıdaki teknik analiz verilerine dayanarak
detaylı, profesyonel ve Türkçe bir piyasa yorumu yaz.

VARLIK: {analiz_verisi.get('sembol', '?')}
FİYAT: ${analiz_verisi.get('fiyat', 'N/A')}
KARAR: {s.get('karar', 'N/A')} (Skor: {s.get('toplam_skor', 'N/A')})

İNDİKATÖRLER:
- MACD Puan: {b.get('macd_puan', 'N/A')} | Histogram: {h.get('macd_hist', 'N/A')}
- RSI Puan: {b.get('rsi_puan', 'N/A')} | Değer: {h.get('rsi_degeri', 'N/A')}
- OBV Puan: {b.get('obv_puan', 'N/A')} | Eğim: %{h.get('obv_egim', 'N/A')}
- Volatilite Puan: {b.get('volatilite_puan', 'N/A')} | Yıllık: %{h.get('volatilite_yillik', 'N/A')}
- Sentiment Puan: {b.get('sentiment_puan', 'N/A')} | Kaynak: {h.get('haber_kaynak', 'N/A')}

GÜVEN: Skor={g.get('guven_skoru', 'N/A')}, Konsensüs={g.get('konsensus_orani', 'N/A')}, Sinyal={g.get('sinyal_gucu', 'N/A')}
Z-Score: {h.get('z_score', 'N/A')}, SMA-20: ${h.get('sma_20', 'N/A')}

KURALLAR:
1. Markdown formatında yaz.
2. Şu bölümleri içer:
   - 📊 **Genel Bakış** (2-3 cümle özet)
   - 📈 **Teknik Analiz** (MACD, RSI, OBV yorumu)
   - 📰 **Piyasa Duyarlılığı** (sentiment analizi)
   - ⚠️ **Risk Değerlendirmesi** (volatilite ve risk)
   - 🎯 **Sonuç** (kısa öneri ve uyarı)
3. Her bölüm 2-3 cümle olsun, çok uzatma.
4. Profesyonel ve güvenilir bir ton kullan.
5. "Bu yatırım tavsiyesi değildir" uyarısını sonunda ekle.
6. Emoji kullanarak okunabilirliği artır."""

    user_prompt = f"{analiz_verisi.get('sembol', 'BTC')} için güncel piyasa yorumunu yaz."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Yorum üretilemedi: {str(e)}"
