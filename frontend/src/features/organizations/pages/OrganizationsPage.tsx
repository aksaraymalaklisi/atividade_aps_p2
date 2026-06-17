import { OrganizationForm } from "../components/OrganizationForm";
import { AdminApprovalPanel } from "../components/AdminApprovalPanel";
import { useAuth } from "@/features/auth/hooks/useAuth";
import { useOrganizations } from "../hooks/useOrganizations";
import { motion } from "framer-motion";

export function OrganizationsPage() {
  const { user } = useAuth();
  const { organizations, isLoading } = useOrganizations();

  // If the user is an operator/admin, show the approval panel
  if (user?.is_staff || user?.is_operator) {
    return (
      <div className="min-h-screen pt-24 pb-12 px-4">
        <AdminApprovalPanel />
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const myOrg = organizations?.find(org => org.is_owner);

  if (myOrg) {
    return (
      <div className="min-h-screen pt-24 pb-12 px-4 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white/80 dark:bg-neutral-900/60 backdrop-blur-xl border border-slate-200 dark:border-white/10 rounded-3xl p-8 max-w-2xl w-full text-center shadow-xl"
        >
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white mb-4">Sua ONG</h2>
          <div className="bg-slate-50 dark:bg-black/20 rounded-2xl p-6 border border-slate-200 dark:border-white/5 inline-block text-left w-full">
            <p className="text-slate-500 dark:text-neutral-400 text-sm font-semibold uppercase mb-1">Nome</p>
            <p className="text-lg font-bold text-slate-900 dark:text-white mb-4">{myOrg.name}</p>
            
            <p className="text-slate-500 dark:text-neutral-400 text-sm font-semibold uppercase mb-1">Status da Solicitação</p>
            <p className={`text-lg font-bold ${
              myOrg.status === 'APPROVED' ? 'text-green-600 dark:text-green-400' :
              myOrg.status === 'REJECTED' ? 'text-red-600 dark:text-red-400' :
              'text-yellow-600 dark:text-yellow-400'
            }`}>
              {myOrg.status === 'APPROVED' ? 'Aprovada' :
               myOrg.status === 'REJECTED' ? 'Rejeitada' :
               'Em Análise (Pendente)'}
            </p>
          </div>
          <p className="mt-6 text-slate-600 dark:text-neutral-400">
            {myOrg.status === 'PENDING' && "Sua solicitação está sendo revisada por nossa equipe. Aguarde nosso retorno."}
            {myOrg.status === 'APPROVED' && "Parabéns! Sua ONG foi aprovada. Em breve você poderá publicar animais para adoção."}
            {myOrg.status === 'REJECTED' && "Sua solicitação não pôde ser aprovada neste momento. Entre em contato com o suporte para mais detalhes."}
          </p>
        </motion.div>
      </div>
    );
  }

  // Otherwise, show the registration form
  return (
    <div className="min-h-screen pt-24 pb-12 px-4">
      <OrganizationForm />
    </div>
  );
}
