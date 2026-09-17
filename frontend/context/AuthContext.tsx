"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";

import { User, getCurrentUser } from "@/lib/auth";

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // On mount, check localStorage for an existing token and validate it
  // against the backend. If the token is expired or invalid, clear it.
  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");

    if (!storedToken) {
      setLoading(false);
      return;
    }

    setToken(storedToken);

    getCurrentUser(storedToken)
      .then((currentUser) => {
        setUser(currentUser);
      })
      .catch(() => {
        // Token invalid or expired — clear everything.
        localStorage.removeItem("access_token");
        setToken(null);
        setUser(null);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  function logout() {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Convenience hook — throws if used outside <AuthProvider>.
export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}
