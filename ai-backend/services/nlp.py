import feedparser
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta

# ============================================================
# VADER + Kripto/Finans Özel Sözlük
# ============================================================
# VADER zaten genel duygu analizi için iyi ama kripto/finans
# terminolojisini ekstra güçlendiriyoruz.

analyzer = SentimentIntensityAnalyzer()

# Kripto/Finans alanına özel kelimeler ve duygu ağırlıkları
# Pozitif değerler = olumlu, negatif değerler = olumsuz
# Ölçek: -4 (çok olumsuz) ile +4 (çok olumlu)
KRIPTO_SOZLUK = {
    # --- GÜÇLÜ POZİTİF ---
    "bullish": 3.0,
    "surge": 2.8,
    "surges": 2.8,
    "surging": 2.8,
    "soar": 2.8,
    "soars": 2.8,
    "soaring": 2.8,
    "rally": 2.5,
    "rallies": 2.5,
    "rallying": 2.5,
    "breakout": 2.5,
    "all-time high": 3.2,
    "ath": 3.0,
    "moon": 2.5,
    "mooning": 2.5,
    "pump": 2.2,
    "pumping": 2.2,
    "skyrocket": 3.0,
    "skyrockets": 3.0,
    "parabolic": 2.5,
    "explode": 2.0,
    "explodes": 2.0,
    "boom": 2.5,
    "booming": 2.5,

    # --- ORTA POZİTİF ---
    "gain": 1.8,
    "gains": 1.8,
    "rise": 1.8,
    "rises": 1.8,
    "rising": 1.8,
    "climb": 1.5,
    "climbs": 1.5,
    "climbing": 1.5,
    "jump": 1.8,
    "jumps": 1.8,
    "recover": 1.5,
    "recovers": 1.5,
    "recovery": 1.5,
    "rebound": 1.5,
    "rebounds": 1.5,
    "uptick": 1.3,
    "uptrend": 2.0,
    "upside": 1.5,
    "outperform": 1.8,
    "outperforms": 1.8,
    "adoption": 2.0,
    "approved": 2.5,
    "approval": 2.5,
    "bullrun": 2.8,
    "bull run": 2.8,
    "accumulate": 1.5,
    "accumulation": 1.5,
    "milestone": 1.8,
    "partnership": 1.5,
    "upgrade": 1.5,
    "breakthrough": 2.0,
    "institutional": 1.3,
    "etf": 1.8,
    "halving": 1.5,

    # --- GÜÇLÜ NEGATİF ---
    "bearish": -3.0,
    "crash": -3.2,
    "crashes": -3.2,
    "crashing": -3.2,
    "plunge": -2.8,
    "plunges": -2.8,
    "plunging": -2.8,
    "dump": -2.5,
    "dumps": -2.5,
    "dumping": -2.5,
    "collapse": -3.0,
    "collapses": -3.0,
    "freefall": -3.0,
    "tank": -2.5,
    "tanks": -2.5,
    "tanking": -2.5,
    "rekt": -3.0,
    "capitulation": -2.8,
    "liquidation": -2.5,
    "liquidated": -2.5,
    "bankrupt": -3.5,
    "bankruptcy": -3.5,
    "scam": -3.5,
    "fraud": -3.5,
    "hack": -3.0,
    "hacked": -3.0,
    "exploit": -2.5,
    "exploited": -2.5,
    "rug pull": -3.5,
    "ponzi": -3.5,

    # --- ORTA NEGATİF ---
    "drop": -2.5,
    "drops": -2.5,
    "dropping": -2.5,
    "fall": -2.2,
    "falls": -2.2,
    "falling": -2.2,
    "decline": -1.8,
    "declines": -1.8,
    "declining": -1.8,
    "sell-off": -2.2,
    "selloff": -2.2,
    "dip": -1.2,
    "tumble": -2.0,
    "tumbles": -2.0,
    "slump": -2.0,
    "slumps": -2.0,
    "downturn": -2.0,
    "downtrend": -2.0,
    "downside": -1.5,
    "losses": -1.5,
    "losing": -1.5,
    "underperform": -1.8,
    "ban": -2.5,
    "banned": -2.5,
    "regulation": -1.0,
    "crackdown": -2.2,
    "investigation": -1.5,
    "lawsuit": -2.0,
    "sec": -0.8,
    "warning": -1.5,
    "bubble": -1.8,
    "volatile": -0.8,
    "fear": -1.5,
    "panic": -2.5,
    "uncertainty": -1.2,
    "concern": -1.0,
    "concerns": -1.0,
    "risk": -0.8,
    "risky": -1.0,
}

