import React, { useState } from 'react';

interface LoanFormProps {
  onSubmit: (data: {
    amount: number;
    term: number;
    applicantName: string;
    annualIncome: number;
    employmentStatus: string;
  }) => void;
}

const LoanForm: React.FC<LoanFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    amount: 0,
    term: 12,
    applicantName: '',
    annualIncome: 0,
    employmentStatus: 'full-time'
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    if (!formData.applicantName.trim()) {
      throw new Error('Name is required');
    }
    if (formData.amount <= 0) {
      throw new Error('Amount must be greater than 0');
    }
    if (formData.term <= 0) {
      throw new Error('Term must be greater than 0 months');
    }
    if (formData.annualIncome <= 0) {
      throw new Error('Annual income must be greater than 0');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      validateForm();
      setLoading(true);

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500));

      onSubmit(formData);

      // Reset form with safe defaults
      setFormData({
        amount: 0,
        term: 12,
        applicantName: '',
        annualIncome: 0,
        employmentStatus: 'full-time'
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: string, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="loan-form">
      <h2>Apply for a Loan</h2>

      {error && (
        <div className="error-message" style={{
          backgroundColor: '#fee',
          color: '#c53030',
          padding: '10px',
          margin: '10px 0',
          borderRadius: '4px'
        }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Full Name:</label>
          <input
            type="text"
            value={formData.applicantName}
            onChange={(e) => handleChange('applicantName', e.target.value)}
            required
            disabled={loading}
          />
        </div>

        <div>
          <label>Loan Amount ($):</label>
          <input
            type="number"
            min="1000"
            max="100000"
            value={formData.amount}
            onChange={(e) => handleChange('amount', Number(e.target.value))}
            required
            disabled={loading}
          />
        </div>

        <div>
          <label>Term (months):</label>
          <input
            type="number"
            min="6"
            max="360"
            value={formData.term}
            onChange={(e) => handleChange('term', Number(e.target.value))}
            required
            disabled={loading}
          />
        </div>

        <div>
          <label>Annual Income:</label>
          <input
            type="number"
            min="1000"
            value={formData.annualIncome}
            onChange={(e) => handleChange('annualIncome', Number(e.target.value))}
            required
            disabled={loading}
          />
        </div>

        <div>
          <label>Employment Status:</label>
          <select
            value={formData.employmentStatus}
            onChange={(e) => handleChange('employmentStatus', e.target.value)}
            disabled={loading}
          >
            <option value="full-time">Full-time</option>
            <option value="part-time">Part-time</option>
            <option value="self-employed">Self-employed</option>
            <option value="unemployed">Unemployed</option>
          </select>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Apply for Loan'}
        </button>
      </form>
    </div>
  );
};

export default LoanForm;
