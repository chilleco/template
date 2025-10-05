import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { LoginForm } from '@/features/auth/components/login-form';

const mutateAsync = vi.fn().mockResolvedValue({ access_token: 'token', refresh_token: 'refresh' });

vi.mock('@/hooks/use-auth', () => ({
  useAuth: () => ({
    login: {
      mutateAsync,
      isPending: false
    }
  })
}));

describe('LoginForm', () => {
  it('renders and submits', async () => {
    render(<LoginForm />);

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'user@example.com' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'SecurePass123' } });

    fireEvent.submit(screen.getByRole('button', { name: /continue/i }));

    expect(mutateAsync).toHaveBeenCalledWith({ identifier: 'user@example.com', password: 'SecurePass123' });
  });
});
