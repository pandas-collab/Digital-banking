import { apiClient } from "./apiClient";

export interface PolicyCreateRequest {
  coverageType: string;
  coverageAmount: number;
  premiumMonthly: number;
}

export interface Policy {
  id: number;
  coverageType: string;
  coverageAmount: number;
  premiumMonthly: number;
  status: string;
  nextPremiumDate: string;
  balanceDue?: number;
}

export const policyApi = {
  purchasePolicy: (payload: PolicyCreateRequest) =>
    apiClient.post<Policy>("/api/v1/policies", payload),
  getPolicy: (id: number) => apiClient.get<Policy>(`/api/v1/policies/${id}`),
};
