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
    fiyat = analiz_verisi.get('fiyat', 'N/A')
    sembol = analiz_verisi.get('sembol', '?')
    karar = s.get('karar', 'N/A')
    skor = s.get('toplam_skor', 0)

    # RSI durumunu yorumla
    rsi = h.get('rsi_degeri', 50)
    try:
        rsi_val = float(rsi)
        if rsi_val < 30: rsi_durum = "asiri satim bolgesinde, potansiyel dip sinyali"
        elif rsi_val < 40: rsi_durum = "zayif bolgede, saticilar baskin"
        elif rsi_val < 60: rsi_durum = "notr bolgede, kararsiz piyasa"
        elif rsi_val < 70: rsi_durum = "guclu bolgede, alicilar baskin"
        else: rsi_durum = "asiri alim bolgesinde, duzeltme riski yuksek"
    except:
        rsi_durum = "belirsiz"

    # Hacim akisi
    obv_egim = h.get('obv_egim', 0)
    try:
        obv_val = float(obv_egim)
        if obv_val > 5: hacim_durum = "guclu para girisi var"
        elif obv_val > 0: hacim_durum = "hafif para girisi var"
        elif obv_val > -5: hacim_durum = "hafif para cikisi var"
        else: hacim_durum = "ciddi para cikisi var"
    except:
        hacim_durum = "belirsiz"

    # Volatilite
    vol = h.get('volatilite_yillik', 50)
    try:
        vol_val = float(vol)
        if vol_val > 80: vol_durum = "cok yuksek, sert hareketler beklenmeli"
        elif vol_val > 50: vol_durum = "yuksek, dikkatli olunmali"
        elif vol_val > 30: vol_durum = "orta seviyede"
        else: vol_durum = "dusuk, sakin piyasa"
    except:
        vol_durum = "belirsiz"

    # SMA karsilastirma
    sma = h.get('sma_20', fiyat)
    try:
        fiyat_vs_sma = "uzerinde seyrediyor (yukselis trendi)" if float(fiyat) > float(sma) else "altinda seyrediyor (dusus trendi)"
    except:
        fiyat_vs_sma = "belirsiz"

    system_prompt = f"""Sen Bloomberg ve Reuters'te 15 yil deneyimli, kidemli bir kripto para piyasa analistisin.
Sana verilen teknik analiz sonuclarini YORUMLAYARAK profesyonel bir piyasa degerlendirmesi yazacaksin.

KRITIK KURALLAR:
1. ASLA ham sayilari veya puan degerlerini dogrudan yazma. "MACD puani 0.455" gibi ifadeler YASAK.
2. Bunun yerine verilerin NE ANLAMA GELDIGINI acikla. "Momentum gostergeleri yukari yonlu bir baski olusturuyor" gibi.
3. Piyasa psikolojisi ve yatirimci davranislarindan bahset.
4. Tarihsel baglam ver: benzer durumlarda piyasa nasil hareket etti?
5. Somut senaryolar sun: "Bu seviye kirilirsa su olabilir, tutunursa su olabilir."
6. Bir arkadasina WhatsApp'tan piyasa analizi anlatir gibi samimi ama profesyonel yaz.
7. Turkce yaz. Markdown formati kullan.
8. Her bolum 3-4 cumle olsun.

SANA VERILEN ANALIZ OZETI (bunu kullaniciya tekrarlama, yorumla):
- Varlik: {sembol}, Fiyat: ${fiyat}
- Sistem karari: {karar} (skor: {skor})
- RSI durumu: {rsi_durum}
- Hacim akisi: {hacim_durum}
- Volatilite: {vol_durum}
- Fiyat SMA-20'nin {fiyat_vs_sma}
- Haber sentiment: {b.get('sentiment_puan', 'N/A')} (negatiften pozitife -1 ile +1 arasi)
- Konsensus: {g.get('konsensus_orani', 'N/A')}, Sinyal gucu: {g.get('sinyal_gucu', 'N/A')}

YAZI YAPISI:
## Piyasa Gorunumu
(Genel durum, fiyatin nerede oldugu, trendin yonu hakkinda baglamsal bir giris)

## Teknik Degerlendirme
(Gostergelerin ne anlattigini YORUMLA - momentum, trend gucu, alici/satici dengesi)

## Piyasa Psikolojisi
(Yatirimcilar su an ne dusunuyor olabilir? Korku mu acgozluluk mu hakim? Haberler ne diyor?)

## Kritik Seviyeler ve Senaryolar
(Fiyat nereye gidebilir? Hangi seviyeler onemli? Iki farkli senaryo sun)

## Strateji Onerisi
(Ne yapilmali? Kisa ve net. Son satirda "Bu bir yatirim tavsiyesi degildir" uyarisi)"""

    user_prompt = f"{sembol} icin piyasa analiz raporunu hazirla."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Yorum uretilemedi: {str(e)}"

