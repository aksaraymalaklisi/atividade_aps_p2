import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { publicationsApi } from "../api/publicationsApi";

export function usePublications(params?: Record<string, string | number>) {
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery({
    queryKey: ["publications", params],
    queryFn: () => publicationsApi.getAll(params),
  });

  const createMutation = useMutation({
    mutationFn: publicationsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["publications"] });
    },
  });

  return {
    publications: data?.results || [],
    count: data?.count || 0,
    isLoading,
    error,
    createPublication: createMutation.mutateAsync,
    isCreating: createMutation.isPending,
  };
}

export function usePublication(id: string) {
  const { data, isLoading, error } = useQuery({
    queryKey: ["publications", id],
    queryFn: () => publicationsApi.getById(id),
    enabled: !!id,
  });

  return {
    publication: data,
    isLoading,
    error,
  };
}
