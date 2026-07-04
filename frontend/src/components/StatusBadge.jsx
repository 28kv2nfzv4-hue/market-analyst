const DIRECTION_STYLES = {
  buy: 'bg-emerald-500/10 text-emerald-400',
  sell: 'bg-rose-500/10 text-rose-400',
}

const RESULT_STYLES = {
  win: 'bg-emerald-500/10 text-emerald-400',
  loss: 'bg-rose-500/10 text-rose-400',
  breakeven: 'bg-sky-500/10 text-sky-400',
  pending: 'bg-amber-500/10 text-amber-400',
}

export function DirectionBadge({ direction }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium uppercase ${DIRECTION_STYLES[direction] ?? 'bg-slate-700 text-slate-300'}`}>
      {direction}
    </span>
  )
}

export function ResultBadge({ result }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium capitalize ${RESULT_STYLES[result] ?? 'bg-slate-700 text-slate-300'}`}>
      {result}
    </span>
  )
}
