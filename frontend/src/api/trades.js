const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export async function fetchTrades() {
  const response = await fetch(`${API_URL}/trades`)

  if (!response.ok) {
    throw new Error(`Failed to load trades (status ${response.status})`)
  }

  return response.json()
}

export async function createTrade(payload) {
  const response = await fetch(`${API_URL}/trades`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(`Failed to create trade (status ${response.status})`)
  }

  return response.json()
}

export async function updateTrade(id, payload) {
  const response = await fetch(`${API_URL}/trades/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(`Failed to update trade (status ${response.status})`)
  }

  return response.json()
}

export async function deleteTrade(id) {
  const response = await fetch(`${API_URL}/trades/${id}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    throw new Error(`Failed to delete trade (status ${response.status})`)
  }

  return response.json()
}
