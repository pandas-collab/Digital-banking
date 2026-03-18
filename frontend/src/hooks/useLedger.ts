import { useEffect, useState } from 'react';
import { LedgerEntry } from '../types/ledgers';

const BASE_URL = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1';

export function useLedger(accountId: number | null) {
  const [ledger, setLedger] = useState<LedgerEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (accountId === null) return;

    setLoading(true);
    setError(null);

    // simple retry strategy: 3 attempts, exponential back-off
    let attempts = 0;
    const maxAttempts = 3;
    const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

    const fetchLedger = async () => {
      try {
        const resp = await fetch(`${BASE_URL}/ledger?account_id=${accountId}`);
        if (!resp.ok) throw new Error(`Server returned ${resp.status}`);
        const json = await resp.json();
        setLedger(json);
      } catch (err: any) {
        if (attempts < maxAttempts - 1) {
          attempts += 1;
          await sleep(500 * Math.pow(2, attempts)); // 0.5s, 1s, 2s
          return fetchLedger();
        }
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchLedger();
  }, [accountId]);

  return { ledger, loading, error };
}
