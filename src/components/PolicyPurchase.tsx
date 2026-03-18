import React, { useState, useEffect } from 'react';
import styles from './PolicyPurchase.module.css';

interface Plan {
  id: string;
  name: string;
  description: string;
  price: number;
  coverage: string;
}

interface FormData {
  email: string;
  phone: string;
  planId: string;
  firstName: string;
  lastName: string;
}

const PolicyPurchase: React.FC = () => {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    email: '',
    phone: '',
    planId: '',
    firstName: '',
    lastName: ''
  });

  // Fetch available plans
  useEffect(() => {
    const fetchPlans = async () => {
      try {
        setLoading(true);
        setError(null);

        // Mock API call - replace with actual endpoint
        const mockPlans: Plan[] = [
          { id: 'basic', name: 'Basic Plan', description: 'Essential coverage', price: 29.99, coverage: '$50,000' },
          { id: 'standard', name: 'Standard Plan', description: 'Balanced coverage', price: 49.99, coverage: '$100,000' },
          { id: 'premium', name: 'Premium Plan', description: 'Maximum protection', price: 79.99, coverage: '$250,000' }
        ];

        setPlans(mockPlans);
      } catch (err) {
        setError('Failed to load plans. Please refresh the page.');
        console.error('Plans fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPlans();
  }, []);

  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError(null);
  };

  // Validate form
  const validateForm = (): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^\d{10}$/;

    if (!formData.email || !emailRegex.test(formData.email)) {
      setError('Please enter a valid email address');
      return false;
    }

    if (!formData.phone || !phoneRegex.test(formData.phone.replace(/\D/g, ''))) {
      setError('Please enter a valid 10-digit phone number');
      return false;
    }

    if (!formData.firstName.trim() || formData.firstName.trim().length < 2) {
      setError('First name must be at least 2 characters');
      return false;
    }

    if (!formData.lastName.trim() || formData.lastName.trim().length < 2) {
      setError('Last name must be at least 2 characters');
      return false;
    }

    if (!formData.planId) {
      setError('Please select a plan');
      return false;
    }

    return true;
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Replace with actual API call
      console.log('Submitting policy purchase:', formData);

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Success response
      setSuccess(true);
      setFormData({
        email: '',
        phone: '',
        planId: '',
        firstName: '',
        lastName: ''
      });

    } catch (err) {
      setError('Failed to process your request. Please try again.');
      console.error('Submission error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Render UI based on loading/error states
  if (loading && !plans.length) {
    return <div className={styles.container}><p>Loading plans...</p></div>;
  }

  return (
    <div className={styles.container}>
      <h2>Purchase Insurance Policy</h2>

      {error && (
        <div className={styles.error}>
          <p>{error}</p>
        </div>
      )}

      {success && (
        <div className={styles.success}>
          <h3>Policy Purchased Successfully!</h3>
          <p>You'll receive a confirmation email shortly.</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label htmlFor="firstName">First Name *</label>
          <input
            type="text"
            id="firstName"
            name="firstName"
            value={formData.firstName}
            onChange={handleInputChange}
            required
            maxLength={50}
            disabled={loading}
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="lastName">Last Name *</label>
          <input
            type="text"
            id="lastName"
            name="lastName"
            value={formData.lastName}
            onChange={handleInputChange}
            required
            maxLength={50}
            disabled={loading}
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="email">Email Address *</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            required
            maxLength={100}
            disabled={loading}
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="phone">Phone Number *</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleInputChange}
            placeholder="1234567890"
            required
            maxLength={10}
            disabled={loading}
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="planId">Select Plan *</label>
          <select
            id="planId"
            name="planId"
            value={formData.planId}
            onChange={handleInputChange}
            required
            disabled={loading}
          >
            <option value="">Choose a plan...</option>
            {plans.map(plan => (
              <option key={plan.id} value={plan.id}>
                {plan.name} - ${plan.price}/month ({plan.coverage} coverage)
              </option>
            ))}
          </select>
        </div>

        <button
          type="submit"
          className={styles.submitButton}
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Purchase Policy'}
        </button>
      </form>

      <div className={styles.testSection}>
        <h3>Test Data</h3>
        <p>Use these values for testing:</p>
        <ul>
          <li>Email: test@example.com</li>
          <li>Phone: 1234567890</li>
          <li>First Name: John</li>
          <li>Last Name: Doe</li>
        </ul>
      </div>
    </div>
  );
};

export default PolicyPurchase;
