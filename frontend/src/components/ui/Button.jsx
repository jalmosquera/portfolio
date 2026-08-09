export function Button({ children, variant = 'primary', href, onClick, className = '' }) {
  const base = 'inline-flex items-center gap-2 px-5 py-2.5 rounded-lg font-medium text-sm transition-all duration-200 cursor-pointer'
  const variants = {
    primary: 'bg-accent text-white hover:bg-accent-hover',
    outline: 'border border-accent text-accent hover:bg-accent hover:text-white',
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
