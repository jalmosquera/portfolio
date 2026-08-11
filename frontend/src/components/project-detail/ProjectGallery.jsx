import { useEffect, useRef, useState } from 'react'
import { getMediaUrl } from '../../lib/config/routes'
import { useLanguage } from '../../context/useLanguage'

const COPY = {
  es: {
    close: 'Cerrar galería',
    previous: 'Imagen anterior',
    next: 'Imagen siguiente',
    open: 'Abrir imagen',
    hint: 'Usá las flechas del teclado para navegar',
    fallback: 'Imagen del proyecto',
  },
  en: {
    close: 'Close gallery',
    previous: 'Previous image',
    next: 'Next image',
    open: 'Open image',
    hint: 'Use the keyboard arrows to navigate',
    fallback: 'Project image',
  },
}

function ArrowIcon({ direction }) {
  return (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
        d={direction === 'left' ? 'M15 19l-7-7 7-7' : 'M9 5l7 7-7 7'}
      />
    </svg>
  )
}

function CloseIcon() {
  return (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
    </svg>
  )
}

export function ProjectGallery({ images }) {
  const { language } = useLanguage()
  const copy = COPY[language] ?? COPY.en
  const galleryImages = images.filter((image) => image.image)
  const [activeIndex, setActiveIndex] = useState(null)
  const touchStartX = useRef(null)
  const closeButtonRef = useRef(null)

  useEffect(() => {
    if (activeIndex === null) return undefined

    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    closeButtonRef.current?.focus()

    const handleKeyDown = (event) => {
      if (event.key === 'Escape') setActiveIndex(null)
      if (event.key === 'ArrowLeft') {
        setActiveIndex((current) => (current - 1 + galleryImages.length) % galleryImages.length)
      }
      if (event.key === 'ArrowRight') {
        setActiveIndex((current) => (current + 1) % galleryImages.length)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => {
      document.body.style.overflow = previousOverflow
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [activeIndex, galleryImages.length])

  const showPrevious = () => {
    setActiveIndex((current) => (current - 1 + galleryImages.length) % galleryImages.length)
  }

  const showNext = () => {
    setActiveIndex((current) => (current + 1) % galleryImages.length)
  }

  const handleTouchStart = (event) => {
    touchStartX.current = event.changedTouches[0].clientX
  }

  const handleTouchEnd = (event) => {
    if (touchStartX.current === null) return
    const distance = event.changedTouches[0].clientX - touchStartX.current
    touchStartX.current = null
    if (Math.abs(distance) < 50) return
    if (distance > 0) showPrevious()
    else showNext()
  }

  const activeImage = activeIndex === null ? null : galleryImages[activeIndex]

  return (
    <>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 min-[2200px]:grid-cols-5">
        {images.map((image) => {
          const galleryIndex = galleryImages.findIndex((item) => item.id === image.id)
          const title = image.title || copy.fallback

          if (!image.image) {
            return (
              <article key={image.id} className="overflow-hidden rounded-lg border border-border bg-card shadow-soft">
                <div className="flex aspect-[4/3] items-center justify-center bg-surface text-4xl text-muted">🖥️</div>
                <p className="min-h-10 px-3 py-2 text-xs text-muted">{title}</p>
              </article>
            )
          }

          return (
            <button
              key={image.id}
              type="button"
              onClick={() => setActiveIndex(galleryIndex)}
              aria-label={`${copy.open}: ${title}`}
              className="group overflow-hidden rounded-lg border border-border bg-card text-left shadow-soft transition duration-300 hover:-translate-y-1 hover:border-accent/60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
            >
              <span className="relative flex aspect-[4/3] items-center justify-center overflow-hidden bg-surface p-2">
                <img
                  src={getMediaUrl(image.image)}
                  alt={title}
                  loading="lazy"
                  decoding="async"
                  fetchPriority="low"
                  sizes="(min-width: 2200px) 20vw, (min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
                  className="h-full w-full object-contain transition-transform duration-300 group-hover:scale-[1.02]"
                />
                <span className="pointer-events-none absolute inset-0 flex items-center justify-center bg-bg/0 transition-colors group-hover:bg-bg/25">
                  <span className="translate-y-2 rounded-full border border-text/20 bg-bg/80 p-3 text-text opacity-0 shadow-strong backdrop-blur-sm transition group-hover:translate-y-0 group-hover:opacity-100">
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-4.553a1.5 1.5 0 10-2.121-2.121L13 7.757M9 14l-4.553 4.553a1.5 1.5 0 002.121 2.121L11 16.243M14 9h6v6M10 15H4V9" />
                    </svg>
                  </span>
                </span>
              </span>
              <span className="block min-h-10 px-3 py-2 text-xs text-muted transition-colors group-hover:text-text">{title}</span>
            </button>
          )
        })}
      </div>

      {activeImage && (
        <div
          className="fixed inset-0 z-[100] flex flex-col bg-bg/95 backdrop-blur-md"
          role="dialog"
          aria-modal="true"
          aria-label={activeImage.title || copy.fallback}
          onClick={() => setActiveIndex(null)}
        >
          <header className="flex h-16 shrink-0 items-center justify-between border-b border-border px-4 sm:px-6">
            <div className="min-w-0">
              <p className="truncate text-sm font-medium text-text">{activeImage.title || copy.fallback}</p>
              <p className="text-xs text-muted">{activeIndex + 1} / {galleryImages.length}</p>
            </div>
            <button
              ref={closeButtonRef}
              type="button"
              onClick={() => setActiveIndex(null)}
              aria-label={copy.close}
              className="rounded-full border border-border bg-card p-2.5 text-muted transition-colors hover:border-accent/60 hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
            >
              <CloseIcon />
            </button>
          </header>

          <div
            className="relative flex min-h-0 flex-1 items-center justify-center px-4 py-5 sm:px-20 sm:py-8"
            onClick={(event) => event.stopPropagation()}
            onTouchStart={handleTouchStart}
            onTouchEnd={handleTouchEnd}
          >
            {galleryImages.length > 1 && (
              <button
                type="button"
                onClick={showPrevious}
                aria-label={copy.previous}
                className="absolute left-3 z-10 rounded-full border border-border bg-card/90 p-3 text-text shadow-strong transition-colors hover:border-accent hover:text-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent sm:left-6"
              >
                <ArrowIcon direction="left" />
              </button>
            )}

            <img
              key={activeImage.id}
              src={getMediaUrl(activeImage.image)}
              alt={activeImage.title || copy.fallback}
              decoding="async"
              className="max-h-full max-w-full select-none object-contain"
            />

            {galleryImages.length > 1 && (
              <button
                type="button"
                onClick={showNext}
                aria-label={copy.next}
                className="absolute right-3 z-10 rounded-full border border-border bg-card/90 p-3 text-text shadow-strong transition-colors hover:border-accent hover:text-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent sm:right-6"
              >
                <ArrowIcon direction="right" />
              </button>
            )}
          </div>

          <footer className="shrink-0 border-t border-border px-4 py-3 text-center text-xs text-muted">
            {copy.hint}
          </footer>
        </div>
      )}
    </>
  )
}
