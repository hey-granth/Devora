import ky, { type KyInstance } from 'ky';
import { useAuthStore } from '@/stores/auth';

function createApiClient(): KyInstance {
  return ky.create({
    prefixUrl: process.env.NEXT_PUBLIC_API_URL,
    hooks: {
      beforeRequest: [
        (request) => {
          const token = useAuthStore.getState().accessToken;
          if (token) {
            request.headers.set('Authorization', `Bearer ${token}`);
          }
        },
      ],
      afterResponse: [
        async (request, options, response) => {
          if (response.status === 401) {
            const refreshed = await useAuthStore.getState().refreshToken();
            if (refreshed) {
              // Retry with new token
              const token = useAuthStore.getState().accessToken;
              request.headers.set('Authorization', `Bearer ${token}`);
              return ky(request);
            }
            useAuthStore.getState().logout();
          }
          return response;
        },
      ],
    },
  });
}

export const apiClient = createApiClient();
