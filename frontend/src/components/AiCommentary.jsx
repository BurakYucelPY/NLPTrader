import { useEffect, useState } from 'react'
import { API_BASE } from '../config/api'

function AiCommentary({ sembol, coinRenk = '#007bff' }) {
    const [yorum, setYorum] = useState(null)
    const [yukleniyor, setYukleniyor] = useState(false)
    const [hata, setHata] = useState(null)

    useEffect(() => {
        if (!sembol) return

        const yorumCek = async () => {
            setYukleniyor(true)
            setHata(null)
            try {
                const res = await fetch(
                    `${API_BASE}/yorum/${sembol.toLowerCase()}`
                )
                const data = await res.json()
                if (data.hata) {
                    setHata(data.hata)
                } else {
                    setYorum(data.yorum)
                }
            } catch (err) {
                setHata('Yapay zeka yorumu yüklenemedi')
                console.error(err)
            } finally {
                setYukleniyor(false)
            }
        }

        yorumCek()
    }, [sembol])

    // Basit markdown render (bold, emoji, headers, lists)
    const renderMarkdown = (text) => {
        if (!text) return null

        return text.split('\n').map((line, i) => {
            // Headers
            if (line.startsWith('### ')) {
                return <h4 key={i} className="ai-md-h3">{parseBold(line.slice(4))}</h4>
            }
            if (line.startsWith('## ')) {
                return <h3 key={i} className="ai-md-h2">{parseBold(line.slice(3))}</h3>
            }
            if (line.startsWith('# ')) {
                return <h2 key={i} className="ai-md-h1">{parseBold(line.slice(2))}</h2>
            }
            // Horizontal rule
            if (line.trim() === '---' || line.trim() === '***') {
                return <hr key={i} className="ai-md-hr" />
            }
            // List items
            if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
                return <li key={i} className="ai-md-li">{parseBold(line.trim().slice(2))}</li>
            }
            // Empty line
            if (line.trim() === '') {
                return <div key={i} className="ai-md-spacer" />
            }
            // Normal text
            return <p key={i} className="ai-md-p">{parseBold(line)}</p>
        })
    }

    // Bold text parser
    const parseBold = (text) => {
        const parts = text.split(/\*\*(.*?)\*\*/g)
        return parts.map((part, i) =>
            i % 2 === 1 ? <strong key={i}>{part}</strong> : part
        )
    }

    return (
        <div className="ai-commentary-box" style={{ borderColor: coinRenk + '25' }}>
            <div className="ai-commentary-header">
                <span className="ai-commentary-header-icon">🤖</span>
                <span className="ai-commentary-header-text">Yapay Zeka Yorumu</span>
                <span
                    className="ai-commentary-live-badge"
                    style={{ background: coinRenk + '20', color: coinRenk }}
                >
                    AI
                </span>
            </div>

            <div className="ai-commentary-body">
                {yukleniyor && (
                    <div className="ai-commentary-loading">
                        <div className="ai-typing-indicator" style={{ '--dot-color': coinRenk }}>
                            <span></span><span></span><span></span>
                        </div>
                        <p>Yapay zeka analiz ediyor...</p>
                    </div>
                )}

                {hata && (
                    <div className="ai-commentary-error">
                        <span>⚠️ {hata}</span>
                    </div>
                )}

                {yorum && !yukleniyor && (
                    <div className="ai-commentary-content">
                        {renderMarkdown(yorum)}
                    </div>
                )}
            </div>
        </div>
    )
}

export default AiCommentary
