import { Link } from "react-router-dom";
import heroImg from "../../assets/jal.jpeg";
import { APP_ROUTES } from "../../lib/config/routes";
import { useLanguage } from '../../context/useLanguage'

export function Hero({ technologies = [] }) {
  const mainTechs = technologies.slice(0, 4);
  const { t } = useLanguage()

  return (
    <section className="relative border-b border-border pt-16">
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-r from-bg via-transparent to-accent-soft/30" />
      <div className="site-container relative grid min-h-[560px] grid-cols-1 lg:grid-cols-[1.05fr_0.95fr] 2xl:min-h-[640px] min-[2200px]:min-h-[720px] min-[2200px]:grid-cols-[1fr_0.9fr]">
        {/* Left: text */}
        <div className="z-20 flex flex-col justify-center gap-7 py-12 sm:py-16 lg:py-20 min-[2200px]:gap-9">
          <div className="space-y-4">
            <h1 className="max-w-2xl text-3xl font-bold leading-tight text-text min-[420px]:text-4xl sm:text-5xl 2xl:text-6xl min-[2200px]:max-w-4xl min-[2200px]:text-7xl">
              {t('heroGreeting')} <span className="text-accent">Jalberth Mosquera.</span><br />
              {t('heroRole')}
            </h1>
            <div className="space-y-2 text-sm sm:text-base min-[2200px]:text-lg">
              <p className="font-medium text-text">Python · Django · Docker · Linux</p>
              <p className="max-w-xl text-muted">{t('heroDescription')}</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Link
              to={APP_ROUTES.projects}
              className="inline-flex items-center gap-2 rounded-md border border-accent/60 bg-accent-soft px-5 py-2.5 text-sm font-semibold text-accent transition-colors hover:bg-accent hover:text-bg"
            >
              {t('viewProjects')}
            </Link>
            <a
              href="/cv.pdf"
              className="inline-flex items-center gap-2 rounded-md border border-border-strong bg-card/70 px-5 py-2.5 text-sm font-semibold text-text transition-colors hover:border-accent hover:text-accent"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              {t('downloadCv')}
            </a>
          </div>

          {mainTechs.length > 0 && (
            <div className="flex flex-wrap gap-2 pt-4">
              {mainTechs.map((tech) => (
                <span
                  key={tech.id}
                  className="inline-flex items-center gap-1.5 rounded-md border border-border bg-card/80 px-3 py-1.5 text-xs font-medium text-text backdrop-blur-sm"
                >
                  <span>{tech.icon}</span>
                  <span>{tech.name}</span>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Right: portrait */}
        <div className="relative min-h-[340px] overflow-hidden min-[420px]:min-h-[420px] lg:min-h-0">
          <div className="pointer-events-none absolute inset-x-0 bottom-0 z-10 h-40 bg-gradient-to-t from-bg to-transparent" />
          <img
            src={heroImg}
            alt="Jalberth Mosquera"
            className="hero-portrait absolute left-1/2 top-0 h-[118%] w-auto max-w-none -translate-x-1/2 object-contain object-top grayscale-[15%]"
          />
        </div>
      </div>
    </section>
  );
}
