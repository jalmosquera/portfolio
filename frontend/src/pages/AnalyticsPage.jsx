import { useEffect, useState } from 'react'
import axios from 'axios'

import { AnalyticsBarChart } from '../components/analytics/AnalyticsBarChart'
import { AnalyticsDonutChart } from '../components/analytics/AnalyticsDonutChart'
import { AnalyticsKpiCard } from '../components/analytics/AnalyticsKpiCard'
import { AnalyticsLineChart } from '../components/analytics/AnalyticsLineChart'
import { AnalyticsSection } from '../components/analytics/AnalyticsSection'
import { getAnalyticsSummary } from '../lib/api/analytics'
import { APP_ROUTES, getBackendUrl } from '../lib/config/routes'

const PERIODS = { daily: 'Diarias', weekly: 'Semanales', monthly: 'Mensuales' }

function formatNumber(value, maximumFractionDigits = 0) {
  return Number(value || 0).toLocaleString('es-ES', { maximumFractionDigits })
}

function formatDuration(seconds) {
  const minutes = Math.floor(seconds / 60)
  const remainder = seconds % 60
  return minutes ? `${minutes}m ${remainder}s` : `${remainder}s`
}

function formatLabel(period, label) {
  if (period === 'daily') return new Intl.DateTimeFormat('es-ES', { day: '2-digit', month: 'short' }).format(new Date(`${label}T12:00:00`))
  if (period === 'monthly') return new Intl.DateTimeFormat('es-ES', { month: 'short', year: '2-digit' }).format(new Date(`${label}-01T12:00:00`))
  const [start] = label.split(' / ')
  return `Sem. ${new Intl.DateTimeFormat('es-ES', { day: '2-digit', month: 'short' }).format(new Date(`${start}T12:00:00`))}`
}

function requestSummary(setSummary, setStatus) {
  setStatus('loading')
  getAnalyticsSummary()
    .then((data) => { setSummary(data); setStatus('ready') })
    .catch((error) => {
      if (axios.isAxiosError(error) && [401, 403].includes(error.response?.status)) setStatus('forbidden')
      else setStatus('error')
    })
}

