// API client configuration
export const API_BASE_URL = (typeof window !== 'undefined' ? '' : 'http://localhost:8000') || 'http://localhost:8000';

// Basic fetch wrapper
export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }

  return response.json();
}

// Auth API functions
export const auth = {
  signIn: (credentials: { email: string; password: string }) =>
    apiRequest('/auth/signin', {
      method: 'POST',
      body: JSON.stringify(credentials),
    }),
  
  signUp: (userData: { email: string; password: string; name: string }) =>
    apiRequest('/auth/signup', {
      method: 'POST', 
      body: JSON.stringify(userData),
    }),
}; 