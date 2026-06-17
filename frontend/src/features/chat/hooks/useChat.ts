import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { chatApi } from '../api/chatApi';

export function useChats() {
  return useQuery({
    queryKey: ['chats'],
    queryFn: chatApi.listChats,
  });
}

export function useUnreadCount(enabled: boolean = true) {
  return useQuery({
    queryKey: ['chats', 'unreadCount'],
    queryFn: chatApi.getUnreadCount,
    refetchInterval: 10000, // Poll every 10 seconds globally
    enabled,
  });
}

export function useChatMessages(roomId: string | undefined) {
  return useQuery({
    queryKey: ['chats', roomId, 'messages'],
    queryFn: () => chatApi.listMessages(roomId!),
    enabled: !!roomId,
    refetchInterval: 3000, // Poll every 3 seconds inside the room
  });
}

export function useStartChat() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (publicationId: string) => chatApi.startChat(publicationId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chats'] });
    },
  });
}

export function useSendMessage() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ 
      roomId, 
      content, 
      messageType = 'TEXT' 
    }: { 
      roomId: string; 
      content: string; 
      messageType?: 'TEXT' | 'CONTACT_SHARE' | 'ADDRESS_SHARE';
    }) => chatApi.sendMessage(roomId, content, messageType),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['chats', variables.roomId, 'messages'] });
      queryClient.invalidateQueries({ queryKey: ['chats'] });
    },
  });
}

export function useMarkAsRead() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (roomId: string) => chatApi.markAsRead(roomId),
    onSuccess: (_, roomId) => {
      queryClient.invalidateQueries({ queryKey: ['chats', roomId, 'messages'] });
      queryClient.invalidateQueries({ queryKey: ['chats', 'unreadCount'] });
      queryClient.invalidateQueries({ queryKey: ['chats'] });
    },
  });
}
