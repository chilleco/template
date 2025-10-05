import { endpoints } from '@/config/api';
import { apiClient } from '@/lib/api-client';
import type { User } from '@/lib/schemas/user';

export async function fetchSession(): Promise<User> {
  const response = await apiClient.get(endpoints.users.me);
  return response.data;
}

export async function login(payload: { identifier: string; password: string }) {
  const response = await apiClient.post(endpoints.auth.login, payload);
  return response.data as { access_token: string; refresh_token: string };
}
