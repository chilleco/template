'use client';

import { Provider } from 'react-redux';
import { ReactNode, useMemo } from 'react';

import { makeStore } from '@/store';

interface Props {
  children: ReactNode;
}

export function ReduxProvider({ children }: Props) {
  const store = useMemo(() => makeStore(), []);
  return <Provider store={store}>{children}</Provider>;
}
