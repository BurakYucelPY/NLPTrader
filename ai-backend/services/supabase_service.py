"""
Supabase Kıyaslamalı Başarı Sistemi Servisi
============================================
Supabase REST API üzerinden trade_signals ve crypto_coins tablolarıyla 
etkileşim kurar. Her analiz çağrısında:
1. Önceki NULL kaydı bulur ve güncel fiyatla kıyaslayarak başarı durumunu günceller
2. Yeni fiyatı NULL başarı durumuyla kaydeder
"""

import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ─── Supabase REST API Yapılandırması ────────────────────────────────────
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
REST_BASE = f"{SUPABASE_URL}/rest/v1"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}


# ─── Temel Veritabanı İşlemleri ─────────────────────────────────────────

def get_coin_id(sembol: str) -> int | None:
    """
    Sembol'e göre crypto_coins tablosundan coin_id döndürür.
    Bulamazsa None döner.
    """
    url = f"{REST_BASE}/crypto_coins"
    params = {
        "select": "coin_id",
        "symbol": f"eq.{sembol.upper()}"
    }
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data[0]["coin_id"] if data else None


def get_last_null_signal(coin_id: int) -> dict | None:
    """
    Belirli bir coin için is_successful değeri NULL olan 
    en son kaydı (en yeni signal_date) döndürür.
    """
    url = f"{REST_BASE}/trade_signals"
    params = {
        "select": "signal_id,entry_price,signal_date",
        "coin_id": f"eq.{coin_id}",
        "is_successful": "is.null",
        "order": "signal_date.desc",
        "limit": "1"
    }
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data[0] if data else None


def update_signal_success(signal_id: int, is_successful: int):
    """
    Eski kaydın is_successful alanını günceller.
    is_successful: 1 (başarılı) veya 0 (başarısız)
    """
    url = f"{REST_BASE}/trade_signals"
    params = {"signal_id": f"eq.{signal_id}"}
    body = {"is_successful": is_successful}
    resp = requests.patch(url, headers=HEADERS, params=params, json=body, timeout=10)
    resp.raise_for_status()
    return resp.json()


def insert_new_signal(coin_id: int, entry_price: float):
    """
    Yeni fiyat kaydını veritabanına ekler.
    is_successful NULL olarak kalır (henüz sonucu belli değil).
    """
    url = f"{REST_BASE}/trade_signals"
    body = {
        "coin_id": coin_id,
        "entry_price": entry_price,
        "is_successful": None,
        "signal_date": datetime.utcnow().isoformat()
    }
    resp = requests.post(url, headers=HEADERS, json=body, timeout=10)
    resp.raise_for_status()
    return resp.json()


# ─── Ana Mantık: Sinyal İşleme ──────────────────────────────────────────

def process_signal(sembol: str, current_price: float) -> dict:
    """
    Kıyaslamalı başarı sisteminin ana fonksiyonu.
    
    1. coin_id'yi bul
    2. Son NULL kaydı getir (varsa)
    3. Güncel fiyatla kıyasla → eski kaydı güncelle
    4. Yeni kayıt ekle (NULL durumla)
    
    Returns:
        dict: İşlem sonucu bilgileri
    """
    coin_id = get_coin_id(sembol)
    if coin_id is None:
        return {"durum": "hata", "mesaj": f"{sembol} coin bulunamadı"}
    
    sonuc = {
        "sembol": sembol.upper(),
        "coin_id": coin_id,
        "guncel_fiyat": current_price,
        "onceki_kayit": None,
        "kiyaslama": None
    }
    
    # Son NULL kaydı kontrol et
    son_kayit = get_last_null_signal(coin_id)
    
    if son_kayit:
        eski_fiyat = float(son_kayit["entry_price"])
        signal_id = son_kayit["signal_id"]
        
        # Kıyaslama: Güncel fiyat > Eski fiyat → Başarılı
        basarili = 1 if current_price > eski_fiyat else 0
        
        # Eski kaydı güncelle
        update_signal_success(signal_id, basarili)
        
        sonuc["onceki_kayit"] = {
            "signal_id": signal_id,
            "eski_fiyat": eski_fiyat,
            "tarih": son_kayit["signal_date"]
        }
        sonuc["kiyaslama"] = {
            "basarili": bool(basarili),
            "fark": round(current_price - eski_fiyat, 8),
            "fark_yuzde": round(((current_price - eski_fiyat) / eski_fiyat) * 100, 2)
        }
    
    # Yeni kayıt ekle (is_successful = NULL)
    insert_new_signal(coin_id, current_price)
    
    sonuc["durum"] = "basarili"
    return sonuc


# ─── Başarı Oranı Hesaplama ─────────────────────────────────────────────

