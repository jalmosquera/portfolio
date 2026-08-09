import { ProjectCard } from '../projects/ProjectCard'
import { Link } from 'react-router-dom'
import { APP_ROUTES } from '../../lib/config/routes'

export function FeaturedProjects({ projects = [] }) {
  return (
    <section className="relative border-b border-border py-16 lg:py-20">
      <div className="relative mx-auto max-w-6xl px-5 sm:px-8">
        <div className="flex items-center justify-between mb-10">
          <div>
            <h2 className="mb-1 text-3xl font-bold text-text">Featured Projects</h2>
            <p className="text-muted text-sm">Some of the real-world applications I've built and deployed.</p>
          </div>
          <Link
            to={APP_ROUTES.projects}
            className="hidden md:inline-flex items-center gap-2 px-4 py-2 border border-border text-text text-sm font-medium rounded-lg hover:border-accent hover:text-accent transition-all"
          >
            View All
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </div>

        {projects.length > 0 ? (
          <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
            {projects.map((project) => <ProjectCard key={project.id} project={project} />)}
          </div>
        ) : (
          <div className="rounded-lg border border-dashed border-border bg-card/50 px-6 py-12 text-center text-sm text-muted">
            Featured projects will appear here once they are published.
          </div>
        )}

        <div className="mt-10 flex justify-center">
          <Link
            to={APP_ROUTES.projects}
            className="inline-flex items-center gap-2 px-6 py-2.5 border border-accent text-accent text-sm font-medium rounded-md hover:bg-accent hover:text-white transition-all"
          >
            View All Projects
          </Link>
        </div>
      </div>
    </section>
  )
}
