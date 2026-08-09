export function TechStack({ technologies = [] }) {
  return (
    <section className="py-20 border-t border-[#1a1a1a]">
      <div className="max-w-6xl mx-auto px-6 relative">
        <div className="absolute -top-10 right-10 w-32 h-32 rounded-full blur-3xl bg-accent/10 pointer-events-none" />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center relative">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2">My Tech Stack</h2>
            <p className="text-muted text-sm mb-8">Technologies I use to build and deploy applications, at scale.</p>

            <div className="flex flex-wrap gap-2.5">
              {technologies.map((tech) => (
                <div
                  key={tech.id}
                  className="flex items-center gap-2 px-4 py-2 bg-card border border-border rounded-lg hover:border-accent/60 hover:-translate-y-0.5 transition-all"
                >
                  <span className="text-base">{tech.icon}</span>
                  <span className="text-sm font-medium" style={{ color: tech.color || '#d1d5db' }}>
                    {tech.name}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Visual side — 3D server illustration placeholder */}
          <div className="hidden lg:flex justify-center items-center">
            <div className="relative w-72 h-56 flex items-end justify-center gap-4">
              {/* Simulated server stack */}
              {['Docker', 'Nginx', 'PostgreSQL'].map((label, i) => (
                <div
                  key={label}
                  className="flex flex-col items-center gap-1"
                  style={{ transform: `translateY(${i * 8}px)` }}
                >
                  <div className="w-20 h-12 bg-card border border-border rounded-lg flex items-center justify-center shadow-[0_12px_26px_rgba(0,0,0,0.45)]">
                    <span className="text-xl">
                      {label === 'Docker' ? '🐳' : label === 'Nginx' ? '🌐' : '🐘'}
                    </span>
                  </div>
                  <span className="text-[10px] text-muted">{label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
