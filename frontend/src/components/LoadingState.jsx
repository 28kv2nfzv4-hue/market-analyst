import { Loader2 } from 'lucide-react'

export default function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-xl border border-slate-800 bg-slate-900/60 p-12 text-slate-400">
      <Loader2 className="h-6 w-6 animate-spin" />
      <p className="text-sm">Loading trades…</p>
    </div>
  )
}
