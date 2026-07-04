import { useTrades } from '../hooks/useTrades'
import Header from '../components/Header'
import TradesTable from '../components/TradesTable'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

export default function Trades() {
  const { trades, status, error, reload } = useTrades()

  return (
    <>
      <Header
        title="Trades"
        subtitle={`${trades.length} logged trade${trades.length === 1 ? '' : 's'}`}
        onRefresh={reload}
        refreshing={status === 'loading' && trades.length > 0}
      />

      <main className="flex flex-1 flex-col gap-6 p-6">
        {status === 'loading' && trades.length === 0 && <LoadingState />}

        {status === 'error' && (
          <ErrorState message={`Couldn't reach the API — ${error}`} onRetry={reload} />
        )}

        {status === 'ready' && <TradesTable trades={trades} />}
      </main>
    </>
  )
}
