import { useEffect, useState } from 'react'
import { SectionTitle } from '../components/ui/SectionTitle'
import { ProjectCard } from '../components/projects/ProjectCard'
import { getProjects } from '../lib/api/projects'

export function ProjectsPage() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getProjects()
      .then(setProjects)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center pt-16">
        <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <main className="pt-24 pb-16">
      <div className="max-w-6xl mx-auto px-6">
        <SectionTitle subtitle="All the projects I've built and deployed.">
          All Projects
        </SectionTitle>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      </div>
    </main>
  )
}
