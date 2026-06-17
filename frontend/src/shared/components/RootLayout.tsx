import { Outlet } from '@tanstack/react-router'

export function RootLayout() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <a href="/" className="text-2xl font-bold text-indigo-600">
            🐾 PetAdopt
          </a>
          <div className="flex items-center gap-4">
            {/* Auth buttons will be added in Phase 2 */}
            <span className="text-sm text-gray-500">v1.0.0</span>
          </div>
        </nav>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-8">
        <Outlet />
      </main>

      <footer className="border-t border-gray-200 bg-white py-6 text-center text-sm text-gray-500">
        PetAdopt © 2026 — Plataforma de Adoção de Animais
      </footer>
    </div>
  )
}
