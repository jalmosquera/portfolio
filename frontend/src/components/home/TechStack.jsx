import stackIllustration from '../../assets/hero.png'

export function TechStack({ technologies = [] }) {
  return (
    <section id="about" className="border-b border-border py-16 lg:py-20">
      <div className="relative mx-auto max-w-6xl px-5 sm:px-8">
        <div className="relative grid grid-cols-1 items-center gap-10 lg:grid-cols-[1.2fr_0.8fr]">
          <div>
            <h2 className="mb-2 text-3xl font-bold text-text">My Tech Stack</h2>
            <p className="text-muted text-sm mb-8">Technologies I use to build and deploy applications, at scale.</p>

            <div className="flex flex-wrap gap-2.5">
              {(technologies.length > 0 ? technologies : [
                { id: 'python', name: 'Python', icon: '🐍' },
                { id: 'django', name: 'Django', icon: '◩' },
                { id: 'docker', name: 'Docker', icon: '🐳' },
                { id: 'linux', name: 'Linux', icon: '♟' },
                { id: 'nginx', name: 'Nginx', icon: '⬡' },
                { id: 'cicd', name: 'CI/CD Tools', icon: '❖' },
              ]).map((tech) => (
                <div
                  key={tech.id}
                  className="flex items-center gap-2 rounded-md border border-border bg-card px-4 py-2 transition-colors hover:border-accent/60"
                >
                  <span className="text-base">{tech.icon}</span>
                  <span className="text-sm font-medium text-text">
                    {tech.name}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="hidden justify-center lg:flex">
            <img src={stackIllustration} alt="Self-hosted infrastructure stack" className="w-full max-w-sm opacity-90" />
          </div>
        </div>
      </div>
    </section>
  )
}
