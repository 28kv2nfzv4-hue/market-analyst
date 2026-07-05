import { createTrade, deleteTrade, fetchTrades, updateTrade } from '../api/trades'
import { useApiResource } from './useApiResource'

export function useTrades() {
  const { data: trades, status, error, reload } = useApiResource(fetchTrades)

  async function addTrade(payload) {
    await createTrade(payload)
    await reload()
  }

  async function editTrade(id, payload) {
    await updateTrade(id, payload)
    await reload()
  }

  async function removeTrade(id) {
    await deleteTrade(id)
    await reload()
  }

  return { trades, status, error, reload, addTrade, editTrade, removeTrade }
}
