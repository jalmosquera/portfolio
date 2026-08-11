import { apiFetch, apiPost } from './client'
import { API_ROUTES } from '../config/routes'

export const recordVisit = () => apiPost(API_ROUTES.analytics.visit)

export const createAnalyticsSession = (payload) => apiPost(API_ROUTES.analytics.sessions, payload)

export const createAnalyticsEvent = (payload) => apiPost(API_ROUTES.analytics.events, payload)

export const getAnalyticsSummary = () => apiFetch(API_ROUTES.analytics.summary)
