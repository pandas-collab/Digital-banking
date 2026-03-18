import React, { useState } from 'react';

interface LoanFormData {
  amount: number;
  term: number;
}

interface LoanFormProps {
  onSubmit: (formData: LoanFormData) => Promise<{ success: boolean; message?: string }>;
}

const LoanForm: React.FC<LoanFormProps> = ({ onSubmit }) => {
  const [amount, setAmount] = useState<string>('');
  const [term, setTerm] = useState<string>('');
  const [errors, setErrors] = useState<{ amount?: string; term?: string; general?: string }>({});
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: { amount?: string; term?: string } = {};

    // Validate amount
    const numAmount = parseFloat(amount);
    if (!amount.trim()) {
      newErrors.amount = 'Loan amount is required';
    } else if (isNaN(numAmount) || numAmount <= 0) {
      newErrors.amount = 'Loan amount must be greater than $0';
    } else if (numAmount > 1000000) {
      newErrors.amount = 'Loan amount cannot exceed $1,000,000';
    }

    // Validate term
    const numTerm = parseInt(term, 10);
    if (!term.trim()) {
      newErrors.term = 'Loan term is required';
    } else if (isNaN(numTerm) || numTerm <= 0) {
      newErrors.term = 'Loan term must be a positive number';
    } else if (numTerm % 1 !== 0) {
      newErrors.term = 'Loan term must be a whole number';
    } else if (numTerm < 1 || numTerm > 360) {
      newErrors.term = 'Loan term must be between 1 and 360 months';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    setSuccess(false);

    // Client-side validation
    if (!validateForm()) {
      console.log('[LOANFORM] Validation failed:', errors);
      return;
    }

    setLoading(true);
    console.log('[LOANFORM] Submitting loan application:', { amount: parseFloat(amount), term: parseInt(term, 10) });

    try {
      const result = await onSubmit({
        amount: parseFloat(amount),
        term: parseInt(term, 10)
      });

      if (result.success) {
        console.log('[LOANFORM] Loan application submitted successfully');
        setSuccess(true);
        setAmount('');
        setTerm('');
      } else {
        console.error('[LOANFORM] Loan application failed:', result.message);
        setErrors({ general: result.message || 'Failed to submit application' });
      }
    } catch (error) {
      console.error('[LOANFORM] Submission error:', error);
      setErrors({ general: 'An unexpected error occurred. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const handleAmountChange = (value: string) => {
    // Allow only numbers and decimal point
    const sanitized = value.replace(/[^\d.]/g, '');
    setAmount(sanitized);
    if (errors.amount) {
      setErrors({ ...errors, amount: undefined });
    }
  };

  const handleTermChange = (value: string) => {
    // Allow only numbers
    const sanitized = value.replace(/[^\d]/g, '');
    setTerm(sanitized);
    if (errors.term) {
      setErrors({ ...errors, term: undefined });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="loan-form" aria-label="Loan Application Form">
      <h2>Apply for a Loan</h2>

      {success && (
        <div className="success-message" role="alert" aria-live="polite">
          Your loan application has been submitted successfully!
        </div>
      )}

      {errors.general && (
        <div className="error-message" role="alert" aria-live="polite">
          {errors.general}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="loan-amount">
          Loan Amount ($)
          <input
            type="text"
            id="loan-amount"
            value={amount}
            onChange={(e) => handleAmountChange(e.target.value)}
            placeholder="10000"
            aria-invalid={errors.amount ? 'true' : 'false'}
            aria-describedby="amount-error"
            maxLength={8}
            disabled={loading}
          />
        </label>
        {errors.amount && (
          <span id="amount-error" className="field-error" role="alert">
            {errors.amount}
          </span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="loan-term">
          Loan Term (months)
          <input
            type="text"
            id="loan-term"
            value={term}
            onChange={(e) => handleTermChange(e.target.value)}
            placeholder="36"
            aria-invalid={errors.term ? 'true' : 'false'}
            aria-describedby="term-error"
            maxLength={3}
            disabled={loading}
          />
        </label>
        {errors.term && (
          <span id="term-error" className="field-error" role="alert">
            {errors.term}
          </span>
        )}
      </div>

      <button type="submit" disabled={loading} aria-busy={loading}>
        {loading ? 'Processing...' : 'Apply Now'}
      </button>

      <style jsx>{`
        .loan-form {
          max-width: 400px;
          margin: 0 auto;
          padding: 2rem;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          background: white;
        }

        .form-group {
          margin-bottom: 1rem;
        }

        label {
          display: block;
          margin-bottom: 0.5rem;
          font-weight: 600;
        }

        input {
          width: 100%;
          padding: 0.5rem;
          font-size: 1rem;
          border: 1px solid #ccc;
          border-radius: 4px;
          transition: border-color 0.3s;
        }

        input:focus {
          border-color: #0070f3;
          outline: none;
        }

        input:invalid {
          border-color: #ff0000;
        }

        button {
          width: 100%;
          padding: 0.75rem;
          font-size: 1rem;
          background: #0070f3;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          transition: background-color 0.3s;
        }

        button:hover:not(:disabled) {
          background: #0051cc;
        }

        button:disabled {
          background: #cccccc;
          cursor: not-allowed;
        }

        .success-message {
          background: #d4edda;
          color: #155724;
          padding: 0.75rem;
          margin-bottom: 1rem;
          border: 1px solid #c3e6cb;
          border-radius: 4px;
        }

        .error-message,
        .field-error {
          display: block;
          color: #dc3545;
          font-size: 0.875rem;
          margin-top: 0.25rem;
        }
      `}</style>
    </form>
  );
};

export default LoanForm;
