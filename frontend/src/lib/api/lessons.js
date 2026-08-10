import { apiFetch } from './client'
import { API_ROUTES } from '../config/routes'

export const getLessons = (projectId, language) => apiFetch(API_ROUTES.lessons.byProject(projectId), language)
