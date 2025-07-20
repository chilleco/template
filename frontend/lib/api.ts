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

// Simple API object for testing (to prevent build hangs)
export const api = {
  GET: (endpoint: string, options?: any) => {
    // Simple path replacement for testing
    let url = endpoint.replace('{user_id}', options?.params?.path?.user_id || 'test');
    return apiRequest(url, { method: 'GET' });
  },
  POST: (endpoint: string, options?: any) => {
    let url = endpoint.replace('{user_id}', options?.params?.path?.user_id || 'test');
    return apiRequest(url, { method: 'POST', body: options?.body ? JSON.stringify(options.body) : undefined });
  },
  PUT: (endpoint: string, options?: any) => {
    let url = endpoint.replace('{user_id}', options?.params?.path?.user_id || 'test');
    return apiRequest(url, { method: 'PUT', body: options?.body ? JSON.stringify(options.body) : undefined });
  },
  DELETE: (endpoint: string, options?: any) => {
    let url = endpoint.replace('{user_id}', options?.params?.path?.user_id || 'test');
    return apiRequest(url, { method: 'DELETE' });
  },
}; 