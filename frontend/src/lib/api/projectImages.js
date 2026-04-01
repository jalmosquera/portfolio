import { apiFetch } from './client'

export const getProjectImages = (projectId) =>
  apiFetch(`/project-images/?project=${projectId}`)
