import React, { useState, useRef, useEffect } from 'react'
import { KRIPTO_LISTESI } from '../routes/paths.jsx'
import { API_BASE } from '../config/api'

const CHATBOT_API = `${API_BASE}/chatbot`

function ChatBot() {
  // Durumlar: 'closed', 'coin-select', 'chat'
  const [durum, setDurum] = useState('closed')
  const [secilenCoin, setSecilenCoin] = useState(null)
  const [mesajlar, setMesajlar] = useState([])
  const [inputDeger, setInputDeger] = useState('')
  const [yukleniyor, setYukleniyor] = useState(false)
  const mesajListeRef = useRef(null)

  // Yeni mesaj geldiğinde en alta scroll
  useEffect(() => {
    if (mesajListeRef.current) {
      mesajListeRef.current.scrollTop = mesajListeRef.current.scrollHeight
    }
  }, [mesajlar])

  // Chatbot aç/kapat
  const toggleChatbot = () => {
    if (durum === 'closed') {
      setDurum('coin-select')
    } else {
      setDurum('closed')
    }
  }

  // Coin seçildiğinde — hoşgeldin mesajı göster
  const coinSec = (coin) => {
    setSecilenCoin(coin)
    setDurum('chat')
    setMesajlar([{
      role: 'assistant',
      content: `Merhaba! 👋 ${coin.ikon} ${coin.ad} (${coin.sembol}) hakkında ne öğrenmek istersin?\n\nÖrneğin şunları sorabilirsin:\n• "Şu anki analiz durumu ne?"\n• "Almalı mıyım satmalı mıyım?"\n• "RSI ve MACD ne gösteriyor?"\n• "Risk analizi yap"`
    }])
  }

  // Mesaj gönder
  const mesajGonder = async () => {
    if (!inputDeger.trim() || yukleniyor) return

    const yeniMesaj = { role: 'user', content: inputDeger.trim() }
    const guncelMesajlar = [...mesajlar, yeniMesaj]
    setMesajlar(guncelMesajlar)
    setInputDeger('')
    setYukleniyor(true)

    try {
      // Konuşma geçmişini gönder
      const gecmis = guncelMesajlar.map(m => ({
        role: m.role,
        content: m.content
      }))

      const response = await fetch(CHATBOT_API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sembol: secilenCoin.sembol,
          mesaj: inputDeger.trim(),
          gecmis: gecmis.slice(0, -1)
        })
      })
      const data = await response.json()
      setMesajlar(prev => [...prev, {
        role: 'assistant',
        content: data.cevap
      }])
    } catch (err) {
      setMesajlar(prev => [...prev, {
        role: 'assistant',
        content: '⚠️ Bir hata oluştu, lütfen tekrar deneyin.'
      }])
    } finally {
      setYukleniyor(false)
    }
  }

  // Enter ile gönder
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      mesajGonder()
    }
  }

  // Geri butonu — coin seçimine dön
  const geriDon = () => {
    setDurum('coin-select')
    setSecilenCoin(null)
    setMesajlar([])
  }

  return (
    <>
      {/* Toggle Butonu */}
      <button className="chatbot-toggle" onClick={toggleChatbot}>
        {durum === 'closed' ? '🤖' : '✕'}
      </button>

      {/* Panel */}
      {durum !== 'closed' && (
        <div className="chatbot-panel">

          {/* Header */}
          <div className="chatbot-header">
            {durum === 'chat' && (
              <button className="chatbot-back" onClick={geriDon}>←</button>
            )}
            <span className="chatbot-title">
              {durum === 'coin-select'
                ? '🤖 NLPTrader Asistan'
                : `💬 ${secilenCoin?.sembol} Analiz Sohbeti`}
            </span>
          </div>

          {/* Coin Seçim Ekranı */}
          {durum === 'coin-select' && (
            <div className="chatbot-coin-list">
              <p className="chatbot-coin-hint">Analiz etmek istediğiniz kripto parayı seçin:</p>
              <div className="chatbot-coins-grid">
                {KRIPTO_LISTESI.map((coin) => (
                  <button
                    key={coin.sembol}
                    className="chatbot-coin-btn"
                    onClick={() => coinSec(coin)}
                    style={{ borderColor: coin.renk }}
                  >
                    <span className="chatbot-coin-icon">{coin.ikon}</span>
                    <span className="chatbot-coin-symbol">{coin.sembol}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Sohbet Ekranı */}
          {durum === 'chat' && (
            <>
              <div className="chatbot-messages" ref={mesajListeRef}>
                {mesajlar.map((m, i) => (
                  <div key={i} className={`chatbot-msg ${m.role}`}>
                    <div className="chatbot-msg-bubble">
                      {m.content}
                    </div>
                  </div>
                ))}
                {yukleniyor && (
                  <div className="chatbot-msg assistant">
                    <div className="chatbot-msg-bubble chatbot-typing">
                      <span></span><span></span><span></span>
                    </div>
                  </div>
                )}
              </div>

              <div className="chatbot-input-area">
                <input
                  type="text"
                  className="chatbot-input"
                  placeholder={`${secilenCoin?.sembol} hakkında sor...`}
                  value={inputDeger}
                  onChange={(e) => setInputDeger(e.target.value)}
                  onKeyDown={handleKeyDown}
                  disabled={yukleniyor}
                />
                <button
                  className="chatbot-send"
                  onClick={mesajGonder}
                  disabled={yukleniyor || !inputDeger.trim()}
                >
                  ➤
                </button>
              </div>
            </>
          )}

        </div>
      )}
    </>
  )
}

export default ChatBot
