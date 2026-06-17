import type { UseFormRegister } from "react-hook-form";

export interface FilterData {
  species?: string;
  size?: string;
  gender?: string;
  include_adopted?: boolean;
}

interface PublicationFiltersProps {
  register: UseFormRegister<FilterData>;
  onFilter: () => void;
  onClear: () => void;
}

export function PublicationFilters({ register, onFilter, onClear }: PublicationFiltersProps) {
  return (
    <div className="bg-white/60 dark:bg-neutral-900/40 backdrop-blur-md border border-slate-200 dark:border-white/5 rounded-2xl p-4 shadow-sm flex flex-col md:flex-row flex-wrap gap-4 items-end mb-8">
      <div className="flex flex-col gap-1.5 flex-1 min-w-[150px]">
        <label className="text-xs font-bold text-slate-500 dark:text-neutral-400 uppercase tracking-wider">Espécie</label>
        <input 
          {...register("species")} 
          placeholder="Ex: Cachorro" 
          className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-white/10 bg-white/50 dark:bg-black/20 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all"
        />
      </div>

      <div className="flex flex-col gap-1.5 flex-1 min-w-[150px]">
        <label className="text-xs font-bold text-slate-500 dark:text-neutral-400 uppercase tracking-wider">Porte</label>
        <select 
          {...register("size")} 
          className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-white/10 bg-white/50 dark:bg-black/20 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all"
        >
          <option value="">Todos</option>
          <option value="SMALL">Pequeno</option>
          <option value="MEDIUM">Médio</option>
          <option value="LARGE">Grande</option>
        </select>
      </div>

      <div className="flex flex-col gap-1.5 flex-1 min-w-[150px]">
        <label className="text-xs font-bold text-slate-500 dark:text-neutral-400 uppercase tracking-wider">Gênero</label>
        <select 
          {...register("gender")} 
          className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-white/10 bg-white/50 dark:bg-black/20 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all"
        >
          <option value="">Todos</option>
          <option value="MALE">Macho</option>
          <option value="FEMALE">Fêmea</option>
        </select>
      </div>

      <div className="flex items-center gap-2 flex-1 min-w-[150px] md:mb-2">
        <label className="flex items-center gap-2 cursor-pointer text-sm font-semibold text-slate-700 dark:text-neutral-300">
          <input 
            type="checkbox" 
            {...register("include_adopted")} 
            className="w-4 h-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
          />
          Incluir Adotados
        </label>
      </div>

      <div className="flex gap-2 w-full md:w-auto">
        <button 
          onClick={onFilter}
          className="flex-1 md:flex-none px-6 py-2 bg-indigo-600 text-white font-bold rounded-xl shadow-md hover:bg-indigo-700 transition-colors cursor-pointer"
        >
          Filtrar
        </button>
        <button 
          onClick={onClear}
          className="flex-1 md:flex-none px-6 py-2 bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-neutral-300 font-bold rounded-xl hover:bg-slate-200 dark:hover:bg-white/10 transition-colors cursor-pointer"
        >
          Limpar
        </button>
      </div>
    </div>
  );
}
