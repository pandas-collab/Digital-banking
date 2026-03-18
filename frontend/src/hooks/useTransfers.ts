import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { transferApi } from '../services/transferApi';
import { CreateTransferRequest } from '../types/transfer.types';

export const useTransfers = (page: number = 1, size: number = 10) => {
  return useQuery({
    queryKey: ['transfers', page, size],
    queryFn: () => transferApi.getTransfers(page, size),
  });
};

export const useCreateTransfer = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateTransferRequest) => transferApi.createTransfer(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transfers'] });
    },
  });
};
