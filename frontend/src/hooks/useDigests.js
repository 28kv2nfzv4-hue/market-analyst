import { fetchDigests } from '../api/digests'
import { useApiResource } from './useApiResource'

export function useDigests() {
  const { data: digests, status, error, reload } = useApiResource(fetchDigests)
  return { digests, status, error, reload }
}
