import { useCallback, useEffect, useState } from 'react'

export function useApiResource(fetchFn) {
  const [data, setData] = useState([])
  const [status, setStatus] = useState('loading') // 'loading' | 'error' | 'ready'
  const [error, setError] = useState(null)

  const reload = useCallback(async () => {
    setStatus((current) => (current === 'ready' ? 'ready' : 'loading'))
    try {
      const result = await fetchFn()
      setData(result)
      setStatus('ready')
      setError(null)
    } catch (err) {
      setError(err.message)
      setStatus('error')
    }
  }, [fetchFn])

  useEffect(() => {
    reload()
  }, [reload])

  return { data, status, error, reload }
}
