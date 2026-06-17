import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().optional(),
  username: z.string().optional(),
  password: z.string().min(8, "A senha deve ter pelo menos 8 caracteres"),
}).superRefine((data, ctx) => {
  if (!data.email && !data.username) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Forneça o e-mail ou o nome de usuário",
      path: ["email"],
    });
  }
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
  is_staff?: boolean;
  first_name?: string;
  last_name?: string;
  is_operator?: boolean;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}
