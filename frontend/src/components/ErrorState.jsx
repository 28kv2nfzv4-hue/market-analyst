import { AlertTriangle } from 'lucide-react'

export default function ErrorState({ message, onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-xl border border-rose-900/50 bg-rose-950/20 p-12 text-center">
      <AlertTriangle className="h-6 w-6 text-rose-400" />
      <p className="text-sm text-rose-300">{message}</p>
      <button
        type="button"
        onClick={onRetry}
        className="rounded-lg border border-rose-800 px-3 py-1.5 text-sm font-medium text-rose-300 transition-colors hover:bg-rose-900/40"
      >
        Try again
      </button>
    </div>
  )
}
