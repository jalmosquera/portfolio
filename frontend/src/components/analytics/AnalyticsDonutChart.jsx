import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'

const COLORS = ['var(--color-accent)', 'var(--color-muted)', 'var(--color-subtle)', 'var(--color-border-strong)', 'var(--color-surface)']

export function AnalyticsDonutChart({ data }) {
  const hasData = data.some((row) => row.value)
  if (!hasData) return <div className="flex h-60 items-center justify-center text-sm text-muted">Sin datos todavía.</div>

  return (
    <div className="grid items-center gap-3 sm:grid-cols-[1fr_auto]">
      <div className="h-52 min-w-0">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="label" innerRadius="54%" outerRadius="80%" paddingAngle={2} stroke="none">
              {data.map((row, index) => <Cell key={row.label} fill={COLORS[index % COLORS.length]} />)}
            </Pie>
            <Tooltip contentStyle={{ background: 'var(--color-card)', border: '1px solid var(--color-border)', borderRadius: 8 }} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <ul className="space-y-2 text-xs text-muted">
        {data.map((row, index) => (
          <li key={row.label} className="flex items-center justify-between gap-5">
            <span className="flex items-center gap-2"><span className="size-2 rounded-full" style={{ background: COLORS[index % COLORS.length] }} />{row.label}</span>
            <strong className="text-text">{row.value}</strong>
          </li>
        ))}
      </ul>
    </div>
  )
}
