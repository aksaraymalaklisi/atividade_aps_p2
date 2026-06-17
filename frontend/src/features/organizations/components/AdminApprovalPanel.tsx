import { motion } from "framer-motion";
import { useOrganizations } from "../hooks/useOrganizations";
import { Button } from "@/shared/components/ui/Button";

export function AdminApprovalPanel() {
  const { organizations, isLoading, approveOrganization, rejectOrganization } = useOrganizations();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const pendingOrgs = organizations?.filter((org) => org.status === "PENDING") || [];

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <div className="mb-8 border-b border-slate-200 dark:border-white/10 pb-4">
        <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">Painel de Auditoria de ONGs</h2>
        <p className="text-slate-600 dark:text-neutral-400 mt-2">Revise as solicitações pendentes e valide os documentos comprobatórios.</p>
      </div>
      
      {pendingOrgs.length === 0 ? (
        <div className="bg-white/60 dark:bg-neutral-900/50 backdrop-blur-md border border-slate-200 dark:border-white/5 rounded-2xl p-12 text-center shadow-sm dark:shadow-none">
          <div className="text-slate-400 dark:text-neutral-500 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-16 h-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          </div>
          <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">Fila de Auditoria Limpa</h3>
          <p className="text-slate-600 dark:text-neutral-400">Não há ONGs aguardando revisão no momento.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {pendingOrgs.map((org) => (
            <motion.div
              key={org.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white/80 dark:bg-neutral-900/60 backdrop-blur-xl border border-slate-200 dark:border-white/10 rounded-2xl p-6 shadow-xl dark:shadow-2xl relative overflow-hidden transition-colors"
            >
              {/* Highlight Bar */}
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-yellow-500"></div>

              <div className="flex flex-col lg:flex-row gap-8">
                {/* Org Info */}
                <div className="flex-1 space-y-4">
                  <div>
                    <h3 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center">
                      {org.name}
                      <span className="ml-3 text-[10px] font-bold uppercase tracking-wider bg-yellow-100 text-yellow-700 dark:bg-yellow-500/20 dark:text-yellow-400 px-2 py-1 rounded-full border border-yellow-200 dark:border-yellow-500/30">
                        Pendente
                      </span>
                    </h3>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-y-4 gap-x-8 bg-slate-50 dark:bg-black/20 p-4 rounded-xl border border-slate-200 dark:border-white/5 transition-colors">
                    <div>
                      <p className="text-xs text-slate-500 dark:text-neutral-500 uppercase font-semibold">CNPJ</p>
                      <p className="text-slate-800 dark:text-neutral-200 font-mono mt-0.5">{org.cnpj || "Não informado"}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500 dark:text-neutral-500 uppercase font-semibold">E-mail</p>
                      <p className="text-slate-800 dark:text-neutral-200 mt-0.5">{org.email || "Não informado"}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500 dark:text-neutral-500 uppercase font-semibold">Telefone</p>
                      <p className="text-slate-800 dark:text-neutral-200 mt-0.5">{org.phone || "Não informado"}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500 dark:text-neutral-500 uppercase font-semibold">Sede</p>
                      <p className="text-slate-800 dark:text-neutral-200 text-sm mt-0.5">{org.address || "Não informado"}</p>
                    </div>
                  </div>

                  <div>
                    <p className="text-xs text-slate-500 dark:text-neutral-500 uppercase font-semibold mb-1">Apresentação Institucional</p>
                    <p className="text-slate-700 dark:text-neutral-300 text-sm leading-relaxed bg-slate-50 dark:bg-black/20 p-4 rounded-xl border border-slate-200 dark:border-white/5 transition-colors">
                      {org.description}
                    </p>
                  </div>
                </div>

                <div className="w-full lg:w-72 flex flex-col justify-between border-t lg:border-t-0 lg:border-l border-slate-200 dark:border-white/10 pt-6 lg:pt-0 lg:pl-6 space-y-6">
                  
                  {/* Document Card */}
                  {org.document_url ? (
                    <div className="bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-500/30 rounded-xl p-4 flex flex-col items-center justify-center text-center transition-colors">
                      <div className="text-indigo-500 dark:text-indigo-400 mb-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>
                      </div>
                      <p className="text-sm text-indigo-700 dark:text-indigo-200 font-medium mb-3">Estatuto Comprobatório</p>
                      <a
                        href={`http://localhost:8000${org.document_url}`}
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs font-semibold uppercase tracking-wider bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg transition-colors w-full"
                      >
                        Abrir PDF
                      </a>
                    </div>
                  ) : (
                    <div className="bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-500/20 rounded-xl p-4 text-center transition-colors">
                      <p className="text-xs text-red-600 dark:text-red-400 font-semibold">Sem documento anexado</p>
                    </div>
                  )}

                  {/* Approve / Reject Buttons */}
                  <div className="flex flex-col gap-3">
                    <Button
                      onClick={() => approveOrganization(org.id)}
                      className="bg-green-600 hover:bg-green-500 text-white w-full py-6 font-bold shadow-[0_0_15px_rgba(34,197,94,0.2)]"
                    >
                      Aprovar Cadastro
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => {
                        const reason = prompt("Justificativa da rejeição (obrigatório):");
                        if (reason && reason.trim() !== "") {
                          rejectOrganization({ id: org.id, reason });
                        }
                      }}
                      className="border-red-500/50 text-red-600 dark:text-red-400 hover:bg-red-500/10 hover:text-red-700 dark:hover:text-red-300 w-full transition-colors"
                    >
                      Rejeitar Solicitação
                    </Button>
                  </div>

                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
