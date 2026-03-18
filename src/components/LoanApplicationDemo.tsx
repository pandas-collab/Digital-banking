'use client';

import React from 'react';
import LoanForm from './LoanForm';
import logger from '../lib/logger';

const LoanApplicationDemo: React.FC = () => {
  const handleLoanSubmit = async (formData: { amount: number; term: number }) => {
    try {
      logger.info('Processing loan application', formData);

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Example validation logic
      if (formData.amount > 500000) {
        return { success: false, message: 'Amount exceeds maximum allowed' };
      }

      // In real app, this would be an API call
      logger.info('Loan submitted successfully', formData);
      return { success: true };
    } catch (error) {
      logger.error('Failed to submit loan application', error);
      return { success: false, message: 'Server error, please try again' };
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Loan Application</h1>
      <p>Complete the form below to apply for a loan.</p>
      <LoanForm onSubmit={handleLoanSubmit} />
    </div>
  );
};

export default LoanApplicationDemo;
