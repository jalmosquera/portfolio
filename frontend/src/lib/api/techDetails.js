import { apiFetch } from './client'

export const getTechDetails = (projectId) =>
  apiFetch(`/tech-details/?project=${projectId}`)
