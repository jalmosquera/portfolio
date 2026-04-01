import { SectionTitle } from '../ui/SectionTitle'
import { ProjectCard } from '../projects/ProjectCard'
import { Link } from 'react-router-dom'

export function FeaturedProjects({ projects = [] }) {
  return (
    <section className="py-20">
      <div className="max-w-6xl mx-auto px-6">
        <SectionTitle subtitle="Some of the real-world applications I've built and deployed.">
          Featured Projects
        </SectionTitle>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>

        <div className="mt-10 flex justify-center">
          <Link
            to="/projects"
            className="inline-flex items-center gap-2 px-6 py-3 border border-border text-muted rounded-lg hover:border-accent hover:text-accent transition-all text-sm font-medium"
          >
            View All Projects
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </div>
      </div>
    </section>
  )
}
