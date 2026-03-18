import React from 'react';
import { LedgerTable } from './src/components/shared/LedgerTable';
import styles from './LoanDashboard.module.css';

function LoanDashboard({ accountId }: { accountId: number }) {
  return (
    <section className={styles.container}>
      <h2>Loan Dashboard - Transactions</h2>
      <LedgerTable accountId={accountId} />
    </section>
  );
}

export default LoanDashboard;
