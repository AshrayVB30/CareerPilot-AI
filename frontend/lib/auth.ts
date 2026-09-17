import { apiRequest } from "./api";

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  created_at?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export async function register(email: string, password: string) {
  return apiRequest<User>("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function login(email: string, password: string) {
  return apiRequest<LoginResponse>("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function getCurrentUser(token: string) {
  return apiRequest<User>("/api/v1/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
