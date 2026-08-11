export function AnalyticsSection({ eyebrow, title, children, className = '' }) {
  return (
    <section className={`min-w-0 rounded-xl border border-border bg-card p-5 shadow-soft sm:p-6 ${className}`}>
      {eyebrow && <p className="text-xs font-semibold uppercase tracking-[0.16em] text-accent">{eyebrow}</p>}
      <h2 className={`${eyebrow ? 'mt-2' : ''} text-lg font-semibold text-text`}>{title}</h2>
      <div className="mt-6">{children}</div>
    </section>
  )
}
