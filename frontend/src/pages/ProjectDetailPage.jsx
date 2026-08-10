import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { TechBadge } from '../components/projects/TechBadge'
import { getProjectBySlug } from '../lib/api/projects'
import { getProjectImages } from '../lib/api/projectImages'
import { getTechDetails } from '../lib/api/techDetails'
import { getLessons } from '../lib/api/lessons'
import { getProblemSolution } from '../lib/api/problemSolution'
import { APP_ROUTES, getMediaUrl } from '../lib/config/routes'
import { PageLoader } from '../components/ui/PageLoader'
import { useLanguage } from '../context/useLanguage'

export function ProjectDetailPage() {
  const { language, t } = useLanguage()
  const { slug } = useParams()
  const [project, setProject] = useState(null)
  const [images, setImages] = useState([])
  const [techDetails, setTechDetails] = useState([])
  const [lessons, setLessons] = useState([])
  const [problemSolution, setProblemSolution] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getProjectBySlug(slug, language)
      .then((proj) => {
        if (!proj) { setError(t('projectNotFound')); return }
        setProject(proj)
        setError(null)
        return Promise.all([
          getProjectImages(proj.id, language),
          getTechDetails(proj.id, language),
          getLessons(proj.id, language),
          getProblemSolution(proj.id, language),
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
      .catch(() => setError(t('projectLoadError')))
      .finally(() => setLoading(false))
  }, [slug, language, t])

  if (loading) {
    return <PageLoader />
  }

  if (error || !project) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center pt-16 gap-4">
        <p className="text-muted">{error || t('projectNotFound')}</p>
        <Link to={APP_ROUTES.projects} className="text-accent hover:underline text-sm">← {t('backProjects')}</Link>
      </div>
    )
  }

  const techByCategory = techDetails.reduce((acc, td) => {
    if (!acc[td.category]) acc[td.category] = []
    acc[td.category].push(td.text)
    return acc
  }, {})

  return (
    <main className="pb-20 pt-28">
      <div className="site-container space-y-12">

        {/* Header */}
        <div className="space-y-5 border-b border-border pb-8">
          <Link to={APP_ROUTES.projects} className="inline-flex items-center gap-1 text-muted hover:text-accent text-sm transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            {t('back')}
          </Link>

          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between min-[2200px]:gap-12">
            <div className="space-y-2">
              <div className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-3 py-1 text-[11px] uppercase tracking-[0.15em] text-muted">
                {project.category || t('caseStudy')}
              </div>
              <h1 className="text-3xl font-bold text-text sm:text-4xl 2xl:text-5xl">{project.title}</h1>
              <p className="max-w-3xl text-muted 2xl:text-lg">{project.short_description}</p>
              <div className="flex flex-wrap gap-2">
                {project.technologies?.map((tech) => (
                  <TechBadge key={tech.id} tech={tech} />
                ))}
              </div>
            </div>
            <div className="flex shrink-0 flex-wrap gap-3">
              {project.live_url && (
                <a
                  href={project.live_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 rounded-md border border-accent/60 bg-accent-soft px-4 py-2 text-sm font-medium text-accent transition-colors hover:bg-accent hover:text-bg"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  {t('liveDemo')}
                </a>
              )}
              {project.github && (
                <a
                  href={project.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-4 py-2 text-sm font-medium text-text transition-colors hover:border-accent hover:text-accent"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
                  </svg>
                  {t('githubRepo')}
                </a>
              )}
            </div>
          </div>
        </div>

        {/* Hero image */}
        {project.image && (
          <div className="overflow-hidden rounded-lg border border-border shadow-[var(--shadow-soft)]">
            <img
              src={getMediaUrl(project.image)}
              alt={project.title}
              className="block h-auto w-full"
            />
          </div>
        )}

        {/* Problem & Solution */}
        {problemSolution && (
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 2xl:gap-8">
            <div className="space-y-3 rounded-lg border border-border bg-card p-6 shadow-[var(--shadow-soft)]">
              <div className="flex items-center gap-2">
                <span className="w-1 h-5 bg-accent rounded-full" />
                <h2 className="font-bold text-text">{t('problem')}</h2>
              </div>
              <p className="text-muted text-sm leading-relaxed">{problemSolution.problem}</p>
            </div>
            <div className="space-y-3 rounded-lg border border-border bg-card p-6 shadow-[var(--shadow-soft)]">
              <div className="flex items-center gap-2">
                <span className="h-5 w-1 rounded-full bg-accent" />
                <h2 className="font-bold text-text">{t('solution')}</h2>
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
              <h2 className="font-bold text-text text-lg">{t('gallery')}</h2>
            </div>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 min-[2200px]:grid-cols-5">
              {images.map((img) => (
                <div key={img.id} className="overflow-hidden rounded-lg border border-border bg-card shadow-[var(--shadow-soft)]">
                  {img.image ? (
                    <img
                      src={getMediaUrl(img.image)}
                      alt={img.title}
                      className="block h-auto w-full"
                    />
                  ) : (
                    <div className="w-full h-44 flex items-center justify-center text-muted text-3xl bg-surface">🖥️</div>
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
            <div className="space-y-4 rounded-lg border border-border bg-card p-6">
              <div className="flex items-center gap-2">
                <span className="w-1 h-5 bg-accent rounded-full" />
                <h2 className="font-bold text-text">{t('techDetails')}</h2>
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
            <div className="space-y-4 rounded-lg border border-border bg-card p-6">
              <div className="flex items-center gap-2">
                <span className="w-1 h-5 bg-accent rounded-full" />
                <h2 className="font-bold text-text">{t('lessons')}</h2>
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
