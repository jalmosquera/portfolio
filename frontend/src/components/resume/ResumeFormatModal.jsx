import { useState } from 'react'
import { sileo } from 'sileo'

import { useLanguage } from '../../context/useLanguage'
import { downloadResume } from '../../lib/api/resume'
import { trackEvent } from '../../lib/analytics/tracker'

const FORMATS = [
  { id: 'concise', titleKey: 'cvConciseTitle', descriptionKey: 'cvConciseDescription', icon: '▤' },
  { id: 'visual', titleKey: 'cvVisualTitle', descriptionKey: 'cvVisualDescription', icon: '◉' },
]

export function ResumeFormatModal({ open, onClose }) {
  const { language, t } = useLanguage()
  const [downloading, setDownloading] = useState(null)

  if (!open) return null

  const handleDownload = async (format) => {
    if (downloading) return
    setDownloading(format)
    try {
      await sileo.promise(() => downloadResume(language, format), {
        loading: { title: t('cvDownloading') },
        success: { title: t('cvDownloaded') },
        error: { title: t('cvDownloadError') },
      })
      trackEvent('cv_download', { target: `${language}:${format}` })
      onClose()
    } catch {
      // Sileo communicates the failed request.
    } finally {
      setDownloading(null)
    }
  }

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/75 px-5 backdrop-blur-sm" role="presentation" onMouseDown={onClose}>
      <section
        role="dialog"
        aria-modal="true"
        aria-labelledby="resume-format-title"
        className="w-full max-w-2xl rounded-2xl border border-border-strong bg-card p-6 shadow-strong sm:p-8"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-6">
          <div>
            <p className="mb-2 text-xs font-semibold uppercase tracking-[0.18em] text-accent">{t('cvEyebrow')}</p>
            <h2 id="resume-format-title" className="text-2xl font-bold text-text sm:text-3xl">{t('cvFormatTitle')}</h2>
            <p className="mt-2 max-w-xl text-sm leading-6 text-muted">{t('cvFormatDescription')}</p>
          </div>
          <button type="button" onClick={onClose} className="rounded-md border border-border px-3 py-1.5 text-muted transition-colors hover:border-accent hover:text-accent" aria-label={t('close')}>×</button>
        </div>

        <div className="mt-7 grid gap-4 sm:grid-cols-2">
          {FORMATS.map((format) => (
            <button
              key={format.id}
              type="button"
              disabled={Boolean(downloading)}
              onClick={() => handleDownload(format.id)}
              className="group rounded-xl border border-border bg-surface p-5 text-left transition-all hover:-translate-y-0.5 hover:border-accent hover:shadow-soft disabled:cursor-wait disabled:opacity-60"
            >
              <span className="mb-5 inline-flex size-10 items-center justify-center rounded-lg border border-accent/40 bg-accent-soft text-xl text-accent">{format.icon}</span>
              <span className="block text-lg font-bold text-text group-hover:text-accent">{t(format.titleKey)}</span>
              <span className="mt-2 block text-sm leading-6 text-muted">{t(format.descriptionKey)}</span>
              <span className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-accent">
                {downloading === format.id ? t('cvDownloading') : t('cvChoose')} <span aria-hidden="true">→</span>
              </span>
            </button>
          ))}
        </div>
      </section>
    </div>
  )
}
