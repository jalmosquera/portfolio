import { apiFetch } from './client'

export const getProblemSolution = (projectId) =>
  apiFetch(`/problem-solutions/?project=${projectId}`).then((list) => list[0] ?? null)
