import useSWR from 'swr';
import useSWRMutation from 'swr/mutation';
import { apiClient } from '@/lib/api';
import type { User } from '@/types';

// Fetch current authenticated user
export function useCurrentUser() {
  return useSWR<User>('/users/me');
}

// Login mutation
async function loginFetcher(
  url: string,
  { arg }: { arg: { email: string; password: string } }
) {
  return apiClient.post(url, { json: arg }).json<{
    access_token: string;
    refresh_token: string;
    user: User;
  }>();
}

export function useLogin() {
  return useSWRMutation('/auth/login', loginFetcher);
}

// Register mutation
async function registerFetcher(
  url: string,
  { arg }: { arg: { email: string; password: string; org_name: string; org_slug: string } }
) {
  return apiClient.post(url, { json: arg }).json<{
    access_token: string;
    refresh_token: string;
    user: User;
  }>();
}

export function useRegister() {
  return useSWRMutation('/auth/register', registerFetcher);
}
