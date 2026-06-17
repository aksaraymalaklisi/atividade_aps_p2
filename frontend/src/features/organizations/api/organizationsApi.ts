import { axiosClient } from "@/shared/api/axiosClient";

export interface Organization {
  id: string;
  name: string;
  cnpj: string;
  email: string;
  phone: string;
  address: string;
  description: string;
  document_url: string;
  status: "PENDING" | "APPROVED" | "REJECTED";
  created_at: string;
  is_owner?: boolean;
}

export const organizationsApi = {
  create: async (data: FormData): Promise<Organization> => {
    const response = await axiosClient.post("organizations/", data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  },
  
  approve: async (id: string): Promise<void> => {
    await axiosClient.post(`organizations/${id}/approve/`);
  },

  reject: async (id: string, reason: string): Promise<void> => {
    await axiosClient.post(`organizations/${id}/reject/`, { reason });
  },

  getAll: async (): Promise<Organization[]> => {
    const response = await axiosClient.get("organizations/");
    return response.data.results || response.data;
  }
};
