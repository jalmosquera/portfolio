import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Navbar } from './components/layout/Navbar'
import { Footer } from './components/layout/Footer'
import { HomePage } from './pages/HomePage'
import { ProjectsPage } from './pages/ProjectsPage'
import { ProjectDetailPage } from './pages/ProjectDetailPage'
import { APP_ROUTES } from './lib/config/routes'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-bg flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path={APP_ROUTES.home} element={<HomePage />} />
            <Route path={APP_ROUTES.projects} element={<ProjectsPage />} />
            <Route path={APP_ROUTES.projectDetail} element={<ProjectDetailPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  )
}

export default App
