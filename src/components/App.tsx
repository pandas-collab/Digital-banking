import React from 'react';
import LoanForm from './LoanForm';

const App = () => {
  const handleLoanSubmit = async (data: { amount: number; term: number }) => {
    // This would typically make an API call
    console.log('Processing loan application:', data);
    await new Promise(resolve => setTimeout(resolve, 1000));
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Loan Application Portal</h1>
      <LoanForm onSubmit={handleLoanSubmit} />
    </div>
  );
};

export default App;
