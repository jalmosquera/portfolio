export function SectionTitle({ children, subtitle }) {
  return (
    <div className="mb-10">
      <div className="flex items-center gap-3 mb-2">
        <span className="w-1 h-6 bg-accent rounded-full inline-block" />
        <h2 className="text-2xl font-bold text-text">{children}</h2>
      </div>
      {subtitle && <p className="text-muted text-sm ml-4">{subtitle}</p>}
    </div>
  )
}
