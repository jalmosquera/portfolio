import { ProjectCard } from '../projects/ProjectCard'
import { Link } from 'react-router-dom'
import { APP_ROUTES } from '../../lib/config/routes'
import { useLanguage } from '../../context/useLanguage'
import { Reveal } from '../ui/Reveal'

export function FeaturedProjects({ projects = [] }) {
  const { t } = useLanguage()
  return (
    <section className="relative border-b border-border py-16 lg:py-20">
      <div className="site-container relative">
        <Reveal className="mb-10 flex items-start justify-between gap-6 sm:items-center">
          <div>
            <h2 className="mb-1 text-3xl font-bold text-text">{t('featuredTitle')}</h2>
            <p className="text-muted text-sm">{t('featuredSubtitle')}</p>
          </div>
          <Link
            to={APP_ROUTES.projects}
            className="hidden md:inline-flex items-center gap-2 px-4 py-2 border border-border text-text text-sm font-medium rounded-lg hover:border-accent hover:text-accent transition-all"
          >
            {t('viewAll')}
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </Reveal>

        {projects.length > 0 ? (
          <div className="mx-auto grid max-w-[90rem] grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3 2xl:gap-7">
            {projects.map((project, index) => <Reveal key={project.id} delay={Math.min(index * 90, 360)} distance="lg"><ProjectCard project={project} /></Reveal>)}
          </div>
        ) : (
          <div className="rounded-lg border border-dashed border-border bg-card/50 px-6 py-12 text-center text-sm text-muted">
            {t('featuredEmpty')}
          </div>
        )}

        <Reveal className="mt-10 flex justify-center" delay={160} distance="sm">
          <Link
            to={APP_ROUTES.projects}
            className="inline-flex cursor-pointer items-center gap-2 rounded-md border border-accent px-6 py-2.5 text-sm font-medium text-accent transition-all hover:bg-accent hover:text-white"
          >
            {t('viewAllProjects')}
          </Link>
        </Reveal>
      </div>
    </section>
  )
}
