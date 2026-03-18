import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import LoanForm from '../src/components/LoanForm';

describe('LoanForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders form correctly', () => {
    render(<LoanForm onSubmit={mockOnSubmit} />);

    expect(screen.getByRole('form')).toHaveAttribute('aria-label', 'Loan Application Form');
    expect(screen.getByLabelText(/loan amount/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/loan term/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /apply now/i })).toBeInTheDocument();
  });

  test('validates required fields', () => {
    render(<LoanForm onSubmit={mockOnSubmit} />);

    const submitButton = screen.getByRole('button', { name: /apply now/i });
    fireEvent.click(submitButton);

    expect(screen.getByText('Loan amount is required')).toBeInTheDocument();
    expect(screen.getByText('Loan term is required')).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('validates invalid amount', () => {
    render(<LoanForm onSubmit={mockOnSubmit} />);

    const amountInput = screen.getByLabelText(/loan amount/i);
    fireEvent.change(amountInput, { target: { value: '-1000' } });

    const submitButton = screen.getByRole('button', { name: /apply now/i });
    fireEvent.click(submitButton);

    expect(screen.getByText('Loan amount must be greater than $0')).toBeInTheDocument();
  });

  test('validates invalid term', () => {
    render(<LoanForm onSubmit={mockOnSubmit} />);

    const termInput = screen.getByLabelText(/loan term/i);
    fireEvent.change(termInput, { target: { value: 'abc' } });

    const submitButton = screen.getByRole('button', { name: /apply now/i });
    fireEvent.click(submitButton);

    expect(screen.getByText('Loan term must be a whole number')).toBeInTheDocument();
  });

  test('submits valid form data', async () => {
    mockOnSubmit.mockResolvedValue({ success: true });

    render(<LoanForm onSubmit={mockOnSubmit} />);

    const amountInput = screen.getByLabelText(/loan amount/i);
    const termInput = screen.getByLabelText(/loan term/i);
    const submitButton = screen.getByRole('button', { name: /apply now/i });

    fireEvent.change(amountInput, { target: { value: '25000' } });
    fireEvent.change(termInput, { target: { value: '60' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        amount: 25000,
        term: 60
      });
      expect(screen.getByText(/your loan application has been submitted/i)).toBeInTheDocument();
    });
  });

  test('handles submission error', async () => {
    mockOnSubmit.mockResolvedValue({ success: false, message: 'Invalid credit score' });

    render(<LoanForm onSubmit={mockOnSubmit} />);

    const amountInput = screen.getByLabelText(/loan amount/i);
    const termInput = screen.getByLabelText(/loan term/i);
    const submitButton = screen.getByRole('button', { name: /apply now/i });

    fireEvent.change(amountInput, { target: { value: '50000' } });
    fireEvent.change(termInput, { target: { value: '120' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Invalid credit score')).toBeInTheDocument();
    });
  });

  test('shows loading state during submission', () => {
    mockOnSubmit.mockImplementation(() => new Promise(() => {}));

    render(<LoanForm onSubmit={mockOnSubmit} />);

    const amountInput = screen.getByLabelText(/loan amount/i);
    const termInput = screen.getByLabelText(/loan term/i);
    const submitButton = screen.getByRole('button', { name: /apply now/i });

    fireEvent.change(amountInput, { target: { value: '15000' } });
    fireEvent.change(termInput, { target: { value: '36' } });
    fireEvent.click(submitButton);

    expect(screen.getByRole('button', { name: /processing/i })).toBeInTheDocument();
    expect(screen.getByRole('button')).toBeDisabled();
  });

  test('clears form on successful submission', async () => {
    mockOnSubmit.mockResolvedValue({ success: true });

    render(<LoanForm onSubmit={mockOnSubmit} />);

    const amountInput = screen.getByLabelText(/loan amount/i);
    const termInput = screen.getByLabelText(/loan term/i);
    const submitButton = screen.getByRole('button', { name: /apply now/i });

    fireEvent.change(amountInput, { target: { value: '40000' } });
    fireEvent.change(termInput, { target: { value: '84' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(amountInput).toHaveValue('');
      expect(termInput).toHaveValue('');
    });
  });
});
