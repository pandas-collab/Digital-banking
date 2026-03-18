import React from 'react';

interface LoanApplication {
  id: string;
  amount: number;
  term: number;
  status: 'pending' | 'approved' | 'rejected';
  applicantName: string;
  annualIncome: number;
  employmentStatus: string;
}

interface LoanDashboardProps {
  applications: LoanApplication[];
}

const LoanDashboard: React.FC<LoanDashboardProps> = ({ applications }) => {
  const getStatusClass = (status: string) => {
    switch (status) {
      case 'approved': return 'status-approved';
      case 'rejected': return 'status-rejected';
      case 'pending': return 'status-pending';
      default: return '';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  if (!applications.length) {
    return (
      <div className="loan-dashboard">
        <h2>Loan Applications</h2>
        <p>No applications submitted yet.</p>
      </div>
    );
  }

  return (
    <div className="loan-dashboard">
      <h2>Loan Applications</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Amount</th>
            <th>Term</th>
            <th>Income</th>
            <th>Employment</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {applications.map(app => (
            <tr key={app.id}>
              <td>{app.applicantName}</td>
              <td>{formatCurrency(app.amount)}</td>
              <td>{app.term} months</td>
              <td>{formatCurrency(app.annualIncome)}</td>
              <td>{app.employmentStatus}</td>
              <td className={getStatusClass(app.status)}>
                {app.status}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LoanDashboard;
