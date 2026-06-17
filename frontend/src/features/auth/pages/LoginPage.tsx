import { LoginForm } from "../components/LoginForm";
import { Link } from "@tanstack/react-router";

export function LoginPage() {
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-slate-50 dark:bg-neutral-950 relative overflow-hidden transition-colors duration-300">
      {/* Dynamic Background Elements */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-indigo-300/30 dark:bg-indigo-600/20 blur-[100px] pointer-events-none transition-colors duration-300" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-violet-300/30 dark:bg-purple-600/20 blur-[100px] pointer-events-none transition-colors duration-300" />
      
      <div className="z-10 flex flex-col items-center w-full px-4">
        <LoginForm />
        <p className="mt-6 text-slate-600 dark:text-neutral-400 transition-colors">
          Ainda não tem conta?{" "}
          <Link to="/register" className="text-indigo-600 dark:text-indigo-400 font-semibold hover:text-indigo-700 dark:hover:text-indigo-300 hover:underline transition-all">
            Cadastre-se aqui
          </Link>
        </p>
      </div>
    </div>
  );
}
