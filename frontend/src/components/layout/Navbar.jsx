import { Link, useLocation } from 'react-router-dom'
import { APP_ROUTES } from '../../lib/config/routes'
import { useLanguage } from '../../context/useLanguage'
import logoMark from '../../assets/logo-mark.jpeg'

export function Navbar() {
  const { pathname } = useLocation()
  const { language, setLanguage, t } = useLanguage()

  return (
    <nav className="fixed inset-x-0 top-0 z-50 border-b border-border bg-bg/90 backdrop-blur-lg">
      <div className="site-container flex h-16 items-center justify-between">
        {/* Logo */}
        <Link to={APP_ROUTES.home} className="flex items-center gap-2">
          <img
            src={logoMark}
            alt=""
            width="40"
            height="40"
            loading="eager"
            decoding="async"
            className="h-10 w-10 rounded-md object-cover ring-1 ring-accent/40"
          />
          <span className="hidden text-sm font-semibold text-text min-[420px]:inline sm:text-base">Jalberth<span className="text-accent"> Mosquera</span></span>
        </Link>

        {/* Links */}
        <div className="flex items-center gap-2 min-[420px]:gap-4 sm:gap-7">
          <Link to={APP_ROUTES.home} className={`hidden text-sm transition-colors sm:block ${pathname === APP_ROUTES.home ? 'text-text' : 'text-muted hover:text-text'}`}>
            {t('navHome')}
          </Link>
          <Link to={APP_ROUTES.projects} className={`text-sm transition-colors ${pathname.startsWith(APP_ROUTES.projects) ? 'text-text' : 'text-muted hover:text-text'}`}>
            {t('navProjects')}
          </Link>
          <a href="/#about" className="hidden text-sm text-muted transition-colors hover:text-text sm:block">{t('navAbout')}</a>
          <div className="flex rounded-md border border-border bg-card p-0.5" aria-label={t('languageSelector')}>
            {['es', 'en'].map((code) => (
              <button key={code} type="button" onClick={() => setLanguage(code)} aria-pressed={language === code} className={`rounded px-2 py-1 text-[11px] font-semibold transition-colors ${language === code ? 'bg-accent text-bg' : 'text-muted hover:text-text'}`}>
                {code.toUpperCase()}
              </button>
            ))}
          </div>
          <a
            href="/#contact"
            className="flex items-center gap-1.5 rounded-md border border-accent/50 bg-accent-soft px-3 py-1.5 text-sm font-medium text-accent transition-colors hover:border-accent hover:bg-accent hover:text-bg sm:px-4"
          >
            <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
              <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
            </svg>
            <span className="hidden min-[520px]:inline">{t('navContact')}</span>
          </a>
        </div>
      </div>
    </nav> 
  )
}
