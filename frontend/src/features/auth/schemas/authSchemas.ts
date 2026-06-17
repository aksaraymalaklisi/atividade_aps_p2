import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email("Formato de e-mail inválido").optional().or(z.literal("")),
  username: z.string().optional(),
  password: z.string().min(8, "A senha deve ter pelo menos 8 caracteres"),
}).refine(data => data.email || data.username, {
  message: "Forneça o e-mail ou o nome de usuário",
  path: ["email"],
});

export type LoginFormData = z.infer<typeof loginSchema>;

export const registerSchema = z.object({
  email: z.string().email("Formato de e-mail inválido"),
  username: z.string().min(3, "Mínimo 3 caracteres").max(150),
  first_name: z.string().optional(),
  last_name: z.string().optional(),
  password: z.string().min(8, "A senha deve ter pelo menos 8 caracteres"),
});

export type RegisterFormData = z.infer<typeof registerSchema>;

export interface User {
  id: string;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  is_operator?: boolean;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}
