import { apiFetch } from './client'
import { API_ROUTES } from '../config/routes'

export const getAbout = () => apiFetch(API_ROUTES.about.detail)
