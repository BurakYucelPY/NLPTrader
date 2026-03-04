import AppRoutes from './routes/AppRoutes.jsx'
import { NewsProvider } from './context/NewsContext.jsx'
import ChatBot from './components/ChatBot.jsx'
import BackendWakeUp from './components/BackendWakeUp.jsx'
import './App.css'

function App() {
  return (
    <NewsProvider>
      <BackendWakeUp />
      <AppRoutes />
      <ChatBot />
    </NewsProvider>
  )
}

export default App

