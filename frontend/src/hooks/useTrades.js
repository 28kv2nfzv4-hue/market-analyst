import { useCallback, useEffect, useState } from 'react'
import { fetchTrades } from '../api/trades'

export function useTrades() {
  const [trades, setTrades] = useState([])
  const [status, setStatus] = useState('loading') // 'loading' | 'error' | 'ready'
  const [error, setError] = useState(null)

  const reload = useCallback(async () => {
    setStatus((current) => (current === 'ready' ? 'ready' : 'loading'))
    try {
      const data = await fetchTrades()
      setTrades(data)
      setStatus('ready')
      setError(null)
    } catch (err) {
      setError(err.message)
      setStatus('error')
    }
  }, [])

  useEffect(() => {
    reload()
  }, [reload])

  return { trades, status, error, reload }
}
