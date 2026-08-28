import stackIllustration from '../../assets/myStack.jpg'
import { useLanguage } from '../../context/useLanguage'
import { technologyIcon } from '../../lib/technology-icons'
import { Reveal } from '../ui/Reveal'

export function TechStack({ technologies = [] }) {
  const { t } = useLanguage()

  const defaultTechnologies = [
    { id: 'python', name: 'Python', icon: '🐍' },
    { id: 'django', name: 'Django', icon: '◩' },
    { id: 'docker', name: 'Docker', icon: '🐳' },
    { id: 'linux', name: 'Linux', icon: '♟' },
    { id: 'nginx', name: 'Nginx', icon: '⬡' },
    { id: 'cicd', name: 'CI/CD Tools', icon: '❖' },
  ]

  const stack = technologies.length > 0
    ? technologies
    : defaultTechnologies

  return (
    <section className="border-b border-border py-16 lg:py-20">
      <div className="site-container relative">
        <div className="relative grid grid-cols-1 items-center gap-10 lg:grid-cols-[1.15fr_0.85fr] min-[2200px]:grid-cols-[1.3fr_0.7fr] min-[2200px]:gap-20">
          <Reveal>
            <h2 className="mb-2 text-3xl font-bold text-text">
              {t('techTitle')}
            </h2>

            <p className="mb-8 text-sm text-muted">
              {t('techSubtitle')}
            </p>

            <div className="flex flex-wrap gap-2.5">
              {stack.map((tech, index) => {
                const icon = technologyIcon(tech.name)

                return (
                  <Reveal
                    key={tech.id}
                    as="div"
                    delay={Math.min(index * 55, 330)}
                    distance="sm"
                    className="interactive-lift flex items-center gap-2 rounded-md border border-border bg-card px-4 py-2 hover:border-accent/60"
                  >
                    {icon ? (
                      <img
                        src={icon}
                        alt=""
                        width="20"
                        height="20"
                        loading="lazy"
                        decoding="async"
                        className="size-5 object-contain"
                      />
                    ) : (
                      <span className="text-base">
                        {tech.icon}
                      </span>
                    )}

                    <span className="text-sm font-medium text-text">
                      {tech.name}
                    </span>
                  </Reveal>
                )
              })}
            </div>
          </Reveal>

          <Reveal
            className="hidden items-center justify-center lg:flex"
            delay={180}
            distance="lg"
          >
            <img
              src={stackIllustration}
              alt={t('techAlt')}
              loading="lazy"
              decoding="async"
              fetchPriority="low"
              className="w-full max-w-107.5 object-contain opacity-95 xl:max-w-117.5 2xl:max-w-130 min-[2200px]:max-w-145"
            />
          </Reveal>
        </div>
      </div>
    </section>
  )
}