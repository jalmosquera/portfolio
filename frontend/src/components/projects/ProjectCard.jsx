import { Link } from 'react-router-dom'
import { TechBadge } from './TechBadge'

export function ProjectCard({ project }) {
  return (
    <div className="bg-card border border-border rounded-xl overflow-hidden hover:border-accent/40 transition-all duration-300 group flex flex-col">
      <div className="h-48 bg-surface overflow-hidden">
        {project.image ? (
          <img
            src={`http://localhost:8000${project.image}`}
            alt={project.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-muted text-4xl">
            🖥️
          </div>
        )}
      </div>

      <div className="p-5 flex flex-col flex-1 gap-3">
        <div className="flex flex-wrap gap-1.5">
          {project.technologies?.slice(0, 3).map((tech) => (
            <TechBadge key={tech.id} tech={tech} />
          ))}
        </div>

        <div className="flex-1">
          <h3 className="font-bold text-text text-lg leading-tight mb-1">{project.title}</h3>
          <p className="text-muted text-sm line-clamp-2">{project.short_description}</p>
        </div>

        <Link
          to={`/projects/${project.slug}`}
          className="inline-flex items-center gap-1 text-accent text-sm font-medium hover:gap-2 transition-all"
        >
          Case Study
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </div>
  )
}
