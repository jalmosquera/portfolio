import { apiFetch } from './client'
import { API_ROUTES } from '../config/routes'

export const getProblemSolution = (projectId) =>
  apiFetch(API_ROUTES.problemSolutions.byProject(projectId)).then((list) => list[0] ?? null)
