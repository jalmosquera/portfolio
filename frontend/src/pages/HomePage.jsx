import { useEffect, useState } from 'react'
import { Hero } from '../components/home/Hero'
import { FeaturedProjects } from '../components/home/FeaturedProjects'
import { TechStack } from '../components/home/TechStack'
import { Contact } from '../components/home/Contact'
import { getFeaturedProjects } from '../lib/api/projects'
import { getTechnologies } from '../lib/api/technology'
import { PageLoader } from '../components/ui/PageLoader'

export function HomePage() {
  const [projects, setProjects] = useState([])
  const [technologies, setTechnologies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    Promise.all([getFeaturedProjects(), getTechnologies()])
      .then(([p, t]) => {
        setProjects(p)
        setTechnologies(t)
      })
      .catch(() => setError('Live portfolio data is temporarily unavailable.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <PageLoader />
  }

  return (
    <>
      <Hero technologies={technologies} />
      {error && (
        <div className="site-container pt-10">
          <p className="rounded-lg border border-accent/30 bg-accent-soft p-4 text-sm text-accent">{error}</p>
        </div>
      )}
      <FeaturedProjects projects={projects} />
      <TechStack technologies={technologies} />
      <Contact />
    </>
  )
}
