import { RegisterForm } from "../components/RegisterForm";
import { Link } from "@tanstack/react-router";

export function RegisterPage() {
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-slate-50 relative overflow-hidden py-12">
      {/* Dynamic Background Elements */}
      <div className="absolute top-[20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-fuchsia-300/20 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-indigo-300/30 blur-[100px] pointer-events-none" />
      
      <div className="z-10 flex flex-col items-center w-full px-4">
        <RegisterForm />
        <p className="mt-6 text-slate-600">
          Já possui conta?{" "}
          <Link to="/login" className="text-indigo-600 font-semibold hover:text-indigo-700 hover:underline transition-all">
            Entre aqui
          </Link>
        </p>
      </div>
    </div>
  );
}
