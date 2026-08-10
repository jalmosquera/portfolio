import { Link } from 'react-router-dom'
import { APP_ROUTES, getMediaUrl } from '../../lib/config/routes'
import { useLanguage } from '../../context/useLanguage'

export function ProjectCard({ project }) {
  const { t } = useLanguage()
  return (
    <article className="group flex flex-col overflow-hidden rounded-lg border border-border bg-card shadow-[var(--shadow-soft)] transition-colors hover:border-accent/50">
      {/* Image */}
      <div className="relative h-48 overflow-hidden bg-surface">
        {project.image ? (
          <Link
            to={APP_ROUTES.project(project.slug)}
            className="block h-full w-full"
          >
            <img
              src={getMediaUrl(project.image)}
              alt={project.title}
              loading="lazy"
              decoding="async"
              fetchPriority="low"
              sizes="(min-width: 2200px) 20vw, (min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
              className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
            />
          </Link>
        ) : (
          <div className="flex h-full w-full items-center justify-center bg-surface">
            <svg className="h-12 w-12 text-subtle" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        )}
        {/* Tech tags overlaid on image */}
        {project.technologies?.length > 0 && (
          <div className="absolute top-3 left-3 flex flex-wrap gap-1.5">
            {project.technologies.slice(0, 3).map((tech) => (
              <span
                key={tech.id}
                className="inline-flex items-center gap-1 rounded border border-border bg-bg/80 px-2 py-0.5 text-[11px] font-medium text-text backdrop-blur-sm"
                style={{ color: tech.color || '#9ca3af' }}
              >
                <span className="text-[10px]">{tech.icon}</span>
                {tech.name}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Content */}
      <div className="flex flex-1 flex-col gap-4 p-4">
        {/* Title & description */}
        <div className="flex-1 space-y-1">
          <h3 className="text-lg font-semibold leading-tight text-text">{project.title}</h3>
          <p className="text-muted text-sm leading-relaxed line-clamp-2">{project.short_description}</p>
        </div>

        {/* CTA */}
        <Link
          to={APP_ROUTES.project(project.slug)}
          className="group/btn inline-flex items-center gap-2 rounded-md border border-border bg-surface px-4 py-2 text-sm text-text transition-colors hover:border-accent hover:text-accent"
        >
          <svg className="w-4 h-4 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z" />
          </svg>
          {t('caseStudy')}
          <svg className="ml-auto h-3.5 w-3.5 text-subtle transition-colors group-hover/btn:text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </article>
  )
}
