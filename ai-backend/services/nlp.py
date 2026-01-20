import feedparser
import requests
from textblob import TextBlob
from datetime import datetime, timedelta

def get_sentiment_data():
    """
    Birden fazla RSS kaynağından son 24 saatin haberlerini çeker ve sentiment analizi yapar.
    En az 100 haber hedeflenir.
    """
    # Çoklu haber kaynakları - kripto odaklı
    kaynaklar = [
        # Kripto Özel Kaynaklar
        "https://cointelegraph.com/rss",
        "https://cointelegraph.com/rss/tag/bitcoin",
        "https://cointelegraph.com/rss/tag/ethereum",
        "https://cointelegraph.com/rss/tag/altcoin",
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cryptonews.com/news/feed/",
        "https://decrypt.co/feed",
        "https://bitcoinmagazine.com/.rss/full/",
        "https://www.newsbtc.com/feed/",
        "https://u.today/rss",
        "https://cryptopotato.com/feed/",
        "https://www.theblock.co/rss.xml",
        "https://cryptobriefing.com/feed/",
        # Finans & Teknoloji
        "https://www.investing.com/rss/news_301.rss",
        "https://feeds.bloomberg.com/crypto/news.rss",
    ]
    
    headers = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" 
    }
    
    # Son 24 saat
    bir_gun_once = datetime.now() - timedelta(days=1)
    
    tum_haberler = []
    gorulen_basliklar = set()  # Tekrar eden haberleri engelle
    
    for url in kaynaklar:
        try:
            response = requests.get(url, headers=headers, timeout=8)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                
                for entry in feed.entries:
                    baslik = entry.title.strip()
                    
                    # Tekrar kontrolü
                    if baslik.lower() in gorulen_basliklar:
                        continue
                    gorulen_basliklar.add(baslik.lower())
                    
                    # Tarih kontrolü (mümkünse)
                    haber_tarihi = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        try:
                            haber_tarihi = datetime(*entry.published_parsed[:6])
                        except:
                            pass
                    
                    # Eğer tarih varsa ve 24 saatten eskiyse atla
                    if haber_tarihi and haber_tarihi < bir_gun_once:
                        continue
                    
                    tum_haberler.append({
                        "baslik": baslik,
                        "tarih": haber_tarihi,
                        "kaynak": url.split('/')[2]
                    })
                    
        except Exception as e:
            continue  # Hatalı kaynağı atla, diğerlerine devam et
    
    if not tum_haberler:
        return 0.0, "Veri Yok", []
    
    # Tarihe göre sırala (en yeni en üstte), tarihi olmayanlar sona
    tum_haberler.sort(key=lambda x: x["tarih"] or datetime.min, reverse=True)
    
    # Sentiment analizi yap
    toplam_skor = 0
    detaylar = []
    
    for haber in tum_haberler:
        baslik = haber["baslik"]
        blob = TextBlob(baslik)
        skor = blob.sentiment.polarity
        
        toplam_skor += skor
        
        detaylar.append({
            "baslik": baslik, 
            "skor": round(skor, 3),
            "durum": "Olumlu" if skor > 0 else ("Olumsuz" if skor < 0 else "Nötr")
        })
    
    haber_sayisi = len(detaylar)
    ortalama_skor = toplam_skor / haber_sayisi if haber_sayisi > 0 else 0
    
    kaynak_bilgisi = f"{haber_sayisi} haber ({len(kaynaklar)} kaynak)"
    
    return ortalama_skor, kaynak_bilgisi, detaylar


def stream_news_data():
    """
    Haberleri tek tek yield ederek stream olarak gönderir.
    Her haber geldiği anda frontend'e iletilir.
    """
    kaynaklar = [
        "https://cointelegraph.com/rss",
        "https://cointelegraph.com/rss/tag/bitcoin",
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cryptonews.com/news/feed/",
        "https://decrypt.co/feed",
        "https://bitcoinmagazine.com/.rss/full/",
        "https://www.newsbtc.com/feed/",
        "https://u.today/rss",
        "https://cryptopotato.com/feed/",
    ]
    
    headers = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" 
    }
    
    bir_gun_once = datetime.now() - timedelta(days=1)
    gorulen_basliklar = set()
    
    for url in kaynaklar:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                
                for entry in feed.entries[:15]:  # Her kaynaktan max 15 haber
                    baslik = entry.title.strip()
                    
                    if baslik.lower() in gorulen_basliklar:
                        continue
                    gorulen_basliklar.add(baslik.lower())
                    
                    # Tarih kontrolü
                    haber_tarihi = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        try:
                            haber_tarihi = datetime(*entry.published_parsed[:6])
                            if haber_tarihi < bir_gun_once:
                                continue
                        except:
                            pass
                    
                    # Sentiment analizi
                    blob = TextBlob(baslik)
                    skor = blob.sentiment.polarity
                    
                    # Her haberi hemen yield et
                    yield {
                        "baslik": baslik,
                        "skor": round(skor, 3),
                        "durum": "Olumlu" if skor > 0 else ("Olumsuz" if skor < 0 else "Nötr")
                    }
                    
        except Exception as e:
            continue