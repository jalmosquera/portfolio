import { useEffect, useState } from 'react'
import { Hero } from '../components/home/Hero'
import { FeaturedProjects } from '../components/home/FeaturedProjects'
import { TechStack } from '../components/home/TechStack'
import { Contact } from '../components/home/Contact'
import { AboutMe } from '../components/home/AboutMe'
import { getFeaturedProjects } from '../lib/api/projects'
import { getTechnologies } from '../lib/api/technology'
import { getAbout } from '../lib/api/about'
import { PageLoader } from '../components/ui/PageLoader'

export function HomePage() {
  const [projects, setProjects] = useState([])
  const [technologies, setTechnologies] = useState([])
  const [about, setAbout] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    Promise.all([getFeaturedProjects(), getTechnologies(), getAbout().catch(() => null)])
      .then(([p, t, aboutData]) => {
        setProjects(p)
        setTechnologies(t)
        setAbout(aboutData)
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
      <AboutMe about={about} />
      <TechStack technologies={technologies} />
      <Contact />
    </>
  )
}
