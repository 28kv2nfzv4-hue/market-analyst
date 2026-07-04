import { useTrades } from '../hooks/useTrades'
import Header from '../components/Header'
import SummaryCards from '../components/SummaryCards'
import TradesTable from '../components/TradesTable'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

export default function Dashboard() {
  const { trades, status, error, reload } = useTrades()

  return (
    <>
      <Header
        title="Trading Dashboard"
        subtitle="Live view of every logged trade"
        onRefresh={reload}
        refreshing={status === 'loading' && trades.length > 0}
      />

      <main className="flex flex-1 flex-col gap-6 p-6">
        {status === 'loading' && trades.length === 0 && <LoadingState />}

        {status === 'error' && (
          <ErrorState message={`Couldn't reach the API — ${error}`} onRetry={reload} />
        )}

        {status === 'ready' && (
          <>
            <SummaryCards trades={trades} />
            <TradesTable trades={trades} />
          </>
        )}
      </main>
    </>
  )
}
