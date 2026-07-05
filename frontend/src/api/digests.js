const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export async function fetchDigests() {
  const response = await fetch(`${API_URL}/digests`)

  if (!response.ok) {
    throw new Error(`Failed to load digests (status ${response.status})`)
  }

  return response.json()
}
