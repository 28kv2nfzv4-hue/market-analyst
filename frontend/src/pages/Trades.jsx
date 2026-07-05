import { useState } from 'react'
import { useTrades } from '../hooks/useTrades'
import Header from '../components/Header'
import TradesTable from '../components/TradesTable'
import TradeForm from '../components/TradeForm'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

export default function Trades() {
  const { trades, status, error, reload, addTrade, editTrade, removeTrade } = useTrades()
  const [formMode, setFormMode] = useState(null) // null | 'create' | trade object being edited
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(payload) {
    setSubmitting(true)
    try {
      if (formMode && formMode !== 'create') {
        await editTrade(formMode.id, payload)
      } else {
        await addTrade(payload)
      }
      setFormMode(null)
    } finally {
      setSubmitting(false)
    }
  }

  async function handleDelete(trade) {
    if (!window.confirm(`Delete ${trade.pair} trade?`)) return
    await removeTrade(trade.id)
  }

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

        {status === 'ready' && (
          <>
            {formMode ? (
              <TradeForm
                initialValues={formMode === 'create' ? null : formMode}
                onSubmit={handleSubmit}
                onCancel={() => setFormMode(null)}
                submitting={submitting}
              />
            ) : (
              <div>
                <button
                  type="button"
                  onClick={() => setFormMode('create')}
                  className="rounded-lg bg-sky-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-sky-400"
                >
                  Add trade
                </button>
              </div>
            )}

            <TradesTable trades={trades} onEdit={setFormMode} onDelete={handleDelete} />
          </>
        )}
      </main>
    </>
  )
}
