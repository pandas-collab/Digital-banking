import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import LoanForm from '../src/components/LoanForm';

describe('LoanForm', () => {
  test('renders all required fields', () => {
    render(<LoanForm />);

    expect(screen.getByLabelText(/Loan Amount/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Term/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Apply Now/i })).toBeInTheDocument();
  });

  test('validates amount field', async () => {
    render(<LoanForm />);

    const amountInput = screen.getByLabelText(/Loan Amount/i);
    const submitButton = screen.getByRole('button', { name: /Apply Now/i });

    fireEvent.change(amountInput, { target: { value: '-100' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Amount must be greater than 0')).toBeInTheDocument();
    });
  });

  test('validates term field', async () => {
    render(<LoanForm />);

    const termInput = screen.getByLabelText(/Term/i);
    const submitButton = screen.getByRole('button', { name: /Apply Now/i });

    fireEvent.change(termInput, { target: { value: '400' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Term cannot exceed 360 months')).toBeInTheDocument();
    });
  });

  test('submits valid form data', async () => {
    const mockSubmit = jest.fn().mockResolvedValue(undefined);
    render(<LoanForm onSubmit={mockSubmit} />);

    const amountInput = screen.getByLabelText(/Loan Amount/i);
    const termInput = screen.getByLabelText(/Term/i);
    const submitButton = screen.getByRole('button', { name: /Apply Now/i });

    fireEvent.change(amountInput, { target: { value: '50000' } });
    fireEvent.change(termInput, { target: { value: '60' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({ amount: 50000, term: 60 });
      expect(screen.getByText('Application submitted successfully!')).toBeInTheDocument();
    });
  });
});
