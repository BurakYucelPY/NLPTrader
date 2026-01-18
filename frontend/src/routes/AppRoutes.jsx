// Route yapılandırması
import { Routes, Route, Navigate } from 'react-router-dom'
import { ROUTES } from './paths.jsx'
import HomePage from '../pages/HomePage'
import AnalysisPage from '../pages/AnalysisPage'

function AppRoutes() {
  return (
    <Routes>
      <Route path={ROUTES.HOME} element={<HomePage />} />
      <Route path={ROUTES.ANALYSIS} element={<AnalysisPage />} />
      <Route path="*" element={<Navigate to={ROUTES.HOME} replace />} />
    </Routes>
  )
}

export { ROUTES }
export default AppRoutes
