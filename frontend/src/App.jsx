import AppRoutes from './routes/AppRoutes.jsx'
import { NewsProvider } from './context/NewsContext.jsx'
import './App.css'

function App() {
  return (
    <NewsProvider>
      <AppRoutes />
    </NewsProvider>
  )
}

export default App
