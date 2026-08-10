import { apiDownload } from './client'
import { API_ROUTES } from '../config/routes'

function responseFilename(headers) {
  const disposition = headers['content-disposition'] ?? ''
  const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i)
  const basicMatch = disposition.match(/filename="?([^";]+)"?/i)
  const encodedFilename = utf8Match?.[1] ?? basicMatch?.[1]
  return encodedFilename ? decodeURIComponent(encodedFilename) : 'Jalberth_Mosquera_CV.pdf'
}

export async function downloadResume(language) {
  const response = await apiDownload(API_ROUTES.resume.download, language)
  const objectUrl = URL.createObjectURL(response.data)
  const link = document.createElement('a')
  link.href = objectUrl
  link.download = responseFilename(response.headers)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.setTimeout(() => URL.revokeObjectURL(objectUrl), 1000)
  return link.download
}
