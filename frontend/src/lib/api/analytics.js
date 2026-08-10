import { apiPost } from './client'
import { API_ROUTES } from '../config/routes'

export const recordVisit = () => apiPost(API_ROUTES.analytics.visit)
