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

// Helper function to replace path parameters
function replacePath(endpoint: string, params?: any): string {
  if (!params?.path) return endpoint;
  
  let result = endpoint;
  for (const [key, value] of Object.entries(params.path)) {
    result = result.replace(`{${key}}`, String(value));
  }
  return result;
}

// Main API object that applications expect
export const api = {
  GET: (endpoint: string, options?: { params?: { path?: Record<string, any> } }) => {
    const url = replacePath(endpoint, options?.params);
    return apiRequest(url, { method: 'GET' });
  },
  POST: (endpoint: string, options?: { params?: { path?: Record<string, any> }; body?: any }) => {
    const url = replacePath(endpoint, options?.params);
    return apiRequest(url, {
      method: 'POST',
      body: options?.body ? JSON.stringify(options.body) : undefined,
    });
  },
  PUT: (endpoint: string, options?: { params?: { path?: Record<string, any> }; body?: any }) => {
    const url = replacePath(endpoint, options?.params);
    return apiRequest(url, {
      method: 'PUT', 
      body: options?.body ? JSON.stringify(options.body) : undefined,
    });
  },
  DELETE: (endpoint: string, options?: { params?: { path?: Record<string, any> } }) => {
    const url = replacePath(endpoint, options?.params);
    return apiRequest(url, { method: 'DELETE' });
  },
}; 