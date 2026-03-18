import axios from 'axios';
import { API_ENDPOINTS } from '../config/endpoints';

export interface CreateLoanApplicationRequest {
  amount: number;
  term_months: number;
  purpose: string;
  annual_income: number;
  employment_status: string;
}

export interface LoanApplication {
  id: string;
  amount: number;
  term_months: number;
  interest_rate: number;
  status: 'pending' | 'approved' | 'rejected' | 'under_review' | 'funded';
  purpose: string;
  annual_income: number;
  employment_status: string;
  credit_score?: number;
  submitted_at: string;
}

export const loanService = {
  async createApplication(params: CreateLoanApplicationRequest): Promise<LoanApplication> {
    const response = await axios.post(API_ENDPOINTS.loans.create, params);
    return response.data;
  },

  async getUserApplications(): Promise<LoanApplication[]> {
    const response = await axios.get(API_ENDPOINTS.loans.list);
    return response.data;
  },

  async getApplication(id: string): Promise<LoanApplication> {
    const response = await axios.get(API_ENDPOINTS.loans.detail(id));
    return response.data;
  }
};
