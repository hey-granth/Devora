import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  org_id: string
  email: string
  role: string
  created_at: string
}

interface Organization {
  id: string
  name: string
  slug: string
  plan: string
  created_at: string
}

interface AuthState {
  // State
  user: User | null
  organization: Organization | null
  accessToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  
  // Actions
  setUser: (user: User | null) => void
  setOrganization: (org: Organization | null) => void
  login: (user: User, organization: Organization) => void
  logout: () => void
  refreshToken: () => Promise<boolean>
  setLoading: (loading: boolean) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // Initial state
      user: null,
      organization: null,
      accessToken: null,
      isAuthenticated: false,
      isLoading: false,
      
      // Actions
      setUser: (user) => set({ user }),
      setOrganization: (organization) => set({ organization }),
      login: (user, organization) =>
        set({
          user,
          organization,
          isAuthenticated: true,
          isLoading: false,
        }),
      logout: () =>
        set({
          user: null,
          organization: null,
          accessToken: null,
          isAuthenticated: false,
          isLoading: false,
        }),
      refreshToken: async () => false,
      setLoading: (isLoading) => set({ isLoading }),
    }),
    {
      name: 'devora-auth',
      partialize: (state) => ({
        user: state.user,
        organization: state.organization,
        accessToken: state.accessToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
