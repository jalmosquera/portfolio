import { apiFetch } from './client'
import { API_ROUTES } from '../config/routes'

export const getProblemSolution = (projectId, language) =>
  apiFetch(API_ROUTES.problemSolutions.byProject(projectId), language).then((list) => list[0] ?? null)
