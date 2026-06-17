import { axiosClient } from "@/shared/api/axiosClient";
import type { Organization } from "@/features/organizations/api/organizationsApi";

export interface PetImage {
  id: string;
  image: string;
  is_primary: boolean;
  order: number;
}

export interface Pet {
  id: string;
  name: string;
  species: string;
  breed: string;
  size: "SMALL" | "MEDIUM" | "LARGE";
  gender: "MALE" | "FEMALE" | "UNKNOWN";
  approximate_age: number;
  description: string;
  vaccinated: boolean;
  neutered: boolean;
  images: PetImage[];
}

export interface Publication {
  id: string;
  publisher_id: string;
  publisher_name: string;
  organization_id: string | null;
  organization: Organization | null;
  status: "ACTIVE" | "ADOPTED" | "REMOVED";
  created_at: string;
  updated_at: string;
  pet: Pet;
  can_edit?: boolean;
}

export interface PublicationsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Publication[];
}

export const publicationsApi = {
  getAll: async (params?: Record<string, string | number>): Promise<PublicationsResponse> => {
    const response = await axiosClient.get("publications/", { params });
    // Handle both paginated and non-paginated responses gracefully
    if (response.data.results) {
      return response.data;
    }
    return {
      count: response.data.length || 0,
      next: null,
      previous: null,
      results: response.data,
    };
  },

  getById: async (id: string): Promise<Publication> => {
    const response = await axiosClient.get(`publications/${id}/`);
    return response.data;
  },

  create: async (data: FormData): Promise<Publication> => {
    const response = await axiosClient.post("publications/", data, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },

  update: async (params: { id: string, data: FormData }): Promise<Publication> => {
    const response = await axiosClient.patch(`publications/${params.id}/`, params.data, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await axiosClient.delete(`publications/${id}/`);
  },

  markAdopted: async (id: string): Promise<Publication> => {
    const response = await axiosClient.post(`publications/${id}/mark_adopted/`);
    return response.data;
  },
};
