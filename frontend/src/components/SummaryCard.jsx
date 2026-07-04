export default function SummaryCard({ label, value, icon: Icon, accent }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-400">{label}</span>
        <span className={`rounded-lg p-2 ${accent.bg}`}>
          <Icon className={`h-4 w-4 ${accent.text}`} />
        </span>
      </div>
      <p className="mt-3 text-2xl font-semibold text-slate-100">{value}</p>
    </div>
  )
}
