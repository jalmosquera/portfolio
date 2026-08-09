export function SectionTitle({ children, subtitle }) {
  return (
    <div className="mb-10 border-b border-border pb-6">
      <h1 className="text-3xl font-bold text-text">{children}</h1>
      {subtitle && <p className="mt-2 text-sm text-muted">{subtitle}</p>}
    </div>
  )
}
