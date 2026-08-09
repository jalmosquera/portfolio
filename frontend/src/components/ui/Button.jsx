export function Button({ children, variant = 'primary', href, onClick, className = '' }) {
  const base = 'inline-flex cursor-pointer items-center gap-2 rounded-md px-5 py-2.5 text-sm font-medium transition-colors duration-200'
  const variants = {
    primary: 'border border-accent/60 bg-accent-soft text-accent hover:bg-accent hover:text-bg',
    outline: 'border border-border bg-card text-text hover:border-accent hover:text-accent',
    ghost: 'text-muted hover:text-text',
  }

  if (href) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className={`${base} ${variants[variant]} ${className}`}>
        {children}
      </a>
    )
  }

  return (
    <button onClick={onClick} className={`${base} ${variants[variant]} ${className}`}>
      {children}
    </button>
  )
}
