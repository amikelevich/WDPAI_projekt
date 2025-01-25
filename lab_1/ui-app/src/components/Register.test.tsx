import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Register from './Register';


const DummyComponent: React.FC = () => {
    return <div>Dummy Component</div>;
  };

describe('Register Component', () => {
  it('renders the register form correctly', () => {
    render(<Register />);
    render(<DummyComponent />);

    // Check if form elements exist
    expect(screen.getByLabelText(/User name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/User mail/i)).toBeInTheDocument();
    expect(screen.getByTestId('register-password')).toBeInTheDocument();
    expect(screen.getByTestId('register-confirmPassword')).toBeInTheDocument();
    expect(screen.getByLabelText(/Accept our beautiful statement/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('shows an error when passwords do not match', async () => {
    render(<Register />);

    // Simulate user input
    fireEvent.change(screen.getByLabelText(/User name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText(/User mail/i), { target: { value: 'john.doe@example.com' } });
    fireEvent.change(screen.getByTestId('register-password'), { target: { value: 'password123' } });
    fireEvent.change(screen.getByTestId('register-confirmPassword'), { target: { value: 'differentPassword' } });
    fireEvent.click(screen.getByLabelText(/Accept our beautiful statement/i));

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    // Check for the error message
    expect(await screen.findByText(/Passwords do not match./i)).toBeInTheDocument();
  });

  it('shows an error for invalid email', async () => {
    render(<Register />);

    // Simulate user input
    fireEvent.change(screen.getByLabelText(/User name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText(/User mail/i), { target: { value: 'invalid-email@xd' } });
    fireEvent.change(screen.getByTestId('register-password'), { target: { value: 'password123' } });
    fireEvent.change(screen.getByTestId('register-confirmPassword'), { target: { value: 'password123' } });
    fireEvent.click(screen.getByLabelText(/Accept our beautiful statement/i));

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    // Check for the error message
    expect(screen.getByText(/Invalid email address./)).toHaveClass("error")
  });

});