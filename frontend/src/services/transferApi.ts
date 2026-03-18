import { apiClient } from './client';
import { CreateTransferRequest, Transfer, TransferListResponse } from '../types/transfer.types';

export const transferApi = {
  async createTransfer(data: CreateTransferRequest): Promise<Transfer> {
    const response = await apiClient.post('/transfers', data);
    return response.data;
  },

  async getTransfers(page: number = 1, size: number = 10): Promise<TransferListResponse> {
    const response = await apiClient.get('/transfers', {
      params: { page, size }
    });
    return response.data;
  }
};
