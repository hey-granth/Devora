'use client';

import { SWRConfig } from 'swr';
import { ReactNode } from 'react';
import { apiClient } from '@/lib/api';

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <SWRConfig
      value={{
        fetcher: (url: string) => apiClient.get(url).json(),
        revalidateOnFocus: false,
        revalidateOnReconnect: true,
        shouldRetryOnError: false,
        dedupingInterval: 5000,
      }}
    >
      {children}
    </SWRConfig>
  );
}
