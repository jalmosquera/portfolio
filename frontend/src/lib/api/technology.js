import { apiFetch } from './client'

export const getTechnologies = () => apiFetch('/technologies/')
