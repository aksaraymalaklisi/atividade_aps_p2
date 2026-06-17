import { useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { motion } from "framer-motion";
import { usePublications } from "../hooks/usePublications";
import { useOrganizations } from "@/features/organizations/hooks/useOrganizations";
import { Button } from "@/shared/components/ui/Button";
import { Input } from "@/shared/components/ui/Input";

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/webp"];

const schema = z.object({
  name: z.string().min(2, "Nome deve ter pelo menos 2 caracteres"),
  species: z.string().min(2, "Espécie é obrigatória"),
  breed: z.string().optional(),
  size: z.enum(["SMALL", "MEDIUM", "LARGE"]),
  gender: z.enum(["MALE", "FEMALE", "UNKNOWN"]),
  approximate_age: z.number().min(0, "Idade não pode ser negativa"),
  description: z.string().optional(),
  vaccinated: z.boolean().default(false),
  neutered: z.boolean().default(false),
  organization_id: z.string().optional().nullable(),
  images: z
    .any()
    .refine((files) => files?.length > 0, "Envie pelo menos 1 foto.")
    .refine((files) => files?.length <= 5, "Máximo de 5 fotos permitidas.")
    .refine((files) => {
      let valid = true;
      for (let i = 0; i < files?.length; i++) {
        if (files[i].size > MAX_FILE_SIZE) valid = false;
      }
      return valid;
    }, `O tamanho máximo por foto é 5MB.`)
    .refine((files) => {
      let valid = true;
      for (let i = 0; i < files?.length; i++) {
        if (!ACCEPTED_IMAGE_TYPES.includes(files[i].type)) valid = false;
      }
      return valid;
    }, "Apenas arquivos .jpg, .jpeg, .png e .webp são aceitos."),
});

type FormData = z.infer<typeof schema>;

export function PublicationForm() {
  const navigate = useNavigate();
  const { createPublication, isCreating } = usePublications();
  const { organizations } = useOrganizations();
  
  const [previewUrls, setPreviewUrls] = useState<string[]>([]);
  const [serverError, setServerError] = useState<string | null>(null);

  const myApprovedOrgs = organizations?.filter(org => org.status === "APPROVED" && org.is_owner) || [];

  const {
    register,
    handleSubmit,
    control,
    setValue,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      size: "MEDIUM",
      gender: "UNKNOWN",
      approximate_age: 0,
      vaccinated: false,
      neutered: false,
      organization_id: null,
    },
  });

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const filesArray = Array.from(e.target.files);
      if (filesArray.length > 5) {
        alert("Máximo de 5 fotos permitidas.");
        return;
      }
      setValue("images", filesArray, { shouldValidate: true });
      
      const newPreviewUrls = filesArray.map(file => URL.createObjectURL(file));
      setPreviewUrls(newPreviewUrls);
    }
  };

  const onSubmit = async (data: FormData) => {
    try {
      setServerError(null);
      const formData = new FormData();
      formData.append("name", data.name);
      formData.append("species", data.species);
      if (data.breed) formData.append("breed", data.breed);
      formData.append("size", data.size);
      formData.append("gender", data.gender);
      formData.append("approximate_age", data.approximate_age.toString());
      if (data.description) formData.append("description", data.description);
      formData.append("vaccinated", data.vaccinated.toString());
      formData.append("neutered", data.neutered.toString());
      if (data.organization_id) {
        formData.append("organization_id", data.organization_id);
      }

      Array.from(data.images).forEach((file: any) => {
        formData.append("images", file);
      });

      const newPub = await createPublication(formData);
      navigate({ to: "/pet/$id", params: { id: newPub.id } });
    } catch (err: any) {
      console.error(err);
      setServerError("Erro ao publicar. Verifique os dados e tente novamente.");
    }
  };

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 flex justify-center">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/80 dark:bg-neutral-900/60 backdrop-blur-xl border border-slate-200 dark:border-white/10 rounded-3xl p-8 max-w-2xl w-full shadow-[0_8px_30px_rgb(0,0,0,0.04)]"
      >
        <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white mb-2">Publicar um Animal</h2>
        <p className="text-slate-600 dark:text-neutral-400 mb-8">Preencha as informações do animal para ajudá-lo a encontrar um novo lar.</p>

        {serverError && (
          <div className="mb-6 p-4 bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 text-red-600 dark:text-red-400 rounded-xl text-sm">
            {serverError}
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white border-b border-slate-100 dark:border-white/5 pb-2">Fotos (até 5)</h3>
            <div>
              <input
                type="file"
                multiple
                accept="image/jpeg, image/png, image/webp"
                onChange={handleImageChange}
                className="block w-full text-sm text-slate-500 dark:text-neutral-400
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-full file:border-0
                  file:text-sm file:font-semibold
                  file:bg-indigo-50 file:text-indigo-700
                  dark:file:bg-indigo-500/20 dark:file:text-indigo-400
                  hover:file:bg-indigo-100 dark:hover:file:bg-indigo-500/30
                  transition-colors cursor-pointer"
              />
              {errors.images && <p className="mt-1 text-sm text-red-500">{errors.images.message as string}</p>}
            </div>
            
            {previewUrls.length > 0 && (
              <div className="flex gap-2 flex-wrap">
                {previewUrls.map((url, idx) => (
                  <div key={idx} className="w-20 h-20 rounded-xl overflow-hidden border border-slate-200 dark:border-white/10 relative">
                    <img src={url} alt="Preview" className="w-full h-full object-cover" />
                    {idx === 0 && (
                      <div className="absolute bottom-0 left-0 right-0 bg-indigo-600/80 text-white text-[10px] font-bold text-center py-0.5 backdrop-blur-sm">
                        Capa
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white border-b border-slate-100 dark:border-white/5 pb-2">Informações Básicas</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Nome do Animal"
                placeholder="Ex: Rex"
                {...register("name")}
                error={errors.name?.message}
              />
              <Input
                label="Espécie"
                placeholder="Ex: Cachorro, Gato"
                {...register("species")}
                error={errors.species?.message}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Raça (opcional)"
                placeholder="Ex: Labrador"
                {...register("breed")}
                error={errors.breed?.message}
              />
              <Input
                type="number"
                label="Idade Aproximada (anos)"
                {...register("approximate_age", { valueAsNumber: true })}
                error={errors.approximate_age?.message}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-semibold text-slate-700 dark:text-neutral-300">Porte</label>
                <select 
                  {...register("size")}
                  className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-white/10 bg-white/50 dark:bg-black/20 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all"
                >
                  <option value="SMALL">Pequeno</option>
                  <option value="MEDIUM">Médio</option>
                  <option value="LARGE">Grande</option>
                </select>
                {errors.size && <p className="text-sm text-red-500">{errors.size.message}</p>}
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-semibold text-slate-700 dark:text-neutral-300">Gênero</label>
                <select 
                  {...register("gender")}
                  className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-white/10 bg-white/50 dark:bg-black/20 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all"
                >
                  <option value="MALE">Macho</option>
                  <option value="FEMALE">Fêmea</option>
                  <option value="UNKNOWN">Desconhecido</option>
                </select>
                {errors.gender && <p className="text-sm text-red-500">{errors.gender.message}</p>}
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white border-b border-slate-100 dark:border-white/5 pb-2">Saúde e Detalhes</h3>
            
            <div className="flex gap-6">
              <label className="flex items-center gap-2 text-slate-700 dark:text-neutral-300 font-medium cursor-pointer group">
                <input type="checkbox" {...register("vaccinated")} className="w-5 h-5 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500" />
                <span className="group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">Vacinado</span>
              </label>
              <label className="flex items-center gap-2 text-slate-700 dark:text-neutral-300 font-medium cursor-pointer group">
                <input type="checkbox" {...register("neutered")} className="w-5 h-5 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500" />
                <span className="group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">Castrado</span>
              </label>
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-semibold text-slate-700 dark:text-neutral-300">História (Opcional)</label>
              <textarea 
                {...register("description")}
                rows={4}
                placeholder="Conte um pouco sobre a personalidade e a história do animal..."
                className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-white/10 bg-white/50 dark:bg-black/20 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all resize-none"
              />
            </div>
          </div>

          {myApprovedOrgs.length > 0 && (
            <div className="space-y-4">
              <h3 className="text-lg font-bold text-slate-900 dark:text-white border-b border-slate-100 dark:border-white/5 pb-2">Vincular a uma ONG</h3>
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-semibold text-slate-700 dark:text-neutral-300">Publicar como:</label>
                <select 
                  {...register("organization_id")}
                  className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-white/10 bg-white/50 dark:bg-black/20 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all"
                >
                  <option value="">Apenas eu (Usuário Independente)</option>
                  {myApprovedOrgs.map(org => (
                    <option key={org.id} value={org.id}>{org.name}</option>
                  ))}
                </select>
                <p className="text-xs text-slate-500 dark:text-neutral-500">Se selecionado, a ONG aparecerá como a publicante deste animal.</p>
              </div>
            </div>
          )}

          <Button 
            type="submit" 
            className="w-full h-14 text-lg font-bold"
            isLoading={isCreating}
          >
            Publicar Animal
          </Button>
        </form>
      </motion.div>
    </div>
  );
}
