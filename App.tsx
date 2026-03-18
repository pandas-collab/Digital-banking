import React, { useState } from 'react';
import LoanForm from './components/LoanForm';
import LoanDashboard from './components/LoanDashboard';
import './index.css';

interface LoanApplication {
  id: string;
  amount: number;
  term: number;
  status: 'pending' | 'approved' | 'rejected';
  applicantName: string;
  annualIncome: number;
  employmentStatus: string;
}

const App: React.FC = () => {
  const [applications, setApplications] = useState<LoanApplication[]>([]);

  const addApplication = (application: Omit<LoanApplication, 'id' | 'status'>) => {
    const newApplication: LoanApplication = {
      ...application,
      id: Date.now().toString(),
      status: 'pending'
    };
    setApplications(prev => [...prev, newApplication]);
    // Log for debugging
    console.log('New application added:', newApplication);
  };

  return (
    <div className="app">
      <header>
        <h1>Core Banking Platform</h1>
      </header>
      <main>
        <LoanForm onSubmit={addApplication} />
        <LoanDashboard applications={applications} />
      </main>
    </div>
  );
};

export default App;
