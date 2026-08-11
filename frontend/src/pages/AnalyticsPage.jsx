import { useEffect, useState } from 'react'
import axios from 'axios'
import { getAnalyticsSummary } from '../lib/api/analytics'
import { APP_ROUTES, getBackendUrl } from '../lib/config/routes'

const PERIODS = {
  daily: { label: 'Diarias', empty: 'No hay visitas registradas en los últimos 30 días.' },
  weekly: { label: 'Semanales', empty: 'No hay visitas registradas en las últimas 12 semanas.' },
  monthly: { label: 'Mensuales', empty: 'No hay visitas registradas en los últimos 12 meses.' },
}

function formatLabel(period, label) {
  if (period === 'daily') {
    return new Intl.DateTimeFormat('es-ES', { day: '2-digit', month: 'short' }).format(new Date(`${label}T12:00:00`))
  }
  if (period === 'monthly') {
    return new Intl.DateTimeFormat('es-ES', { month: 'short', year: '2-digit' }).format(new Date(`${label}-01T12:00:00`))
  }
  const [start] = label.split(' / ')
  return `Sem. ${new Intl.DateTimeFormat('es-ES', { day: '2-digit', month: 'short' }).format(new Date(`${start}T12:00:00`))}`
}

function StatCard({ label, value, detail }) {
  return (
    <article className="rounded-xl border border-border bg-card p-5 shadow-soft">
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">{label}</p>
      <p className="mt-3 text-4xl font-bold text-text">{value.toLocaleString('es-ES')}</p>
      <p className="mt-2 text-sm text-subtle">{detail}</p>
    </article>
  )
}

function VisitChart({ period, rows }) {
  const maxVisits = Math.max(...rows.map((row) => row.visits), 1)
  const hasVisits = rows.some((row) => row.visits > 0)

  return (
    <section className="rounded-xl border border-border bg-card p-5 shadow-soft sm:p-7">
      <div className="flex items-end justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-accent">Evolución</p>
          <h2 className="mt-2 text-xl font-semibold text-text">Visitas {PERIODS[period].label.toLowerCase()}</h2>
        </div>
        <p className="text-sm text-muted">Máximo: {maxVisits === 1 && !hasVisits ? 0 : maxVisits}</p>
      </div>

      {!hasVisits ? (
        <div className="mt-8 rounded-lg border border-dashed border-border px-5 py-14 text-center text-sm text-muted">
          {PERIODS[period].empty}
        </div>
      ) : (
        <div className="mt-8 overflow-x-auto pb-3">
          <div className="flex h-72 min-w-max items-end gap-2 border-b border-border px-1">
            {rows.map((row) => (
              <div key={row.label} className="group flex w-12 flex-col items-center justify-end gap-2 sm:w-14">
                <span className="text-xs font-semibold text-text opacity-0 transition-opacity group-hover:opacity-100">
                  {row.visits}
                </span>
                <div
                  className="w-full min-h-1 rounded-t-md bg-accent/80 transition-colors group-hover:bg-accent"
                  style={{ height: `${Math.max((row.visits / maxVisits) * 210, row.visits ? 4 : 0)}px` }}
                  title={`${formatLabel(period, row.label)}: ${row.visits} visitas`}
                />
                <span className="h-8 text-center text-[10px] leading-tight text-subtle">
                  {formatLabel(period, row.label)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  )
}

function requestSummary(setSummary, setStatus) {
  setStatus('loading')
  getAnalyticsSummary()
    .then((data) => {
      setSummary(data)
      setStatus('ready')
    })
    .catch((error) => {
      if (axios.isAxiosError(error) && (error.response?.status === 401 || error.response?.status === 403)) {
        setStatus('forbidden')
        return
      }
      setStatus('error')
    })
}

export function AnalyticsPage() {
  const [summary, setSummary] = useState(null)
  const [period, setPeriod] = useState('daily')
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    requestSummary(setSummary, setStatus)
  }, [])

  const loadSummary = () => requestSummary(setSummary, setStatus)

  const loginUrl = getBackendUrl(`/admin/login/?next=${encodeURIComponent(APP_ROUTES.analytics)}`)

  if (status === 'loading') {
    return <div className="site-container flex min-h-[70vh] items-center justify-center pt-24 text-muted">Cargando analítica…</div>
  }

  if (status === 'forbidden') {
    return (
      <div className="site-container flex min-h-[75vh] items-center justify-center pt-24">
        <section className="max-w-lg rounded-xl border border-border bg-card p-8 text-center shadow-strong">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Acceso privado</p>
          <h1 className="mt-3 text-3xl font-bold text-text">Panel protegido</h1>
          <p className="mt-4 leading-7 text-muted">Esta ruta requiere una sesión activa de superusuario de Django.</p>
          <a href={loginUrl} className="mt-7 inline-flex rounded-md border border-accent bg-accent px-5 py-2.5 text-sm font-semibold text-bg transition-colors hover:bg-accent-hover">
            Iniciar sesión
          </a>
        </section>
      </div>
    )
  }

  if (status === 'error' || !summary) {
    return (
      <div className="site-container flex min-h-[75vh] items-center justify-center pt-24">
        <section className="max-w-lg rounded-xl border border-border bg-card p-8 text-center">
          <h1 className="text-2xl font-bold text-text">No se pudo cargar la analítica</h1>
          <p className="mt-3 text-muted">Revisá el backend o intentá nuevamente.</p>
          <button type="button" onClick={loadSummary} className="mt-6 rounded-md border border-accent/60 px-5 py-2.5 text-sm font-semibold text-accent hover:bg-accent-soft">
            Reintentar
          </button>
        </section>
      </div>
    )
  }

  return (
    <div className="site-container pb-20 pt-28">
      <header className="flex flex-col gap-5 border-b border-border pb-8 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Analítica privada</p>
          <h1 className="mt-3 text-3xl font-bold text-text sm:text-4xl">Visitas del portfolio</h1>
          <p className="mt-3 max-w-2xl text-muted">Resumen agregado sin almacenar direcciones IP ni información personal de los visitantes.</p>
        </div>
        <button type="button" onClick={loadSummary} className="self-start rounded-md border border-border px-4 py-2 text-sm font-medium text-muted transition-colors hover:border-accent/60 hover:text-text sm:self-auto">
          Actualizar
        </button>
      </header>

      <section className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Hoy" value={summary.today} detail="Desde las 00:00" />
        <StatCard label="Semana" value={summary.current_week} detail="Desde el lunes" />
        <StatCard label="Mes" value={summary.current_month} detail="Mes natural actual" />
        <StatCard label="Histórico" value={summary.all_time} detail="Desde el primer registro" />
      </section>

      <div className="mt-10 flex w-fit rounded-lg border border-border bg-surface p-1">
        {Object.entries(PERIODS).map(([key, item]) => (
          <button
            key={key}
            type="button"
            onClick={() => setPeriod(key)}
            className={`rounded-md px-4 py-2 text-sm font-semibold transition-colors ${period === key ? 'bg-accent text-bg' : 'text-muted hover:text-text'}`}
          >
            {item.label}
          </button>
        ))}
      </div>

      <div className="mt-5">
        <VisitChart period={period} rows={summary[period]} />
      </div>
    </div>
  )
}
