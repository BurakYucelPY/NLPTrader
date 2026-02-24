import { useEffect, useRef, useState, useCallback } from 'react'
import { createChart, ColorType, AreaSeries, HistogramSeries } from 'lightweight-charts'

const PERIYOTLAR = [
    { label: '1G', value: '1d' },
    { label: '5G', value: '5d' },
    { label: '1A', value: '1mo' },
    { label: '6A', value: '6mo' },
    { label: '1Y', value: '1y' },
    { label: 'Maks', value: 'max' },
]

function PriceChart({ sembol, coinRenk = '#007bff' }) {
    const chartContainerRef = useRef(null)
    const chartRef = useRef(null)
    const seriesRef = useRef(null)
    const volumeSeriesRef = useRef(null)

    const [periyot, setPeriyot] = useState('6mo')
    const [yukleniyor, setYukleniyor] = useState(false)
    const [grafik, setGrafik] = useState(null)
    const [hata, setHata] = useState(null)

    // Grafik verisini çek
    const veriCek = useCallback(async (secilenPeriyot) => {
        setYukleniyor(true)
        setHata(null)
        try {
            const res = await fetch(
                `http://localhost:5199/api/Finans/grafik/${sembol.toLowerCase()}?periyot=${secilenPeriyot}`
            )
            const data = await res.json()
            if (data.hata) {
                setHata(data.hata)
                return
            }
            setGrafik(data)
        } catch (err) {
            setHata('Grafik verisi yüklenemedi')
            console.error(err)
        } finally {
            setYukleniyor(false)
        }
    }, [sembol])

    // İlk yükleme ve periyot değişiminde veri çek
    useEffect(() => {
        veriCek(periyot)
    }, [periyot, veriCek])

    // Chart'ı oluştur / güncelle
    useEffect(() => {
        if (!chartContainerRef.current || !grafik?.veri?.length) return

        // Eğer chart yoksa oluştur
        if (!chartRef.current) {
            const chart = createChart(chartContainerRef.current, {
                autoSize: true,
                layout: {
                    background: { type: ColorType.Solid, color: 'transparent' },
                    textColor: '#9ca3af',
                    fontSize: 12,
                },
                grid: {
                    vertLines: { color: 'rgba(255,255,255,0.04)' },
                    horzLines: { color: 'rgba(255,255,255,0.04)' },
                },
                crosshair: {
                    mode: 0,
                    vertLine: {
                        color: coinRenk + '60',
                        width: 1,
                        style: 2,
                        labelBackgroundColor: coinRenk,
                    },
                    horzLine: {
                        color: coinRenk + '60',
                        width: 1,
                        style: 2,
                        labelBackgroundColor: coinRenk,
                    },
                },
                rightPriceScale: {
                    borderColor: 'rgba(255,255,255,0.08)',
                    scaleMargins: { top: 0.1, bottom: 0.25 },
                },
                timeScale: {
                    borderColor: 'rgba(255,255,255,0.08)',
                    timeVisible: periyot === '1d' || periyot === '5d',
                    secondsVisible: false,
                    fixLeftEdge: true,
                    fixRightEdge: true,
                    rightOffset: 0,
                },
                handleScroll: { mouseWheel: false, pressedMouseMove: true, horzTouchDrag: true, vertTouchDrag: false },
                handleScale: { mouseWheel: false, pinch: false, axisPressedMouseMove: false },
            })

            // Area serisi (çizgi + gradyan dolgu)
            const areaSeries = chart.addSeries(AreaSeries, {
                lineColor: coinRenk,
                lineWidth: 2,
                topColor: coinRenk + '40',
                bottomColor: coinRenk + '05',
                crosshairMarkerBackgroundColor: coinRenk,
                crosshairMarkerBorderColor: '#fff',
                crosshairMarkerBorderWidth: 2,
                crosshairMarkerRadius: 5,
                priceFormat: { type: 'price', minMove: 0.01, precision: 2 },
            })

            // Hacim serisi
            const volumeSeries = chart.addSeries(HistogramSeries, {
                color: coinRenk + '30',
                priceFormat: { type: 'volume' },
                priceScaleId: '',
            })
            volumeSeries.priceScale().applyOptions({
                scaleMargins: { top: 0.85, bottom: 0 },
            })

            chartRef.current = chart
            seriesRef.current = areaSeries
            volumeSeriesRef.current = volumeSeries
        }

        // TimeScale ayarını güncelle
        chartRef.current.timeScale().applyOptions({
            timeVisible: periyot === '1d' || periyot === '5d',
        })

        // Verileri güncelle
        const areaData = grafik.veri.map(d => ({
            time: d.time,
            value: d.close,
        }))

        const volumeData = grafik.veri.map(d => ({
            time: d.time,
            value: d.volume,
            color: d.close >= d.open ? coinRenk + '30' : '#ef444430',
        }))

        seriesRef.current.setData(areaData)
        volumeSeriesRef.current.setData(volumeData)
        chartRef.current.timeScale().fitContent()

    }, [grafik, coinRenk, periyot])

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            if (chartRef.current) {
                chartRef.current.remove()
                chartRef.current = null
                seriesRef.current = null
                volumeSeriesRef.current = null
            }
        }
    }, [])

    const degisimPozitif = grafik && grafik.degisim >= 0

    return (
        <div className="price-chart-wrapper">
            {/* Fiyat Header */}
            {grafik && !hata && (
                <div className="chart-price-header">
                    <div className="chart-price-main">
                        <span className="chart-price-value">${grafik.fiyat?.toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
                    </div>
                    <div className={`chart-price-change ${degisimPozitif ? 'positive' : 'negative'}`}>
                        {degisimPozitif ? '+' : ''}{grafik.degisim?.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                        ({degisimPozitif ? '+' : ''}{grafik.degisim_yuzde?.toFixed(2)}%)
                        <span className="chart-period-label">
                            {PERIYOTLAR.find(p => p.value === periyot)?.label || periyot}
                        </span>
                    </div>
                </div>
            )}

            {/* Periyot Butonları */}
            <div className="chart-period-buttons">
                {PERIYOTLAR.map((p) => (
                    <button
                        key={p.value}
                        className={`chart-period-btn ${periyot === p.value ? 'active' : ''}`}
                        onClick={() => {
                            // Chart'ı sıfırla ki yeni veriye uygun yeniden render olsun
                            if (chartRef.current) {
                                chartRef.current.remove()
                                chartRef.current = null
                                seriesRef.current = null
                                volumeSeriesRef.current = null
                            }
                            setPeriyot(p.value)
                        }}
                        style={{
                            '--btn-color': coinRenk,
                        }}
                    >
                        {p.label}
                    </button>
                ))}
            </div>

            {/* Grafik Alanı */}
            <div className="chart-container">
                {yukleniyor && (
                    <div className="chart-loading">
                        <div className="chart-loading-spinner" style={{ borderTopColor: coinRenk }}></div>
                        <span>Grafik yükleniyor...</span>
                    </div>
                )}
                {hata && (
                    <div className="chart-error">
                        <span>⚠️ {hata}</span>
                    </div>
                )}
                <div
                    ref={chartContainerRef}
                    className="chart-canvas"
                    style={{ opacity: yukleniyor ? 0.3 : 1 }}
                />
            </div>
        </div>
    )
}

export default PriceChart
