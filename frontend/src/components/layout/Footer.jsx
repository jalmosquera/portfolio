import logoMark from '../../assets/logo-mark.jpeg'

export function Footer() {
  return (
    <footer className="border-t border-border py-6">
      <div className="site-container flex items-center justify-center">
        <div className="flex items-center gap-2">
          <img
            src={logoMark}
            alt=""
            className="h-8 w-8 rounded object-cover ring-1 ring-accent/40"
          />
          <span className="text-sm font-semibold text-text">Jalberth<span className="text-accent"> Mosquera</span></span>
        </div>
      </div>
    </footer>
  )
}
