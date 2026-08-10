import { apiFetch } from './client'
import { API_ROUTES } from '../config/routes'

export const getProjects = (language) => apiFetch(API_ROUTES.projects.list, language)

export const getFeaturedProjects = (language) => apiFetch(API_ROUTES.projects.featured, language)

export const getProjectBySlug = (slug, language) =>
  apiFetch(API_ROUTES.projects.bySlug(slug), language).then((list) => list[0] ?? null)
