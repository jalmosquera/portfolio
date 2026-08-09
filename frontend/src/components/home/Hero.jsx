import { Link } from "react-router-dom";
import heroImg from "../../assets/jal.jpeg";
import { APP_ROUTES } from "../../lib/config/routes";

export function Hero({ technologies = [] }) {
  const mainTechs = technologies.slice(0, 4);

  return (
    <section className="relative border-b border-border pt-16">
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-r from-bg via-transparent to-accent-soft/30" />
      <div className="relative mx-auto grid min-h-[560px] max-w-6xl grid-cols-1 px-5 sm:px-8 lg:grid-cols-[1.05fr_0.95fr]">
        {/* Left: text */}
        <div className="z-20 flex flex-col justify-center gap-7 py-16 lg:py-20">
          <div className="space-y-4">
            <h1 className="max-w-2xl text-4xl font-bold leading-tight text-text sm:text-5xl">
              Hi, I'm <span className="text-accent">Jalberth Mosquera.</span><br />
              I'm a Backend Developer.
            </h1>
            <div className="space-y-2 text-sm sm:text-base">
              <p className="font-medium text-text">Python · Django · Docker · Linux</p>
              <p className="max-w-xl text-muted">Deploying self-hosted solutions that drive a business' growth.</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Link
              to={APP_ROUTES.projects}
              className="inline-flex items-center gap-2 rounded-md border border-accent/60 bg-accent-soft px-5 py-2.5 text-sm font-semibold text-accent transition-colors hover:bg-accent hover:text-bg"
            >
              View Projects
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
              Download CV
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
        <div className="relative min-h-[420px] overflow-hidden lg:min-h-0">
          <div className="pointer-events-none absolute inset-0 z-10 bg-gradient-to-r from-bg via-transparent to-transparent" />
          <div className="pointer-events-none absolute inset-x-0 bottom-0 z-10 h-40 bg-gradient-to-t from-bg to-transparent" />
          <img
            src={heroImg}
            alt="Jalberth Mosquera"
            className="absolute inset-0 h-full w-full object-cover object-top grayscale-[15%]"
          />
        </div>
      </div>
    </section>
  );
}
