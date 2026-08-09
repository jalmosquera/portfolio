import { apiFetch } from './client'
import { API_ROUTES } from '../config/routes'

export const getLessons = (projectId) =>
  apiFetch(API_ROUTES.lessons.byProject(projectId))
