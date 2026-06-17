import { motion } from "framer-motion";
import { Link } from "@tanstack/react-router";

export function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] relative">
      {/* Background Orbs */}
      <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-indigo-500/10 dark:bg-indigo-600/20 rounded-full blur-[100px] -z-10 transition-colors duration-300" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 dark:bg-purple-600/20 rounded-full blur-[100px] -z-10 transition-colors duration-300" />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="text-center max-w-4xl px-4"
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/60 dark:bg-white/5 border border-slate-200 dark:border-white/10 text-indigo-600 dark:text-indigo-300 text-sm font-semibold mb-8 backdrop-blur-md shadow-sm"
        >
          <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
          Fase 3 Concluída
        </motion.div>

        <h1 className="text-5xl md:text-7xl font-black text-slate-900 dark:text-transparent dark:bg-clip-text dark:bg-gradient-to-r dark:from-white dark:via-neutral-200 dark:to-neutral-500 tracking-tight mb-6">
          Conectando Pets a <br className="hidden md:block" />
          <span className="text-indigo-600 dark:text-indigo-400">Famílias Amorosas</span>
        </h1>

        <p className="text-lg md:text-xl text-slate-600 dark:text-neutral-400 mb-10 max-w-2xl mx-auto leading-relaxed">
          Nossa plataforma moderniza e simplifica o processo de adoção. 
          Auditoria de ONGs, controle de operadoras e gestão de adoção de ponta a ponta.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            to="/organizations"
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-indigo-600 dark:bg-white text-white dark:text-black font-bold hover:bg-indigo-700 dark:hover:bg-neutral-200 hover:scale-105 active:scale-95 transition-all shadow-lg shadow-indigo-500/20 dark:shadow-[0_0_30px_rgba(255,255,255,0.1)]"
          >
            Cadastrar minha ONG
          </Link>
          <Link
            to="/register"
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-white dark:bg-white/5 text-slate-700 dark:text-white border border-slate-200 dark:border-white/10 font-bold hover:bg-slate-50 dark:hover:bg-white/10 hover:border-slate-300 dark:hover:border-white/20 transition-all backdrop-blur-md shadow-sm"
          >
            Criar conta de Adotante
          </Link>
        </div>
      </motion.div>

      {/* Feature Grid */}
      <motion.div 
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.8 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl mt-32 px-4"
      >
        <div className="p-6 rounded-2xl bg-white/60 dark:bg-neutral-900/50 border border-slate-200 dark:border-white/5 backdrop-blur-sm shadow-sm dark:shadow-none">
          <div className="w-12 h-12 rounded-lg bg-indigo-100 dark:bg-indigo-500/20 flex items-center justify-center text-indigo-600 dark:text-indigo-400 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">Auditoria Estrita</h3>
          <p className="text-slate-600 dark:text-neutral-400 text-sm">Operadores analisam os estatutos de todas as ONGs para garantir segurança.</p>
        </div>

        <div className="p-6 rounded-2xl bg-white/60 dark:bg-neutral-900/50 border border-slate-200 dark:border-white/5 backdrop-blur-sm shadow-sm dark:shadow-none">
          <div className="w-12 h-12 rounded-lg bg-purple-100 dark:bg-purple-500/20 flex items-center justify-center text-purple-600 dark:text-purple-400 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" /></svg>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">Processo Claro</h3>
          <p className="text-slate-600 dark:text-neutral-400 text-sm">Design pensado na experiência do usuário para facilitar adoções responsáveis.</p>
        </div>

        <div className="p-6 rounded-2xl bg-white/60 dark:bg-neutral-900/50 border border-slate-200 dark:border-white/5 backdrop-blur-sm shadow-sm dark:shadow-none">
          <div className="w-12 h-12 rounded-lg bg-blue-100 dark:bg-blue-500/20 flex items-center justify-center text-blue-600 dark:text-blue-400 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15a4.5 4.5 0 004.5 4.5H18a3.75 3.75 0 001.332-7.257 3 3 0 00-3.758-3.848 5.25 5.25 0 00-10.233 2.33A4.502 4.502 0 002.25 15z" /></svg>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">Clean Architecture</h3>
          <p className="text-slate-600 dark:text-neutral-400 text-sm">Escalável, com testes de BDD e arquitetura totalmente isolada por camadas.</p>
        </div>
      </motion.div>
    </div>
  );
}
