import { createAnalyticsEvent, createAnalyticsSession } from '../api/analytics'
import { APP_ROUTES } from '../config/routes'

const VISITOR_KEY = 'portfolio_analytics_visitor'
const SESSION_KEY = 'portfolio_analytics_session'
const recentEvents = new Map()
let sessionPromise
let lastActivity = Date.now()
const SESSION_TIMEOUT_MS = 30 * 60 * 1000
let memoryVisitorId
let memorySessionId

function readStorage(storageName, key) {
  try { return window[storageName].getItem(key) } catch { return null }
}

function writeStorage(storageName, key, value) {
  try { window[storageName].setItem(key, value) } catch { /* Privacy settings may disable storage. */ }
}

function randomId() {
  if (crypto.randomUUID) return crypto.randomUUID()
  const bytes = crypto.getRandomValues(new Uint8Array(16))
  bytes[6] = (bytes[6] & 0x0f) | 0x40
  bytes[8] = (bytes[8] & 0x3f) | 0x80
  const hex = [...bytes].map((value) => value.toString(16).padStart(2, '0')).join('')
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`
}

function getVisitorId() {
  let visitorId = readStorage('localStorage', VISITOR_KEY) || memoryVisitorId
  if (!visitorId) {
    visitorId = randomId()
    memoryVisitorId = visitorId
    writeStorage('localStorage', VISITOR_KEY, visitorId)
  }
  return visitorId
}

function deviceType() {
  const agent = navigator.userAgent
  if (/tablet|ipad/i.test(agent)) return 'tablet'
  if (/mobile|iphone|android/i.test(agent)) return 'mobile'
  return 'desktop'
}

function browser() {
  const agent = navigator.userAgent
  if (/edg/i.test(agent)) return 'Edge'
  if (/firefox/i.test(agent)) return 'Firefox'
  if (/chrome|crios/i.test(agent)) return 'Chrome'
  if (/safari/i.test(agent)) return 'Safari'
  return 'Other'
}

function operatingSystem() {
  const agent = navigator.userAgent
  if (/windows/i.test(agent)) return 'Windows'
  if (/android/i.test(agent)) return 'Android'
  if (/iphone|ipad|ipod/i.test(agent)) return 'iOS'
  if (/mac os/i.test(agent)) return 'macOS'
  if (/linux/i.test(agent)) return 'Linux'
  return 'Other'
}

function sessionPayload() {
  const params = new URLSearchParams(window.location.search)
  return {
    visitor_id: getVisitorId(),
    session_id: readStorage('sessionStorage', SESSION_KEY) || memorySessionId || undefined,
    landing_path: `${window.location.pathname}${window.location.search}`,
    referrer: document.referrer,
    utm_source: params.get('utm_source') || '',
    utm_medium: params.get('utm_medium') || '',
    utm_campaign: params.get('utm_campaign') || '',
    device_type: deviceType(),
    browser: browser(),
    operating_system: operatingSystem(),
    language: navigator.language || '',
  }
}

async function ensureSession() {
  if (!sessionPromise) {
    sessionPromise = createAnalyticsSession(sessionPayload())
      .then((response) => {
        memorySessionId = response.session_id
        writeStorage('sessionStorage', SESSION_KEY, response.session_id)
        return response.session_id
      })
      .catch((error) => {
        sessionPromise = undefined
        throw error
      })
  }
  return sessionPromise
}

export async function trackEvent(eventType, { path = window.location.pathname, target = '' } = {}) {
  if (window.location.pathname === APP_ROUTES.analytics) return
  const key = `${eventType}:${path}:${target}`
  const now = Date.now()
  if (now - lastActivity > SESSION_TIMEOUT_MS) sessionPromise = undefined
  lastActivity = now
  if (now - (recentEvents.get(key) || 0) < 1500) return
  recentEvents.set(key, now)

  try {
    const sessionId = await ensureSession()
    await createAnalyticsEvent({ session_id: sessionId, event_type: eventType, path, target })
  } catch {
    recentEvents.delete(key)
  }
}
