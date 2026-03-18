import React, { useState } from 'react';

const TransferForm: React.FC = () => {
  const [amount, setAmount] = useState('');
  const [recipient, setRecipient] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Transfer submitted:', { amount, recipient });
    setAmount('');
    setRecipient('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Transfer Form</h2>
      <div>
        <label>Recipient:</label>
        <input
          type="text"
          value={recipient}
          onChange={(e) => setRecipient(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Amount:</label>
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />
      </div>
      <button type="submit">Transfer</button>
    </form>
  );
};

export default TransferForm;
