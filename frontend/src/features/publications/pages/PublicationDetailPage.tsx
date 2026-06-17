import { useState } from "react";
import { useParams, Link } from "@tanstack/react-router";
import { motion, AnimatePresence } from "framer-motion";
import { usePublication } from "../hooks/usePublications";
import { Button } from "@/shared/components/ui/Button";

export function PublicationDetailPage() {
  const { id } = useParams({ strict: false });
  const { publication, isLoading, error } = usePublication(id as string);
  const [currentImageIdx, setCurrentImageIdx] = useState(0);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (error || !publication) {
    return (
      <div className="min-h-screen flex items-center justify-center flex-col gap-4">
        <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-200">Publicação não encontrada</h2>
        <Link to="/">
          <Button variant="outline">Voltar ao Início</Button>
        </Link>
      </div>
    );
  }

  const { pet, organization, publisher_name } = publication;
  const images = pet.images && pet.images.length > 0 
    ? pet.images.sort((a, b) => a.order - b.order) 
    : [{ id: 'default', image: '/placeholder-pet.png', is_primary: true, order: 0 }];
    
  const currentImage = images[currentImageIdx];

  const genderIcon = pet.gender === "MALE" ? "♂ Macho" : pet.gender === "FEMALE" ? "♀ Fêmea" : "Desconhecido";
  const sizeText = pet.size === "SMALL" ? "Pequeno" : pet.size === "MEDIUM" ? "Médio" : "Grande";

  return (
    <div className="min-h-screen pt-24 pb-20 px-4 max-w-6xl mx-auto">
      <Link to="/" className="inline-flex items-center gap-2 text-indigo-600 dark:text-indigo-400 font-medium mb-8 hover:opacity-80 transition-opacity">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
        </svg>
        Voltar para o catálogo
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Left: Image Carousel */}
        <div className="flex flex-col gap-4">
          <div className="relative aspect-square md:aspect-[4/3] rounded-3xl overflow-hidden bg-slate-100 dark:bg-neutral-800 shadow-xl border border-slate-200 dark:border-white/5">
            <AnimatePresence mode="wait">
              <motion.img
                key={currentImageIdx}
                initial={{ opacity: 0, scale: 1.05 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.3 }}
                src={currentImage.image.startsWith('/') ? `http://localhost:8000${currentImage.image}` : currentImage.image}
                alt={pet.name}
                className="w-full h-full object-cover"
              />
            </AnimatePresence>
            
            {publication.status !== "ACTIVE" && (
              <div className="absolute top-4 left-4 z-20 px-4 py-2 bg-red-500 text-white text-sm font-bold uppercase rounded-full tracking-wider shadow-lg">
                {publication.status === "ADOPTED" ? "Adotado" : "Indisponível"}
              </div>
            )}
          </div>

          {/* Thumbnails */}
          {images.length > 1 && (
            <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
              {images.map((img, idx) => (
                <button
                  key={img.id}
                  onClick={() => setCurrentImageIdx(idx)}
                  className={`relative flex-shrink-0 w-20 h-20 rounded-xl overflow-hidden border-2 transition-all ${
                    idx === currentImageIdx 
                      ? "border-indigo-500 shadow-md scale-105" 
                      : "border-transparent opacity-60 hover:opacity-100"
                  }`}
                >
                  <img 
                    src={img.image.startsWith('/') ? `http://localhost:8000${img.image}` : img.image} 
                    alt={`Preview ${idx + 1}`} 
                    className="w-full h-full object-cover"
                  />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Right: Details */}
        <div className="flex flex-col">
          <div className="mb-6">
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-4xl md:text-5xl font-black text-slate-900 dark:text-white tracking-tight">{pet.name}</h1>
              <span className={`px-3 py-1 text-sm font-bold rounded-full ${
                pet.gender === 'MALE' ? 'bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-400' :
                pet.gender === 'FEMALE' ? 'bg-pink-100 text-pink-700 dark:bg-pink-500/20 dark:text-pink-400' :
                'bg-slate-100 text-slate-700 dark:bg-slate-500/20 dark:text-slate-400'
              }`}>
                {genderIcon}
              </span>
            </div>
            <p className="text-xl text-slate-500 dark:text-neutral-400 font-medium">{pet.breed || "Sem Raça Definida"} • {pet.species}</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-slate-50 dark:bg-white/5 rounded-2xl p-4 border border-slate-100 dark:border-white/10 flex flex-col items-center justify-center text-center">
              <span className="text-slate-400 dark:text-neutral-500 text-xs font-bold uppercase tracking-wider mb-1">Idade</span>
              <span className="text-lg font-bold text-slate-800 dark:text-white">{pet.approximate_age} anos</span>
            </div>
            <div className="bg-slate-50 dark:bg-white/5 rounded-2xl p-4 border border-slate-100 dark:border-white/10 flex flex-col items-center justify-center text-center">
              <span className="text-slate-400 dark:text-neutral-500 text-xs font-bold uppercase tracking-wider mb-1">Porte</span>
              <span className="text-lg font-bold text-slate-800 dark:text-white">{sizeText}</span>
            </div>
            <div className={`rounded-2xl p-4 border flex flex-col items-center justify-center text-center ${
              pet.vaccinated 
                ? "bg-green-50 border-green-100 dark:bg-green-500/10 dark:border-green-500/20" 
                : "bg-slate-50 border-slate-100 dark:bg-white/5 dark:border-white/10"
            }`}>
              <span className="text-slate-400 dark:text-neutral-500 text-xs font-bold uppercase tracking-wider mb-1">Vacina</span>
              <span className={`text-lg font-bold ${pet.vaccinated ? "text-green-600 dark:text-green-400" : "text-slate-800 dark:text-white"}`}>
                {pet.vaccinated ? "Sim" : "Não"}
              </span>
            </div>
            <div className={`rounded-2xl p-4 border flex flex-col items-center justify-center text-center ${
              pet.neutered 
                ? "bg-green-50 border-green-100 dark:bg-green-500/10 dark:border-green-500/20" 
                : "bg-slate-50 border-slate-100 dark:bg-white/5 dark:border-white/10"
            }`}>
              <span className="text-slate-400 dark:text-neutral-500 text-xs font-bold uppercase tracking-wider mb-1">Castrado</span>
              <span className={`text-lg font-bold ${pet.neutered ? "text-green-600 dark:text-green-400" : "text-slate-800 dark:text-white"}`}>
                {pet.neutered ? "Sim" : "Não"}
              </span>
            </div>
          </div>

          <div className="mb-8 flex-1">
            <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">História do Pet</h3>
            <div className="prose prose-slate dark:prose-invert max-w-none text-slate-600 dark:text-neutral-300">
              {pet.description ? (
                <p className="whitespace-pre-wrap leading-relaxed">{pet.description}</p>
              ) : (
                <p className="italic opacity-70">Nenhuma história informada pelo publicante.</p>
              )}
            </div>
          </div>

          <div className="p-6 bg-indigo-50 dark:bg-indigo-500/10 rounded-3xl border border-indigo-100 dark:border-indigo-500/20 flex flex-col sm:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold text-xl shadow-md">
                {(organization?.name || publisher_name).charAt(0).toUpperCase()}
              </div>
              <div>
                <p className="text-sm text-indigo-600 dark:text-indigo-400 font-bold uppercase tracking-wider mb-0.5">Publicado por</p>
                <p className="text-lg font-bold text-slate-900 dark:text-white">
                  {organization ? organization.name : publisher_name}
                </p>
              </div>
            </div>
            <Button 
              className="w-full sm:w-auto h-12 px-8 rounded-xl shadow-lg shadow-indigo-500/20 text-lg"
              disabled={publication.status !== "ACTIVE"}
            >
              Tenho Interesse
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