export function AnalyticsPage() {
  const [summary, setSummary] = useState(null)
  const [period, setPeriod] = useState('daily')
  const [status, setStatus] = useState('loading')

  useEffect(() => { requestSummary(setSummary, setStatus) }, [])
  const loadSummary = () => requestSummary(setSummary, setStatus)
  const loginUrl = getBackendUrl(`/admin/login/?next=${encodeURIComponent(APP_ROUTES.analytics)}`)

  if (status === 'loading') return <div className="site-container flex min-h-[70vh] items-center justify-center pt-24 text-muted">Cargando analítica…</div>
  if (status === 'forbidden') return (
    <div className="site-container flex min-h-[75vh] items-center justify-center pt-24">
      <section className="max-w-lg rounded-xl border border-border bg-card p-8 text-center shadow-strong">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Acceso privado</p>
        <h1 className="mt-3 text-3xl font-bold text-text">Panel protegido</h1>
        <p className="mt-4 leading-7 text-muted">Esta ruta requiere una sesión activa de superusuario de Django.</p>
        <a href={loginUrl} className="mt-7 inline-flex rounded-md border border-accent bg-accent px-5 py-2.5 text-sm font-semibold text-bg hover:bg-accent-hover">Iniciar sesión</a>
      </section>
    </div>
  )
  if (status === 'error' || !summary) return (
    <div className="site-container flex min-h-[75vh] items-center justify-center pt-24">
      <section className="max-w-lg rounded-xl border border-border bg-card p-8 text-center">
        <h1 className="text-2xl font-bold text-text">No se pudo cargar la analítica</h1>
        <p className="mt-3 text-muted">Revisá el backend o intentá nuevamente.</p>
        <button type="button" onClick={loadSummary} className="mt-6 rounded-md border border-accent/60 px-5 py-2.5 text-sm font-semibold text-accent hover:bg-accent-soft">Reintentar</button>
      </section>
    </div>
  )

  const kpis = [
    ['Hoy', summary.today, 'Sesiones desde las 00:00'],
    ['Semana', summary.current_week, 'Desde el lunes'],
    ['Mes', summary.current_month, 'Mes natural actual'],
    ['Histórico', summary.all_time, 'Desde el primer registro'],
    ['Visitantes únicos', summary.unique_visitors, 'Identificadores anónimos'],
    ['Sesiones', summary.sessions, 'Sesiones first-party'],
    ['Páginas vistas', summary.pageviews, 'Eventos page_view'],
    ['Páginas / sesión', formatNumber(summary.pages_per_session, 2), 'Profundidad media'],
    ['Duración media', formatDuration(summary.average_session_seconds), 'Actividad por sesión'],
    ['Rebote', `${formatNumber(summary.bounce_rate, 1)}%`, 'Una sola página vista'],
    ['Nuevos', summary.new_visitors, 'Primera sesión registrada'],
    ['Recurrentes', summary.returning_visitors, 'Visitantes que regresaron'],
  ]
  const conversions = Object.entries(summary.conversions || {}).map(([label, value]) => ({ label: label.replaceAll('_', ' '), value }))
  const sources = summary.sources.map((item) => ({ ...item, label: ({ Direct: 'Directo', Other: 'Otros' })[item.label] || item.label }))
  const devices = summary.devices.map((item) => ({ ...item, label: ({ desktop: 'Desktop', mobile: 'Mobile', tablet: 'Tablet' })[item.label] || item.label }))

  return (
    <div className="site-container pb-20 pt-28">
      <header className="flex flex-col gap-5 border-b border-border pb-8 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Analítica privada</p>
          <h1 className="mt-3 text-3xl font-bold text-text sm:text-4xl">Rendimiento del portfolio</h1>
          <p className="mt-3 max-w-2xl text-muted">Resumen agregado sin almacenar direcciones IP ni información personal de los visitantes.</p>
        </div>
        <button type="button" onClick={loadSummary} className="self-start rounded-md border border-border px-4 py-2 text-sm font-medium text-muted hover:border-accent/60 hover:text-text sm:self-auto">Actualizar</button>
      </header>

      <section className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {kpis.map(([label, value, detail]) => <AnalyticsKpiCard key={label} label={label} value={typeof value === 'number' ? formatNumber(value, 2) : value} detail={detail} />)}
      </section>

      <div className="mt-10 grid min-w-0 gap-5 xl:grid-cols-3">
        <AnalyticsSection eyebrow="Evolución" title="Sesiones y visitantes únicos" className="xl:col-span-2">
          <div className="mb-5 flex w-fit max-w-full overflow-x-auto rounded-lg border border-border bg-surface p-1">
            {Object.entries(PERIODS).map(([key, label]) => <button key={key} type="button" onClick={() => setPeriod(key)} className={`rounded-md px-4 py-2 text-sm font-semibold ${period === key ? 'bg-accent text-bg' : 'text-muted hover:text-text'}`}>{label}</button>)}
          </div>
          <AnalyticsLineChart data={summary[period]} formatLabel={(label) => formatLabel(period, label)} />
        </AnalyticsSection>
        <AnalyticsSection eyebrow="Adquisición" title="Origen del tráfico"><AnalyticsDonutChart data={sources} /></AnalyticsSection>
      </div>

      <div className="mt-5 grid min-w-0 gap-5 xl:grid-cols-3">
        <AnalyticsSection eyebrow="Audiencia" title="Dispositivos"><AnalyticsDonutChart data={devices} /></AnalyticsSection>
        <AnalyticsSection eyebrow="Contenido" title="Páginas más vistas" className="xl:col-span-2"><AnalyticsBarChart data={summary.top_pages} /></AnalyticsSection>
      </div>

      <div className="mt-5 grid min-w-0 gap-5 lg:grid-cols-2 xl:grid-cols-3">
        <AnalyticsSection title="Navegadores"><AnalyticsBarChart data={summary.browsers} /></AnalyticsSection>
        <AnalyticsSection title="Sistemas operativos"><AnalyticsBarChart data={summary.operating_systems} /></AnalyticsSection>
        <AnalyticsSection title="Países" className="lg:col-span-2 xl:col-span-1"><AnalyticsBarChart data={summary.countries} /></AnalyticsSection>
      </div>

      <div className="mt-5 grid min-w-0 gap-5 lg:grid-cols-2">
        <AnalyticsSection eyebrow="Interés" title="Proyectos más vistos"><AnalyticsBarChart data={summary.top_projects} /></AnalyticsSection>
        <AnalyticsSection eyebrow="Acciones" title="Conversiones y clicks"><AnalyticsBarChart data={conversions} /></AnalyticsSection>
      </div>
    </div>
  )
}
