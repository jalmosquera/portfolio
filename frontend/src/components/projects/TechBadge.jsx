export function TechBadge({ tech }) {
  return (
    <span
      className="inline-flex items-center gap-1.5 rounded-md border border-border bg-surface px-2.5 py-1 text-xs font-medium text-text"
    >
      <span>{tech.icon}</span>
      <span>{tech.name}</span>
    </span>
  )
}
