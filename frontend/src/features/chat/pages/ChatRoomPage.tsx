import { useState, useEffect, useRef } from 'react';
import { useParams, Link } from '@tanstack/react-router';
import { useAuth } from '@/features/auth/hooks/useAuth';
import { useChats, useChatMessages, useSendMessage, useMarkAsRead } from '../hooks/useChat';
import { Button } from '@/shared/components/ui/Button';

export function ChatRoomPage() {
  const { roomId } = useParams({ strict: false });
  const { user } = useAuth();
  const [newMessage, setNewMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Actually we need the specific chat room details. We can find it from the list.
  const { data: chats } = useChats();
  const room = chats?.find(c => c.id === roomId);
  
  const { data: messages, isLoading } = useChatMessages(roomId);
  const sendMessageMutation = useSendMessage();
  const markAsReadMutation = useMarkAsRead();

  // Scroll to bottom when messages load
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Mark as read when entering/updating
  useEffect(() => {
    if (roomId && messages && messages.some(m => !m.is_read && m.sender_id !== user?.id)) {
      markAsReadMutation.mutate(roomId);
    }
  }, [roomId, messages, user?.id]);

  if (!room && !isLoading) {
    return <div>Chat não encontrado.</div>;
  }

  const isPublisher = room?.publisher_user_id === user?.id;

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim() || !roomId) return;
    
    sendMessageMutation.mutate({ roomId, content: newMessage });
    setNewMessage('');
  };

  const handleShareContact = () => {
    if (!roomId) return;
    sendMessageMutation.mutate({ 
      roomId, 
      content: "Compartilhou contato", 
      messageType: 'CONTACT_SHARE' 
    });
  };

  const handleShareAddress = () => {
    if (!roomId) return;
    sendMessageMutation.mutate({ 
      roomId, 
      content: "Compartilhou endereço", 
      messageType: 'ADDRESS_SHARE' 
    });
  };

  return (
    <div className="mx-auto flex max-w-4xl flex-col h-[calc(100vh-12rem)] bg-white dark:bg-neutral-900 rounded-3xl shadow-sm border border-slate-200 dark:border-white/5 overflow-hidden">
      
      {/* Header */}
      <header className="flex items-center justify-between border-b border-slate-200 dark:border-white/10 p-4 bg-slate-50 dark:bg-neutral-950/50">
        <div className="flex items-center gap-4">
          <Link to="/chats" className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-200 dark:bg-neutral-800 hover:bg-slate-300 dark:hover:bg-neutral-700 transition-colors">
            ←
          </Link>
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 overflow-hidden rounded-full bg-slate-200 dark:bg-neutral-800">
              {room?.publication_image_url && (
                <img 
                  src={room.publication_image_url.startsWith('http') ? room.publication_image_url : `${import.meta.env.VITE_BACKEND_BASE || 'http://localhost:8000'}${room.publication_image_url}`} 
                  alt={room.publication_title}
                  className="h-full w-full object-cover"
                />
              )}
            </div>
            <div>
              <h2 className="font-bold leading-tight">{room?.other_user_name}</h2>
              <p className="text-xs text-slate-500">Sobre: {room?.publication_title}</p>
            </div>
          </div>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50/50 dark:bg-neutral-900/50">
        {messages?.map((msg) => {
          const isMe = msg.sender_id === user?.id;
          
          if (msg.message_type === 'CONTACT_SHARE') {
            return (
              <div key={msg.id} className={`flex ${isMe ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] rounded-2xl p-4 shadow-sm ${isMe ? 'bg-indigo-50 text-indigo-900 dark:bg-indigo-500/20 dark:text-indigo-100' : 'bg-white dark:bg-neutral-800 border border-slate-100 dark:border-white/5'}`}>
                  <div className="flex items-center gap-3 mb-2">
                    <div className="h-10 w-10 rounded-full bg-indigo-100 dark:bg-indigo-500/30 flex items-center justify-center text-xl">📱</div>
                    <div>
                      <p className="font-bold text-sm">Contato Compartilhado</p>
                      <p className="text-xs opacity-70">Enviado por {isMe ? 'você' : room?.other_user_name}</p>
                    </div>
                  </div>
                  <p className="font-mono text-center py-2 bg-white/50 dark:bg-black/20 rounded-lg">
                    [Oculto no MVP]
                  </p>
                </div>
              </div>
            );
          }

          if (msg.message_type === 'ADDRESS_SHARE') {
            return (
              <div key={msg.id} className={`flex ${isMe ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] rounded-2xl p-4 shadow-sm ${isMe ? 'bg-emerald-50 text-emerald-900 dark:bg-emerald-500/20 dark:text-emerald-100' : 'bg-white dark:bg-neutral-800 border border-slate-100 dark:border-white/5'}`}>
                  <div className="flex items-center gap-3 mb-2">
                    <div className="h-10 w-10 rounded-full bg-emerald-100 dark:bg-emerald-500/30 flex items-center justify-center text-xl">📍</div>
                    <div>
                      <p className="font-bold text-sm">Endereço Compartilhado</p>
                      <p className="text-xs opacity-70">Para visita/retirada</p>
                    </div>
                  </div>
                  <p className="text-sm py-2 px-3 bg-white/50 dark:bg-black/20 rounded-lg">
                    [Oculto no MVP]
                  </p>
                </div>
              </div>
            );
          }

          // TEXT
          return (
            <div key={msg.id} className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}>
              <div className={`max-w-[70%] rounded-2xl px-4 py-2 ${
                isMe 
                  ? 'bg-indigo-600 text-white rounded-br-none' 
                  : 'bg-white dark:bg-neutral-800 text-slate-800 dark:text-neutral-200 border border-slate-100 dark:border-white/5 rounded-bl-none shadow-sm'
              }`}>
                <p className="whitespace-pre-wrap break-words text-sm">{msg.content}</p>
              </div>
              <span className="text-[10px] text-slate-400 mt-1 mx-1">
                {new Date(msg.sent_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                {isMe && <span className="ml-1">{msg.is_read ? '✓✓' : '✓'}</span>}
              </span>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>

      {/* Action Bar */}
      {isPublisher && (
        <div className="bg-slate-50 dark:bg-neutral-950/30 p-2 border-t border-slate-200 dark:border-white/5 flex gap-2 overflow-x-auto">
          <button 
            onClick={handleShareContact}
            className="whitespace-nowrap text-xs font-semibold px-4 py-1.5 bg-indigo-100 text-indigo-700 dark:bg-indigo-500/20 dark:text-indigo-300 rounded-full hover:bg-indigo-200 dark:hover:bg-indigo-500/40 transition-colors"
          >
            📱 Compartilhar Contato
          </button>
          <button 
            onClick={handleShareAddress}
            className="whitespace-nowrap text-xs font-semibold px-4 py-1.5 bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300 rounded-full hover:bg-emerald-200 dark:hover:bg-emerald-500/40 transition-colors"
          >
            📍 Compartilhar Endereço
          </button>
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSend} className="flex gap-2 p-4 bg-white dark:bg-neutral-900 border-t border-slate-200 dark:border-white/5">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Digite uma mensagem..."
          className="flex-1 rounded-xl border-0 bg-slate-100 dark:bg-neutral-800 px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500 outline-none transition-shadow"
        />
        <Button 
          type="submit" 
          disabled={!newMessage.trim() || sendMessageMutation.isPending}
          className="rounded-xl px-6"
        >
          Enviar
        </Button>
      </form>
    </div>
  );
}
