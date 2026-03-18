import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface TransferFormData {
  amount: string;
  account: string;
}

interface TransferFormProps {
  onSubmit?: (data: TransferFormData) => Promise<void>;
  accountPlaceholder?: string;
  maxAmount?: number;
  currency?: string;
}

interface ValidationErrors {
  amount?: string;
  account?: string;
  general?: string;
}

function log(level: 'info' | 'error' | 'warn', message: string, data?: any) {
  const timestamp = new Date().toISOString();
  console[level](`[TransferForm] ${timestamp}: ${message}`, data ? JSON.stringify(data) : '');
}

export default function TransferForm({
  onSubmit,
  accountPlaceholder = 'Enter account number',
  maxAmount = 10000,
  currency = 'USD',
}: TransferFormProps) {
  const [formData, setFormData] = useState<TransferFormData>({
    amount: '',
    account: '',
  });
  const [errors, setErrors] = useState<ValidationErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isValid, setIsValid] = useState(false);
  const router = useRouter();

  // Validate form data
  const validateForm = (data: TransferFormData): ValidationErrors => {
    const newErrors: ValidationErrors = {};

    try {
      // Amount validation
      if (!data.amount.trim()) {
        newErrors.amount = 'Amount is required';
      } else {
        const amount = parseFloat(data.amount);
        if (isNaN(amount) || amount <= 0) {
          newErrors.amount = 'Please enter a valid amount greater than 0';
        } else if (amount > maxAmount) {
          newErrors.amount = `Maximum amount exceeded: ${maxAmount} ${currency}`;
        } else if (!/^\d*\.?\d{0,2}$/.test(data.amount)) {
          newErrors.amount = 'Please enter no more than 2 decimal places';
        }
      }

      // Account validation
      if (!data.account.trim()) {
        newErrors.account = 'Account number is required';
      } else if (!/^[a-zA-Z0-9\s-]+$/.test(data.account)) {
        newErrors.account = 'Account number can only contain letters, numbers, spaces, and hyphens';
      } else if (data.account.trim().length < 8) {
        newErrors.account = 'Account number must be at least 8 characters';
      }

      log('info', 'Validation completed', { errors: newErrors });
      return newErrors;
    } catch (error) {
      log('error', 'Validation error', error);
      return { general: 'An error occurred during validation' };
    }
  };

  // Check if form is valid
  useEffect(() => {
    const newErrors = validateForm(formData);
    setIsValid(Object.keys(newErrors).length === 0);
  }, [formData, maxAmount]);

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear specific error when user starts typing
    if (errors[name as keyof ValidationErrors]) {
      setErrors((prev) => ({
        ...prev,
        [name]: undefined,
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    log('info', 'Form submission started', { formData });

    const validationErrors = validateForm(formData);
    if (Object.keys(validationErrors).length > 0) {
      log('warn', 'Validation failed', validationErrors);
      setErrors(validationErrors);
      return;
    }

    setIsSubmitting(true);
    setErrors({});

    try {
      const submitData = {
        amount: formData.amount,
        account: formData.account.trim().toUpperCase(),
      };

      if (onSubmit) {
        await onSubmit(submitData);
        log('info', 'Transfer submitted successfully', submitData);
      } else {
        // Default behavior - simulate API call
        await simulateTransfer(submitData);
        log('info', 'Transfer simulated successfully', submitData);

        // Show success and redirect after 1 second
        setTimeout(() => {
          router.push('/dashboard');
        }, 1000);
      }

      // Reset form after successful submission
      setFormData({ amount: '', account: '' });

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Transfer failed';
      log('error', 'Transfer submission failed', error);
      setErrors({ general: errorMessage });
    } finally {
      setIsSubmitting(false);
    }
  };

  // Simulate transfer for testing purposes
  const simulateTransfer = async (data: TransferFormData): Promise<void> => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const shouldFail = Math.random() < 0.1; // 10% failure rate for testing
        if (shouldFail) {
          reject(new Error('Insufficient funds'));
        } else {
          resolve();
        }
      }, 1000);
    });
  };

  const formatCurrency = (amount: string) => {
    const num = parseFloat(amount);
    if (isNaN(num)) return '';
    return `${currency} ${num.toFixed(2)}`;
  };

  return (
    <form onSubmit={handleSubmit} className="transfer-form" aria-labelledby="transfer-form-title">
      <h2 id="transfer-form-title">Transfer Funds</h2>

      {errors.general && (
        <div className="error-message" role="alert" aria-live="polite">
          {errors.general}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="amount">Amount ({currency})</label>
        <input
          type="text"
          id="amount"
          name="amount"
          value={formData.amount}
          onChange={handleInputChange}
          placeholder="0.00"
          maxLength={15}
          aria-invalid={errors.amount ? 'true' : 'false'}
          aria-describedby="amount-error"
          disabled={isSubmitting}
        />
        {errors.amount && (
          <span id="amount-error" className="error-text" role="alert">
            {errors.amount}
          </span>
        )}
        <div className="currency-preview" aria-live="polite">
          {formData.amount && formatCurrency(formData.amount)}
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="account">Account Number</label>
        <input
          type="text"
          id="account"
          name="account"
          value={formData.account}
          onChange={handleInputChange}
          placeholder={accountPlaceholder}
          maxLength={30}
          minLength={8}
          aria-invalid={errors.account ? 'true' : 'false'}
          aria-describedby="account-error"
          disabled={isSubmitting}
        />
        {errors.account && (
          <span id="account-error" className="error-text" role="alert">
            {errors.account}
          </span>
        )}
      </div>

      <button
        type="submit"
        disabled={!isValid || isSubmitting}
        aria-busy={isSubmitting}
      >
        {isSubmitting ? (
          <>
            <span className="spinner" aria-hidden="true"></span>
            Processing...
          </>
        ) : (
          'Transfer Now'
        )}
      </button>

      <style jsx>{`
        .transfer-form {
          max-width: 400px;
          margin: 0 auto;
          padding: 2rem;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        }

        h2 {
          margin-bottom: 1.5rem;
          color: #1a1a1a;
          font-weight: 600;
          text-align: center;
        }

        .form-group {
          margin-bottom: 1.5rem;
        }

        label {
          display: block;
          margin-bottom: 0.5rem;
          font-weight: 500;
          color: #374151;
        }

        input[type="text"] {
          width: 100%;
          padding: 0.75rem;
          border: 1px solid #d1d5db;
          border-radius: 0.375rem;
          font-size: 1rem;
          transition: all 0.2s;
        }

        input[type="text"]:focus {
          outline: none;
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        input[type="text"]:disabled {
          background-color: #f3f4f6;
          cursor: not-allowed;
        }

        .error-message {
          background-color: #fee2e2;
          color: #991b1b;
          padding: 0.75rem;
          border-radius: 0.375rem;
          margin-bottom: 1rem;
          font-size: 0.875rem;
        }

        .error-text {
          display: block;
          color: #dc2626;
          font-size: 0.875rem;
          margin-top: 0.25rem;
        }

        .currency-preview {
          margin-top: 0.25rem;
          font-size: 0.875rem;
          color: #6b7280;
          font-weight: 500;
        }

        button[type="submit"] {
          width: 100%;
          background-color: #3b82f6;
          color: white;
          padding: 0.75rem 1.5rem;
          border: none;
          border-radius: 0.375rem;
          font-size: 1rem;
          font-weight: 500;
          cursor: pointer;
          transition: background-color 0.2s;
        }

        button[type="submit"]:hover:not(:disabled) {
          background-color: #2563eb;
        }

        button[type="submit"]:disabled {
          background-color: #9ca3af;
          cursor: not-allowed;
        }

        button[type="submit"]:active:not(:disabled) {
          transform: translateY(1px);
        }

        .spinner {
          animation: spin 1s linear infinite;
          margin-right: 0.5rem;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        @media (max-width: 640px) {
          .transfer-form {
            padding: 1rem;
          }
        }
      `}</style>
    </form>
  );
}
