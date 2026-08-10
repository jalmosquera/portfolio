import axios from 'axios'
import { API_BASE_URL } from '../config/routes'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

const languageOptions = (language) => language ? { headers: { 'Accept-Language': language } } : {}

export const apiFetch = (path, language) =>
  apiClient.get(path, languageOptions(language)).then(({ data }) => data)

export const apiPost = (path, payload, language) =>
  apiClient.post(path, payload, languageOptions(language)).then(({ data }) => data)

export const apiDownload = (path, language) => apiClient.get(path, {
  ...languageOptions(language),
  responseType: 'blob',
})
