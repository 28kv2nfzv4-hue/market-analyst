import { fetchTrades } from '../api/trades'
import { useApiResource } from './useApiResource'

export function useTrades() {
  const { data: trades, status, error, reload } = useApiResource(fetchTrades)
  return { trades, status, error, reload }
}
