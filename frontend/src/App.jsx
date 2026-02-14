import AppRoutes from './routes/AppRoutes.jsx'
import { NewsProvider } from './context/NewsContext.jsx'
import ChatBot from './components/ChatBot.jsx'
import './App.css'

function App() {
  return (
    <NewsProvider>
      <AppRoutes />
      <ChatBot />
    </NewsProvider>
  )
}

export default App
