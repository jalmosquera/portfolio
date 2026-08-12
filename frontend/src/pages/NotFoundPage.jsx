import { Link, useLocation } from 'react-router-dom'

import { useLanguage } from '../context/useLanguage'
import { APP_ROUTES } from '../lib/config/routes'

export function NotFoundPage() {
  const { pathname } = useLocation()
  const { t } = useLanguage()

  return (
    <section className="site-container flex min-h-[calc(100vh-4rem)] items-center justify-center py-28">
      <div className="relative w-full max-w-3xl overflow-hidden rounded-2xl border border-border bg-card px-6 py-14 text-center shadow-strong sm:px-12 sm:py-20">
        <div className="pointer-events-none absolute inset-x-0 top-0 mx-auto h-48 w-96 max-w-full bg-[radial-gradient(ellipse_at_top,var(--color-accent-soft),transparent_70%)] opacity-70" />

        <div className="relative">
          <p className="text-[clamp(5rem,18vw,10rem)] font-bold leading-none tracking-[-0.08em] text-accent" aria-hidden="true">404</p>
          <p className="mt-5 text-xs font-semibold uppercase tracking-[0.22em] text-accent">{t('notFoundEyebrow')}</p>
          <h1 className="mt-3 text-3xl font-bold text-text sm:text-4xl">{t('notFoundTitle')}</h1>
          <p className="mx-auto mt-4 max-w-xl text-sm leading-7 text-muted sm:text-base">{t('notFoundDescription')}</p>
          <code className="mt-5 inline-block max-w-full truncate rounded-md border border-border bg-surface px-3 py-2 text-xs text-subtle">{pathname}</code>

          <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
            <Link to={APP_ROUTES.home} className="interactive-lift rounded-md border border-accent bg-accent px-5 py-2.5 text-sm font-semibold text-bg hover:bg-accent-hover">
              {t('notFoundHome')}
            </Link>
            <Link to={APP_ROUTES.projects} className="interactive-lift rounded-md border border-border-strong bg-surface px-5 py-2.5 text-sm font-semibold text-text hover:border-accent hover:text-accent">
              {t('notFoundProjects')}
            </Link>
          </div>
        </div>
      </div>
    </section>
  )
}
