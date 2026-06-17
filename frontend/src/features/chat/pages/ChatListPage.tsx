import { Link } from '@tanstack/react-router';
import { useChats } from '../hooks/useChat';
import { useAuth } from '@/features/auth/hooks/useAuth';

export function ChatListPage() {
  const { data: chats, isLoading } = useChats();
  const { user } = useAuth();

  if (isLoading) {
    return (
      <div className="flex h-[50vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="mb-8 text-3xl font-black tracking-tight text-slate-900 dark:text-white">
        Minhas Mensagens
      </h1>

      {!chats || chats.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-3xl bg-white/50 dark:bg-neutral-900/50 p-12 text-center backdrop-blur-sm border border-slate-200 dark:border-white/5">
          <div className="mb-4 text-6xl">💬</div>
          <h2 className="mb-2 text-xl font-bold text-slate-700 dark:text-neutral-200">
            Nenhuma conversa ainda
          </h2>
          <p className="text-slate-500 dark:text-neutral-400">
            Quando você demonstrar interesse em um pet ou alguém entrar em contato com você, as conversas aparecerão aqui.
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          {chats.map((chat) => (
            <Link
              key={chat.id}
              to={`/chats/$roomId`}
              params={{ roomId: chat.id }}
              className="group relative flex items-center gap-6 rounded-2xl bg-white dark:bg-neutral-900 p-4 shadow-sm transition-all hover:shadow-md hover:-translate-y-0.5 border border-slate-100 dark:border-white/5"
            >
              {chat.unread_count > 0 && (
                <div className="absolute -left-2 -top-2 flex h-6 w-6 items-center justify-center rounded-full bg-red-500 text-xs font-bold text-white shadow-lg">
                  {chat.unread_count}
                </div>
              )}
              
              <div className="h-16 w-16 shrink-0 overflow-hidden rounded-xl bg-slate-100 dark:bg-neutral-800">
                {chat.publication_image_url ? (
                  <img 
                    src={chat.publication_image_url.startsWith('http') ? chat.publication_image_url : `http://localhost:8000${chat.publication_image_url}`} 
                    alt={chat.publication_title}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <div className="flex h-full w-full items-center justify-center text-2xl">🐾</div>
                )}
              </div>

              <div className="flex flex-1 flex-col justify-center overflow-hidden">
                <div className="flex items-center justify-between">
                  <h3 className="truncate text-lg font-bold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                    {chat.other_user_name}
                  </h3>
                  {chat.last_message_at && (
                    <span className="shrink-0 text-xs text-slate-500 dark:text-neutral-500">
                      {new Date(chat.last_message_at).toLocaleDateString()}
                    </span>
                  )}
                </div>
                
                <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-neutral-400">
                  <span className="font-semibold px-2 py-0.5 bg-indigo-50 text-indigo-600 dark:bg-indigo-500/10 dark:text-indigo-400 rounded-md text-xs">
                    {chat.publication_title}
                  </span>
                  <p className="truncate flex-1">
                    {chat.last_message || "Iniciar conversa"}
                  </p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
