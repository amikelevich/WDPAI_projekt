import { BrowserRouter, Route, Routes, Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Register from './components/Register';
import Login from './components/Login';
import UsersList from './UserList';

const Navigation = () => {
  return (
    <nav>
      <div className="nav-left">
        <Link to="/">Home</Link>
      </div>
      <div className="nav-right">
        <Link to="/login">Login</Link>
        <Link to="/register">Register</Link>
      </div>
    </nav>
  );
};

const Home = () => {
  const [fundraisers, setFundraisers] = useState<any[]>([]);
  const [isAdmin, setIsAdmin] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [newCampaign, setNewCampaign] = useState({ name: '', description: '', target_amount: 0, raised_amount: 0, status: 'active' });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCampaign, setSelectedCampaign] = useState<any>(null);
  const [donationAmount, setDonationAmount] = useState(0);
  const [error, setError] = useState('');

  const checkIfAdminAndLoggedIn = () => {
    const token = sessionStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
    }

    axios.get('http://localhost:8000/api/user/', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(response => setIsAdmin(response.data.is_admin))
      .catch(error => console.error('Error fetching user data:', error));
  };

  useEffect(() => {
    checkIfAdminAndLoggedIn();

    axios.get('http://localhost:8000/api/campaigns/')
      .then(response => setFundraisers(response.data))
      .catch(error => console.error('Error fetching campaigns:', error));
  }, []);

  const addCampaign = () => {
    const token = sessionStorage.getItem('token');

    axios.post(
      'http://localhost:8000/api/campaigns/create/',
      newCampaign,
      { headers: { Authorization: `Bearer ${token}` } },
    )
      .then(response => {
        setFundraisers([...fundraisers, response.data]);
        setNewCampaign({ name: '', description: '', target_amount: 0, raised_amount: 0, status: 'active' });
        setIsModalOpen(false);
      })
      .catch(error => console.error('Error adding campaign:', error));
  };

  const deleteCampaign = (campaignId: number) => {
    const token = sessionStorage.getItem('token');

    axios.delete(
      `http://localhost:8000/api/campaigns/delete/${campaignId}/`,
      { headers: { Authorization: `Bearer ${token}` } },
    )
      .then(() => {
        setFundraisers(fundraisers.filter(campaign => campaign.campaign_id !== campaignId));
      })
      .catch(error => console.error('Error deleting campaign:', error));
  };

  const handleDonate = (campaignId: number) => {
    if (donationAmount <= 0) {
      setError("Donation amount must be greater than 0.");
      return;
    }
  
    const token = sessionStorage.getItem('token');
    if (!token) {
      setError("You need to be logged in to donate.");
      return;
    }
  
    const campaign = fundraisers.find(campaign => campaign.campaign_id === campaignId);
  
    if (!campaign) {
      setError("Campaign not found.");
      return;
    }
  
    const remainingAmount = campaign.target_amount - campaign.raised_amount;
  
    if (donationAmount > remainingAmount) {
      setError(`The maximum you can donate is ${remainingAmount.toFixed(2)} PLN to reach the target.`);
      return;
    }
  
    setError("");
    
    axios.put(
      `http://localhost:8000/api/campaigns/update/${campaignId}/`,
      { donation_amount: donationAmount },
      { headers: { Authorization: `Bearer ${token}` } }
    )
      .then(() => {
        return axios.get('http://localhost:8000/api/campaigns/');
      })
      .then(response => {
        setFundraisers(response.data);
        setSelectedCampaign(null);
        setDonationAmount(0);
      })
      .catch(error => {
        console.error('Error making donation:', error);
        setError("Failed to process your donation. Please try again.");
      });
  };
  
  

  const handleDonateButtonText = (fundraiser: any) => {
    return fundraiser.status === 'completed' ? "Cel osiągnięty" : "Szczegóły";
  };

  const handleDonateButtonDisabled = (fundraiser: any) => {
    return fundraiser.status === 'completed';
  };

  return (
    <div className="home-container">
      <Navigation />

      <header className="home-header">
        <h1>Pomagajmy Razem</h1>
        <p>Wspieraj potrzebujących w prosty i przejrzysty sposób. Każda złotówka ma znaczenie.</p>
        <Link to="/register" className="cta-button">Dołącz do nas</Link>
      </header>

      {isAdmin && (
        <>
          <button className="add-campaign-button" onClick={() => setIsModalOpen(true)}>
            +
          </button>

          {isModalOpen && (
            <div className="modal">
              <div className="modal-content">
                <h3>Dodaj nową kampanię</h3>
                <input
                  type="text"
                  placeholder="Nazwa kampanii"
                  value={newCampaign.name}
                  onChange={e => setNewCampaign({ ...newCampaign, name: e.target.value })}
                />
                <textarea
                  placeholder="Opis kampanii"
                  value={newCampaign.description}
                  onChange={e => setNewCampaign({ ...newCampaign, description: e.target.value })}
                />
                <input
                  type="number"
                  placeholder="Kwota docelowa"
                  value={newCampaign.target_amount}
                  onChange={e => setNewCampaign({
                    ...newCampaign,
                    target_amount: parseFloat(e.target.value) || 0,
                  })}
                />
                <div className="modal-actions">
                  <button onClick={addCampaign}>Dodaj Kampanię</button>
                  <button onClick={() => setIsModalOpen(false)}>Anuluj</button>
                </div>
              </div>
            </div>
          )}
        </>
      )}

      <section className="fundraiser-list">
        <h2>Aktualne Kampanie</h2>
        {fundraisers.length === 0 ? (
          <p>Brak dostępnych kampanii.</p>
        ) : (
          fundraisers.map(fundraiser => (
            <div key={fundraiser.campaign_id} className="fundraiser-item">
              <h3>{fundraiser.name}</h3>
              <p>{fundraiser.description}</p>
              <p><strong>Kwota docelowa:</strong> {fundraiser.target_amount} PLN</p>
              <p><strong>Zebrano:</strong> {fundraiser.raised_amount} PLN</p>
              <div className="progress-bar">
                <div
                  className="progress"
                  style={{ width: `${(fundraiser.raised_amount / fundraiser.target_amount) * 100}%` }}
                ></div>
              </div>

              {isLoggedIn && !isAdmin && (
                <button
                  onClick={() => { setSelectedCampaign(fundraiser); setIsModalOpen(true); }}
                  disabled={handleDonateButtonDisabled(fundraiser)}
                  className={handleDonateButtonDisabled(fundraiser) ? "goal-achieved" : ""}
                >
                  {handleDonateButtonText(fundraiser)}
                </button>
              )}

              {isAdmin && (
                <button className="delete-button" onClick={() => deleteCampaign(fundraiser.campaign_id)}>
                  -
                </button>
              )}
            </div>
          ))
        )}
      </section>

      {selectedCampaign && (
        <div className="donation-modal">
          <div className="donation-modal-content">
            <h3>{selectedCampaign.name}</h3>
            <p>{selectedCampaign.description}</p>
            <p><strong>Kwota docelowa:</strong> {selectedCampaign.target_amount} PLN</p>
            <p><strong>Zebrano:</strong> {selectedCampaign.raised_amount} PLN</p>

            <input
              type="number"
              placeholder="Kwota do darowizny"
              value={donationAmount}
              onChange={e => setDonationAmount(parseFloat(e.target.value) || 0)}
            />

            {error && <p className="error">{error}</p>}

            <div className="modal-actions">
              <button onClick={() => handleDonate(selectedCampaign.campaign_id)}>Donate</button>
              <button onClick={() => setSelectedCampaign(null)}>Zamknij</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};


function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/users" element={<UsersList />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
