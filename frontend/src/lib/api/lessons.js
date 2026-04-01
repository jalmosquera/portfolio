import { apiFetch } from './client'

export const getLessons = (projectId) =>
  apiFetch(`/lessons/?project=${projectId}`)
