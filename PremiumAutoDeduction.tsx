import React, { useState, useEffect } from 'react';

interface DeductionSchedule {
  id: string;
  policy_id: string;
  amount: number;
  frequency_days: number;
  next_deduction: string;
  status: string;
}

export const PremiumAutoDeduction: React.FC = () => {
  const [schedules, setSchedules] = useState<DeductionSchedule[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    policy_id: '',
    amount: '',
    frequency_days: '30'
  });

  const apiClient = async (endpoint: string, options?: RequestInit) => {
    const url = `http://localhost:8000${endpoint}`;
    const response = await fetch(url, {
      headers: { 'Content-Type': 'application/json' },
      ...options
    });
    if (!response.ok) {
      throw new Error(await response.text());
    }
    return response.json();
  };

  const handleSchedule = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await apiClient('/api/schedule-premium', {
        method: 'POST',
        body: JSON.stringify({
          policy_id: formData.policy_id,
          amount: parseFloat(formData.amount),
          frequency_days: parseInt(formData.frequency_days)
        })
      });
      console.log('Scheduled:', result);
      setFormData({ policy_id: '', amount: '', frequency_days: '30' });
      await loadSchedules();
    } catch (err: any) {
      setError(err.message || 'Failed to schedule premium');
    } finally {
      setLoading(false);
    }
  };

  const loadSchedules = async () => {
    try {
      // In real implementation, fetch from API
      setSchedules([]); // Placeholder
    } catch (err) {
      setError('Failed to load schedules');
    }
  };

  useEffect(() => {
    loadSchedules();
  }, []);

  return (
    <div className="premium-auto-deduction">
      <h2>Premium Auto-Deduction Management</h2>

      {error && (
        <div className="error-message" style={{color: 'red', marginBottom: '10px'}}>
          {error}
        </div>
      )}

      <form onSubmit={handleSchedule}>
        <div>
          <label>Policy ID:</label>
          <input
            type="text"
            value={formData.policy_id}
            onChange={(e) => setFormData({...formData, policy_id: e.target.value})}
            required
          />
        </div>

        <div>
          <label>Amount ($):</label>
          <input
            type="number"
            step="0.01"
            value={formData.amount}
            onChange={(e) => setFormData({...formData, amount: e.target.value})}
            required
          />
        </div>

        <div>
          <label>Frequency (days):</label>
          <select
            value={formData.frequency_days}
            onChange={(e) => setFormData({...formData, frequency_days: e.target.value})}
          >
            <option value="30">Monthly</option>
            <option value="90">Quarterly</option>
            <option value="365">Yearly</option>
          </select>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Scheduling...' : 'Schedule Auto-Deduction'}
        </button>
      </form>

      {schedules.length > 0 && (
        <div>
          <h3>Active Schedules</h3>
          <ul>
            {schedules.map(schedule => (
              <li key={schedule.id}>
                Policy {schedule.policy_id}: ${schedule.amount} every {schedule.frequency_days} days
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
