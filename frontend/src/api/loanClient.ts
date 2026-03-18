import { apiClient } from './apiClient';

export interface LoanCreateRequest {
  amount: number;
  interestRate: number;
  termMonths: number;
}

export interface LoanResponse {
  id: number;
  amount: number;
  interestRate: number;
  termMonths: number;
  status: string;
  balanceDue: number;
  monthlyRepayment: number;
  nextDueDate?: string;
  createdAt: string;
}

export const loanClient = {
  create: async (request: LoanCreateRequest, accountId: number): Promise<LoanResponse> => {
    const response = await apiClient.post('/loans', request, { params: { account_id: accountId } });
    return response.data;
  },

  get: async (id: number): Promise<LoanResponse> => {
    const response = await apiClient.get(`/loans/${id}`);
    return response.data;
  }
};
