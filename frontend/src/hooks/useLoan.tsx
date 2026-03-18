import { useCallback } from 'react';
import { loanClient } from '../api/loanClient';
import { LoanCreateRequest, LoanResponse } from '../api/loanClient';

export const useLoan = () => {
  const createLoan = useCallback(async (request: LoanCreateRequest, accountId: number) => {
    return loanClient.create(request, accountId);
  }, []);

  const getLoan = useCallback(async (loanId: number): Promise<LoanResponse> => {
    return loanClient.get(loanId);
  }, []);

  return { createLoan, getLoan };
};
