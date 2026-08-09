import { Link } from 'react-router-dom'
import { APP_ROUTES, getMediaUrl } from '../../lib/config/routes'

export function ProjectCard({ project }) {
  return (
    <div className="bg-card border border-border rounded-2xl overflow-hidden hover:border-accent/60 transition-all duration-300 group flex flex-col shadow-[var(--shadow-soft)]">
      {/* Image */}
      <div className="h-48 bg-[#111] overflow-hidden relative">
        {project.image ? (
          <img
            src={getMediaUrl(project.image)}
            alt={project.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-[#0f0f0f]">
            <svg className="w-12 h-12 text-[#2a2a2a]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
                className="inline-flex items-center gap-1 px-2 py-0.5 bg-[#0d0d0d]/80 border border-[#2a2a2a] rounded text-[11px] font-medium backdrop-blur-sm shadow-sm"
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
      <div className="p-5 flex flex-col flex-1 gap-4">
        {/* Title & description */}
        <div className="flex-1 space-y-1">
          <h3 className="font-bold text-white text-lg leading-tight">{project.title}</h3>
          <p className="text-muted text-sm leading-relaxed line-clamp-2">{project.short_description}</p>
        </div>

        {/* CTA */}
        <Link
          to={APP_ROUTES.project(project.slug)}
          className="inline-flex items-center gap-2 px-4 py-2 bg-[#1b1b1b] border border-border rounded-lg text-sm text-text hover:border-accent hover:text-accent transition-all group/btn"
        >
          <svg className="w-4 h-4 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z" />
          </svg>
          Case Study
          <svg className="w-3.5 h-3.5 ml-auto text-[#444] group-hover/btn:text-accent transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </div>
  )
}
