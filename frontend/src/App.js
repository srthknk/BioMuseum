import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { QrReader } from 'react-qr-reader';
import "./App.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Configure axios with longer timeout
axios.defaults.timeout = 30000; // 30 seconds for long operations

// Context for admin authentication
const AdminContext = React.createContext();

const AdminProvider = ({ children }) => {
  const [isAdmin, setIsAdmin] = useState(!!localStorage.getItem('admin_token'));
  const [token, setToken] = useState(localStorage.getItem('admin_token'));

  const login = (token) => {
    localStorage.setItem('admin_token', token);
    setToken(token);
    setIsAdmin(true);
  };

  const logout = () => {
    localStorage.removeItem('admin_token');
    setToken(null);
    setIsAdmin(false);
  };

  return (
    <AdminContext.Provider value={{ isAdmin, token, login, logout }}>
      {children}
    </AdminContext.Provider>
  );
};

// Homepage Component
const Homepage = () => {
  const [organisms, setOrganisms] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const navigate = useNavigate();
  const { login } = React.useContext(AdminContext);

  useEffect(() => {
    fetchOrganisms();
  }, []);

  const fetchOrganisms = async () => {
    try {
      const response = await axios.get(`${API}/organisms`);
      setOrganisms(response.data);
    } catch (error) {
      console.error('Error fetching organisms:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchTerm.trim()) {
      fetchOrganisms();
      return;
    }

    try {
      const response = await axios.get(`${API}/search?q=${searchTerm}`);
      setOrganisms(response.data);
    } catch (error) {
      console.error('Error searching organisms:', error);
    }
  };

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;

    try {
      const response = await axios.post(`${API}/admin/login`, { username, password });
      login(response.data.access_token);
      setShowAdminLogin(false);
      navigate('/admin');
    } catch (error) {
      alert('Invalid credentials');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-linear-to-br from-green-50 to-blue-50 flex items-center justify-center loading-container">
        <div className="text-center">
          {/* Creative DNA Spinner */}
          <div className="mb-8 flex justify-center">
            <div className="dna-spinner">
              <div className="text-6xl">🧬</div>
            </div>
          </div>

          {/* Animated Text */}
          <div className="mb-4">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">BioMuseum</h2>
            <p className="text-gray-600 mb-4">Discovering the wonders of life...</p>
          </div>

          {/* Animated Loading Bar */}
          <div className="w-64 mx-auto mb-4">
            <div className="h-2 bg-gray-300 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-green-400 to-blue-500 rounded-full animate-pulse" 
                   style={{ animation: 'pulse 1.5s ease-in-out infinite' }}>
              </div>
            </div>
          </div>

          {/* Animated Particles */}
          <div className="flex gap-2 justify-center">
            <div className="w-2 h-2 bg-green-500 rounded-full pulse-glow"></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full pulse-glow" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-green-400 rounded-full pulse-glow" style={{ animationDelay: '0.4s' }}></div>
          </div>

          <p className="text-sm text-gray-500 mt-6">Loading organisms...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-linear-to-br from-green-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b-4 border-green-600">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-center md:text-left mb-4 md:mb-0">
              <h1 className="text-4xl font-bold text-gray-800 mb-2">🧬 Biology Museum</h1>
              <p className="text-gray-600">Discover the wonders of life science</p>
            </div>
            <div className="flex gap-4">
              <button
                onClick={() => setShowAdminLogin(true)}
                className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
              >
                🔐 Admin
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">

      {/* Search Section */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <form onSubmit={handleSearch} className="mb-8">
          <div className="flex gap-2 max-w-2xl mx-auto">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search organisms by name or scientific name..."
              className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
            />
            <button
              type="submit"
              className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              Search
            </button>
          </div>
        </form>

        {/* Organisms Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {organisms.map((organism) => (
            <div
              key={organism.id}
              onClick={() => navigate(`/organism/${organism.id}`)}
              className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all cursor-pointer border-2 hover:border-green-300 organism-card-enter hover:scale-105 transform duration-300"
            >
              <div className="flex items-center justify-center bg-gray-50 rounded-t-xl overflow-hidden h-48">
                {organism.images && organism.images[0] ? (
                  <img
                    src={organism.images[0]}
                    alt={organism.name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="text-6xl">🦁</div>
                )}
              </div>
              <div className="p-6 text-center">
                <h3 className="text-xl font-bold text-gray-800 mb-2">{organism.name}</h3>
                <p className="text-sm text-gray-600 italic mb-3">{organism.scientific_name}</p>
                {organism.classification && (
                  <div className="mt-3">
                    <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                      {organism.classification.kingdom || 'Unknown Kingdom'}
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {organisms.length === 0 && (
          <div className="text-center py-12">
            <p className="text-xl text-gray-600">No organisms found.</p>
            <p className="text-gray-500 mt-2">Try a different search term or browse all specimens.</p>
          </div>
        )}
      </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white">
        <div className="max-w-7xl mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* About Section */}
            <div>
              <h3 className="text-2xl font-bold mb-4">🧬 BioMuseum</h3>
              <p className="text-gray-300 text-sm">
                Discover the wonders of life science through our interactive biology museum. 
                Learn about diverse organisms and their fascinating characteristics.
              </p>
            </div>

            {/* Quick Links */}
            <div>
              <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li><a href="/" className="hover:text-green-400 transition-colors">🏠 Home</a></li>
               <li><a onClick={() => setShowAdminLogin(true)} className="hover:text-green-400 transition-colors cursor-pointer">🔐 Admin Panel</a></li>
              </ul>
            </div>

            {/* Contact Info */}
            <div>
              <h4 className="text-lg font-semibold mb-4">Contact & Social</h4>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li>📧 Email: sarthaknk07@outlook.com</li>
                <li>📍 Location : Zoology Department, SBES College of Science</li>
                <li></li>
              </ul>
            </div>
          </div>

          {/* Divider */}
          <div className="border-t border-gray-700 mt-8 pt-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <p className="text-gray-400 text-sm">
                © Made with Love @ Chh.SambhajiNagar.
              </p>
              <div className="text-right text-gray-400 text-sm">
                <h5>Created by Sarthak N. Kulkarni B.Sc First Year</h5>
                
              </div>
            </div>
          </div>
        </div>
      </footer>

      {/* Admin Login Modal */}
      {showAdminLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4">
            <h2 className="text-2xl font-bold mb-6 text-center">Admin Login</h2>
            <form onSubmit={handleAdminLogin}>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  Username
                </label>
                <input
                  type="text"
                  name="username"
                  className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                  required
                />
              </div>
              <div className="mb-6">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  Password
                </label>
                <input
                  type="password"
                  name="password"
                  className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                  required
                />
              </div>
              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => setShowAdminLogin(false)}
                  className="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-2 rounded-lg transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg transition-colors"
                >
                  Login
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

// QR Scanner Component
const QRScanner = () => {
  const [error, setError] = useState('');
  const [scannedData, setScannedData] = useState('');
  const navigate = useNavigate();

  const handleScan = (result, error) => {
    if (result) {
      setScannedData(result.text);
      
      // Check if it's a museum organism URL
      const organismMatch = result.text.match(/\/organism\/([a-f0-9-]+)/);
      if (organismMatch) {
        navigate(`/organism/${organismMatch[1]}`);
      } else {
        setError('QR code does not contain a valid organism link');
      }
    }
    
    if (error) {
      console.error('QR Scanner Error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 to-green-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <button
            onClick={() => navigate('/')}
            className="mb-4 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
          >
            ← Back to Home
          </button>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">📱 QR Code Scanner</h1>
          <p className="text-gray-600">Scan a QR code on any specimen to learn more</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="max-w-md mx-auto">
            <QrReader
              onResult={handleScan}
              style={{ width: '100%' }}
              constraints={{ facingMode: 'environment' }}
            />
          </div>
          
          {error && (
            <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}
          
          {scannedData && (
            <div className="mt-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
              <strong>Scanned:</strong> {scannedData}
            </div>
          )}
          
          <div className="mt-6 text-center text-sm text-gray-600">
            <p>• Allow camera access when prompted</p>
            <p>• Point your camera at the QR code</p>
            <p>• Make sure the QR code is well-lit and in focus</p>
          </div>
        </div>
      </div>
    </div>
  );
};

// Organism Detail Component
const OrganismDetail = () => {
  const { id } = useParams();
  const [organism, setOrganism] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchOrganism();
  }, [id]);

  const fetchOrganism = async () => {
    try {
      const response = await axios.get(`${API}/organisms/${id}`);
      setOrganism(response.data);
    } catch (error) {
      console.error('Error fetching organism:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-linear-to-br from-green-50 to-blue-50 flex items-center justify-center">
        <div className="text-xl">Loading organism details...</div>
      </div>
    );
  }

  if (!organism) {
    return (
      <div className="min-h-screen bg-linear-to-br from-green-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Organism not found</h2>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
          >
            Go Back Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-green-50 to-blue-50">
      <div className="max-w-6xl mx-auto px-4 py-2">
        <button
          onClick={() => navigate('/')}
          className="mb-2 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
        >
          ← Back to Home
        </button>

        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Header */}
          <div className="bg-linear-to-br from-green-600 to-blue-600 text-white p-4">
            <h1 className="text-4xl font-bold mb-2">{organism.name}</h1>
            <p className="text-xl italic opacity-90">{organism.scientific_name}</p>
          </div>

          <div className="grid md:grid-cols-2 gap-4 p-4">
            {/* Left Column - Images and QR */}
            <div>
              {organism.images && organism.images.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-xl font-semibold mb-4">📸 Images</h3>
                  <div className="grid gap-4">
                    {organism.images.map((image, index) => (
                      <div key={index} className="flex items-center justify-center bg-gray-50 rounded-lg w-80 h-64 mx-auto">
                        <img
                          src={image}
                          alt={`${organism.name} ${index + 1}`}
                          className="max-w-full max-h-full object-contain rounded-lg shadow-md"
                        />
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {organism.qr_code_image && (
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h3 className="text-xl font-semibold mb-4">📱 QR Code</h3>
                  <div className="text-center">
                    <img
                      src={organism.qr_code_image}
                      alt="QR Code"
                      className="mx-auto mb-4 border-2 border-gray-300 rounded w-40 h-40"
                    />
                    <p className="text-sm text-gray-600">
                      Scan this QR code to share this organism with others
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Right Column - Details */}
            <div className="space-y-6">
              {/* Classification */}
              {organism.classification && (
                <div>
                  <h3 className="text-xl font-semibold mb-4">🔬 Classification</h3>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    {Object.entries(organism.classification).map(([key, value]) => (
                      <div key={key} className="flex justify-between py-2 border-b last:border-b-0">
                        <span className="font-medium capitalize">{key}:</span>
                        <span>{value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Morphology */}
              {organism.morphology && (
                <div>
                  <h3 className="text-xl font-semibold mb-4">🏗️ Morphology</h3>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-gray-700 whitespace-pre-line">{organism.morphology}</p>
                  </div>
                </div>
              )}

              {/* Physiology */}
              {organism.physiology && (
                <div>
                  <h3 className="text-xl font-semibold mb-4">⚡ Physiology</h3>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-gray-700 whitespace-pre-line">{organism.physiology}</p>
                  </div>
                </div>
              )}

              {/* Description */}
              {organism.description && (
                <div>
                  <h3 className="text-xl font-semibold mb-4">📝 Description</h3>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-gray-700 whitespace-pre-line">{organism.description}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Admin Panel with full functionality
const AdminPanel = () => {
  const { isAdmin, logout, token } = React.useContext(AdminContext);
  const navigate = useNavigate();
  const [activeView, setActiveView] = useState('dashboard');
  const [organisms, setOrganisms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editingOrganism, setEditingOrganism] = useState(null);

  useEffect(() => {
    if (isAdmin) {
      fetchOrganisms();
    }
  }, [isAdmin]);

  const fetchOrganisms = async () => {
    try {
      const response = await axios.get(`${API}/organisms`);
      setOrganisms(response.data);
    } catch (error) {
      console.error('Error fetching organisms:', error);
    }
  };

  if (!isAdmin) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-purple-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">🔧 Admin Panel</h1>
          <div className="flex gap-4">
            <button
              onClick={() => navigate('/')}
              className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
            >
              Home
            </button>
            <button
              onClick={logout}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-xl shadow-lg mb-8">
          <div className="flex border-b">
            <button
              onClick={() => setActiveView('dashboard')}
              className={`px-6 py-4 font-semibold ${activeView === 'dashboard' 
                ? 'border-b-2 border-blue-500 text-blue-600' 
                : 'text-gray-600 hover:text-blue-600'}`}
            >
              📊 Dashboard
            </button>
            <button
              onClick={() => setActiveView('add')}
              className={`px-6 py-4 font-semibold ${activeView === 'add' 
                ? 'border-b-2 border-blue-500 text-blue-600' 
                : 'text-gray-600 hover:text-blue-600'}`}
            >
              ➕ Add Organism
            </button>
            <button
              onClick={() => setActiveView('manage')}
              className={`px-6 py-4 font-semibold ${activeView === 'manage' 
                ? 'border-b-2 border-blue-500 text-blue-600' 
                : 'text-gray-600 hover:text-blue-600'}`}
            >
              📝 Manage Organisms
            </button>
          </div>
          
          <div className="p-8">
            {activeView === 'dashboard' && (
              <DashboardView organisms={organisms} />
            )}
            {activeView === 'add' && (
              <AddOrganismForm 
                token={token} 
                onSuccess={() => {
                  fetchOrganisms();
                  setActiveView('manage');
                }} 
              />
            )}
            {activeView === 'manage' && (
              <ManageOrganisms 
                organisms={organisms}
                token={token}
                onUpdate={fetchOrganisms}
                onEdit={setEditingOrganism}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Dashboard View Component
const DashboardView = ({ organisms }) => {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-6">📊 Dashboard</h2>
      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-green-100 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-green-800 mb-2">Total Organisms</h3>
          <p className="text-3xl font-bold text-green-600">{organisms.length}</p>
        </div>
        <div className="bg-blue-100 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-blue-800 mb-2">With Images</h3>
          <p className="text-3xl font-bold text-blue-600">
            {organisms.filter(org => org.images && org.images.length > 0).length}
          </p>
        </div>
        <div className="bg-purple-100 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-purple-800 mb-2">QR Codes</h3>
          <p className="text-3xl font-bold text-purple-600">{organisms.length}</p>
        </div>
      </div>
      
      <div className="mt-8">
        <h3 className="text-xl font-semibold mb-4">Recent Organisms</h3>
        <div className="space-y-3">
          {organisms.slice(0, 5).map((organism) => (
            <div key={organism.id} className="flex items-center justify-between bg-gray-50 p-4 rounded-lg">
              <div>
                <h4 className="font-semibold">{organism.name}</h4>
                <p className="text-sm text-gray-600 italic">{organism.scientific_name}</p>
              </div>
              <span className="text-sm text-gray-500">
                {organism.classification?.kingdom || 'Unknown Kingdom'}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Add Organism Form Component
const AddOrganismForm = ({ token, onSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    scientific_name: '',
    classification: {
      kingdom: '',
      phylum: '',
      class: '',
      order: '',
      family: '',
      genus: '',
      species: ''
    },
    morphology: '',
    physiology: '',
    description: '',
    images: []
  });
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [imageUrl, setImageUrl] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name.startsWith('classification.')) {
      const classField = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        classification: {
          ...prev.classification,
          [classField]: value
        }
      }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleImageUpload = async (files) => {
    const newImages = [];
    for (const file of files) {
      if (file.type.startsWith('image/')) {
        const base64 = await convertToBase64(file);
        newImages.push(base64);
      }
    }
    setFormData(prev => ({
      ...prev,
      images: [...prev.images, ...newImages]
    }));
  };

  const convertToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleImageUpload(Array.from(e.dataTransfer.files));
    }
  };

  const removeImage = (index) => {
    setFormData(prev => ({
      ...prev,
      images: prev.images.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API}/admin/organisms`, formData, {
        headers: { Authorization: `Bearer ${token}` },
        timeout: 30000 // 30 second timeout
      });
      
      alert('Organism added successfully!');
      setFormData({
        name: '',
        scientific_name: '',
        classification: {
          kingdom: '', phylum: '', class: '', order: '', family: '', genus: '', species: ''
        },
        morphology: '',
        physiology: '',
        description: '',
        images: []
      });
      onSuccess();
    } catch (error) {
      const errorMsg = error.response?.data?.detail || error.message || 'Network error - please check your connection';
      alert('Error adding organism: ' + errorMsg);
      console.error('Detailed error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-semibold">➕ Add New Organism</h2>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Common Name *
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., African Elephant"
            />
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Scientific Name *
            </label>
            <input
              type="text"
              name="scientific_name"
              value={formData.scientific_name}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., Loxodonta africana"
            />
          </div>
        </div>

        {/* Classification */}
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-4">🔬 Taxonomic Classification</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'].map((field) => (
              <div key={field}>
                <label className="block text-sm font-medium text-gray-700 mb-1 capitalize">
                  {field}
                </label>
                <input
                  type="text"
                  name={`classification.${field}`}
                  value={formData.classification[field]}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder={`e.g., ${field === 'kingdom' ? 'Animalia' : field === 'phylum' ? 'Chordata' : '...'}`}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Description Fields */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              🏗️ Morphology (Physical Structure) *
            </label>
            <textarea
              name="morphology"
              value={formData.morphology}
              onChange={handleInputChange}
              required
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Describe the physical characteristics, size, shape, structure..."
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              ⚡ Physiology (Biological Functions) *
            </label>
            <textarea
              name="physiology"
              value={formData.physiology}
              onChange={handleInputChange}
              required
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Describe biological processes, metabolism, reproduction, behavior..."
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              📝 General Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={3}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Additional information, conservation status, interesting facts..."
            />
          </div>
        </div>

        {/* Image Upload */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            📸 Images
          </label>
          
          <div className="mb-4 p-4 border border-gray-300 rounded-lg">
            <div className="flex gap-2 mb-4">
              <input
                type="url"
                value={imageUrl}
                onChange={(e) => setImageUrl(e.target.value)}
                placeholder="Paste image URL from internet..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <button
                type="button"
                onClick={() => {
                  if (imageUrl.trim()) {
                    setFormData(prev => ({
                      ...prev,
                      images: [...prev.images, imageUrl]
                    }));
                    setImageUrl('');
                  }
                }}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium"
              >
                Add URL
              </button>
            </div>
            <div className="text-center text-sm text-gray-500">or</div>
          </div>
          
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="space-y-2">
              <div className="text-4xl">📁</div>
              <div>
                <label className="cursor-pointer text-blue-600 hover:text-blue-700 font-medium">
                  Click to upload images
                  <input
                    type="file"
                    multiple
                    accept="image/*"
                    onChange={(e) => handleImageUpload(Array.from(e.target.files))}
                    className="hidden"
                  />
                </label>
                <p className="text-gray-500">or drag and drop</p>
              </div>
              <p className="text-sm text-gray-400">PNG, JPG, GIF up to 10MB each</p>
            </div>
          </div>

          {/* Image Preview */}
          {formData.images.length > 0 && (
            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
              {formData.images.map((image, index) => (
                <div key={index} className="relative group">
                  <img
                    src={image}
                    alt={`Preview ${index + 1}`}
                    className="w-full h-24 object-cover rounded-lg"
                  />
                  <button
                    type="button"
                    onClick={() => removeImage(index)}
                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 text-xs hover:bg-red-600 opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Submit Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className={`px-8 py-3 rounded-lg font-semibold text-white ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-green-600 hover:bg-green-700'
            } transition-colors`}
          >
            {loading ? 'Adding Organism...' : '✅ Add Organism'}
          </button>
        </div>
      </form>
    </div>
  );
};

// Manage Organisms Component
const ManageOrganisms = ({ organisms, token, onUpdate }) => {
  const [editingOrganism, setEditingOrganism] = useState(null);

  const handleDelete = async (organismId, organismName) => {
    if (window.confirm(`Are you sure you want to delete "${organismName}"? This action cannot be undone.`)) {
      try {
        await axios.delete(`${API}/admin/organisms/${organismId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert('Organism deleted successfully!');
        onUpdate();
      } catch (error) {
        alert('Error deleting organism: ' + (error.response?.data?.detail || error.message));
      }
    }
  };

  if (editingOrganism) {
    return (
      <EditOrganismForm
        organism={editingOrganism}
        token={token}
        onSuccess={() => {
          setEditingOrganism(null);
          onUpdate();
        }}
        onCancel={() => setEditingOrganism(null)}
      />
    );
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-6">📝 Manage Organisms</h2>
      
      <div className="space-y-4">
        {organisms.map((organism) => (
          <div key={organism.id} className="bg-gray-50 rounded-lg p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-4 mb-2">
                  <h3 className="text-xl font-semibold">{organism.name}</h3>
                  <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
                    {organism.classification?.kingdom || 'Unknown'}
                  </span>
                </div>
                <p className="text-gray-600 italic mb-2">{organism.scientific_name}</p>
                <p className="text-sm text-gray-700 line-clamp-2">{organism.description}</p>
                
                {organism.images && organism.images.length > 0 && (
                  <div className="mt-3 flex gap-2">
                    {organism.images.slice(0, 3).map((image, index) => (
                      <img
                        key={index}
                        src={image}
                        alt={`${organism.name} ${index + 1}`}
                        className="w-16 h-16 object-cover rounded border"
                      />
                    ))}
                    {organism.images.length > 3 && (
                      <div className="w-16 h-16 bg-gray-200 rounded border flex items-center justify-center text-sm">
                        +{organism.images.length - 3}
                      </div>
                    )}
                  </div>
                )}
              </div>
              
              <div className="flex gap-2 ml-4">
                <button
                  onClick={() => setEditingOrganism(organism)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium"
                >
                  ✏️ Edit
                </button>
                <button
                  onClick={() => handleDelete(organism.id, organism.name)}
                  className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium"
                >
                  🗑️ Delete
                </button>
              </div>
            </div>
          </div>
        ))}
        
        {organisms.length === 0 && (
          <div className="text-center py-12">
            <p className="text-xl text-gray-600">No organisms found.</p>
            <p className="text-gray-500 mt-2">Add your first organism using the "Add Organism" tab.</p>
          </div>
        )}
      </div>
    </div>
  );
};

// Edit Organism Form Component
const EditOrganismForm = ({ organism, token, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    name: organism.name || '',
    scientific_name: organism.scientific_name || '',
    classification: organism.classification || {
      kingdom: '', phylum: '', class: '', order: '', family: '', genus: '', species: ''
    },
    morphology: organism.morphology || '',
    physiology: organism.physiology || '',
    description: organism.description || '',
    images: organism.images || []
  });
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name.startsWith('classification.')) {
      const classField = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        classification: {
          ...prev.classification,
          [classField]: value
        }
      }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleImageUpload = async (files) => {
    const newImages = [];
    for (const file of files) {
      if (file.type.startsWith('image/')) {
        const base64 = await convertToBase64(file);
        newImages.push(base64);
      }
    }
    setFormData(prev => ({
      ...prev,
      images: [...prev.images, ...newImages]
    }));
  };

  const convertToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  };

  const removeImage = (index) => {
    setFormData(prev => ({
      ...prev,
      images: prev.images.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await axios.put(`${API}/admin/organisms/${organism.id}`, formData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      alert('Organism updated successfully!');
      onSuccess();
    } catch (error) {
      alert('Error updating organism: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-semibold">✏️ Edit Organism: {organism.name}</h2>
        <button
          onClick={onCancel}
          className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg"
        >
          Cancel
        </button>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Common Name *
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Scientific Name *
            </label>
            <input
              type="text"
              name="scientific_name"
              value={formData.scientific_name}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        {/* Classification */}
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-4">🔬 Taxonomic Classification</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'].map((field) => (
              <div key={field}>
                <label className="block text-sm font-medium text-gray-700 mb-1 capitalize">
                  {field}
                </label>
                <input
                  type="text"
                  name={`classification.${field}`}
                  value={formData.classification[field] || ''}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Description Fields */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              🏗️ Morphology *
            </label>
            <textarea
              name="morphology"
              value={formData.morphology}
              onChange={handleInputChange}
              required
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              ⚡ Physiology *
            </label>
            <textarea
              name="physiology"
              value={formData.physiology}
              onChange={handleInputChange}
              required
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              📝 Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={3}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        {/* Image Management */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            📸 Images
          </label>
          
          {/* Existing Images */}
          {formData.images.length > 0 && (
            <div className="mb-4 grid grid-cols-2 md:grid-cols-4 gap-4">
              {formData.images.map((image, index) => (
                <div key={index} className="relative group">
                  <img
                    src={image}
                    alt={`${formData.name} ${index + 1}`}
                    className="w-full h-24 object-cover rounded-lg"
                  />
                  <button
                    type="button"
                    onClick={() => removeImage(index)}
                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 text-xs hover:bg-red-600"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          )}
          
          {/* Add New Images */}
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
            <label className="cursor-pointer text-blue-600 hover:text-blue-700 font-medium">
              📁 Add More Images
              <input
                type="file"
                multiple
                accept="image/*"
                onChange={(e) => handleImageUpload(Array.from(e.target.files))}
                className="hidden"
              />
            </label>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end gap-4">
          <button
            type="button"
            onClick={onCancel}
            className="px-6 py-3 border border-gray-300 rounded-lg font-semibold text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className={`px-8 py-3 rounded-lg font-semibold text-white ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            } transition-colors`}
          >
            {loading ? 'Updating...' : '✅ Update Organism'}
          </button>
        </div>
      </form>
    </div>
  );
};

function App() {
  return (
    <AdminProvider>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path="/scanner" element={<QRScanner />} />
            <Route path="/organism/:id" element={<OrganismDetail />} />
            <Route path="/admin" element={<AdminPanel />} />
          </Routes>
        </BrowserRouter>
      </div>
    </AdminProvider>
  );
}

export default App;