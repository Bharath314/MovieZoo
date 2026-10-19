import { createFetch } from '@vueuse/core'
import { useAuthStore } from './stores/auth'

export const API_URL = import.meta.env.VITE_API_URL ?? '/api/v1'

export const useApi = createFetch({
  baseUrl: API_URL,
  options: {
    async beforeFetch({ options }) {
      const authStore = useAuthStore();
      const token = authStore.access_token;
      if (token) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token}`,
        }
      }
      return { options }
    }
  }
})
