export function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <h1 className="mb-4 text-5xl font-bold text-gray-900">
        🐾 PetAdopt
      </h1>
      <p className="mb-8 max-w-2xl text-center text-lg text-gray-600">
        Plataforma de adoção de animais. Conectando pets a famílias amorosas.
      </p>
      <div className="flex gap-4">
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h2 className="mb-2 text-xl font-semibold text-indigo-600">Backend</h2>
          <p className="text-sm text-gray-500">Django + DRF + Clean Architecture</p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h2 className="mb-2 text-xl font-semibold text-indigo-600">Frontend</h2>
          <p className="text-sm text-gray-500">React + Tanstack + TailwindCSS</p>
        </div>
      </div>
      <p className="mt-12 text-sm text-gray-400">
        Fase 1 completa — estrutura de projeto inicializada.
      </p>
    </div>
  )
}
