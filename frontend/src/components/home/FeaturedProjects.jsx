import { ProjectCard } from '../projects/ProjectCard'
import { Link } from 'react-router-dom'

export function FeaturedProjects({ projects = [] }) {
  return (
    <section className="py-20 bg-[#0d0d0d]">
      <div className="max-w-6xl mx-auto px-6">
        <div className="mb-10">
          <h2 className="text-2xl font-bold text-white mb-1">Featured Projects</h2>
          <p className="text-[#6b7280] text-sm">Some of the real-world applications I've built and deployed.</p>
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
