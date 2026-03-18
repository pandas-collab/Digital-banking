import React, { useState, useEffect } from 'react';

interface Transfer {
  id: string;
  from: string;
  to: string;
  amount: number;
  timestamp: string;
  status: 'completed' | 'pending' | 'failed';
}

interface TransferHistoryProps {
  apiEndpoint?: string;
  pageSize?: number;
}

const TransferHistory: React.FC<TransferHistoryProps> = ({
  apiEndpoint = '/api/transfers',
  pageSize = 5
}) => {
  const [transfers, setTransfers] = useState<Transfer[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);

  const validateTransfer = (transfer: any): transfer is Transfer => {
    return (
      transfer &&
      typeof transfer.id === 'string' &&
      typeof transfer.from === 'string' &&
      typeof transfer.to === 'string' &&
      typeof transfer.amount === 'number' &&
      typeof transfer.timestamp === 'string' &&
      ['completed', 'pending', 'failed'].includes(transfer.status)
    );
  };

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (timestamp: string): string => {
    try {
      return new Date(timestamp).toLocaleString();
    } catch (e) {
      console.error('Invalid date:', timestamp);
      return 'Invalid date';
    }
  };

  const getStatusColor = (status: Transfer['status']): string => {
    const colors = {
      completed: 'text-green-600 bg-green-50',
      pending: 'text-yellow-600 bg-yellow-50',
      failed: 'text-red-600 bg-red-50'
    };
    return colors[status] || 'text-gray-600 bg-gray-50';
  };

  const fetchTransfers = async (page: number) => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: pageSize.toString()
      });

      const response = await fetch(`${apiEndpoint}?${params}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (!data.transfers || !Array.isArray(data.transfers)) {
        throw new Error('Invalid response format');
      }

      const validatedTransfers = data.transfers.filter(validateTransfer);

      if (validatedTransfers.length !== data.transfers.length) {
        console.warn('Some transfers were invalid and filtered out');
      }

      setTransfers(validatedTransfers);
      setTotalPages(Math.max(1, Math.ceil(data.total / pageSize)));

      console.log(`Fetched ${validatedTransfers.length} transfers for page ${page}`);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      console.error('Failed to fetch transfers:', errorMessage);
      setError(`Failed to load transfers: ${errorMessage}`);

      // Fallback to mock data for development
      if (process.env.NODE_ENV === 'development') {
        const mockTransfers: Transfer[] = [
          {
            id: '1',
            from: 'Alice',
            to: 'Bob',
            amount: 100,
            timestamp: new Date(Date.now() - 86400000).toISOString(),
            status: 'completed'
          },
          {
            id: '2',
            from: 'Charlie',
            to: 'Diana',
            amount: 250,
            timestamp: new Date(Date.now() - 43200000).toISOString(),
            status: 'pending'
          }
        ];
        setTransfers(mockTransfers);
        setTotalPages(1);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransfers(currentPage);
  }, [currentPage, pageSize]);

  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages && newPage !== currentPage) {
      console.log(`Changing to page ${newPage}`);
      setCurrentPage(newPage);
    }
  };

  const Pagination = () => {
    if (totalPages <= 1) return null;

    return (
      <div className="flex items-center justify-between mt-4">
        <div className="text-sm text-gray-700">
          Page {currentPage} of {totalPages}
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage <= 1 || loading}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <button
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage >= totalPages || loading}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      </div>
    );
  };

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-md">
        <h3 className="text-lg font-medium text-red-800">Error</h3>
        <p className="mt-2 text-sm text-red-700">{error}</p>
        <button
          onClick={() => fetchTransfers(currentPage)}
          className="mt-2 px-3 py-1 text-sm font-medium text-red-700 bg-red-100 border border-red-300 rounded-md hover:bg-red-200"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4" data-testid="transfer-history">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-900">Transfer History</h2>
        {loading && (
          <div className="text-sm text-gray-600">
            Loading...
          </div>
        )}
      </div>

      {transfers.length === 0 ? (
        <p className="text-center py-8 text-gray-500">
          {loading ? 'Loading transfers...' : 'No transfers found'}
        </p>
      ) : (
        <div className="space-y-2">
          {transfers.map((transfer) => (
            <div
              key={transfer.id}
              data-testid={`transfer-${transfer.id}`}
              className="p-4 bg-white border border-gray-200 rounded-lg shadow-sm"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">
                    From: {transfer.from} -> To: {transfer.to}
                  </p>
                  <p className="text-sm text-gray-600">
                    {formatDate(transfer.timestamp)}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-gray-900">
                    {formatCurrency(transfer.amount)}
                  </p>
                  <span
                    className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(
                      transfer.status
                    )}`}
                  >
                    {transfer.status}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <Pagination />
    </div>
  );
};

export default TransferHistory;
