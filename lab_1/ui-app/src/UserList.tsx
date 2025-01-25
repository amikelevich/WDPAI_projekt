import axios from 'axios';
import { useState, useEffect } from 'react';

interface User {
    id: number;
    first_name: string;
    last_name: string;
    role: string;
}

const UserList = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [newUser, setNewUser] = useState({
        first_name: '',
        last_name: '',
        role: '',
    });
    const [privacyAccepted, setPrivacyAccepted] = useState(false);

    const fetchUsers = async () => {
        try {
            const token = sessionStorage.getItem('token');
            const response = await axios.get('http://localhost:8000/api/business-users/', {
                headers: {
                    Authorization: `Bearer ${token}`, // Dodanie tokena do nagłówków, w celu weryfikacji uzytkownika
                },
            });
            setUsers(response.data);
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    const handleAddUser = async () => {
        if (!privacyAccepted) {
            alert('You must agree to the privacy policy to proceed.');
            return;
        }

        if (!newUser.first_name || !newUser.last_name || !newUser.role) {
            alert('All fields are required.');
            return;
        }

        try {
            const token = sessionStorage.getItem('token');
            const response = await axios.post('http://localhost:8000/api/business-users/', newUser, {
                headers: {
                    Authorization: `Bearer ${token}`, 
                },
            });
            setUsers((prevUsers) => [...prevUsers, response.data]);
        } catch (error) {
            console.error('Error adding user:', error);
        }
    };

    const handleDeleteUser = async (id: number) => {
        try {
            const token = sessionStorage.getItem('token');
            await axios.delete(`http://localhost:8000/api/business-users/${id}/`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setUsers((prevUsers) => prevUsers.filter((user) => user.id !== id));
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    };

    return (
        <div className="container">
            <div id="putinto">
                <h2>Let's level up your brand, together</h2>
                <h3>Enter First Name</h3>
                <input
                    type="text"
                    placeholder="First Name"
                    value={newUser.first_name}
                    onChange={(e) => setNewUser({ ...newUser, first_name: e.target.value })}
                />
                <h3>Enter Last Name</h3>
                <input
                    type="text"
                    placeholder="Last Name"
                    value={newUser.last_name}
                    onChange={(e) => setNewUser({ ...newUser, last_name: e.target.value })}
                />
                <h3>Role</h3>
                <input
                    type="text"
                    placeholder="Role"
                    value={newUser.role}
                    onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                />
                <div id="privacy">
                    <input
                        type="checkbox"
                        id="privacyPolicy"
                        checked={privacyAccepted}
                        onChange={(e) => setPrivacyAccepted(e.target.checked)}
                    />
                    <label htmlFor="privacyPolicy" className="privacyPolicy">
                        You agree to our friendly{' '}
                        <a href="https://www.w3schools.com" target="_blank">
                            privacy policy.
                        </a>
                    </label>
                </div>
                <button id="submitbut" onClick={handleAddUser}>
                    SUBMIT
                </button>
            </div>
            <div id="usersList">
                {users.map((user) => (
                    <div key={user.id} className="user-item">
                        <div>
                            <span>
                                {user.first_name} {user.last_name}
                            </span>
                            <small>{user.role}</small>
                        </div>
                        <button onClick={() => handleDeleteUser(user.id)}>
                            <i className="fa-regular fa-trash-can"></i>
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default UserList;
