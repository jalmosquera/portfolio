import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { TechBadge } from '../components/projects/TechBadge'
import { getProjectBySlug } from '../lib/api/projects'
import { getProjectImages } from '../lib/api/projectImages'
import { getTechDetails } from '../lib/api/techDetails'
import { getLessons } from '../lib/api/lessons'
import { getProblemSolution } from '../lib/api/problemSolution'

export function ProjectDetailPage() {
  const { slug } = useParams()
  const [project, setProject] = useState(null)
  const [images, setImages] = useState([])
  const [techDetails, setTechDetails] = useState([])
  const [lessons, setLessons] = useState([])
  const [problemSolution, setProblemSolution] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getProjectBySlug(slug)
      .then((proj) => {
        if (!proj) { setError('Project not found'); return }
        setProject(proj)
        return Promise.all([
          getProjectImages(proj.id),
          getTechDetails(proj.id),
          getLessons(proj.id),
          getProblemSolution(proj.id),
        ])
      })
      .then((results) => {
        if (!results) return
        const [imgs, details, lsns, ps] = results
        setImages(imgs)
        setTechDetails(details)
        setLessons(lsns)
        setProblemSolution(ps)
      })
      .catch(() => setError('Failed to load project'))
      .finally(() => setLoading(false))
  }, [slug])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center pt-16">
        <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (error || !project) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center pt-16 gap-4">
        <p className="text-muted">{error || 'Project not found'}</p>
        <Link to="/projects" className="text-accent hover:underline text-sm">← Back to Projects</Link>
      </div>
    )
  }

  const techByCategory = techDetails.reduce((acc, td) => {
    if (!acc[td.category]) acc[td.category] = []
    acc[td.category].push(td.text)
    return acc
  }, {})

  return (
    <main className="pt-24 pb-16">
      <div className="max-w-5xl mx-auto px-6 space-y-16">

        {/* Header */}
        <div className="space-y-4">
          <Link to="/projects" className="inline-flex items-center gap-1 text-muted hover:text-accent text-sm transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </Link>

          <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold text-text">{project.title}</h1>
              <p className="text-muted">{project.short_description}</p>
            </div>
            <div className="flex gap-3 shrink-0">
              {project.live_url && (
                <a
                  href={project.live_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-accent text-white text-sm font-medium rounded-lg hover:bg-accent-hover transition-colors"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  Live Demo
                </a>
              )}
              {project.github && (
                <a
                  href={project.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 border border-border text-text text-sm font-medium rounded-lg hover:border-accent hover:text-accent transition-all"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
                  </svg>
                  GitHub Repo
                </a>
              )}
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            {project.technologies?.map((tech) => (
              <TechBadge key={tech.id} tech={tech} />
            ))}
          </div>
        </div>

        {/* Hero image */}
        {project.image && (
          <div className="rounded-xl overflow-hidden border border-border">
            <img
              src={`http://localhost:8000${project.image}`}
              alt={project.title}
              className="w-full max-h-96 object-cover"
            />
          </div>
        )}

        {/* Problem & Solution */}
        {problemSolution && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-card border border-border rounded-xl p-6 space-y-3">
              <div className="flex items-center gap-2">
                <span className="w-1 h-5 bg-red-500 rounded-full" />
                <h2 className="font-bold text-text">The Problem</h2>
              </div>
              <p className="text-muted text-sm leading-relaxed">{problemSolution.problem}</p>
            </div>
            <div className="bg-card border border-border rounded-xl p-6 space-y-3">
              <div className="flex items-center gap-2">
                <span className="w-1 h-5 bg-green-500 rounded-full" />
                <h2 className="font-bold text-text">The Solution</h2>
              </div>
              <p className="text-muted text-sm leading-relaxed">{problemSolution.solution}</p>
            </div>
          </div>
        )}

        {/* Gallery */}
        {images.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <span className="w-1 h-5 bg-accent rounded-full" />
              <h2 className="font-bold text-text text-lg">Gallery</h2>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {images.map((img) => (
                <div key={img.id} className="rounded-xl overflow-hidden border border-border bg-card">
                  {img.image ? (
                    <img
                      src={`http://localhost:8000${img.image}`}
                      alt={img.title}
                      className="w-full h-40 object-cover"
                    />
                  ) : (
                    <div className="w-full h-40 flex items-center justify-center text-muted text-3xl bg-surface">🖥️</div>
                  )}
                  <p className="text-xs text-muted px-3 py-2">{img.title}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tech Details + Lessons */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Object.keys(techByCategory).length > 0 && (
            <div className="bg-card border border-border rounded-xl p-6 space-y-4">
              <div className="flex items-center gap-2">
                <span className="w-1 h-5 bg-accent rounded-full" />
                <h2 className="font-bold text-text">Tech Details</h2>
              </div>
              <div className="space-y-3">
                {Object.entries(techByCategory).map(([category, items]) => (
                  <div key={category}>
                    <p className="text-xs font-semibold text-accent mb-1">{category}</p>
                    <div className="flex flex-wrap gap-1.5">
                      {items.map((item, i) => (
                        <span key={i} className="text-xs bg-surface border border-border px-2 py-0.5 rounded text-text">
                          {item}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {lessons.length > 0 && (
            <div className="bg-card border border-border rounded-xl p-6 space-y-4">
              <div className="flex items-center gap-2">
                <span className="w-1 h-5 bg-accent rounded-full" />
                <h2 className="font-bold text-text">Lessons Learned</h2>
              </div>
              <ul className="space-y-2">
                {lessons.map((lesson) => (
                  <li key={lesson.id} className="flex items-start gap-2 text-sm text-muted">
                    <span className="text-accent mt-0.5">›</span>
                    <span>{lesson.text}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

      </div>
    </main>
  )
}
