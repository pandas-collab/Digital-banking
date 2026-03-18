import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import TransferForm from '../../src/components/TransferForm';

describe('TransferForm', () => {
  beforeEach(() => {
    // Mock console methods
    jest.spyOn(console, 'info').mockImplementation(() => {});
    jest.spyOn(console, 'error').mockImplementation(() => {});
    jest.spyOn(console, 'warn').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('renders all form elements', () => {
    render(<TransferForm />);

    expect(screen.getByText('Transfer Funds')).toBeInTheDocument();
    expect(screen.getByLabelText('Amount (USD)')).toBeInTheDocument();
    expect(screen.getByLabelText('Account Number')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Transfer Now' })).toBeInTheDocument();
  });

  it('validates amount field', async () => {
    render(<TransferForm />);

    const amountInput = screen.getByLabelText('Amount (USD)');
    fireEvent.change(amountInput, { target: { value: '-10' } });

    expect(await screen.findByText('Please enter a valid amount greater than 0')).toBeInTheDocument();
  });

  it('validates account field', async () => {
    render(<TransferForm />);

    const accountInput = screen.getByLabelText('Account Number');
    fireEvent.change(accountInput, { target: { value: 'abc' } });

    expect(await screen.findByText('Account number must be at least 8 characters')).toBeInTheDocument();
  });

  it('displays currency preview', () => {
    render(<TransferForm />);

    const amountInput = screen.getByLabelText('Amount (USD)');
    fireEvent.change(amountInput, { target: { value: '100' } });

    expect(screen.getByText('USD 100.00')).toBeInTheDocument();
  });

  it('disables submit button when form is invalid', () => {
    render(<TransferForm />);

    const submitButton = screen.getByRole('button', { name: 'Transfer Now' });
    expect(submitButton).toBeDisabled();
  });

  it('enables submit button when form is valid', async () => {
    render(<TransferForm />);

    const amountInput = screen.getByLabelText('Amount (USD)');
    const accountInput = screen.getByLabelText('Account Number');
    fireEvent.change(amountInput, { target: { value: '100.50' } });
    fireEvent.change(accountInput, { target: { value: 'ACC123456789' } });

    const submitButton = screen.getByRole('button', { name: 'Transfer Now' });
    expect(submitButton).not.toBeDisabled();
  });

  it('calls onSubmit handler when form is submitted', async () => {
    const mockSubmit = jest.fn().mockResolvedValue(undefined);
    render(<TransferForm onSubmit={mockSubmit} />);

    const amountInput = screen.getByLabelText('Amount (USD)');
    const accountInput = screen.getByLabelText('Account Number');
    const submitButton = screen.getByRole('button', { name: 'Transfer Now' });

    fireEvent.change(amountInput, { target: { value: '100' } });
    fireEvent.change(accountInput, { target: { value: 'ACC123456789' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({
        amount: '100',
        account: 'ACC123456789',
      });
    });
  });

  it('shows loading state during submission', async () => {
    const mockSubmit = jest.fn().mockImplementation(() =>
      new Promise(resolve => setTimeout(resolve, 100))
    );
    render(<TransferForm onSubmit={mockSubmit} />);

    const amountInput = screen.getByLabelText('Amount (USD)');
    const accountInput = screen.getByLabelText('Account Number');
    const submitButton = screen.getByRole('button', { name: 'Transfer Now' });

    fireEvent.change(amountInput, { target: { value: '100' } });
    fireEvent.change(accountInput, { target: { value: 'ACC123456789' } });
    fireEvent.click(submitButton);

    expect(screen.getByText('Processing...')).toBeInTheDocument();
    expect(submitButton).toBeDisabled();

    await waitFor(() => {
      expect(screen.queryByText('Processing...')).not.toBeInTheDocument();
    });
  });

  it('displays general error message', async () => {
    const mockSubmit = jest.fn().mockRejectedValue(new Error('Network error'));
    render(<TransferForm onSubmit={mockSubmit} />);

    const amountInput = screen.getByLabelText('Amount (USD)');
    const accountInput = screen.getByLabelText('Account Number');
    const submitButton = screen.getByRole('button', { name: 'Transfer Now' });

    fireEvent.change(amountInput, { target: { value: '100' } });
    fireEvent.change(accountInput, { target: { value: 'ACC123456789' } });
    fireEvent.click(submitButton);

    expect(await screen.findByText('Network error')).toBeInTheDocument();
  });

  it('clears field-specific errors when user types', async () => {
    render(<TransferForm />);

    const accountInput = screen.getByLabelText('Account Number');
    fireEvent.change(accountInput, { target: { value: 'abc' } });
    expect(await screen.findByText('Account number must be at least 8 characters')).toBeInTheDocument();

    fireEvent.change(accountInput, { target: { value: 'ABCDEFGH' } });
    expect(screen.queryByText('Account number must be at least 8 characters')).toBeNull();
  });

  it('respects custom currency and maxAmount props', () => {
    render(<TransferForm currency="EUR" maxAmount={1000} />);

    expect(screen.getByText('Amount (EUR)')).toBeInTheDocument();

    const amountInput = screen.getByLabelText('Amount (EUR)');
    fireEvent.change(amountInput, { target: { value: '1500' } });

    expect(screen.getByText('Maximum amount exceeded: 1000 EUR')).toBeInTheDocument();
  });
});
