export interface ApiClientOptions {
  baseUrl?: string;
  getAccessToken?: () => string | null;
  getPreAuthToken?: () => string | null;
}

export class ApiClient {
  private baseUrl: string;
  private getAccessToken?: () => string | null;
  private getPreAuthToken?: () => string | null;

  constructor(options: ApiClientOptions = {}) {
    this.baseUrl = options.baseUrl ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
    this.getAccessToken = options.getAccessToken;
    this.getPreAuthToken = options.getPreAuthToken;
  }

  async post<T>(path: string, body?: unknown): Promise<T> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json"
    };
    const accessToken = this.getAccessToken?.();
    if (accessToken) {
      headers.Authorization = `Bearer ${accessToken}`;
    }
    const preAuth = this.getPreAuthToken?.();
    if (preAuth) {
      headers["X-Pre-Auth-Token"] = preAuth;
    }

    const response = await fetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers,
      body: body ? JSON.stringify(body) : undefined
    });

    if (!response.ok) {
      throw new Error(`API error ${response.status}`);
    }
    return (await response.json()) as T;
  }
}
