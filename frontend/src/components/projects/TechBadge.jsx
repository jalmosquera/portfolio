export function TechBadge({ tech }) {
  return (
    <span
      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border border-border bg-surface"
      style={{ color: tech.color || '#e5e5e5' }}
    >
      <span>{tech.icon}</span>
      <span>{tech.name}</span>
    </span>
  )
}
