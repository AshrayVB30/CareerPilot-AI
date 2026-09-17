// Base URL comes from the environment variable.
// NEXT_PUBLIC_ prefix makes it available to browser-side JS.
// Falls back to localhost:8000 for local development.
const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Generic HTTP client used by every API call in this app.
//
// Usage:
//   const user = await apiRequest<UserResponse>("/api/v1/auth/me", {
//     method: "GET",
//     headers: { Authorization: `Bearer ${token}` },
//   });
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      // Spread any caller-provided headers (e.g. Authorization).
      ...(options.headers || {}),
    },
  });

  // Attempt to parse JSON; returns null if the body is empty or non-JSON.
  const data = await response.json().catch(() => null);

  // Throw on any non-2xx status so callers don't have to check response.ok.
  // FastAPI validation errors surface under `data.detail`.
  if (!response.ok) {
    throw new Error(data?.detail || "Something went wrong");
  }

  return data as T;
}
