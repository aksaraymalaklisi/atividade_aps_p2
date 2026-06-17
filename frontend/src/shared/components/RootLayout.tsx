import { Outlet, Link } from '@tanstack/react-router'
import { useAuth } from '@/features/auth/hooks/useAuth'

export function RootLayout() {
  const { user, logout } = useAuth()

  return (
    <div className="flex min-h-screen flex-col bg-slate-50 text-slate-900 dark:bg-neutral-950 dark:text-neutral-100 font-sans selection:bg-indigo-500/30 transition-colors duration-300">
      <header className="sticky top-0 z-50 border-b border-slate-200 dark:border-white/5 bg-white/80 dark:bg-neutral-950/80 backdrop-blur-md transition-colors duration-300">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <Link to="/" className="text-2xl font-black tracking-tighter text-slate-900 dark:text-white flex items-center gap-2 group">
            <span className="text-indigo-600 dark:text-indigo-500 group-hover:scale-110 transition-transform duration-300">🐾</span> 
            PetAdopt<span className="text-indigo-600 dark:text-indigo-500">.</span>
          </Link>
          <div className="flex items-center gap-6">
            <Link 
              to="/organizations" 
              className="text-sm font-semibold text-slate-600 dark:text-neutral-400 hover:text-indigo-600 dark:hover:text-white transition-colors"
            >
              Organizações
            </Link>
            
            {user ? (
              <div className="flex items-center gap-4 border-l border-slate-200 dark:border-white/10 pl-6">
                <span className="text-sm text-slate-700 dark:text-neutral-300 font-medium">
                  {user.first_name || user.username}
                  {(user.is_staff || user.is_operator) && (
                    <span className="ml-2 text-[10px] uppercase tracking-wider bg-indigo-100 text-indigo-700 dark:bg-indigo-500/20 dark:text-indigo-400 px-2 py-0.5 rounded-full border border-indigo-200 dark:border-indigo-500/30">
                      Operador
                    </span>
                  )}
                </span>
                <button 
                  onClick={logout}
                  className="text-sm font-semibold text-slate-600 dark:text-neutral-400 hover:text-red-500 dark:hover:text-red-400 transition-colors cursor-pointer"
                >
                  Sair
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-4 border-l border-slate-200 dark:border-white/10 pl-6">
                <Link 
                  to="/login" 
                  className="text-sm font-semibold text-slate-600 dark:text-neutral-300 hover:text-indigo-600 dark:hover:text-white transition-colors"
                >
                  Entrar
                </Link>
                <Link 
                  to="/register" 
                  className="text-sm font-semibold bg-slate-900 text-white dark:bg-white dark:text-black px-5 py-2 rounded-full hover:bg-slate-800 dark:hover:bg-neutral-200 transition-all hover:scale-105 active:scale-95 shadow-sm"
                >
                  Criar Conta
                </Link>
              </div>
            )}
          </div>
        </nav>
      </header>

      <main className="mx-auto flex-1 w-full max-w-7xl px-6 py-8 relative">
        {/* Subtle background glow for the whole app */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-indigo-500/5 blur-[120px] rounded-full pointer-events-none -z-10" />
        <Outlet />
      </main>

      <footer className="border-t border-slate-200 dark:border-white/5 bg-slate-50 dark:bg-neutral-950 py-8 text-center text-sm text-slate-500 dark:text-neutral-500 transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4">
          <p>PetAdopt © 2026 — Plataforma Open-Source de Adoção de Animais.</p>
          <div className="flex gap-4">
            <a href="#" className="hover:text-indigo-600 dark:hover:text-white transition-colors">Termos</a>
            <a href="#" className="hover:text-indigo-600 dark:hover:text-white transition-colors">Privacidade</a>
            <a href="#" className="hover:text-indigo-600 dark:hover:text-white transition-colors">Contato</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
