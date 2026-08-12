import { useEffect, useRef, useState } from 'react'

export function Reveal({ children, className = '', delay = 0, distance = 'md', as = 'div', ...props }) {
  const elementRef = useRef(null)
  const [visible, setVisible] = useState(false)
  const Component = as

  useEffect(() => {
    const element = elementRef.current
    if (!element) return undefined

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return
        setVisible(true)
        observer.unobserve(entry.target)
      },
      { rootMargin: '0px 0px -10% 0px', threshold: 0.08 },
    )

    observer.observe(element)
    return () => observer.disconnect()
  }, [])

  return (
    <Component
      ref={elementRef}
      className={`reveal reveal-${distance} ${visible ? 'is-visible' : ''} ${className}`}
      style={{ '--reveal-delay': `${delay}ms` }}
      {...props}
    >
      {children}
    </Component>
  )
}
