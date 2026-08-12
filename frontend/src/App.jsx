import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Navbar } from './components/layout/Navbar'
import { Footer } from './components/layout/Footer'
import { HomePage } from './pages/HomePage'
import { ProjectsPage } from './pages/ProjectsPage'
import { ProjectDetailPage } from './pages/ProjectDetailPage'
import { AnalyticsPage } from './pages/AnalyticsPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { APP_ROUTES } from './lib/config/routes'
import { LanguageProvider } from './context/LanguageContext'
import { Toaster } from 'sileo'
import 'sileo/styles.css'
import { AnalyticsTracker } from './components/analytics/AnalyticsTracker'

function App() {
  return (
    <LanguageProvider><BrowserRouter>
      <AnalyticsTracker />
      <Toaster position="top-right" offset={{ top: 80, right: 20 }} theme="dark" />
      <div className="min-h-screen bg-bg flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path={APP_ROUTES.home} element={<HomePage />} />
            <Route path={APP_ROUTES.projects} element={<ProjectsPage />} />
            <Route path={APP_ROUTES.projectDetail} element={<ProjectDetailPage />} />
            <Route path={APP_ROUTES.analytics} element={<AnalyticsPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter></LanguageProvider>
  )
}

export default App
