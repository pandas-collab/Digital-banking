import React, { useState } from 'react';

interface TransferFormProps {
  onSubmit?: (transferData: { amount: number; account: string }) => Promise<void>;
}

interface FormErrors {
  amount?: string;
  account?: string;
}

interface TransferFormState {
  amount: string;
  account: string;
  errors: FormErrors;
  isSubmitting: boolean;
  successMessage: string;
}

const TransferForm: React.FC<TransferFormProps> = ({ onSubmit }) => {
  const [state, setState] = useState<TransferFormState>({
    amount: '',
    account: '',
    errors: {},
    isSubmitting: false,
    successMessage: ''
  });

  const validateForm = (): boolean => {
    const errors: FormErrors = {};
    const amount = parseFloat(state.amount);

    if (isNaN(amount) || amount <= 0) {
      errors.amount = 'Please enter a valid amount greater than 0';
    }

    if (!state.account.trim()) {
      errors.account = 'Please enter a valid account number';
    } else if (!/^[A-Za-z0-9-]+$/.test(state.account.trim())) {
      errors.account = 'Account number can only contain letters, numbers, and hyphens';
    }

    setState(prev => ({ ...prev, errors }));
    return Object.keys(errors).length === 0;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setState(prev => ({
      ...prev,
      [name]: value,
      errors: { ...prev.errors, [name]: undefined },
      successMessage: ''
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Clear previous messages
    setState(prev => ({ ...prev, successMessage: '' }));
    
    if (!validateForm()) {
      console.warn('Transfer form validation failed:', state.errors);
      return;
    }

    setState(prev => ({ ...prev, isSubmitting: true }));
    console.info('Starting transfer submission:', { amount: state.amount, account: state.account });

    try {
      if (onSubmit) {
        await onSubmit({ amount: parseFloat(state.amount), account: state.account.trim() });
      }
      setState(prev => ({
        ...prev,
        amount: '',
        account: '',
        isSubmitting: false,
        successMessage: 'Transfer completed successfully!'
      }));
      console.info('Transfer completed successfully');
      
      // Clear success message after 5 seconds
      setTimeout(() => {
        setState(prev => ({ ...prev, successMessage: '' }));
      }, 5000);
    } catch (error) {
      console.error('Transfer submission failed:', error);
      setState(prev => ({
        ...prev,
        isSubmitting: false,
        errors: { amount: 'Transfer failed. Please try again.' }
      }));
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px', border: '1px solid #ddd', borderRadius: '8px', fontFamily: 'Arial, sans-serif' }}>
      <h2 style={{ marginTop: 0 }}>Transfer Funds</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="amount" style={{ display: 'block', marginBottom: '5px' }}>
            Amount ($)
          </label>
          <input
            type="number"
            id="amount"
            name="amount"
            value={state.amount}
            onChange={handleInputChange}
            placeholder="Enter amount"
            step="0.01"
            min="0"
            disabled={state.isSubmitting}
            style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box' }}
          />
          {state.errors.amount && (
            <span style={{ color: 'red', fontSize: '0.8em', display: 'block', marginTop: '5px' }}>
              {state.errors.amount}
            </span>
          )}
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="account" style={{ display: 'block', marginBottom: '5px' }}>
            Account Number
          </label>
          <input
            type="text"
            id="account"
            name="account"
            value={state.account}
            onChange={handleInputChange}
            placeholder="Enter account number"
            disabled={state.isSubmitting}
            style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box' }}
          />
          {state.errors.account && (
            <span style={{ color: 'red', fontSize: '0.8em', display: 'block', marginTop: '5px' }}>
              {state.errors.account}
            </span>
          )}
        </div>

        {state.successMessage && (
          <div style={{ backgroundColor: '#d4edda', color: '#155724', padding: '10px', borderRadius: '4px', marginBottom: '15px', fontSize: '0.9em' }}>
            {state.successMessage}
          </div>
        )}

        <button
          type="submit"
          disabled={state.isSubmitting}
          style={{ width: '100%', padding: '10px', backgroundColor: state.isSubmitting ? '#ccc' : '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: state.isSubmitting ? 'not-allowed' : 'pointer', fontSize: '16px' }}
        >
          {state.isSubmitting ? 'Processing...' : 'Transfer Funds'}
        </button>
      </form>
      
      {/* Hidden test component for CI/CD */}
      <div
        id="test-harness"
        style={{ display: 'none' }}
        data-test-fields={JSON.stringify({
          amountSelector: '[data-testid="amount-input"]',
          accountSelector: '[data-testid="account-input"]',
          submitSelector: '[data-testid="submit-button"]'
        })}
      />
    </div>
  );
};

export default TransferForm;

// Test interface for verification
export const testTransferForm = {
  validateAmount: (amount: string) => !isNaN(parseFloat(amount)) && parseFloat(amount) > 0,
  validateAccount: (account: string) => /^[A-Za-z0-9-]+$/.test(account.trim()) && account.trim() !== ''
};
