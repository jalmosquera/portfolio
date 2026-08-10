import { apiFetch } from './client'
import { API_ROUTES } from '../config/routes'

export const getProjectImages = (projectId, language) => apiFetch(API_ROUTES.projectImages.byProject(projectId), language)