def get_success_rate(sembol: str) -> dict:
    """
    Tek bir coin'in başarı oranını ve istatistiklerini döndürür.
    Sadece is_successful değeri NULL olmayan (sonuçlanmış) kayıtları sayar.
    """
    coin_id = get_coin_id(sembol)
    if coin_id is None:
        return {"hata": f"{sembol} coin bulunamadı"}
    
    url = f"{REST_BASE}/trade_signals"
    
    # Başarılı kayıtlar (is_successful = 1)
    params_basarili = {
        "select": "signal_id",
        "coin_id": f"eq.{coin_id}",
        "is_successful": "eq.1"
    }
    resp_basarili = requests.get(url, headers={**HEADERS, "Prefer": "count=exact"}, params=params_basarili, timeout=10)
    resp_basarili.raise_for_status()
    basarili_sayi = len(resp_basarili.json())
    
    # Başarısız kayıtlar (is_successful = 0)
    params_basarisiz = {
        "select": "signal_id",
        "coin_id": f"eq.{coin_id}",
        "is_successful": "eq.0"
    }
    resp_basarisiz = requests.get(url, headers={**HEADERS, "Prefer": "count=exact"}, params=params_basarisiz, timeout=10)
    resp_basarisiz.raise_for_status()
    basarisiz_sayi = len(resp_basarisiz.json())
    
    # Bekleyen kayıtlar (is_successful = NULL)
    params_bekleyen = {
        "select": "signal_id",
        "coin_id": f"eq.{coin_id}",
        "is_successful": "is.null"
    }
    resp_bekleyen = requests.get(url, headers={**HEADERS, "Prefer": "count=exact"}, params=params_bekleyen, timeout=10)
    resp_bekleyen.raise_for_status()
    bekleyen_sayi = len(resp_bekleyen.json())
    
    toplam_sonuclanan = basarili_sayi + basarisiz_sayi
    oran = round((basarili_sayi / toplam_sonuclanan) * 100, 1) if toplam_sonuclanan > 0 else None
    
    return {
        "sembol": sembol.upper(),
        "basari_orani": oran,
        "basarili": basarili_sayi,
        "basarisiz": basarisiz_sayi,
        "bekleyen": bekleyen_sayi,
        "toplam_sinyal": basarili_sayi + basarisiz_sayi + bekleyen_sayi
    }


def get_all_success_rates() -> list:
    """
    Tüm coinlerin başarı oranlarını topluca döndürür.
    Tek seferde tüm sinyalleri çeker ve Python'da hesaplar (hızlı).
    """
    # 1. Tüm coinleri çek (tek istek)
    coins_url = f"{REST_BASE}/crypto_coins"
    coins_params = {"select": "coin_id,symbol,name", "order": "coin_id.asc"}
    coins_resp = requests.get(coins_url, headers=HEADERS, params=coins_params, timeout=10)
    coins_resp.raise_for_status()
    coins = coins_resp.json()
    
    # 2. Tüm sinyalleri tek seferde çek (tek istek)
    signals_url = f"{REST_BASE}/trade_signals"
    signals_params = {
        "select": "coin_id,is_successful",
        "limit": "10000"
    }
    signals_resp = requests.get(signals_url, headers=HEADERS, params=signals_params, timeout=15)
    signals_resp.raise_for_status()
    all_signals = signals_resp.json()
    
    # 3. Python'da hesapla (çok hızlı)
    stats = {}
    for signal in all_signals:
        cid = signal["coin_id"]
        if cid not in stats:
            stats[cid] = {"basarili": 0, "basarisiz": 0, "bekleyen": 0}
        
        is_success = signal["is_successful"]
        if is_success is None:
            stats[cid]["bekleyen"] += 1
        elif is_success == 1:
            stats[cid]["basarili"] += 1
        else:
            stats[cid]["basarisiz"] += 1
    
    # 4. Coin bilgileriyle birleştir
    sonuclar = []
    for coin in coins:
        cid = coin["coin_id"]
        s = stats.get(cid, {"basarili": 0, "basarisiz": 0, "bekleyen": 0})
        toplam_sonuclanan = s["basarili"] + s["basarisiz"]
        oran = round((s["basarili"] / toplam_sonuclanan) * 100, 1) if toplam_sonuclanan > 0 else None
        
        sonuclar.append({
            "sembol": coin["symbol"],
            "ad": coin["name"],
            "basari_orani": oran,
            "basarili": s["basarili"],
            "basarisiz": s["basarisiz"],
            "bekleyen": s["bekleyen"],
            "toplam_sinyal": s["basarili"] + s["basarisiz"] + s["bekleyen"]
        })
    
    return sonuclar
