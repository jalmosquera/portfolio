import { useEffect, useState } from 'react'
import { SectionTitle } from '../components/ui/SectionTitle'
import { ProjectCard } from '../components/projects/ProjectCard'
import { getProjects } from '../lib/api/projects'
import { PageLoader } from '../components/ui/PageLoader'

export function ProjectsPage() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getProjects()
      .then(setProjects)
      .catch(() => setError('Projects could not be loaded. Please try again later.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <PageLoader />
  }

  return (
    <main className="pb-20 pt-28">
      <div className="site-container">
        <SectionTitle subtitle="All the projects I've built and deployed.">
          All Projects
        </SectionTitle>
        {error && <div className="rounded-lg border border-accent/30 bg-accent-soft p-6 text-sm text-accent">{error}</div>}
        {!error && projects.length === 0 && (
          <div className="rounded-lg border border-dashed border-border bg-card/50 px-6 py-16 text-center text-sm text-muted">
            New case studies are being prepared.
          </div>
        )}
        {!error && projects.length > 0 && (
          <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 2xl:gap-7 min-[2200px]:grid-cols-5 min-[3200px]:grid-cols-6">
            {projects.map((project) => <ProjectCard key={project.id} project={project} />)}
          </div>
        )}
      </div>
    </main>
  )
}
