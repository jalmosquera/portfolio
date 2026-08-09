import { apiFetch } from './client'
import { API_ROUTES } from '../config/routes'

export const getProjects = () => apiFetch(API_ROUTES.projects.list)

export const getFeaturedProjects = () => apiFetch(API_ROUTES.projects.featured)

export const getProjectBySlug = (slug) =>
  apiFetch(API_ROUTES.projects.bySlug(slug)).then((list) => list[0] ?? null)
