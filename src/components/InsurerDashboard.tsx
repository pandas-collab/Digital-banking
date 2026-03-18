import { useEffect, useState } from 'react';
import type { NextPage } from 'next';

interface Policy {
  policyId: number;
  policyType: string;
  status: string;
  nextPremiumDate: string | null;
  amountDue: number;
  isLapsed: boolean;
}

const InsurerDashboard: NextPage = () => {
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  const fetchPolicies = async () => {
    try {
      console.log('Fetching policies...');
      const response = await fetch('http://localhost:8000/api/v1/policies');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      const mappedPolicies: Policy[] = data.map((item: any) => ({
        policyId: item.policy_id,
        policyType: item.policy_type,
        status: item.status,
        nextPremiumDate: item.next_premium_date,
        amountDue: item.amount_due,
        isLapsed: item.is_lapsed
      }));

      setPolicies(mappedPolicies);
      setError('');
      console.log('Fetched policies:', mappedPolicies);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(`Failed to load policies: ${message}`);
      console.error('Error fetching policies:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
    const interval = setInterval(fetchPolicies, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Insurer Dashboard</h1>
      <button onClick={fetchPolicies} disabled={loading}>
        {loading ? 'Loading...' : 'Refresh'}
      </button>

      {error && <p style={{color: 'red'}}>{error}</p>}

      <table style={{width: '100%', borderCollapse: 'collapse', marginTop: '1rem'}}>
        <thead>
          <tr>
            <th style={{border: '1px solid #ddd', padding: '8px', textAlign: 'left'}}>Policy ID</th>
            <th style={{border: '1px solid #ddd', padding: '8px', textAlign: 'left'}}>Type</th>
            <th style={{border: '1px solid #ddd', padding: '8px', textAlign: 'left'}}>Status</th>
            <th style={{border: '1px solid #ddd', padding: '8px', textAlign: 'left'}}>Next Premium</th>
            <th style={{border: '1px solid #ddd', padding: '8px', textAlign: 'left'}}>Amount Due</th>
          </tr>
        </thead>
        <tbody>
          {policies.filter(p => p.isLapsed || p.amountDue > 0).map(policy => (
            <tr key={policy.policyId} style={{color: policy.amountDue > 0 ? 'red' : 'inherit'}}>
              <td style={{border: '1px solid #ddd', padding: '8px'}}>{policy.policyId}</td>
              <td style={{border: '1px solid #ddd', padding: '8px'}}>{policy.policyType}</td>
              <td style={{border: '1px solid #ddd', padding: '8px'}}>{policy.status}</td>
              <td style={{border: '1px solid #ddd', padding: '8px'}}>{policy.nextPremiumDate || 'N/A'}</td>
              <td style={{border: '1px solid #ddd', padding: '8px'}}>${policy.amountDue.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {policies.filter(p => p.isLapsed || p.amountDue > 0).length === 0 && !error && (
        <p>No lapsed policies or defaulters found.</p>
      )}
    </div>
  );
};

export default InsurerDashboard;
