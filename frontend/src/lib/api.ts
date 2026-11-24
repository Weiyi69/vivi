const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/api/v1";

async function csrfToken(): Promise<string> {
  const response = await fetch(`${API_URL}/auth/csrf`, {
    credentials: "include",
  });
  if (!response.ok) throw new Error("Could not initialize the secure form");
  const data = (await response.json()) as { csrf_token: string };
  return data.csrf_token;
}

export async function apiRequest(
  path: string,
  options: RequestInit = {},
): Promise<{ status: number; data: Record<string, unknown> }> {
  const method = options.method ?? "GET";
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");

  if (!["GET", "HEAD", "OPTIONS"].includes(method.toUpperCase())) {
    headers.set("X-CSRF-Token", await csrfToken());
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
    credentials: "include",
  });
  const data = (await response.json().catch(() => ({
    message: "The server returned an invalid response",
  }))) as Record<string, unknown>;
  return { status: response.status, data };
}

export function apiMessage(data: Record<string, unknown>, fallback: string): string {
  return typeof data.detail === "string"
    ? data.detail
    : typeof data.message === "string"
      ? data.message
      : fallback;
}
