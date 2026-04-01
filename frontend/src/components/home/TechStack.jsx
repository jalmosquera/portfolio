import { SectionTitle } from '../ui/SectionTitle'

export function TechStack({ technologies = [] }) {
  return (
    <section className="py-20 bg-surface">
      <div className="max-w-6xl mx-auto px-6">
        <SectionTitle subtitle="Technologies I use to build and deploy applications, at scale.">
          My Tech Stack
        </SectionTitle>

        <div className="flex flex-wrap gap-3">
          {technologies.map((tech) => (
            <div
              key={tech.id}
              className="flex items-center gap-2 px-4 py-2.5 bg-card border border-border rounded-xl hover:border-accent/40 transition-colors"
            >
              <span className="text-xl">{tech.icon}</span>
              <span className="text-sm font-medium" style={{ color: tech.color || '#e5e5e5' }}>
                {tech.name}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
