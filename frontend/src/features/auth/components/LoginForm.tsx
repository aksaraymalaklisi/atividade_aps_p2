import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { motion } from "framer-motion";
import { Lock, User as UserIcon } from "lucide-react";
import { Input } from "@/shared/components/ui/Input";
import { Button } from "@/shared/components/ui/Button";
import { loginSchema, type LoginFormData } from "../schemas/authSchemas";
import { useAuth } from "../hooks/useAuth";

export function LoginForm() {
  const { login, isLoggingIn } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      const isEmail = data.email?.includes("@");
      const payload = {
        email: isEmail ? data.email : undefined,
        username: !isEmail ? data.email : undefined,
        password: data.password,
      };
      await login(payload);
    } catch (err) {
      const axiosError = err as import("axios").AxiosError;
      if (axiosError.response?.status === 401) {
        setError("root", { type: "server", message: "Credenciais inválidas" });
      } else {
        setError("root", { type: "server", message: "Ocorreu um erro no servidor" });
      }
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-md p-8 rounded-3xl bg-white/60 dark:bg-neutral-900/60 backdrop-blur-xl border border-slate-200 dark:border-white/10 shadow-2xl shadow-indigo-100 dark:shadow-none transition-colors duration-300"
    >
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-violet-500 dark:from-indigo-400 dark:to-violet-400">
          Bem-vindo de volta
        </h2>
        <p className="text-slate-500 dark:text-neutral-400 mt-2 transition-colors">Acesse sua conta para continuar</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="space-y-5">
          <Input
            label="E-mail ou Usuário"
            placeholder="seu@email.com"
            icon={<UserIcon className="w-5 h-5" />}
            error={errors.email?.message || errors.username?.message}
            {...register("email")}
          />
          <Input
            label="Senha"
            type="password"
            placeholder="••••••••"
            icon={<Lock className="w-5 h-5" />}
            error={errors.password?.message}
            {...register("password")}
          />
        </div>

        {errors.root && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-3 rounded-lg bg-red-50 dark:bg-red-500/10 text-red-600 dark:text-red-400 text-sm text-center border border-red-100 dark:border-red-500/20 transition-colors"
          >
            {errors.root.message}
          </motion.div>
        )}

        <Button
          type="submit"
          className="w-full"
          isLoading={isLoggingIn}
        >
          Entrar
        </Button>
      </form>
    </motion.div>
  );
}
