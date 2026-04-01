import { Button } from '../ui/Button'
import { Link } from 'react-router-dom'

export function Hero({ technologies = [] }) {
  const mainTechs = technologies.slice(0, 4)

  return (
    <section className="min-h-screen flex items-center pt-16">
      <div className="max-w-6xl mx-auto px-6 w-full grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        <div className="space-y-6">
          <h1 className="text-5xl lg:text-6xl font-bold leading-tight text-text">
            Hi, I'm <span className="text-accent">Jalberth</span><br />
            Mosquera.
          </h1>
          <p className="text-xl text-muted font-medium">
            Python · Django · Docker · Linux
          </p>
          <p className="text-muted leading-relaxed max-w-md">
            Deploying self-hosted solutions that drive business growth.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Link
              to="/projects"
              className="inline-flex items-center gap-2 px-6 py-3 bg-accent text-white font-semibold rounded-lg hover:bg-accent-hover transition-colors"
            >
              View Projects
            </Link>
            <Button variant="outline" href="https://github.com/jalmosquera">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
              </svg>
              GitHub
            </Button>
          </div>

          {mainTechs.length > 0 && (
            <div className="flex flex-wrap gap-2 pt-2">
              {mainTechs.map((tech) => (
                <span
                  key={tech.id}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-surface border border-border rounded-full text-sm"
                  style={{ color: tech.color || '#e5e5e5' }}
                >
                  <span>{tech.icon}</span>
                  <span>{tech.name}</span>
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="hidden lg:flex justify-center items-center">
          <div className="w-80 h-80 rounded-2xl bg-surface border border-border flex items-center justify-center text-8xl">
            👨‍💻
          </div>
        </div>
      </div>
    </section>
  )
}
