import { NavLink } from 'react-router-dom'
import { LayoutDashboard, LineChart, MessageCircle, Newspaper, Settings, TrendingUp } from 'lucide-react'

const NAV_ITEMS = [
  { label: 'Dashboard', icon: LayoutDashboard, to: '/', end: true },
  { label: 'Trades', icon: LineChart, to: '/trades' },
  { label: 'Digests', icon: Newspaper, to: '/digests' },
  { label: 'Settings', icon: Settings, to: '/settings' },
]

const TELEGRAM_BOT_USERNAME = import.meta.env.VITE_TELEGRAM_BOT_USERNAME

export default function Sidebar() {
  return (
    <aside className="hidden w-60 shrink-0 flex-col border-r border-slate-800 bg-slate-900/60 p-4 md:flex">
      <div className="mb-8 flex items-center gap-2 px-2">
        <TrendingUp className="h-6 w-6 text-emerald-400" />
        <span className="text-lg font-semibold text-slate-100">Atlas</span>
      </div>

      <nav className="flex flex-col gap-1">
        {NAV_ITEMS.map(({ label, icon: Icon, to, end }) => (
          <NavLink
            key={label}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-emerald-500/10 text-emerald-400'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`
            }
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}
      </nav>

      {TELEGRAM_BOT_USERNAME && (
        <a
          href={`https://t.me/${TELEGRAM_BOT_USERNAME}`}
          target="_blank"
          rel="noreferrer"
          className="mt-auto flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-200"
        >
          <MessageCircle className="h-4 w-4" />
          Chat on Telegram
        </a>
      )}
    </aside>
  )
}
