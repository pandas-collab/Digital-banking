import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import TransferHistory from './TransferHistory';

describe('TransferHistory Component', () => {
  it('renders loading state initially', () => {
    render(<TransferHistory />);
    expect(screen.getByText(/Loading transfers.../i)).toBeInTheDocument();
  });

  it('displays error message when fetch fails', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('Network error'));
    render(<TransferHistory />);
    await waitFor(() => {
      expect(screen.getByText(/Failed to load transfers/i)).toBeInTheDocument();
    });
  });

  it('renders no transfers message when empty', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ transfers: [], total: 0 })
    });
    render(<TransferHistory />);
    await waitFor(() => {
      expect(screen.getByText(/No transfers found/i)).toBeInTheDocument();
    });
  });
});
