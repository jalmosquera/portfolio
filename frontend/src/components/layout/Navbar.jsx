import { Link, useLocation } from 'react-router-dom'

export function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-bg/90 backdrop-blur-sm border-b border-border">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-bold text-lg">
          <span className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center text-white font-black text-sm">M</span>
          <span className="text-text">MosqueraSoft</span>
        </Link>

        <div className="flex items-center gap-6">
          <Link to="/" className={`text-sm transition-colors ${pathname === '/' ? 'text-accent' : 'text-muted hover:text-text'}`}>
            Home
          </Link>
          <Link to="/projects" className={`text-sm transition-colors ${pathname.startsWith('/projects') ? 'text-accent' : 'text-muted hover:text-text'}`}>
            Projects
          </Link>
          <a
            href="mailto:jalberth@example.com"
            className="text-sm border border-accent text-accent px-4 py-1.5 rounded-lg hover:bg-accent hover:text-white transition-all"
          >
            Contact
          </a>
        </div>
      </div>
    </nav>
  )
}
