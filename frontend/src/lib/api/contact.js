import { apiPost } from './client'
import { API_ROUTES } from '../config/routes'

export const createContactInquiry = (payload, language) => apiPost(API_ROUTES.contact.create, payload, language)
