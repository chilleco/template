'use client';

import { useMutation, useQuery } from '@tanstack/react-query';
import { useAppDispatch } from './use-redux';
import { apiClient } from '@/lib/api-client';
import { endpoints } from '@/config/api';
import { clearSession, setTokens, setUser } from '@/store/sessionSlice';
import { getSessionToken } from '@/store/sessionSlice';

export function useAuth() {
  const dispatch = useAppDispatch();

  const token = getSessionToken();

  const { data: profile } = useQuery({
    queryKey: ['session', 'me'],
    queryFn: async () => {
      const response = await apiClient.get(endpoints.users.me);
      dispatch(setUser(response.data));
      return response.data;
    },
    retry: 1,
    enabled: Boolean(token)
  });

  const login = useMutation({
    mutationFn: async (payload: { identifier: string; password: string }) => {
      const response = await apiClient.post(endpoints.auth.login, payload);
      dispatch(setTokens(response.data));
      return response.data;
    }
  });

  const logout = () => {
    dispatch(clearSession());
  };

  return { profile, login, logout };
}
