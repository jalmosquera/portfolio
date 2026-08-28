import { useState } from 'react'
import { sileo } from 'sileo'
import { createContactInquiry } from '../../lib/api/contact'
import { SOCIAL_LINKS } from '../../lib/config/routes'
import { useLanguage } from '../../context/useLanguage'
import { trackEvent } from '../../lib/analytics/tracker'
import { Reveal } from '../ui/Reveal'

const INITIAL_FORM = {
  company_or_recruiter: '',
  phone: '',
  email: '',
  description: '',
}

const fieldClassName = 'w-full rounded-md border border-border bg-surface px-4 py-3 text-sm text-text outline-none transition-colors placeholder:text-subtle focus:border-accent'

function getErrorMessage(error, t) {
  const responseData = error.response?.data
  if (!responseData || typeof responseData !== 'object') {
    return t('sendError')
  }

  const firstError = Object.values(responseData).flat()[0]
  return typeof firstError === 'string' ? firstError : t('formError')
}

export function Contact() {
  const { language, t } = useLanguage()
  const [form, setForm] = useState(INITIAL_FORM)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [sent, setSent] = useState(false)

  const handleChange = ({ target }) => {
    setForm((current) => ({ ...current, [target.name]: target.value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setSubmitting(true)
    setError('')

    try {
      await sileo.promise(() => createContactInquiry(form, language), {
        loading: { title: t('sending') },
        success: { title: t('sent'), duration: 6000 },
        error: { title: t('sendError') },
      })
      trackEvent('contact_click', { target: 'form_submit' })
      setForm(INITIAL_FORM)
      setSent(true)
    } catch (requestError) {
      setSent(false)
      setError(getErrorMessage(requestError, t))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section id="contact" className="py-16 lg:py-20">
      <div className="site-container">
        <div className="grid gap-10 lg:grid-cols-[0.75fr_1.25fr] lg:gap-16 min-[2200px]:gap-24">
          <Reveal>
            <p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-accent">{t('contactEyebrow')}</p>
            <h2 className="text-3xl font-bold text-text">{t('contactTitle')}</h2>
            <p className="mt-4 max-w-lg text-sm leading-7 text-muted sm:text-base">
              {t('contactIntro')}
            </p>

            <div className="mt-8 flex flex-wrap gap-3">
              <a
                href={SOCIAL_LINKS.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => trackEvent('linkedin_click', { target: SOCIAL_LINKS.linkedin })}
                className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-4 py-2.5 text-sm font-medium text-text transition-colors hover:border-accent hover:text-accent"
              >
                LinkedIn
              </a>
              <a
                href={SOCIAL_LINKS.github}
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => trackEvent('github_click', { target: SOCIAL_LINKS.github })}
                className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-4 py-2.5 text-sm font-medium text-text transition-colors hover:border-accent hover:text-accent"
              >
                GitHub
              </a>
            </div>
          </Reveal>

          <Reveal as="form" onSubmit={handleSubmit} className="grid gap-5 rounded-lg border border-border bg-card p-5 shadow-soft sm:grid-cols-2 sm:p-7" delay={140} distance="lg">
            <label className="space-y-2">
              <span className="text-sm font-medium text-text">{t('company')}</span>
              <input
                name="company_or_recruiter"
                value={form.company_or_recruiter}
                onChange={handleChange}
                required
                minLength={2}
                maxLength={160}
                autoComplete="organization"
                className={fieldClassName}
                placeholder={t('companyPlaceholder')}
              />
            </label>

            <label className="space-y-2">
              <span className="text-sm font-medium text-text">Email</span>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                required
                autoComplete="email"
                className={fieldClassName}
                placeholder="name@company.com"
              />
            </label>

            <label className="space-y-2 sm:col-span-2">
              <span className="text-sm font-medium text-text">{t('phone')}</span>
              <input
                type="tel"
                name="phone"
                value={form.phone}
                onChange={handleChange}
                required
                minLength={7}
                maxLength={32}
                autoComplete="tel"
                className={fieldClassName}
                placeholder="+34 600 000 000"
              />
            </label>

            <label className="space-y-2 sm:col-span-2">
              <span className="text-sm font-medium text-text">{t('description')}</span>
              <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
                required
                minLength={20}
                rows={6}
                className={`${fieldClassName} resize-y`}
                placeholder={t('descriptionPlaceholder')}
              />
            </label>

            <div className="flex flex-col gap-3 sm:col-span-2 sm:flex-row sm:items-center sm:justify-between">
              <div aria-live="polite">
                {sent && <p className="text-sm text-accent">{t('sent')}</p>}
                {error && <p className="text-sm text-accent">{error}</p>}
              </div>
              <button
                type="submit"
                disabled={submitting}
                className="inline-flex min-w-36 items-center justify-center rounded-md border border-accent/60 bg-accent-soft px-5 py-3 text-sm font-semibold text-accent transition-colors hover:bg-accent hover:text-bg disabled:cursor-not-allowed disabled:opacity-60"
              >
                {submitting ? t('sending') : t('send')}
              </button>
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  )
}
