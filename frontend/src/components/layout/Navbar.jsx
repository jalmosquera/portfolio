import { Link, useLocation } from 'react-router-dom'
import { APP_ROUTES } from '../../lib/config/routes'

export function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0b0b0b]/85 backdrop-blur-lg border-b border-border">
      <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
        {/* Logo */}
        <Link to={APP_ROUTES.home} className="flex items-center gap-2">
          <div className="w-9 h-9 bg-accent rounded-lg flex items-center justify-center shadow-[0_10px_20px_rgba(215,121,44,0.35)]">
            <span className="text-white font-black text-sm">M</span>
          </div>
          <span className="text-white font-semibold text-sm">MosqueraSoft</span>
        </Link>

        {/* Links */}
        <div className="flex items-center gap-7">
          <Link to={APP_ROUTES.home} className={`text-sm transition-colors ${pathname === APP_ROUTES.home ? 'text-white' : 'text-[#9ca3af] hover:text-white'}`}>
            Home
          </Link>
          <Link to={APP_ROUTES.projects} className={`text-sm transition-colors flex items-center gap-1 ${pathname.startsWith(APP_ROUTES.projects) ? 'text-white' : 'text-[#9ca3af] hover:text-white'}`}>
            Projects
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </Link>
          <a href="#about" className="text-sm text-[#9ca3af] hover:text-white transition-colors">About</a>
          <a
            href="mailto:jalberth@mosquera.dev"
            className="flex items-center gap-1.5 text-sm border border-accent text-accent px-4 py-1.5 rounded-md hover:bg-accent hover:text-white transition-all font-medium shadow-[0_10px_24px_rgba(215,121,44,0.25)]"
          >
            <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
              <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
            </svg>
            Contact
          </a>
        </div>
      </div>
    </nav>
  )
}
