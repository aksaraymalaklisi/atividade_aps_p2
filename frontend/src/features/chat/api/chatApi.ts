import { axiosClient } from '@/shared/api/axiosClient';

export interface ChatRoom {
  id: string;
  publication_id: string;
  interested_user_id: string;
  publisher_user_id: string;
  created_at: string;
  publication_title: string;
  publication_image_url: string | null;
  other_user_id: string;
  other_user_name: string;
  last_message: string | null;
  last_message_at: string | null;
  unread_count: number;
}

export interface ChatMessage {
  id: string;
  sender_id: string;
  content: string;
  message_type: 'TEXT' | 'CONTACT_SHARE' | 'ADDRESS_SHARE';
  is_read: boolean;
  sent_at: string;
}

export const chatApi = {
  listChats: async (): Promise<ChatRoom[]> => {
    const { data } = await axiosClient.get<ChatRoom[]>('/chats/');
    return data;
  },

  startChat: async (publication_id: string): Promise<{ room_id: string }> => {
    const { data } = await axiosClient.post<{ room_id: string }>('/chats/', { publication_id });
    return data;
  },

  getUnreadCount: async (): Promise<{ unread_count: number }> => {
    const { data } = await axiosClient.get<{ unread_count: number }>('/chats/unread-count/');
    return data;
  },

  listMessages: async (room_id: string): Promise<ChatMessage[]> => {
    const { data } = await axiosClient.get<ChatMessage[]>(`/chats/${room_id}/messages/`);
    return data;
  },

  sendMessage: async (room_id: string, content: string, message_type: 'TEXT' | 'CONTACT_SHARE' | 'ADDRESS_SHARE' = 'TEXT'): Promise<{ message_id: string }> => {
    const { data } = await axiosClient.post<{ message_id: string }>(`/chats/${room_id}/messages/send/`, {
      content,
      message_type,
    });
    return data;
  },

  markAsRead: async (room_id: string): Promise<{ updated_count: number }> => {
    const { data } = await axiosClient.post<{ updated_count: number }>(`/chats/${room_id}/messages/read/`);
    return data;
  },
};
