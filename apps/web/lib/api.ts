import ky, { HTTPError } from 'ky'
import { z } from 'zod'

// API base URL from environment
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

// Error response schema
const ErrorResponseSchema = z.object({
  error: z.string(),
  code: z.string(),
  details: z.record(z.any()).optional(),
})

export type ErrorResponse = z.infer<typeof ErrorResponseSchema>

// Create ky instance with default configuration
export const api = ky.create({
  prefixUrl: API_URL,
  hooks: {
    beforeRequest: [
      (request) => {
        // Add auth header if token exists
        const token = getAccessToken()
        if (token) {
          request.headers.set('Authorization', `Bearer ${token}`)
        }
      },
    ],
    afterResponse: [
      async (request, options, response) => {
        // Handle 401 errors - try to refresh token
        if (response.status === 401) {
          try {
            const newToken = await refreshAccessToken()
            if (newToken) {
              // Retry the original request with new token
              request.headers.set('Authorization', `Bearer ${newToken}`)
              return ky(request)
            }
          } catch (refreshError) {
            // Refresh failed, redirect to login
            clearTokens()
            window.location.href = '/auth/login'
            return response
          }
        }
        return response
      },
    ],
  },
})

// Token management
const ACCESS_TOKEN_KEY = 'devora_access_token'
const REFRESH_TOKEN_KEY = 'devora_refresh_token'

export function getAccessToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem(ACCESS_TOKEN_KEY)
}

export function getRefreshToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem(REFRESH_TOKEN_KEY)
}

export function setTokens(accessToken: string, refreshToken: string): void {
  if (typeof window === 'undefined') return
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
}

export function clearTokens(): void {
  if (typeof window === 'undefined') return
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = getRefreshToken()
  if (!refreshToken) return null

  try {
    const response = await api
      .post('auth/refresh', {
        json: { refresh_token: refreshToken },
      })
      .json<{ access_token: string; refresh_token: string }>()

    setTokens(response.access_token, response.refresh_token)
    return response.access_token
  } catch (error) {
    return null
  }
}

// Type-safe API client methods
export const authApi = {
  register: (data: {
    org_name: string
    org_slug: string
    email: string
    password: string
  }) =>
    api.post('auth/register', { json: data }).json<{
      access_token: string
      refresh_token: string
      token_type: string
      expires_in: number
    }>(),

  login: (data: { email: string; password: string }) =>
    api.post('auth/login', { json: data }).json<{
      access_token: string
      refresh_token: string
      token_type: string
      expires_in: number
    }>(),

  refresh: (refreshToken: string) =>
    api.post('auth/refresh', { json: { refresh_token: refreshToken } }).json<{
      access_token: string
      refresh_token: string
      token_type: string
      expires_in: number
    }>(),

  logout: (refreshToken: string) =>
    api.post('auth/logout', { json: { refresh_token: refreshToken } }),
}

export const orgApi = {
  getCurrent: () =>
    api.get('orgs/me').json<{
      id: string
      name: string
      slug: string
      plan: string
      created_at: string
    }>(),

  update: (data: { name?: string; slug?: string }) =>
    api.patch('orgs/me', { json: data }).json<{
      id: string
      name: string
      slug: string
      plan: string
      created_at: string
    }>(),

  rotateApiKey: () =>
    api.post('orgs/me/rotate-key').json<{ api_key: string }>(),
}

export const userApi = {
  getCurrent: () =>
    api.get('users/me').json<{
      id: string
      org_id: string
      email: string
      role: string
      created_at: string
    }>(),

  list: (params?: { limit?: number; cursor?: string }) =>
    api.get('users', { searchParams: params }).json<
      Array<{
        id: string
        org_id: string
        email: string
        role: string
        created_at: string
      }>
    >(),

  invite: (data: { email: string; password: string; role?: string }) =>
    api.post('users/invite', { json: data }).json<{
      id: string
      org_id: string
      email: string
      role: string
      created_at: string
    }>(),

  remove: (userId: string) => api.delete(`users/${userId}`),
}
