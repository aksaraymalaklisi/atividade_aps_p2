import { Link } from "@tanstack/react-router";
import { motion } from "framer-motion";
import type { Publication } from "../api/publicationsApi";

interface PetCardProps {
  publication: Publication;
}

export function PetCard({ publication }: PetCardProps) {
  const { pet, organization, publisher_name } = publication;
  const primaryImage = pet.images.find(img => img.is_primary) || pet.images[0];
  const imageUrl = primaryImage ? `${import.meta.env.VITE_BACKEND_BASE || 'http://localhost:8000'}${primaryImage.image}` : "/placeholder-pet.png";

  const genderIcon = pet.gender === "MALE" ? "♂" : pet.gender === "FEMALE" ? "♀" : "";
  const genderColor = pet.gender === "MALE" ? "text-blue-500 bg-blue-100 dark:bg-blue-500/20" : pet.gender === "FEMALE" ? "text-pink-500 bg-pink-100 dark:bg-pink-500/20" : "text-slate-500 bg-slate-100 dark:bg-slate-500/20";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -8, scale: 1.02 }}
      transition={{ duration: 0.3 }}
      className="group relative flex flex-col bg-white/70 dark:bg-neutral-900/60 backdrop-blur-xl border border-white/20 dark:border-white/5 rounded-3xl overflow-hidden shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.12)] dark:hover:shadow-[0_20px_40px_rgba(255,255,255,0.05)] cursor-pointer"
    >
      <Link to="/pet/$id" params={{ id: publication.id }} className="absolute inset-0 z-[100]" />
      
      {/* Image Section */}
      <div className="relative h-64 overflow-hidden bg-slate-100 dark:bg-neutral-800">
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent z-10" />
        <img 
          src={imageUrl} 
          alt={pet.name} 
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" 
        />
        
        {/* Status Badge */}
        {publication.status !== "ACTIVE" && (
          <div className="absolute top-4 left-4 z-20 px-3 py-1 bg-red-500 text-white text-xs font-bold uppercase rounded-full tracking-wider shadow-lg">
            {publication.status === "ADOPTED" ? "Adotado" : "Indisponível"}
          </div>
        )}

        {/* Name & Basic Info Overlay */}
        <div className="absolute bottom-4 left-4 right-4 z-20 flex justify-between items-end">
          <div>
            <h3 className="text-2xl font-black text-white drop-shadow-md">{pet.name}</h3>
            <p className="text-white/90 text-sm font-medium drop-shadow-sm">{pet.breed || "Sem Raça Definida"}</p>
          </div>
          <div className={`flex items-center justify-center w-8 h-8 rounded-full ${genderColor} backdrop-blur-md shadow-lg`}>
            <span className="text-lg leading-none font-bold">{genderIcon}</span>
          </div>
        </div>
      </div>

      {/* Details Section */}
      <div className="p-5 flex-1 flex flex-col">
        <div className="flex flex-wrap gap-2 mb-4">
          <span className="px-3 py-1 text-xs font-semibold bg-indigo-50 text-indigo-600 dark:bg-indigo-500/10 dark:text-indigo-400 rounded-full border border-indigo-100 dark:border-indigo-500/20">
            {pet.size === "SMALL" ? "Pequeno" : pet.size === "MEDIUM" ? "Médio" : "Grande"}
          </span>
          <span className="px-3 py-1 text-xs font-semibold bg-emerald-50 text-emerald-600 dark:bg-emerald-500/10 dark:text-emerald-400 rounded-full border border-emerald-100 dark:border-emerald-500/20">
            {pet.approximate_age} anos
          </span>
        </div>

        <div className="flex gap-4 mb-4 text-sm font-medium text-slate-500 dark:text-neutral-400">
          <div className="flex items-center gap-1.5">
            <div className={`w-2 h-2 rounded-full ${pet.vaccinated ? "bg-green-500" : "bg-slate-300 dark:bg-neutral-600"}`} />
            <span>Vacinado</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className={`w-2 h-2 rounded-full ${pet.neutered ? "bg-green-500" : "bg-slate-300 dark:bg-neutral-600"}`} />
            <span>Castrado</span>
          </div>
        </div>

        <div className="mt-auto pt-4 border-t border-slate-100 dark:border-white/5 flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white font-bold text-xs shadow-inner">
            {(organization?.name || publisher_name).charAt(0).toUpperCase()}
          </div>
          <div className="flex flex-col">
            <span className="text-xs text-slate-400 dark:text-neutral-500 uppercase font-semibold tracking-wider">Publicado por</span>
            <span className="text-sm font-bold text-slate-700 dark:text-white truncate max-w-[200px]">
              {organization ? organization.name : publisher_name}
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
