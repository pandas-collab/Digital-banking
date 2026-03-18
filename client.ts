// API client for backend communication
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  success: boolean;
}

export interface LoanApplicationRequest {
  applicantName: string;
  amount: number;
  term: number;
  annualIncome: number;
  employmentStatus: string;
}

export interface LoanApplication extends LoanApplicationRequest {
  id: string;
  status: 'pending' | 'approved' | 'rejected';
  createdAt: string;
}

export const api = {
  async submitLoanApplication(data: LoanApplicationRequest): Promise<ApiResponse<LoanApplication>> {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));

      const application: LoanApplication = {
        ...data,
        id: `loan_${Date.now()}`,
        status: 'pending',
        createdAt: new Date().toISOString()
      };

      return {
        success: true,
        data: application
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }
};
