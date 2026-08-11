import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

export function AnalyticsBarChart({ data, height = 260 }) {
  const hasData = data.some((row) => row.value)
  if (!hasData) return <div className="flex h-60 items-center justify-center text-sm text-muted">Sin datos todavía.</div>

  return (
    <div className="w-full" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ top: 0, right: 12, bottom: 0, left: 8 }}>
          <CartesianGrid stroke="var(--color-border)" strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" allowDecimals={false} stroke="var(--color-subtle)" tick={{ fontSize: 11 }} />
          <YAxis type="category" dataKey="label" width={96} stroke="var(--color-subtle)" tick={{ fontSize: 11 }} tickFormatter={(value) => value.length > 16 ? `${value.slice(0, 15)}…` : value} />
          <Tooltip contentStyle={{ background: 'var(--color-card)', border: '1px solid var(--color-border)', borderRadius: 8 }} />
          <Bar dataKey="value" name="Total" fill="var(--color-accent)" radius={[0, 4, 4, 0]} maxBarSize={24} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
