import { Link } from "react-router-dom";
import heroImg from "../../assets/jal.jpeg";

export function Hero({ technologies = [] }) {
  const mainTechs = technologies.slice(0, 4);

  return (
    <section className="relative mt-14 overflow-hidden rounded-3xl border border-border/70 bg-gradient-to-r from-[#0d0d0d] via-[#111]/90 to-[#0f0f0f] shadow-[var(--shadow-strong)]">
      {/* Glow + vignette */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(215,121,44,0.15),transparent_35%)]" />
        <div className="absolute inset-0 bg-gradient-to-r from-[#0c0c0c] via-transparent to-[#0c0c0c]" />
      </div>

      {/* Content */}
      <div className="relative grid grid-cols-1 lg:grid-cols-[1.1fr_0.9fr]">
        {/* Left: text */}
        <div className="px-10 lg:px-16 py-16 flex flex-col gap-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#ffffff0d] border border-[#ffffff12] text-[11px] uppercase tracking-[0.15em] text-muted w-fit">
            Backend Developer · Self-hosted
          </div>

          <div className="space-y-2">
            <h1 className="text-4xl lg:text-5xl font-bold text-white leading-tight">
              Hi, I'm <span className="text-accent">Jalberth Mosquera</span>.
            </h1>
            <p className="text-lg text-muted max-w-xl">
              Python · Django · Docker · Linux — deploying self-hosted solutions
              that drive a business' growth.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Link
              to="/projects"
              className="inline-flex items-center gap-2 px-6 py-3 bg-accent text-white font-semibold text-sm rounded-xl shadow-[0_18px_40px_rgba(215,121,44,0.35)] hover:bg-accent-hover transition-all"
            >
              View Projects
            </Link>
            <a
              href="/cv.pdf"
              className="inline-flex items-center gap-2 px-6 py-3 border border-border-strong text-text text-sm font-semibold rounded-xl hover:border-accent hover:text-accent transition-all"
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

          <div className="grid grid-cols-2 gap-4">
            {[
              { label: "Python", value: "Django · FastAPI · DRF" },
              { label: "Platform", value: "Docker · Nginx · Linux" },
              { label: "Data", value: "PostgreSQL · Redis" },
              { label: "Reliability", value: "CI/CD · Observability" },
            ].map((item) => (
              <div
                key={item.label}
                className="bg-card/70 border border-border rounded-xl px-4 py-3"
              >
                <p className="text-[11px] uppercase tracking-[0.12em] text-muted">
                  {item.label}
                </p>
                <p className="text-sm text-text mt-1">{item.value}</p>
              </div>
            ))}
          </div>

          {mainTechs.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {mainTechs.map((tech) => (
                <span
                  key={tech.id}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-[#ffffff10] border border-[#ffffff15] rounded-full text-xs font-medium backdrop-blur-sm"
                  style={{ color: tech.color || "#d1d5db" }}
                >
                  <span>{tech.icon}</span>
                  <span>{tech.name}</span>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Right: portrait */}
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-l from-[#0b0b0b] via-transparent to-transparent" />
          <img
            src={heroImg}
            alt="Jalberth Mosquera"
            className="w-full h-full object-cover object-top mix-blend-lighten"
          />
        </div>
      </div>
    </section>
  );
}
