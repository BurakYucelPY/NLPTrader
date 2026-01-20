// Route yapılandırması
import { Routes, Route, Navigate } from 'react-router-dom'
import { ROUTES } from './paths.jsx'
import HomePage from '../pages/HomePage'
import BTCPage from '../pages/coins/BTCPage'
import ETHPage from '../pages/coins/ETHPage'
import BNBPage from '../pages/coins/BNBPage'
import SOLPage from '../pages/coins/SOLPage'
import XRPPage from '../pages/coins/XRPPage'
import DOGEPage from '../pages/coins/DOGEPage'
import ADAPage from '../pages/coins/ADAPage'
import AVAXPage from '../pages/coins/AVAXPage'
import SHIBPage from '../pages/coins/SHIBPage'
import TRXPage from '../pages/coins/TRXPage'
import DOTPage from '../pages/coins/DOTPage'
import LINKPage from '../pages/coins/LINKPage'
import LTCPage from '../pages/coins/LTCPage'
import BCHPage from '../pages/coins/BCHPage'
import NEARPage from '../pages/coins/NEARPage'
import FETPage from '../pages/coins/FETPage'

function AppRoutes() {
  return (
    <Routes>
      <Route path={ROUTES.HOME} element={<HomePage />} />
      <Route path={ROUTES.BTC} element={<BTCPage />} />
      <Route path={ROUTES.ETH} element={<ETHPage />} />
      <Route path={ROUTES.BNB} element={<BNBPage />} />
      <Route path={ROUTES.SOL} element={<SOLPage />} />
      <Route path={ROUTES.XRP} element={<XRPPage />} />
      <Route path={ROUTES.DOGE} element={<DOGEPage />} />
      <Route path={ROUTES.ADA} element={<ADAPage />} />
      <Route path={ROUTES.AVAX} element={<AVAXPage />} />
      <Route path={ROUTES.SHIB} element={<SHIBPage />} />
      <Route path={ROUTES.TRX} element={<TRXPage />} />
      <Route path={ROUTES.DOT} element={<DOTPage />} />
      <Route path={ROUTES.LINK} element={<LINKPage />} />
      <Route path={ROUTES.LTC} element={<LTCPage />} />
      <Route path={ROUTES.BCH} element={<BCHPage />} />
      <Route path={ROUTES.NEAR} element={<NEARPage />} />
      <Route path={ROUTES.FET} element={<FETPage />} />
      <Route path="*" element={<Navigate to={ROUTES.HOME} replace />} />
    </Routes>
  )
}

export { ROUTES }
export default AppRoutes
