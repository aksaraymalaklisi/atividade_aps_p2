import { useState } from "react";
import { useForm } from "react-hook-form";
import { motion } from "framer-motion";
import { Link } from "@tanstack/react-router";
import { usePublications } from "../hooks/usePublications";
import { PetCard } from "../components/PetCard";
import { PublicationFilters, type FilterData } from "../components/PublicationFilters";

export function HomePage() {
  const [filters, setFilters] = useState<Record<string, string>>({});
  const { publications, isLoading } = usePublications(filters);
  const { register, getValues, reset } = useForm<FilterData>();

  const handleFilter = () => {
    const values = getValues();
    const activeFilters: Record<string, string> = {};
    if (values.species) activeFilters['pet__species'] = values.species;
    if (values.size) activeFilters['pet__size'] = values.size;
    if (values.gender) activeFilters['pet__gender'] = values.gender;
    if (values.include_adopted) activeFilters['include_adopted'] = 'true';
    setFilters(activeFilters);
  };

  const handleClear = () => {
    reset();
    setFilters({});
  };

  return (
    <div className="flex flex-col min-h-screen relative">
      {/* Background Orbs */}
      <div className="absolute top-0 left-1/4 w-72 h-72 bg-indigo-500/10 dark:bg-indigo-600/20 rounded-full blur-[100px] -z-10 transition-colors duration-300" />
      <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-purple-500/10 dark:bg-purple-600/20 rounded-full blur-[100px] -z-10 transition-colors duration-300" />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 flex flex-col items-center justify-center text-center max-w-4xl mx-auto">
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/60 dark:bg-white/5 border border-slate-200 dark:border-white/10 text-indigo-600 dark:text-indigo-300 text-sm font-semibold mb-8 backdrop-blur-md shadow-sm"
        >
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
          Adoção Aberta
        </motion.div>

        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.6 }}
          className="text-5xl md:text-7xl font-black text-slate-900 dark:text-transparent dark:bg-clip-text dark:bg-gradient-to-r dark:from-white dark:via-neutral-200 dark:to-neutral-500 tracking-tight mb-6"
        >
          Conectando Pets a <br className="hidden md:block" />
          <span className="text-indigo-600 dark:text-indigo-400">Novas Famílias</span>
        </motion.h1>

        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.6 }}
          className="text-lg md:text-xl text-slate-600 dark:text-neutral-400 max-w-2xl mx-auto leading-relaxed"
        >
          Encontre o seu novo melhor amigo. Explore os animais disponíveis para adoção de ONGs e protetores independentes verificados.
        </motion.p>
      </section>

      {/* Catalog Section */}
      <section className="flex-1 w-full max-w-7xl mx-auto px-4 pb-24">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white">Animais Disponíveis</h2>
          <div className="flex gap-2">
            <Link 
              to="/publications/new" 
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg font-bold text-sm hover:bg-indigo-700 transition-colors shadow-md"
            >
              Publicar Pet
            </Link>
          </div>
        </div>

        <PublicationFilters 
          register={register} 
          onFilter={handleFilter} 
          onClear={handleClear} 
        />

        {isLoading ? (
          <div className="flex justify-center items-center py-20">
            <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : publications.length === 0 ? (
          <div className="text-center py-20 bg-white/50 dark:bg-neutral-900/50 rounded-3xl border border-slate-200 dark:border-white/5">
            <p className="text-slate-500 dark:text-neutral-400 text-lg">Nenhum animal publicado no momento.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {publications.map((pub) => (
              <PetCard key={pub.id} publication={pub} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
