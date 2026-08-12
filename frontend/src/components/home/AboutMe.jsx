import { useLanguage } from '../../context/useLanguage'
import { Reveal } from '../ui/Reveal'

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
  const { language, t } = useLanguage()
  const content = about?.translations?.[language] ?? about?.translations?.en ?? Object.values(about?.translations ?? {})[0]

  if (!content) return null

  return (
    <section id="about" className="border-b border-border py-16 lg:py-20">
      <div className="site-container">
        <div className="grid gap-8 lg:grid-cols-[0.45fr_1fr] lg:gap-16 min-[2200px]:gap-24">
          <Reveal>
            <div>
              <p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-accent">{t('profile')}</p>
              <h2 className="text-3xl font-bold text-text">{content.title}</h2>
            </div>
          </Reveal>

          <Reveal className="max-w-4xl space-y-6" delay={120} distance="lg">
            <div className="space-y-5 text-base leading-8 text-muted sm:text-lg">
              <AboutBody body={content.body} />
            </div>
            <div className="flex flex-wrap gap-3 text-sm">
              {content.location && <span className="rounded-md border border-border bg-card px-3 py-2 text-text">⌖ {content.location}</span>}
              {content.availability && <span className="rounded-md border border-accent/30 bg-accent-soft px-3 py-2 text-accent">● {content.availability}</span>}
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  )
}
