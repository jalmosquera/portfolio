import { useEffect, useState } from 'react'
import { Hero } from '../components/home/Hero'
import { FeaturedProjects } from '../components/home/FeaturedProjects'
import { TechStack } from '../components/home/TechStack'
import { Contact } from '../components/home/Contact'
import { getFeaturedProjects } from '../lib/api/projects'
import { getTechnologies } from '../lib/api/technology'

export function HomePage() {
  const [projects, setProjects] = useState([])
  const [technologies, setTechnologies] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getFeaturedProjects(), getTechnologies()])
      .then(([p, t]) => {
        setProjects(p)
        setTechnologies(t)
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <>
      <Hero technologies={technologies} />
      <FeaturedProjects projects={projects} />
      <TechStack technologies={technologies} />
      <Contact />
    </>
  )
}
