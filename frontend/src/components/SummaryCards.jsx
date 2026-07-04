import { CheckCircle2, Clock, ListChecks, XCircle } from 'lucide-react'
import SummaryCard from './SummaryCard'

export default function SummaryCards({ trades }) {
  const total = trades.length
  const wins = trades.filter((trade) => trade.result === 'win').length
  const losses = trades.filter((trade) => trade.result === 'loss').length
  const pending = trades.filter((trade) => trade.result === 'pending').length

  const cards = [
    { label: 'Total Trades', value: total, icon: ListChecks, accent: { bg: 'bg-sky-500/10', text: 'text-sky-400' } },
    { label: 'Wins', value: wins, icon: CheckCircle2, accent: { bg: 'bg-emerald-500/10', text: 'text-emerald-400' } },
    { label: 'Losses', value: losses, icon: XCircle, accent: { bg: 'bg-rose-500/10', text: 'text-rose-400' } },
    { label: 'Pending', value: pending, icon: Clock, accent: { bg: 'bg-amber-500/10', text: 'text-amber-400' } },
  ]

  return (
    <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
      {cards.map((card) => (
        <SummaryCard key={card.label} {...card} />
      ))}
    </div>
  )
}
