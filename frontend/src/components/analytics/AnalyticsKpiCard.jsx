export function AnalyticsKpiCard({ label, value, detail }) {
  return (
    <article className="rounded-xl border border-border bg-card p-5 shadow-soft">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-muted">{label}</p>
      <p className="mt-3 text-3xl font-bold text-text">{value}</p>
      <p className="mt-2 text-xs text-subtle">{detail}</p>
    </article>
  )
}
