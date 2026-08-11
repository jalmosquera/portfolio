import { useEffect } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Navbar } from './components/layout/Navbar'
import { Footer } from './components/layout/Footer'
import { HomePage } from './pages/HomePage'
import { ProjectsPage } from './pages/ProjectsPage'
import { ProjectDetailPage } from './pages/ProjectDetailPage'
import { AnalyticsPage } from './pages/AnalyticsPage'
import { APP_ROUTES } from './lib/config/routes'
import { LanguageProvider } from './context/LanguageContext'
import { Toaster } from 'sileo'
import 'sileo/styles.css'
import { recordVisit } from './lib/api/analytics'

const VISIT_SESSION_KEY = 'portfolio_visit_recorded'

function App() {
  useEffect(() => {
    if (window.location.pathname === APP_ROUTES.analytics) return

    try {
      if (sessionStorage.getItem(VISIT_SESSION_KEY)) return

      sessionStorage.setItem(VISIT_SESSION_KEY, 'true')
      recordVisit().catch(() => sessionStorage.removeItem(VISIT_SESSION_KEY))
    } catch {
      recordVisit().catch(() => {})
    }
  }, [])

  return (
    <LanguageProvider><BrowserRouter>
      <Toaster position="top-right" offset={{ top: 80, right: 20 }} theme="dark" />
      <div className="min-h-screen bg-bg flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path={APP_ROUTES.home} element={<HomePage />} />
            <Route path={APP_ROUTES.projects} element={<ProjectsPage />} />
            <Route path={APP_ROUTES.projectDetail} element={<ProjectDetailPage />} />
            <Route path={APP_ROUTES.analytics} element={<AnalyticsPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter></LanguageProvider>
  )
}

export default App
