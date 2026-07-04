import Header from '../components/Header'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export default function Settings() {
  return (
    <>
      <Header title="Settings" subtitle="Dashboard configuration" />

      <main className="flex flex-1 flex-col gap-6 p-6">
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="text-sm font-medium text-slate-200">API connection</h2>
          <p className="mt-1 text-sm text-slate-400">
            Trades are read from{' '}
            <code className="rounded bg-slate-800 px-1.5 py-0.5 text-slate-200">{API_URL}</code>.
            Set <code className="rounded bg-slate-800 px-1.5 py-0.5 text-slate-200">VITE_API_URL</code>{' '}
            in <code className="rounded bg-slate-800 px-1.5 py-0.5 text-slate-200">frontend/.env</code>{' '}
            to point at a different backend.
          </p>
        </div>
      </main>
    </>
  )
}
