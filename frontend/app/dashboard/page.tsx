"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function DashboardPage() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  // Redirect unauthenticated users to /login.
  useEffect(() => {
    if (!loading && !user) {
      router.replace("/login");
    }
  }, [loading, user, router]);

  if (loading) {
    return <p>Loading...</p>;
  }

  // Render nothing while the redirect is in flight.
  if (!user) {
    return null;
  }

  function handleLogout() {
    logout();
    router.replace("/login");
  }

  return (
    <main>
      <h1>CareerPilot AI</h1>

      <h2>Dashboard</h2>

      <p>Welcome, {user.email}</p>

      <p>
        Account status:{" "}
        {user.is_active ? "Active" : "Inactive"}
      </p>

      <button onClick={handleLogout}>Logout</button>
    </main>
  );
}
