import { Link } from 'react-router-dom'

export function Hero({ technologies = [] }) {
  const mainTechs = technologies.slice(0, 4)

  return (
    <section className="relative mt-14 overflow-hidden" style={{ height: 'calc(100vh - 56px)' }}>

      {/* Photo — right side, full height, absolute */}
      <div className="absolute right-0 top-0 w-[55%] h-full">
        <img
          src="/photo.jpg"
          alt="Jalberth Mosquera"
          className="w-full h-full object-cover object-top"
          onError={(e) => { e.target.style.display = 'none' }}
        />
        {/* Gradient: funde la foto con el fondo oscuro */}
        <div className="absolute inset-0 bg-gradient-to-r from-[#0d0d0d] via-[#0d0d0d]/70 to-transparent" />
        <div className="absolute inset-0 bg-gradient-to-t from-[#0d0d0d] via-transparent to-transparent" />
      </div>

      {/* Text — left side */}
      <div className="relative z-10 h-full flex flex-col justify-center px-10 lg:px-16 max-w-2xl">
        <h1 className="text-4xl lg:text-5xl font-bold text-white leading-tight mb-1">
          Hi, I'm <span className="text-accent">Jalberth Mosquera.</span>
        </h1>
        <h1 className="text-4xl lg:text-5xl font-bold text-white leading-tight mb-4">
          I'm a Backend Developer.
        </h1>

        <p className="text-[#9ca3af] text-sm font-medium mb-2">
          Python • Django • Docker • Linux
        </p>
        <p className="text-[#6b7280] text-sm leading-relaxed mb-7 max-w-xs">
          Deploying self-hosted solutions that drive a business growth.
        </p>

        <div className="flex flex-wrap items-center gap-3 mb-8">
          <Link
            to="/projects"
            className="inline-flex items-center px-5 py-2.5 bg-accent text-white font-semibold text-sm rounded-md hover:bg-accent-hover transition-colors"
          >
            View Projects
          </Link>
          <a
            href="/cv.pdf"
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-transparent border border-[#3a3a3a] text-[#d1d5db] text-sm font-medium rounded-md hover:border-[#555] transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Download CV
          </a>
        </div>

        {mainTechs.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {mainTechs.map((tech) => (
              <span
                key={tech.id}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-[#ffffff08] border border-[#ffffff15] rounded-full text-xs font-medium backdrop-blur-sm"
                style={{ color: tech.color || '#d1d5db' }}
              >
                <span>{tech.icon}</span>
                <span>{tech.name}</span>
              </span>
            ))}
          </div>
        )}
      </div>

    </section>
  )
}
