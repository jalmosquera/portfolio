import { useState } from 'react'

const LANGUAGE_LABELS = {
  en: 'EN',
  es: 'ES',
}

function renderInlineFormatting(text) {
  return text.split(/(\*\*.*?\*\*)/g).filter(Boolean).map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={`${part}-${index}`} className="font-semibold text-text">{part.slice(2, -2)}</strong>
    }

    return part
  })
}

function AboutBody({ body }) {
  const blocks = body.split('\n\n').filter(Boolean)

  return blocks.map((block, index) => {
    const lines = block.split('\n')
    const isHeading = lines.length === 1 && /^\*\*.*\*\*$/.test(block)
    const isStack = lines.length > 1

    if (isHeading) {
      return <h3 key={block} className="pt-3 text-xl font-semibold text-text">{block.slice(2, -2)}</h3>
    }

    if (isStack) {
      return (
        <div key={index} className="grid gap-2 rounded-lg border border-border bg-card p-5 text-sm leading-6 sm:grid-cols-2 sm:p-6">
          {lines.map((line) => <p key={line}>{renderInlineFormatting(line)}</p>)}
        </div>
      )
    }

    return <p key={index}>{renderInlineFormatting(block)}</p>
  })
}

export function AboutMe({ about }) {
  const availableLanguages = Object.keys(about?.translations ?? {})
  const preferredLanguage = navigator.language.toLowerCase().startsWith('es') ? 'es' : 'en'
  const initialLanguage = availableLanguages.includes(preferredLanguage)
    ? preferredLanguage
    : availableLanguages[0]
  const [language, setLanguage] = useState(initialLanguage)
  const content = about?.translations?.[language]

  if (!content) return null

  return (
    <section id="about" className="border-b border-border py-16 lg:py-20">
      <div className="site-container">
        <div className="grid gap-8 lg:grid-cols-[0.45fr_1fr] lg:gap-16 min-[2200px]:gap-24">
          <div className="flex items-start justify-between gap-4 lg:block">
            <div>
              <p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-accent">{language === 'es' ? 'Perfil' : 'Profile'}</p>
              <h2 className="text-3xl font-bold text-text">{content.title}</h2>
            </div>
            <div className="flex rounded-md border border-border bg-card p-1 lg:mt-6 lg:w-fit" aria-label="About me language">
              {availableLanguages.map((languageCode) => (
                <button
                  key={languageCode}
                  type="button"
                  onClick={() => setLanguage(languageCode)}
                  className={`rounded px-3 py-1.5 text-xs font-semibold transition-colors ${languageCode === language ? 'bg-accent text-bg' : 'text-muted hover:text-text'}`}
                  aria-pressed={languageCode === language}
                >
                  {LANGUAGE_LABELS[languageCode] ?? languageCode.toUpperCase()}
                </button>
              ))}
            </div>
          </div>

          <div className="max-w-4xl space-y-6">
            <div className="space-y-5 text-base leading-8 text-muted sm:text-lg">
              <AboutBody body={content.body} />
            </div>
            <div className="flex flex-wrap gap-3 text-sm">
              {content.location && <span className="rounded-md border border-border bg-card px-3 py-2 text-text">⌖ {content.location}</span>}
              {content.availability && <span className="rounded-md border border-accent/30 bg-accent-soft px-3 py-2 text-accent">● {content.availability}</span>}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
