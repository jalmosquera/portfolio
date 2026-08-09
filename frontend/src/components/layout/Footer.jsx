export function Footer() {
  return (
    <footer className="border-t border-border py-6">
      <div className="site-container flex items-center justify-center">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded bg-accent-soft text-accent ring-1 ring-accent/40">
            <span className="text-xs font-black">M.</span>
          </div>
          <span className="text-sm font-semibold text-text">Mosquera<span className="text-accent">Soft</span></span>
        </div>
      </div>
    </footer>
  )
}
