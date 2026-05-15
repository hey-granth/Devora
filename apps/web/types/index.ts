// Core API types for Devora frontend

export interface ApiError {
  error: string;
  code: string;
  details?: Record<string, unknown>;
}

export interface User {
  id: string;
  org_id: string;
  email: string;
  role: 'owner' | 'admin' | 'member';
  created_at: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  plan: 'free' | 'growth' | 'enterprise';
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  user: User;
}
