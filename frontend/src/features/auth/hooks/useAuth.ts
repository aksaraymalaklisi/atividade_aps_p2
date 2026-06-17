import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { authService } from "../api/authService";
import type { LoginFormData, RegisterFormData } from "../schemas/authSchemas";
import { useNavigate } from "@tanstack/react-router";

export const authKeys = {
  all: ["auth"] as const,
  profile: () => [...authKeys.all, "profile"] as const,
};

export function useAuth() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const profileQuery = useQuery({
    queryKey: authKeys.profile(),
    queryFn: authService.getProfile,
    retry: false,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });

  const loginMutation = useMutation({
    mutationFn: (data: LoginFormData) => authService.login(data),
    onSuccess: (data) => {
      localStorage.setItem("accessToken", data.access);
      localStorage.setItem("refreshToken", data.refresh);
      // Pre-fill cache with the returned user
      queryClient.setQueryData(authKeys.profile(), data.user);
      navigate({ to: "/" });
    },
  });

  const registerMutation = useMutation({
    mutationFn: (data: RegisterFormData) => authService.register(data),
    onSuccess: () => {
      // Upon successful registration, we typically want to route them to login
      navigate({ to: "/login" });
    },
  });

  const logout = () => {
    authService.logout();
    queryClient.setQueryData(authKeys.profile(), null);
    navigate({ to: "/login" });
  };

  return {
    user: profileQuery.data,
    isLoading: profileQuery.isLoading,
    isError: profileQuery.isError,
    login: loginMutation.mutateAsync,
    isLoggingIn: loginMutation.isPending,
    loginError: loginMutation.error,
    register: registerMutation.mutateAsync,
    isRegistering: registerMutation.isPending,
    registerError: registerMutation.error,
    logout,
  };
}
