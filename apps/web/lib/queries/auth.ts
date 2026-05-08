import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { authApi, orgApi, setTokens, clearTokens } from '../api'
import { useAuthStore } from '../../stores/auth'

export function useLogin() {
  const queryClient = useQueryClient()
  const login = useAuthStore((state) => state.login)

  return useMutation({
    mutationFn: authApi.login,
    onSuccess: async (data, variables) => {
      // Store tokens
      setTokens(data.access_token, data.refresh_token)
      
      // Fetch user and org data
      const [userResponse, orgResponse] = await Promise.all([
        fetch('/api/v1/users/me', {
          headers: { Authorization: `Bearer ${data.access_token}` },
        }).then((res) => res.json()),
        fetch('/api/v1/orgs/me', {
          headers: { Authorization: `Bearer ${data.access_token}` },
        }).then((res) => res.json()),
      ])
      
      // Update store
      login(userResponse, orgResponse)
      
      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ['user'] })
      queryClient.invalidateQueries({ queryKey: ['organization'] })
    },
    onError: (error) => {
      clearTokens()
    },
  })
}

export function useRegister() {
  const queryClient = useQueryClient()
  const login = useAuthStore((state) => state.login)

  return useMutation({
    mutationFn: authApi.register,
    onSuccess: async (data, variables) => {
      // Store tokens
      setTokens(data.access_token, data.refresh_token)
      
      // Fetch user and org data
      const [userResponse, orgResponse] = await Promise.all([
        fetch('/api/v1/users/me', {
          headers: { Authorization: `Bearer ${data.access_token}` },
        }).then((res) => res.json()),
        fetch('/api/v1/orgs/me', {
          headers: { Authorization: `Bearer ${data.access_token}` },
        }).then((res) => res.json()),
      ])
      
      // Update store
      login(userResponse, orgResponse)
      
      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ['user'] })
      queryClient.invalidateQueries({ queryKey: ['organization'] })
    },
    onError: (error) => {
      clearTokens()
    },
  })
}

export function useLogout() {
  const queryClient = useQueryClient()
  const logout = useAuthStore((state) => state.logout)
  const refreshToken = useAuthStore((state) => state.refreshToken)

  return useMutation({
    mutationFn: () => {
      if (refreshToken) {
        return authApi.logout(refreshToken)
      }
      return Promise.resolve()
    },
    onSuccess: () => {
      // Clear tokens and store
      clearTokens()
      logout()
      
      // Clear all queries
      queryClient.clear()
    },
  })
}

export function useCurrentUser() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  
  return useQuery({
    queryKey: ['user'],
    queryFn: authApi.getCurrent,
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useCurrentOrganization() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  
  return useQuery({
    queryKey: ['organization'],
    queryFn: orgApi.getCurrent,
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}
