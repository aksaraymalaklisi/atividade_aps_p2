import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { organizationsApi } from "../api/organizationsApi";

export const useOrganizations = () => {
  const queryClient = useQueryClient();

  const organizationsQuery = useQuery({
    queryKey: ["organizations"],
    queryFn: organizationsApi.getAll,
  });

  const createMutation = useMutation({
    mutationFn: organizationsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] });
    },
  });

  const approveMutation = useMutation({
    mutationFn: organizationsApi.approve,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] });
    },
  });

  const rejectMutation = useMutation({
    mutationFn: ({ id, reason }: { id: string; reason: string }) =>
      organizationsApi.reject(id, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] });
    },
  });

  return {
    organizations: organizationsQuery.data,
    isLoading: organizationsQuery.isLoading,
    createOrganization: createMutation.mutateAsync,
    approveOrganization: approveMutation.mutateAsync,
    rejectOrganization: rejectMutation.mutateAsync,
  };
};
