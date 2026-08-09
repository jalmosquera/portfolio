import { apiFetch } from './client'
import { API_ROUTES } from '../config/routes'

export const getTechnologies = () => apiFetch(API_ROUTES.technologies.list)
