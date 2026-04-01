import { Link } from 'react-router-dom'

export function Hero({ technologies = [] }) {
  const mainTechs = technologies.slice(0, 4)

  return (
    <section className="relative min-h-screen flex items-center pt-14 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#0d0d0d] via-[#111111] to-[#0d0d0d]" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_70%_50%,rgba(249,115,22,0.05),transparent_60%)]" />

      <div className="relative max-w-6xl mx-auto px-6 w-full grid grid-cols-1 lg:grid-cols-2 gap-8 items-center py-20">
        {/* Text */}
        <div className="space-y-5">
          <h1 className="text-5xl lg:text-[3.5rem] font-bold leading-[1.15] text-white">
            Hi, I'm <span className="text-accent">Jalberth Mosquera.</span><br />
            I'm a Backend Developer.
          </h1>

          <p className="text-[#9ca3af] text-base font-medium tracking-wide">
            Python • Django • Docker • Linux
          </p>
          <p className="text-[#6b7280] text-sm leading-relaxed max-w-sm">
            Deploying self-hosted solutions that drive a business growth.
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <Link
              to="/projects"
              className="inline-flex items-center px-5 py-2.5 bg-accent text-white font-semibold text-sm rounded-md hover:bg-accent-hover transition-colors"
            >
              View Projects
            </Link>
            <a
              href="/cv.pdf"
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#1a1a1a] border border-[#2a2a2a] text-[#d1d5db] text-sm font-medium rounded-md hover:border-[#444] transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download CV
            </a>
          </div>

          {mainTechs.length > 0 && (
            <div className="flex flex-wrap gap-2 pt-3">
              {mainTechs.map((tech) => (
                <span
                  key={tech.id}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-[#1a1a1a] border border-[#2a2a2a] rounded-full text-xs font-medium"
                  style={{ color: tech.color || '#e5e5e5' }}
                >
                  <span>{tech.icon}</span>
                  <span>{tech.name}</span>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Photo placeholder — replace src with your actual photo */}
        <div className="hidden lg:flex justify-end items-center">
          <div className="relative w-[420px] h-[520px] rounded-2xl overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-t from-[#0d0d0d] via-transparent to-transparent z-10" />
            <div className="absolute inset-0 bg-gradient-to-r from-[#0d0d0d] via-transparent to-transparent z-10" />
            {/* Replace this div with an <img src="/your-photo.jpg"> */}
            <div className="w-full h-full bg-[#1a1a1a] flex items-center justify-center">
              <span className="text-[#333] text-sm">Tu foto va aquí → <code className="text-accent">/public/photo.jpg</code></span>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
