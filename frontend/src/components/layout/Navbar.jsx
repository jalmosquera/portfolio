import { Link, useLocation } from 'react-router-dom'
import { APP_ROUTES } from '../../lib/config/routes'

export function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="fixed inset-x-0 top-0 z-50 border-b border-border bg-bg/90 backdrop-blur-lg">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5 sm:px-8">
        {/* Logo */}
        <Link to={APP_ROUTES.home} className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-md bg-accent-soft text-accent ring-1 ring-accent/40">
            <span className="text-xl font-black">M.</span>
          </div>
          <span className="text-sm font-semibold text-text sm:text-base">Mosquera<span className="text-accent">Soft</span></span>
        </Link>

        {/* Links */}
        <div className="flex items-center gap-4 sm:gap-7">
          <Link to={APP_ROUTES.home} className={`hidden text-sm transition-colors sm:block ${pathname === APP_ROUTES.home ? 'text-text' : 'text-muted hover:text-text'}`}>
            Home
          </Link>
          <Link to={APP_ROUTES.projects} className={`flex items-center gap-1 text-sm transition-colors ${pathname.startsWith(APP_ROUTES.projects) ? 'text-text' : 'text-muted hover:text-text'}`}>
            Projects
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </Link>
          <a href="#about" className="hidden text-sm text-muted transition-colors hover:text-text sm:block">About</a>
          <a
            href="mailto:jalberth@mosquera.dev"
            className="flex items-center gap-1.5 rounded-md border border-accent/50 bg-accent-soft px-3 py-1.5 text-sm font-medium text-accent transition-colors hover:border-accent hover:bg-accent hover:text-bg sm:px-4"
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
