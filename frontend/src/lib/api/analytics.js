import { apiFetch, apiPost } from './client'
import { API_ROUTES } from '../config/routes'

export const recordVisit = () => apiPost(API_ROUTES.analytics.visit)

export const getAnalyticsSummary = () => apiFetch(API_ROUTES.analytics.summary)
