import feedparser
import requests
from textblob import TextBlob

def get_sentiment_data():
    """
    RSS kaynaklarından haber çeker ve sentiment analizi yapar.
    """
    kaynaklar = [
        "https://cointelegraph.com/rss/tag/bitcoin",
        "https://www.coindesk.com/arc/outboundfeeds/rss/"
    ]
    # Bot korumasını aşmak için tarayıcı gibi davranıyoruz
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    
    secilen_feed = None
    kullanilan_kaynak = ""

    for url in kaynaklar:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                if feed.entries:
                    secilen_feed = feed
                    kullanilan_kaynak = "Cointelegraph" if "cointelegraph" in url else "CoinDesk"
                    break
        except:
            continue
            
    if not secilen_feed:
        return 0.0, "Veri Yok", []

    toplam_skor = 0
    haber_sayisi = 0
    detaylar = []

    # İlk 5 haberi analiz et
    for entry in secilen_feed.entries[:5]:
        baslik = entry.title
        blob = TextBlob(baslik)
        skor = blob.sentiment.polarity
        
        toplam_skor += skor
        haber_sayisi += 1
        
        detaylar.append({
            "baslik": baslik, 
            "skor": skor,
            "durum": "Olumlu" if skor > 0 else "Olumsuz/Nötr"
        })

    ortalama_skor = toplam_skor / haber_sayisi if haber_sayisi > 0 else 0
    
    return ortalama_skor, kullanilan_kaynak, detaylar