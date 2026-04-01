import { apiFetch } from './client'

export const getProjects = () => apiFetch('/projects/')

export const getFeaturedProjects = () => apiFetch('/projects/?is_featured=true')

export const getProjectBySlug = (slug) =>
  apiFetch(`/projects/?slug=${slug}`).then((list) => list[0] ?? null)
