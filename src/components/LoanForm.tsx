import React, { useState, useCallback } from 'react';
import { ErrorBoundary } from './ErrorBoundary';

interface LoanFormProps {
  onSubmit?: (data: { amount: number; term: number }) => Promise<void>;
}

interface LoanFormData {
  amount: string;
  term: string;
}

interface FormErrors {
  amount?: string;
  term?: string;
  submit?: string;
}

const LoanForm: React.FC<LoanFormProps> = ({ onSubmit }) => {
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});
  const [data, setData] = useState<LoanFormData>({ amount: '', term: '' });
  const [success, setSuccess] = useState(false);

  const validate = useCallback((formData: LoanFormData): FormErrors => {
    const newErrors: FormErrors = {};

    if (!formData.amount || parseFloat(formData.amount) <= 0) {
      newErrors.amount = 'Amount must be greater than 0';
    } else if (parseFloat(formData.amount) > 1000000) {
      newErrors.amount = 'Amount cannot exceed $1,000,000';
    }

    if (!formData.term || parseInt(formData.term) <= 0) {
      newErrors.term = 'Term must be greater than 0 months';
    } else if (parseInt(formData.term) > 360) {
      newErrors.term = 'Term cannot exceed 360 months (30 years)';
    }

    return newErrors;
  }, []);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setData(prev => ({ ...prev, [name]: value }));
    setErrors(prev => ({ ...prev, [name]: undefined }));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccess(false);

    const validationErrors = validate(data);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      console.error('Validation failed:', validationErrors);
      return;
    }

    setLoading(true);
    setErrors({});

    try {
      console.log('Submitting loan application:', data);

      if (onSubmit) {
        await onSubmit({
          amount: parseFloat(data.amount),
          term: parseInt(data.term)
        });
      } else {
        // Default submission to console
        console.log('Loan application received:', {
          amount: parseFloat(data.amount),
          term: parseInt(data.term),
          monthlyPayment: (parseFloat(data.amount) / parseInt(data.term)).toFixed(2),
          submittedAt: new Date().toISOString()
        });
      }

      setSuccess(true);
      setData({ amount: '', term: '' });

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to submit application';
      setErrors({ submit: errorMessage });
      console.error('Submission error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ErrorBoundary fallback={<div>Something went wrong loading the form.</div>}>
      <form onSubmit={handleSubmit} style={{ maxWidth: '400px', padding: '20px' }}>
        <h2>Loan Application</h2>

        {errors.submit && (
          <div style={{ color: 'red', marginBottom: '10px' }} aria-live="polite">
            {errors.submit}
          </div>
        )}

        {success && (
          <div style={{ color: 'green', marginBottom: '10px' }} aria-live="polite">
            Application submitted successfully!
          </div>
        )}

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="amount">Loan Amount ($)</label>
          <input
            type="number"
            id="amount"
            name="amount"
            value={data.amount}
            onChange={handleChange}
            min="1"
            max="1000000"
            step="0.01"
            required
            disabled={loading}
            style={{ width: '100%', padding: '8px', border: errors.amount ? '1px solid red' : '1px solid #ccc' }}
          />
          {errors.amount && (
            <div style={{ color: 'red', fontSize: '14px' }}>{errors.amount}</div>
          )}
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="term">Term (months)</label>
          <input
            type="number"
            id="term"
            name="term"
            value={data.term}
            onChange={handleChange}
            min="1"
            max="360"
            required
            disabled={loading}
            style={{ width: '100%', padding: '8px', border: errors.term ? '1px solid red' : '1px solid #ccc' }}
          />
          {errors.term && (
            <div style={{ color: 'red', fontSize: '14px' }}>{errors.term}</div>
          )}
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Processing...' : 'Apply Now'}
        </button>
      </form>
    </ErrorBoundary>
  );
};

export default LoanForm;
