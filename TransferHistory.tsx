import React from 'react';
import { LedgerTable } from './src/components/shared/LedgerTable';
import styles from './TransferHistory.module.css';

// expects prop: accountId:number
function TransferHistory({ accountId }: { accountId: number }) {
  return (
    <section className={styles.container}>
      <h2>Transaction History</h2>
      <LedgerTable accountId={accountId} />
    </section>
  );
}

export default TransferHistory;
