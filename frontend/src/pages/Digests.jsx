import { useDigests } from '../hooks/useDigests'
import Header from '../components/Header'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

export default function Digests() {
  const { digests, status, error, reload } = useDigests()

  return (
    <>
      <Header
        title="Market Briefings"
        subtitle={`${digests.length} saved digest${digests.length === 1 ? '' : 's'}`}
        onRefresh={reload}
        refreshing={status === 'loading' && digests.length > 0}
      />

      <main className="flex flex-1 flex-col gap-4 p-6">
        {status === 'loading' && digests.length === 0 && <LoadingState />}

        {status === 'error' && (
          <ErrorState message={`Couldn't reach the API — ${error}`} onRetry={reload} />
        )}

        {status === 'ready' && digests.length === 0 && (
          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-8 text-center text-sm text-slate-400">
            No digests sent yet.
          </div>
        )}

        {status === 'ready' &&
          digests.map((digest) => (
            <article key={digest.id} className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
              <time className="text-xs uppercase tracking-wide text-slate-500">
                {new Date(digest.created_at).toLocaleString()}
              </time>
              <p className="mt-2 whitespace-pre-line text-sm text-slate-200">{digest.content}</p>
            </article>
          ))}
      </main>
    </>
  )
}
