import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

const tooltipStyle = { background: 'var(--color-card)', border: '1px solid var(--color-border)', borderRadius: 8 }

export function AnalyticsLineChart({ data, formatLabel }) {
  const hasData = data.some((row) => row.visits || row.unique_visitors)
  if (!hasData) return <div className="flex h-72 items-center justify-center rounded-lg border border-dashed border-border px-5 text-center text-sm text-muted">Todavía no hay datos suficientes para este período.</div>

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 8, right: 8, left: -24, bottom: 8 }}>
          <CartesianGrid stroke="var(--color-border)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="label" tickFormatter={formatLabel} stroke="var(--color-subtle)" tick={{ fontSize: 11 }} minTickGap={28} />
          <YAxis allowDecimals={false} stroke="var(--color-subtle)" tick={{ fontSize: 11 }} />
          <Tooltip contentStyle={tooltipStyle} labelFormatter={formatLabel} />
          <Line type="monotone" dataKey="visits" name="Sesiones" stroke="var(--color-accent)" strokeWidth={2.5} dot={false} activeDot={{ r: 4 }} />
          <Line type="monotone" dataKey="unique_visitors" name="Visitantes únicos" stroke="var(--color-muted)" strokeWidth={2} strokeDasharray="5 4" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
