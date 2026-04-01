export function Footer() {
  return (
    <footer className="border-t border-border py-8 mt-24">
      <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2 font-bold">
          <span className="w-6 h-6 bg-accent rounded flex items-center justify-center text-white font-black text-xs">M</span>
          <span className="text-text text-sm">MosqueraSoft</span>
        </div>
        <div className="flex items-center gap-6">
          <a href="mailto:jalberth@example.com" className="text-muted hover:text-accent text-sm transition-colors">Email</a>
          <a href="https://linkedin.com/in/jalmosquera" target="_blank" rel="noopener noreferrer" className="text-muted hover:text-accent text-sm transition-colors">LinkedIn</a>
          <a href="https://github.com/jalmosquera" target="_blank" rel="noopener noreferrer" className="text-muted hover:text-accent text-sm transition-colors">GitHub</a>
        </div>
      </div>
    </footer>
  )
}
