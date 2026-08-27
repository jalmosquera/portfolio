const LOCAL_API_URL = 'http://127.0.0.1:8000/api'
const PRODUCTION_API_URL = 'https://adminportfolio.mosquerasoft.com/api'
const configuredApiUrl = import.meta.env.VITE_API_URL
const isLoopbackUrl = (url) => /^https?:\/\/(?:127\.0\.0\.1|localhost)(?::\d+)?(?:\/|$)/.test(url || '')

// A loopback address in a production bundle points to each visitor's device.
export const API_BASE_URL = import.meta.env.DEV
  ? configuredApiUrl || LOCAL_API_URL
  : isLoopbackUrl(configuredApiUrl)
    ? PRODUCTION_API_URL
    : configuredApiUrl || PRODUCTION_API_URL

const BACKEND_BASE_URL = API_BASE_URL.replace(/\/api\/?$/, '')

const withProjectQuery = (path, projectId) =>
  `${path}?${new URLSearchParams({ project: projectId })}`

export const API_ROUTES = {
  analytics: {
    visit: '/visits/',
    sessions: '/analytics/sessions/',
    events: '/analytics/events/',
    summary: '/analytics/summary/',
  },
  about: {
    detail: '/about/',
  },
  contact: {
    create: '/contact/',
  },
  resume: {
    detail: '/cv/',
    download: '/cv/download/',
  },
  projects: {
    list: '/projects/',
    featured: '/projects/?is_featured=true',
    bySlug: (slug) => `/projects/?${new URLSearchParams({ slug })}`,
  },
  technologies: {
    list: '/technologies/',
  },
  projectImages: {
    byProject: (projectId) => withProjectQuery('/project-images/', projectId),
  },
  techDetails: {
    byProject: (projectId) => withProjectQuery('/tech-details/', projectId),
  },
  lessons: {
    byProject: (projectId) => withProjectQuery('/lessons/', projectId),
  },
  problemSolutions: {
    byProject: (projectId) => withProjectQuery('/problem-solutions/', projectId),
  },
}

export const APP_ROUTES = {
  home: '/',
  projects: '/projects',
  projectDetail: '/projects/:slug',
  project: (slug) => `/projects/${slug}`,
  analytics: '/analytics',
}

export function getBackendUrl(path) {
  return `${BACKEND_BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`
}

export const SOCIAL_LINKS = {
  github: 'https://github.com/jalmosquera',
  linkedin: 'https://www.linkedin.com/in/jalberth-mosquera-077975387/',
}

export function getMediaUrl(path) {
  if (!path || /^(?:https?:|data:)/.test(path)) return path

  return `${BACKEND_BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`
}
