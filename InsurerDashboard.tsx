import React from 'react';
import { LedgerTable } from './src/components/shared/LedgerTable';
import styles from './InsurerDashboard.module.css';

// expects prop: accountId:number
function InsurerDashboard({ accountId }: { accountId: number }) {
  return (
    <section className={styles.container}>
      <h2>Policy Dashboard - Transactions</h2>
      <LedgerTable accountId={accountId} />
    </section>
  );
}

export default InsurerDashboard;
