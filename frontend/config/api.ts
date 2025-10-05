export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';

export const endpoints = {
  auth: {
    login: '/auth/login',
    register: '/auth/register/password',
    refresh: '/auth/refresh',
    snapshot: '/auth/snapshot'
  },
  users: {
    me: '/users/me'
  },
  posts: '/posts'
} as const;
