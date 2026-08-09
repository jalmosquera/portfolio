import axios from 'axios'
import { API_BASE_URL } from '../config/routes'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

export const apiFetch = (path) =>
  apiClient.get(path).then(({ data }) => data)
