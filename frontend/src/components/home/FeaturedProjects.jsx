import { ProjectCard } from '../projects/ProjectCard'
import { Link } from 'react-router-dom'

export function FeaturedProjects({ projects = [] }) {
  return (
    <section className="py-16 lg:py-20 relative">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#0b0b0b] to-transparent pointer-events-none" />
      <div className="max-w-6xl mx-auto px-6 relative">
        <div className="flex items-center justify-between mb-10">
          <div>
            <h2 className="text-3xl font-bold text-white mb-1">Featured Projects</h2>
            <p className="text-muted text-sm">Some of the real-world applications I've built and deployed.</p>
          </div>
          <Link
            to="/projects"
            className="hidden md:inline-flex items-center gap-2 px-4 py-2 border border-border text-text text-sm font-medium rounded-lg hover:border-accent hover:text-accent transition-all"
          >
            View All
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>

        <div className="mt-10 flex justify-center">
          <Link
            to="/projects"
            className="inline-flex items-center gap-2 px-6 py-2.5 border border-accent text-accent text-sm font-medium rounded-md hover:bg-accent hover:text-white transition-all"
          >
            View All Projects
          </Link>
        </div>
      </div>
    </section>
  )
}
