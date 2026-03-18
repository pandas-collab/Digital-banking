import React, { useState, useEffect } from 'react';
import apiClient from './apiClient';

interface InsurancePolicy {
  id: string;
  type: string;
  premium: number;
  coverage: number;
  duration: number;
}

const PolicyPurchase: React.FC = () => {
  const [policies, setPolicies] = useState<InsurancePolicy[]>([]);
  const [selectedPolicy, setSelectedPolicy] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  useEffect(() => {
    fetchPolicies();
  }, []);

  const fetchPolicies = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await apiClient.get('/api/insurance/policies');
      setPolicies(response.data);
    } catch (err) {
      setError('Failed to fetch insurance policies. Please try again.');
      console.error('Error fetching policies:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = async () => {
    if (!selectedPolicy) {
      setError('Please select an insurance policy');
      return;
    }

    try {
      setLoading(true);
      setError('');
      await apiClient.post('/api/insurance/purchase', {
        policyId: selectedPolicy
      });
      setSuccess('Insurance policy purchased successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err: any) {
      const message = err.response?.data?.error || 'Failed to purchase policy';
      setError(message);
      console.error('Purchase error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="policy-purchase-container" style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h2>Purchase Insurance</h2>

      {error && (
        <div style={{ backgroundColor: '#fee', color: '#c53030', padding: '12px', marginBottom: '16px', borderRadius: '4px' }}>
          {error}
        </div>
      )}

      {success && (
        <div style={{ backgroundColor: '#f0fdf4', color: '#22543d', padding: '12px', marginBottom: '16px', borderRadius: '4px' }}>
          {success}
        </div>
      )}

      {loading ? (
        <div>Loading insurance policies...</div>
      ) : (
        <div>
          <label>Select Policy Type:</label>
          <select
            value={selectedPolicy}
            onChange={(e) => setSelectedPolicy(e.target.value)}
            style={{ width: '100%', padding: '8px', margin: '8px 0', fontSize: '16px' }}
          >
            <option value="">Choose a policy...</option>
            {policies.map(policy => (
              <option key={policy.id} value={policy.id}>
                {policy.type} - ${policy.coverage} coverage (${policy.premium} premium)
              </option>
            ))}
          </select>

          <button
            onClick={handlePurchase}
            disabled={loading || !selectedPolicy}
            style={{
              padding: '12px 24px',
              backgroundColor: '#4299e1',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontSize: '16px',
              marginTop: '16px'
            }}
          >
            {loading ? 'Processing...' : 'Purchase Policy'}
          </button>
        </div>
      )}
    </div>
  );
};

export default PolicyPurchase;
