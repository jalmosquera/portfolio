export function PageLoader() {
  return (
    <div className="site-container min-h-screen pb-20 pt-28" aria-label="Loading content">
      <div className="animate-pulse space-y-6">
        <div className="h-3 w-24 rounded bg-border" />
        <div className="h-10 w-full max-w-xl rounded bg-card" />
        <div className="h-4 w-full max-w-md rounded bg-border" />
        <div className="grid grid-cols-1 gap-5 pt-8 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 min-[2200px]:grid-cols-5">
          {[0, 1, 2].map((item) => (
            <div key={item} className="overflow-hidden rounded-lg border border-border bg-card">
              <div className="h-48 bg-surface" />
              <div className="space-y-3 p-4">
                <div className="h-5 w-2/3 rounded bg-border" />
                <div className="h-3 w-full rounded bg-border" />
                <div className="h-9 w-full rounded bg-surface" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
