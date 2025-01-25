import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);

    //mowimy ze przekazujemy form'sa do funkcji
    //preventDefault pozwala na niezaładowywanie sie ponowne strony po kliknieciu submit
    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();

        setError(null);
        setSuccessMessage(null);

        const credentials = { username, password };

        try {
            const response = await axios.post('http://localhost:8000/api/login/', credentials);
            sessionStorage.setItem('token', response.data.access);
            setSuccessMessage('Login successful!');
        } catch (error) {
            setError('Login failed. Please check your credentials.');
        }
    };

    //form onSubmit formułka, ktora pozwoli obsluzyc logowanie
    return (
        <div className="login-form-wrapper">
            <h2>Login</h2>
            {error && <div className="error">{error}</div>}
            {successMessage && <div className="success">{successMessage}</div>}

            <form onSubmit={handleLogin}>
                <label htmlFor="login-username">Username</label>
                <input
                    type="text"
                    id="login-username"
                    placeholder="John Doe"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />

                <label htmlFor="login-password">Password</label>
                <input
                    type="password"
                    id="login-password"
                    placeholder="min 8 characters"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default Login;