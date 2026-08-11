import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'

import { trackEvent } from '../../lib/analytics/tracker'

export function AnalyticsTracker() {
  const { pathname } = useLocation()

  useEffect(() => {
    trackEvent('page_view', { path: pathname })
  }, [pathname])

  return null
}
