import React, { useState, useEffect } from 'react';

interface Loan {
  id: string;
  userId: string;
  amount: number;
  term: string;
  rate: number;
  status: 'ACTIVE' | 'COMPLETED' | 'DEFAULT';
  dueDate: string;
  outstanding: number;
}

interface LoanDashboardProps {
  userId?: string;
}

const LoanDashboard: React.FC<LoanDashboardProps> = ({ userId }) => {
  const [loans, setLoans] = useState<Loan[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLoan, setSelectedLoan] = useState<Loan | null>(null);

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const fetchLoans = async () => {
    setLoading(true);
    setError(null);

    try {
      const url = userId ? `${API_BASE}/api/loans?userId=${userId}` : `${API_BASE}/api/loans`;
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      if (!Array.isArray(data)) {
        throw new Error('Invalid response format: expected array');
      }

      // Validate loan data structure
      const validLoans = data.filter(validateLoan).slice(0, 20); // Limit to 20 loans
      setLoans(validLoans);

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch loans';
      console.error(' Loan fetch error:', errorMessage);
      setError(errorMessage);
      setLoans(generateSampleLoans());
    } finally {
      setLoading(false);
    }
  };

  const validateLoan = (loan: unknown): loan is Loan => {
    if (!loan || typeof loan !== 'object') return false;

    const l = loan as any;
    return !!(l.id && l.amount && l.status && l.userId && l.dueDate);
  };

  const generateSampleLoans = (): Loan[] => {
    const users = ['user1', 'user2', 'user3'];
    const statuses: ('ACTIVE' | 'COMPLETED' | 'DEFAULT')[] = ['ACTIVE', 'COMPLETED', 'DEFAULT'];

    return Array.from({ length: 5 }, (_, i) => ({
      id: `loan-${Date.now()}-${i}`,
      userId: users[i % 3],
      amount: Math.round(Math.random() * 50000 + 1000),
      term: `${Math.floor(Math.random() * 36) + 6} months`,
      rate: Math.round((Math.random() * 10 + 5) * 100) / 100,
      status: statuses[Math.floor(Math.random() * 3)],
      dueDate: new Date(Date.now() + Math.random() * 1000 * 60 * 60 * 24 * 365).toISOString().split('T')[0],
      outstanding: Math.round(Math.random() * 40000 + 500),
    }));
  };

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const getStatusColor = (status: string): string => {
    const colors = {
      ACTIVE: '#10b981',
      COMPLETED: '#3b82f6',
      DEFAULT: '#ef4444',
    };
    return colors[status as keyof typeof colors] || '#6b7280';
  };

  useEffect(() => {
    fetchLoans();
    const interval = setInterval(fetchLoans, 30000);
    return () => clearInterval(interval);
  }, [userId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error && !loans.length) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-lg font-semibold text-red-800"> Error Loading Loans</h3>
        <p className="mt-2 text-red-600">{error}</p>
        <button
          onClick={fetchLoans}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Loan Dashboard</h1>
        <button
          onClick={fetchLoans}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Refresh
        </button>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded text-yellow-800">
           {error} (Showing sample data)
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 bg-gray-50 border-b">
            <h2 className="text-xl font-semibold">Active Loans</h2>
            <p className="text-sm text-gray-600">{loans.length} loans found</p>
          </div>

          <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
            {loans.map((loan) => (
              <div
                key={loan.id}
                className="p-4 hover:bg-gray-50 cursor-pointer transition"
                onClick={() => setSelectedLoan(loan)}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-900">{formatCurrency(loan.amount)}</p>
                    <p className="text-sm text-gray-500">User {loan.userId}</p>
                  </div>
                  <div className="text-right">
                    <span
                      className="px-2 py-1 text-xs font-semibold rounded-full text-white"
                      style={{ backgroundColor: getStatusColor(loan.status) }}
                    >
                      {loan.status}
                    </span>
                    <p className="text-sm text-gray-500 mt-1">Due: {loan.dueDate}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 bg-gray-50 border-b">
            <h2 className="text-xl font-semibold">Loan Details</h2>
          </div>

          {!selectedLoan ? (
            <div className="p-8 text-center text-gray-500">
              Select a loan to view details
            </div>
          ) : (
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Loan ID</label>
                <p className="mt-1 text-gray-900">{selectedLoan.id}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Amount</label>
                <p className="mt-1 text-2xl font-bold">{formatCurrency(selectedLoan.amount)}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Outstanding</label>
                <p className="mt-1 text-lg">{formatCurrency(selectedLoan.outstanding)}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Term</label>
                  <p className="mt-1 text-gray-900">{selectedLoan.term}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Rate</label>
                  <p className="mt-1 text-gray-900">{selectedLoan.rate}%</p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Due Date</label>
                <p className="mt-1 text-gray-900">{selectedLoan.dueDate}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LoanDashboard;
