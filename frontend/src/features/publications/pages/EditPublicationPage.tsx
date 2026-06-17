import { useParams, useNavigate } from "@tanstack/react-router";
import { usePublication } from "../hooks/usePublications";
import { PublicationForm } from "../components/PublicationForm";

export function EditPublicationPage() {
  const params = useParams({ strict: false });
  const id = params.id ?? "";
  const navigate = useNavigate();
  const { publication, isLoading, error } = usePublication(id);

  if (isLoading) {
    return (
      <div className="min-h-screen pt-24 pb-12 flex justify-center items-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error || !publication) {
    return (
      <div className="min-h-screen pt-24 pb-12 flex justify-center items-center flex-col gap-4 text-center px-4">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Publicação não encontrada</h2>
        <p className="text-slate-600 dark:text-slate-400">Não foi possível carregar os dados desta publicação para edição.</p>
        <button 
          onClick={() => navigate({ to: "/" })}
          className="px-6 py-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700"
        >
          Voltar ao Início
        </button>
      </div>
    );
  }

  if (!publication.can_edit) {
    return (
      <div className="min-h-screen pt-24 pb-12 flex justify-center items-center flex-col gap-4 text-center px-4">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Acesso Negado</h2>
        <p className="text-slate-600 dark:text-slate-400">Você não tem permissão para editar esta publicação.</p>
        <button 
          onClick={() => navigate({ to: "/pet/$id", params: { id } })}
          className="px-6 py-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700"
        >
          Voltar para Publicação
        </button>
      </div>
    );
  }

  return <PublicationForm initialData={publication} />;
}
