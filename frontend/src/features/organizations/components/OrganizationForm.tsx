import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion } from "framer-motion";
import { Input } from "@/shared/components/ui/Input";
import { Button } from "@/shared/components/ui/Button";
import { useOrganizations } from "../hooks/useOrganizations";

const organizationSchema = z.object({
  name: z.string().min(3, "O nome deve ter pelo menos 3 caracteres"),
  cnpj: z.string().regex(/^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$|^\d{14}$/, "CNPJ inválido"),
  email: z.string().email("E-mail corporativo inválido"),
  phone: z.string().min(10, "Telefone inválido (mínimo 10 dígitos)").max(15, "Telefone muito longo"),
  address: z.string().min(10, "Por favor, insira o endereço completo"),
  description: z.string().min(20, "Forneça uma descrição detalhada sobre a causa (mínimo 20 caracteres)"),
  document: z.any().refine((file) => file?.length === 1, "O envio de um documento comprobatório em PDF é obrigatório"),
});

type OrganizationFormData = z.infer<typeof organizationSchema>;

export function OrganizationForm() {
  const { createOrganization } = useOrganizations();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting, isValid },
  } = useForm<OrganizationFormData>({
    resolver: zodResolver(organizationSchema),
    mode: "onTouched", // Validação inline
  });

  const onSubmit = async (data: OrganizationFormData) => {
    try {
      const formData = new FormData();
      formData.append("name", data.name);
      formData.append("cnpj", data.cnpj.replace(/[^\d]/g, ""));
      formData.append("email", data.email);
      formData.append("phone", data.phone);
      formData.append("address", data.address);
      formData.append("description", data.description);
      formData.append("document", data.document[0]);

      await createOrganization(formData);
      reset();
      alert("Solicitação enviada! Nossa equipe revisará seus dados em breve.");
    } catch (error) {
      console.error(error);
      alert("Houve um erro ao processar o cadastro. Tente novamente.");
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-4xl mx-auto p-8 lg:p-12 relative overflow-hidden rounded-3xl"
    >
      {/* Background Decorativo e Glassmorphism Effect */}
      <div className="absolute inset-0 bg-white/60 dark:bg-neutral-900/60 backdrop-blur-xl border border-slate-200 dark:border-white/10 shadow-[0_0_80px_-20px_rgba(0,0,0,0.1)] dark:shadow-[0_0_80px_-20px_rgba(255,255,255,0.05)] rounded-3xl -z-10 transition-colors duration-300" />
      <div className="absolute -top-40 -right-40 w-96 h-96 bg-indigo-500/10 rounded-full blur-[100px] pointer-events-none -z-10" />
      <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-purple-500/10 rounded-full blur-[100px] pointer-events-none -z-10" />

      {/* Header */}
      <div className="mb-10 text-center lg:text-left">
        <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight mb-2">Solicitar Cadastro de ONG</h2>
        <p className="text-slate-600 dark:text-neutral-400 text-sm max-w-xl">
          Preencha os dados institucionais abaixo com cuidado. As informações serão submetidas ao nosso comitê de Operadores para auditoria e aprovação na plataforma.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        
        {/* Sessão 1: Informações Básicas (Grid de 2 colunas) */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white/90 border-b border-slate-200 dark:border-white/10 pb-2">Identidade e Registro</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex flex-col">
              <Input label="Nome da Organização" placeholder="Ex: Instituto Proteção Animal" {...register("name")} className="bg-white/50 dark:bg-neutral-950/50 text-slate-900 dark:text-white border-slate-200 dark:border-neutral-800 focus:border-indigo-500 transition-colors" />
              {errors.name && <span className="text-red-500 dark:text-red-400 text-xs mt-2 font-medium flex items-center"><span className="mr-1">⚠</span> {errors.name.message}</span>}
            </div>
            
            <div className="flex flex-col">
              <Input label="CNPJ" placeholder="00.000.000/0000-00" {...register("cnpj")} className="bg-white/50 dark:bg-neutral-950/50 text-slate-900 dark:text-white border-slate-200 dark:border-neutral-800 focus:border-indigo-500 transition-colors" />
              {errors.cnpj && <span className="text-red-500 dark:text-red-400 text-xs mt-2 font-medium flex items-center"><span className="mr-1">⚠</span> {errors.cnpj.message}</span>}
            </div>
          </div>
        </div>

        {/* Sessão 2: Contato e Localização */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white/90 border-b border-slate-200 dark:border-white/10 pb-2">Contato e Localização</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex flex-col">
              <Input label="E-mail Institucional" type="email" placeholder="contato@ong.org" {...register("email")} className="bg-white/50 dark:bg-neutral-950/50 text-slate-900 dark:text-white border-slate-200 dark:border-neutral-800 focus:border-indigo-500 transition-colors" />
              {errors.email && <span className="text-red-500 dark:text-red-400 text-xs mt-2 font-medium flex items-center"><span className="mr-1">⚠</span> {errors.email.message}</span>}
            </div>
            
            <div className="flex flex-col">
              <Input label="Telefone Base" type="tel" placeholder="(11) 90000-0000" {...register("phone")} className="bg-white/50 dark:bg-neutral-950/50 text-slate-900 dark:text-white border-slate-200 dark:border-neutral-800 focus:border-indigo-500 transition-colors" />
              {errors.phone && <span className="text-red-500 dark:text-red-400 text-xs mt-2 font-medium flex items-center"><span className="mr-1">⚠</span> {errors.phone.message}</span>}
            </div>
          </div>
          
          <div className="flex flex-col mt-4">
            <Input label="Endereço Completo Sede" placeholder="Av. Paulista, 1000 - São Paulo, SP - CEP 01310-100" {...register("address")} className="bg-white/50 dark:bg-neutral-950/50 text-slate-900 dark:text-white border-slate-200 dark:border-neutral-800 focus:border-indigo-500 transition-colors w-full" />
            {errors.address && <span className="text-red-500 dark:text-red-400 text-xs mt-2 font-medium flex items-center"><span className="mr-1">⚠</span> {errors.address.message}</span>}
          </div>
        </div>

        {/* Sessão 3: Apresentação e Auditoria */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white/90 border-b border-slate-200 dark:border-white/10 pb-2">Apresentação Institucional</h3>
          <div className="flex flex-col">
            <label className="block text-slate-700 dark:text-white/80 text-sm font-medium mb-1.5">Descrição da Causa</label>
            <textarea 
              {...register("description")} 
              placeholder="Descreva a história, propósito e principais atuações da sua ONG..."
              className="bg-white/50 dark:bg-neutral-950/50 text-slate-900 dark:text-white border border-slate-200 dark:border-neutral-800 focus:border-indigo-500 rounded-lg p-3 min-h-[120px] resize-y transition-colors w-full outline-none" 
            />
            {errors.description && <span className="text-red-500 dark:text-red-400 text-xs mt-2 font-medium flex items-center"><span className="mr-1">⚠</span> {errors.description.message}</span>}
          </div>

          <div className="flex flex-col p-5 bg-white/40 dark:bg-neutral-950/40 rounded-xl border border-slate-200 dark:border-white/5 hover:border-slate-300 dark:hover:border-white/10 transition-colors relative group">
            <div className="flex justify-between items-start">
              <div>
                <label className="block text-slate-900 dark:text-white font-medium mb-1">Estatuto / Documento de Comprovação</label>
                <p className="text-xs text-slate-500 dark:text-neutral-400 mb-4">Envie um arquivo PDF comprovando a legalidade da instituição (max 10MB).</p>
              </div>
              <div className="bg-slate-100 dark:bg-white/5 rounded-full p-2 text-slate-500 dark:text-neutral-400 group-hover:text-indigo-600 dark:group-hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
              </div>
            </div>
            
            {/* Escondemos o Input original e apenas o usamos para manter os props do form */}
            <Input label="" type="file" accept=".pdf" {...register("document")} className="file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 text-slate-700 dark:text-neutral-300" />
            
            {errors.document && <span className="text-red-500 dark:text-red-400 text-xs mt-3 font-medium flex items-center"><span className="mr-1">⚠</span> {errors.document.message as string}</span>}
          </div>
        </div>

        {/* CTA (Submit) */}
        <div className="pt-4 flex items-center justify-end">
          <Button 
            type="submit" 
            isLoading={isSubmitting} 
            disabled={!isValid && false} // Optional: block submission visually if wanted, mas mantido disabled pelo Zod ao clicar
            className="w-full md:w-auto px-8 py-3 bg-indigo-600 dark:bg-white text-white dark:text-black hover:bg-indigo-700 dark:hover:bg-neutral-200 font-semibold rounded-lg shadow-[0_0_20px_rgba(79,70,229,0.2)] dark:shadow-[0_0_20px_rgba(255,255,255,0.1)] transition-all"
          >
            Submeter Solicitação de Análise
          </Button>
        </div>

      </form>
    </motion.div>
  );
}
