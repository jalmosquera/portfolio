import { useEffect, useState } from 'react'
import { SectionTitle } from '../components/ui/SectionTitle'
import { ProjectCard } from '../components/projects/ProjectCard'
import { getProjects } from '../lib/api/projects'
import { PageLoader } from '../components/ui/PageLoader'
import { useLanguage } from '../context/useLanguage'
import { Reveal } from '../components/ui/Reveal'

export function ProjectsPage() {
  const { language, t } = useLanguage()
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getProjects(language)
      .then((data) => { setProjects(data); setError(null) })
      .catch(() => setError(t('projectsError')))
      .finally(() => setLoading(false))
  }, [language, t])

  if (loading) {
    return <PageLoader />
  }

  return (
    <main className="pb-20 pt-28">
      <div className="site-container">
        <Reveal><SectionTitle subtitle={t('allProjectsSubtitle')}>{t('allProjects')}</SectionTitle></Reveal>
        {error && <div className="rounded-lg border border-accent/30 bg-accent-soft p-6 text-sm text-accent">{error}</div>}
        {!error && projects.length === 0 && (
          <div className="rounded-lg border border-dashed border-border bg-card/50 px-6 py-16 text-center text-sm text-muted">
            {t('projectsEmpty')}
          </div>
        )}
        {!error && projects.length > 0 && (
          <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 2xl:gap-7 min-[2200px]:grid-cols-5 min-[3200px]:grid-cols-6">
            {projects.map((project, index) => <Reveal key={project.id} delay={Math.min(index * 70, 350)} distance="lg"><ProjectCard project={project} /></Reveal>)}
          </div>
        )}
      </div>
    </main>
  )
}
