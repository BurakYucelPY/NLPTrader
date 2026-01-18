// Route yapılandırması
import { Routes, Route, Navigate } from 'react-router-dom'
import { ROUTES } from './paths.jsx'
import HomePage from '../pages/HomePage'
import BTCPage from '../pages/BTCPage'
import ETHPage from '../pages/ETHPage'
import BNBPage from '../pages/BNBPage'
import SOLPage from '../pages/SOLPage'
import XRPPage from '../pages/XRPPage'
import DOGEPage from '../pages/DOGEPage'
import ADAPage from '../pages/ADAPage'
import AVAXPage from '../pages/AVAXPage'
import SHIBPage from '../pages/SHIBPage'
import TRXPage from '../pages/TRXPage'
import DOTPage from '../pages/DOTPage'
import LINKPage from '../pages/LINKPage'
import MATICPage from '../pages/MATICPage'
import LTCPage from '../pages/LTCPage'
import BCHPage from '../pages/BCHPage'
import NEARPage from '../pages/NEARPage'
import UNIPage from '../pages/UNIPage'
import PEPEPage from '../pages/PEPEPage'
import FETPage from '../pages/FETPage'
import RNDRPage from '../pages/RNDRPage'

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
      <Route path={ROUTES.MATIC} element={<MATICPage />} />
      <Route path={ROUTES.LTC} element={<LTCPage />} />
      <Route path={ROUTES.BCH} element={<BCHPage />} />
      <Route path={ROUTES.NEAR} element={<NEARPage />} />
      <Route path={ROUTES.UNI} element={<UNIPage />} />
      <Route path={ROUTES.PEPE} element={<PEPEPage />} />
      <Route path={ROUTES.FET} element={<FETPage />} />
      <Route path={ROUTES.RNDR} element={<RNDRPage />} />
      <Route path="*" element={<Navigate to={ROUTES.HOME} replace />} />
    </Routes>
  )
}

export { ROUTES }
export default AppRoutes
