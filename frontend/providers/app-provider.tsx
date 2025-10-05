'use client';

import { ReactNode } from 'react';
import { Toaster } from 'sonner';

import { QueryProvider } from './query-provider';
import { ReduxProvider } from './redux-provider';
import { ThemeProvider } from './theme-provider';

interface Props {
  children: ReactNode;
}

export function AppProvider({ children }: Props) {
  return (
    <ReduxProvider>
      <QueryProvider>
        <ThemeProvider>
          {children}
          <Toaster richColors closeButton position="top-right" />
        </ThemeProvider>
      </QueryProvider>
    </ReduxProvider>
  );
}
