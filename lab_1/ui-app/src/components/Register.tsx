import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [privacyAccepted, setPrivacyAccepted] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);

    const validateEmail = (email: string) => {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    };

    //mowimy ze przekazujemy form'sa do funkcji
    //preventDefault pozwala na niezaładowywanie sie ponowne strony po kliknieciu submit
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        setError(null);
        setSuccessMessage(null);

        if (!validateEmail(email)) {
            setError('Invalid email address.');
            return;
        }

        if (password.length < 8) {
            setError('Password must be at least 8 characters long.');
            return;
        }

        if (password !== confirmPassword) {
            setError('Passwords do not match.');
            return;
        }

        if (!privacyAccepted) {
            setError('You must accept the privacy policy.');
            return;
        }

        const formData = { username ,email, password };

        try {
            await axios.post('http://localhost:8000/api/register/', formData);
            setSuccessMessage('Registration successful!');
        } catch (error) {
            setError('Registration failed. Please try again.');
        }
    };

    //form onSubmit formułka, ktora pozwoli obsluzyc rejestracje
    return (
        <div className="register-form-wrapper">
            <h2>Register</h2>
            {error && <div className="error">{error}</div>}
            {successMessage && <div className="success">{successMessage}</div>}

            <form onSubmit={handleSubmit}>
            <label htmlFor="register-username">User name</label>
                <input
                    type="text"
                    id="register-username"
                    placeholder="John Doe"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <label htmlFor="register-email">User mail</label>
                <input
                    type="email"
                    id="register-email"
                    placeholder="john.doe@gmail.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <label htmlFor="register-password">Password</label>
                <input
                    type="password"
                    id="register-password"
                    placeholder="min 8 characters"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    data-testid="register-password"
                />
                <label htmlFor="register-confirmPassword">Confirm password</label>
                <input
                    type="password"
                    id="register-confirmPassword"
                    placeholder="min 8 characters"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    data-testid="register-confirmPassword"
                />

                <div id="privacy">
                    <input
                        type="checkbox"
                        id="privacyPolicy"
                        checked={privacyAccepted}
                        onChange={(e) => setPrivacyAccepted(e.target.checked)}
                    />
                    <label htmlFor="privacyPolicy" className="privacyPolicy">
                        Accept our beautiful{' '}
                        <a href="https://www.w3schools.com" target="_blank" rel="noopener noreferrer">
                            statement.                  
                        </a>
                    </label>
                </div>

                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default Register;
