import { Navigate, Outlet } from "@tanstack/react-router";
import { useAuth } from "../hooks/useAuth";

export function ProtectedRoute() {
  const { user, isLoading } = useAuth();
  const token = localStorage.getItem("accessToken");

  if (isLoading) {
    return (
      <div className="flex h-screen w-full items-center justify-center">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-indigo-200 border-t-indigo-600" />
      </div>
    );
  }

  // Se não tem token ou falhou ao buscar perfil (token expirado/inválido não recuperado)
  if (!token || (!user && !isLoading)) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
