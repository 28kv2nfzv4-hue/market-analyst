import { DirectionBadge, ResultBadge } from './StatusBadge'

const COLUMNS = ['Pair', 'Direction', 'Entry', 'Stop Loss', 'Take Profit', 'Risk %', 'Result', 'Notes']

export default function TradesTable({ trades }) {
  if (trades.length === 0) {
    return (
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-8 text-center text-sm text-slate-400">
        No trades logged yet. Trades saved via POST /trades will show up here.
      </div>
    )
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/60">
      <table className="w-full min-w-max text-left text-sm">
        <thead>
          <tr className="border-b border-slate-800 text-xs uppercase tracking-wide text-slate-500">
            {COLUMNS.map((column) => (
              <th key={column} className="px-4 py-3 font-medium">
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {trades.map((trade) => (
            <tr key={trade.id} className="border-b border-slate-800/60 last:border-0 hover:bg-slate-800/40">
              <td className="px-4 py-3 font-medium text-slate-100">{trade.pair}</td>
              <td className="px-4 py-3">
                <DirectionBadge direction={trade.direction} />
              </td>
              <td className="px-4 py-3 text-slate-300">{trade.entry_price}</td>
              <td className="px-4 py-3 text-slate-300">{trade.stop_loss}</td>
              <td className="px-4 py-3 text-slate-300">{trade.take_profit}</td>
              <td className="px-4 py-3 text-slate-300">{trade.risk_percent}%</td>
              <td className="px-4 py-3">
                <ResultBadge result={trade.result} />
              </td>
              <td className="max-w-xs truncate px-4 py-3 text-slate-400">{trade.notes || '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
