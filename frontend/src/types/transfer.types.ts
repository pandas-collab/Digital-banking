export interface Transfer {
  id: string;
  fromAccount: string;
  toAccount: string;
  amount: number;
  status: 'PENDING' | 'COMPLETED' | 'FAILED';
  createdAt: string;
}

export interface CreateTransferRequest {
  fromAccount: string;
  toAccount: string;
  amount: number;
}

export interface TransferListResponse {
  data: Transfer[];
  total: number;
  page: number;
  size: number;
}
