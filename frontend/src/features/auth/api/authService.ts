import { axiosClient } from "@/shared/api/axiosClient";
import type { LoginFormData, RegisterFormData, AuthResponse, User } from "../schemas/authSchemas";

export const authService = {
  login: async (data: LoginFormData): Promise<AuthResponse> => {
    const response = await axiosClient.post<AuthResponse>("/accounts/login/", data);
    return response.data;
  },

  register: async (data: RegisterFormData): Promise<User> => {
    const response = await axiosClient.post<User>("/accounts/register/", data);
    return response.data;
  },

  getProfile: async (): Promise<User> => {
    const response = await axiosClient.get<User>("/accounts/profile/");
    return response.data;
  },
  
  logout: () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    window.dispatchEvent(new Event("auth:logout"));
  }
};