# Sözlüğü VADER'a ekle
analyzer.lexicon.update(KRIPTO_SOZLUK)


def _skor_hesapla(baslik):
    """
    VADER ile gelişmiş sentiment skoru hesapla.
    compound skoru kullanır: -1 (çok olumsuz) ile +1 (çok olumlu).
    """
    sonuc = analyzer.polarity_scores(baslik)
    return sonuc['compound']


def _durum_belirle(skor):
    """Skor eşiklerine göre durum belirle"""
    if skor >= 0.05:
        return "Olumlu"
    elif skor <= -0.05:
        return "Olumsuz"
    else:
        return "Nötr"


def get_sentiment_data():
    """
    Birden fazla RSS kaynağından son 24 saatin haberlerini çeker ve sentiment analizi yapar.
    VADER + Kripto özel sözlük ile geliştirilmiş analiz.
    """
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
    
    bir_gun_once = datetime.now() - timedelta(days=1)
    
    tum_haberler = []
    gorulen_basliklar = set()
    
    for url in kaynaklar:
        try:
            response = requests.get(url, headers=headers, timeout=8)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                
                for entry in feed.entries:
                    baslik = entry.title.strip()
                    
                    if baslik.lower() in gorulen_basliklar:
                        continue
                    gorulen_basliklar.add(baslik.lower())
                    
                    haber_tarihi = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        try:
                            haber_tarihi = datetime(*entry.published_parsed[:6])
                        except:
                            pass
                    
                    if haber_tarihi and haber_tarihi < bir_gun_once:
                        continue
                    
                    tum_haberler.append({
                        "baslik": baslik,
                        "tarih": haber_tarihi,
                        "kaynak": url.split('/')[2]
                    })
                    
        except Exception as e:
            continue
    
    if not tum_haberler:
        return 0.0, "Veri Yok", []
    
    tum_haberler.sort(key=lambda x: x["tarih"] or datetime.min, reverse=True)
    
    # VADER + Kripto sözlük ile sentiment analizi
    toplam_skor = 0
    detaylar = []
    
    for haber in tum_haberler:
        baslik = haber["baslik"]
        skor = _skor_hesapla(baslik)
        
        toplam_skor += skor
        
        detaylar.append({
            "baslik": baslik, 
            "skor": round(skor, 3),
            "durum": _durum_belirle(skor)
        })
    
    haber_sayisi = len(detaylar)
    ortalama_skor = toplam_skor / haber_sayisi if haber_sayisi > 0 else 0
    
    kaynak_bilgisi = f"{haber_sayisi} haber ({len(kaynaklar)} kaynak)"
    
    return ortalama_skor, kaynak_bilgisi, detaylar


def stream_news_data():
    """
    Haberleri tek tek yield ederek stream olarak gönderir.
    VADER + Kripto sözlük ile geliştirilmiş analiz.
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
                
                for entry in feed.entries[:15]:
                    baslik = entry.title.strip()
                    
                    if baslik.lower() in gorulen_basliklar:
                        continue
                    gorulen_basliklar.add(baslik.lower())
                    
                    haber_tarihi = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        try:
                            haber_tarihi = datetime(*entry.published_parsed[:6])
                            if haber_tarihi < bir_gun_once:
                                continue
                        except:
                            pass
                    
                    # VADER ile sentiment analizi
                    skor = _skor_hesapla(baslik)
                    
                    yield {
                        "baslik": baslik,
                        "skor": round(skor, 3),
                        "durum": _durum_belirle(skor)
                    }
                    
        except Exception as e:
            continue