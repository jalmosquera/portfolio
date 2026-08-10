export const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const BACKEND_BASE_URL = API_BASE_URL.replace(/\/api\/?$/, '')

const withProjectQuery = (path, projectId) =>
  `${path}?${new URLSearchParams({ project: projectId })}`

export const API_ROUTES = {
  analytics: {
    visit: '/visits/',
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
}

export const SOCIAL_LINKS = {
  github: 'https://github.com/jalmosquera',
  linkedin: 'https://www.linkedin.com/in/jalberth-mosquera-077975387/',
}

export function getMediaUrl(path) {
  if (!path || /^(?:https?:|data:)/.test(path)) return path

  return `${BACKEND_BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`
}
