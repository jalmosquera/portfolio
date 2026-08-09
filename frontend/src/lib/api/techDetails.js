import { apiFetch } from './client'
import { API_ROUTES } from '../config/routes'

export const getTechDetails = (projectId) =>
  apiFetch(API_ROUTES.techDetails.byProject(projectId))
