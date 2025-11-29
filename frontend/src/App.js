import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { QrReader } from 'react-qr-reader';
import "./App.css";

// Determine backend URL based on current location
const BACKEND_URL = (() => {
  // If env var is set, use it
  if (process.env.REACT_APP_BACKEND_URL) {
    return process.env.REACT_APP_BACKEND_URL;
  }
  
  // On deployed Vercel (bio-museum.vercel.app), use Render backend
  if (window.location.hostname.includes('vercel.app')) {
    return 'https://biomuseum.onrender.com';
  }
  
  // On localhost, use local backend
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8000';
  }
  
  // Fallback to localhost
  return 'http://localhost:8000';
})();

const API = `${BACKEND_URL}/api`;

// Configure axios with longer timeout
axios.defaults.timeout = 30000; // 30 seconds for long operations

// Theme Context
const ThemeContext = React.createContext();

const ThemeProvider = ({ children }) => {
  const [isDark, setIsDark] = useState(() => {
    const saved = localStorage.getItem('theme_mode');
    if (saved) return saved === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    localStorage.setItem('theme_mode', isDark ? 'dark' : 'light');
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  const toggleTheme = () => setIsDark(!isDark);

  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

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
  const { isDark, toggleTheme } = React.useContext(ThemeContext);

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
      <div className={`min-h-screen ${isDark ? 'bg-gray-900' : 'bg-gradient-to-br from-green-50 to-blue-50'} flex items-center justify-center loading-container`}>
        <div className="text-center">
          {/* Creative DNA Spinner */}
          <div className="mb-8 flex justify-center">
            <div className="dna-spinner">
              <div className="text-6xl">🧬</div>
            </div>
          </div>

          {/* Animated Text */}
          <div className="mb-4">
            <h2 className={`text-2xl font-bold mb-2 ${isDark ? 'text-white' : 'text-gray-800'}`}>BioMuseum</h2>
            <p className={isDark ? 'text-gray-400' : 'text-gray-600'}>Discovering the wonders of life...</p>
          </div>

          {/* Animated Loading Bar */}
          <div className="w-64 mx-auto mb-4">
            <div className={`h-2 ${isDark ? 'bg-gray-700' : 'bg-gray-300'} rounded-full overflow-hidden`}>
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

          <p className={`text-sm mt-6 ${isDark ? 'text-gray-500' : 'text-gray-500'}`}>Loading organisms...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex flex-col min-h-screen ${isDark ? 'bg-gray-900' : 'bg-white'}`}>
      {/* Navbar */}
      <header className={`${isDark ? 'bg-gray-800 border-gray-700' : 'bg-gradient-to-r from-green-600 to-green-700 border-green-800'} shadow-lg border-b-4 sticky top-0 z-50`}>
        <div className="max-w-7xl mx-auto px-3 sm:px-4 py-2 sm:py-3">
          <div className="flex justify-between items-center">
            <div className="text-left">
              <h1 className="text-xl sm:text-2xl font-bold text-white">🌿 BioMuseum</h1>
            </div>
            <div className="flex gap-2 sm:gap-3 items-center">
              <button
                onClick={toggleTheme}
                className={`${isDark ? 'bg-gray-700 hover:bg-gray-600' : 'bg-white hover:bg-gray-100'} ${isDark ? 'text-yellow-400' : 'text-gray-800'} px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all duration-200 flex items-center gap-1 sm:gap-2 shadow-md hover:shadow-lg`}
              >
                <i className={`fas ${isDark ? 'fa-sun' : 'fa-moon'}`}></i> <span className="hidden sm:inline">{isDark ? 'Light' : 'Dark'}</span>
              </button>
              <button
                onClick={() => setShowAdminLogin(true)}
                className={`${isDark ? 'bg-gray-700 hover:bg-gray-600 text-green-400' : 'bg-white hover:bg-gray-100 text-green-700'} px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all duration-200 flex items-center gap-1 sm:gap-2 shadow-md hover:shadow-lg`}
              >
                <i className="fas fa-shield-alt"></i> <span className="hidden sm:inline">Admin</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section with Video Background */}
      <div className="relative h-screen md:h-[calc(100vh-80px)] overflow-hidden flex items-center justify-center">
        <video 
          autoPlay 
          muted 
          loop 
          className="absolute top-0 left-0 w-full h-full object-cover"
          playsInline
        >
          <source src="https://res.cloudinary.com/dhmgyv2ps/video/upload/v1764422065/Generated_File_November_29_2025_-_6_34PM_gvi1ux.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        
        {/* Overlay for text */}
        <div className="absolute inset-0 bg-black bg-opacity-50 flex flex-col justify-center items-center">
          <div className="text-center text-white px-4 sm:px-6 py-8">
            <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-3 sm:mb-4 leading-tight drop-shadow-lg">BioMuseum: A Journey Through Living Wonders</h2>
            <p className="text-sm sm:text-base md:text-lg lg:text-xl mb-6 sm:mb-8 max-w-2xl mx-auto leading-relaxed drop-shadow-md">
              Discover the wonders of life science through our interactive biology museum. Learn about diverse organisms and their fascinating characteristics.
            </p>
            <button
              onClick={() => navigate('/organisms')}
              className="bg-green-500 hover:bg-green-600 active:bg-green-700 text-white px-6 sm:px-8 py-2.5 sm:py-3 rounded-lg font-semibold text-sm sm:text-base md:text-lg transition-all duration-200 inline-flex items-center gap-2 shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              <i className="fas fa-arrow-right"></i> <span>Explore</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="flex-1">
      </main>

      {/* Footer */}
      <footer className={`${isDark ? 'bg-gradient-to-b from-gray-800 to-gray-900 border-gray-700' : 'bg-gradient-to-b from-gray-900 to-gray-950 border-green-600'} text-white mt-0 border-t-4`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 sm:py-10">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8">
            {/* About Section */}
            <div className="text-center sm:text-left">
              <h3 className={`text-lg sm:text-2xl font-bold mb-3 sm:mb-4 ${isDark ? 'text-green-400' : 'text-green-400'}`}>🌿 BioMuseum</h3>
              <p className={isDark ? 'text-gray-400' : 'text-gray-300'}>
               Our World is Built on Biology and Once We Begin to Understand it, it Becomes a Technology
              </p>
            </div>

            {/* Quick Links */}
            <div className="text-center sm:text-left">
              <h4 className={`text-base sm:text-lg font-semibold mb-3 sm:mb-4 ${isDark ? 'text-green-400' : 'text-green-400'}`}>Quick Links</h4>
              <ul className={`space-y-2 text-xs sm:text-sm ${isDark ? 'text-gray-400' : 'text-gray-300'}`}>
                <li><a href="/" className={`hover:${isDark ? 'text-green-300' : 'text-green-400'} transition-colors duration-200 flex items-center justify-center sm:justify-start gap-2`}><i className="fas fa-home"></i><span>Home</span></a></li>
                <li><a onClick={() => setShowAdminLogin(true)} className={`hover:${isDark ? 'text-green-300' : 'text-green-400'} transition-colors duration-200 cursor-pointer flex items-center justify-center sm:justify-start gap-2`}><i className="fas fa-shield-alt"></i><span>Admin Panel</span></a></li>
              </ul>
            </div>

            {/* Contact Info */}
            <div className="text-center sm:text-left">
              <h4 className={`text-base sm:text-lg font-semibold mb-3 sm:mb-4 ${isDark ? 'text-green-400' : 'text-green-400'}`}>Contact</h4>
              <ul className={`space-y-2 text-xs sm:text-sm ${isDark ? 'text-gray-400' : 'text-gray-300'}`}>
                <li><a href="mailto:sarthaknk07@outlook.com" className={`hover:${isDark ? 'text-green-300' : 'text-green-400'} transition-colors duration-200 flex items-center justify-center sm:justify-start gap-2`}><i className="fas fa-envelope"></i><span>sarthaknk07@outlook.com</span></a></li>
                <li className="flex items-center justify-center sm:justify-start gap-2"><i className="fas fa-map-marker-alt"></i><span>Zoology Department, SBES College of Science</span></li>
              </ul>
            </div>
          </div>

          {/* Divider */}
          <div className={`border-t ${isDark ? 'border-gray-700' : 'border-gray-700'} mt-8 sm:mt-10 pt-6 sm:pt-8`}>
            <div className={`text-center text-xs sm:text-sm ${isDark ? 'text-gray-500' : 'text-gray-400'}`}>
              <p className="mb-2">© Made with ❤️ @ Chh. Sambhaji Nagar</p>
              <p>Created by Sarthak N. Kulkarni B.Sc First Year</p>
            </div>
          </div>
        </div>
      </footer>

      {/* Admin Login Modal */}
      {showAdminLogin && (
        <div className={`fixed inset-0 ${isDark ? 'bg-black bg-opacity-70' : 'bg-black bg-opacity-50'} flex items-center justify-center z-50 p-4 sm:p-0`}>
          <div className={`${isDark ? 'bg-gray-800 border-green-600' : 'bg-white'} rounded-xl shadow-2xl p-6 sm:p-8 max-w-md w-full mx-auto border-t-4`}>
            <div className="text-center mb-6 sm:mb-8">
              <div className="text-4xl mb-2">🔐</div>
              <h2 className={`text-2xl sm:text-3xl font-bold ${isDark ? 'text-white' : 'text-gray-800'}`}>Admin Login</h2>
            </div>
            <form onSubmit={handleAdminLogin}>
              <div className="mb-4 sm:mb-5">
                <label className={`block text-sm font-bold mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                  <i className="fas fa-user mr-2 text-green-600"></i>Username
                </label>
                <input
                  type="text"
                  name="username"
                  className={`w-full px-4 py-2.5 border-2 rounded-lg focus:outline-none transition-all text-sm sm:text-base ${isDark ? 'bg-gray-700 border-gray-600 text-white focus:border-green-500 focus:ring-2 focus:ring-green-900' : 'border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200'}`}
                  placeholder="Enter username"
                  required
                />
              </div>
              <div className="mb-6 sm:mb-8">
                <label className={`block text-sm font-bold mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                  <i className="fas fa-lock mr-2 text-green-600"></i>Password
                </label>
                <input
                  type="password"
                  name="password"
                  className={`w-full px-4 py-2.5 border-2 rounded-lg focus:outline-none transition-all text-sm sm:text-base ${isDark ? 'bg-gray-700 border-gray-600 text-white focus:border-green-500 focus:ring-2 focus:ring-green-900' : 'border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200'}`}
                  placeholder="Enter password"
                  required
                />
              </div>
              <div className="flex gap-3 sm:gap-4">
                <button
                  type="button"
                  onClick={() => setShowAdminLogin(false)}
                  className={`flex-1 ${isDark ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-500 hover:bg-gray-600'} text-white py-2.5 rounded-lg font-semibold transition-all duration-200 text-sm sm:text-base`}
                >
                  <i className="fas fa-times mr-1"></i>Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-green-600 hover:bg-green-700 active:bg-green-800 text-white py-2.5 rounded-lg font-semibold transition-all duration-200 text-sm sm:text-base shadow-md hover:shadow-lg"
                >
                  <i className="fas fa-sign-in-alt mr-1"></i>Login
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
  const { isDark, toggleTheme } = React.useContext(ThemeContext);
  const navigate = useNavigate();
  const [activeView, setActiveView] = useState('dashboard');
  const [organisms, setOrganisms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editingOrganism, setEditingOrganism] = useState(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

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
    <div className={`min-h-screen ${isDark ? 'bg-gray-900' : 'bg-gradient-to-br from-purple-50 to-blue-50'}`}>
      {/* Header */}
      <header className={`${isDark ? 'bg-gray-800 border-gray-700' : 'bg-gradient-to-r from-purple-600 to-blue-600 border-purple-800'} shadow-lg border-b-4 sticky top-0 z-40`}>
        <div className="max-w-7xl mx-auto px-3 sm:px-4 py-3 sm:py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-lg sm:text-2xl font-bold text-white">🔧 Admin Panel</h1>
            <div className="flex gap-2 sm:gap-3 items-center">
              <button
                onClick={toggleTheme}
                className={`${isDark ? 'bg-gray-700 hover:bg-gray-600 text-yellow-400' : 'bg-white hover:bg-gray-100 text-gray-800'} px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all`}
              >
                <i className={`fas ${isDark ? 'fa-sun' : 'fa-moon'}`}></i>
              </button>
              <button
                onClick={() => navigate('/')}
                className={`${isDark ? 'bg-gray-700 hover:bg-gray-600' : 'bg-white hover:bg-gray-100'} ${isDark ? 'text-white' : 'text-purple-700'} px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all hidden sm:flex items-center gap-1`}
              >
                <i className="fas fa-home"></i> <span>Home</span>
              </button>
              <button
                onClick={logout}
                className="bg-red-600 hover:bg-red-700 text-white px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all flex items-center gap-1"
              >
                <i className="fas fa-sign-out-alt"></i> <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className={`${isDark ? 'bg-gray-800' : 'bg-white'} border-b ${isDark ? 'border-gray-700' : 'border-gray-200'} sticky top-16 z-30`}>
        <div className="max-w-7xl mx-auto">
          {/* Mobile Menu Button */}
          <div className="sm:hidden flex items-center justify-between px-3 py-2">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className={`px-3 py-2 rounded-lg ${isDark ? 'bg-gray-700' : 'bg-gray-100'}`}
            >
              <i className={`fas fa-bars ${isDark ? 'text-white' : 'text-gray-800'}`}></i>
            </button>
          </div>

          {/* Desktop Menu */}
          <div className={`hidden sm:flex border-b ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
            <button
              onClick={() => setActiveView('dashboard')}
              className={`px-6 py-4 font-semibold transition-all ${activeView === 'dashboard' 
                ? `border-b-2 ${isDark ? 'border-purple-500 text-purple-400' : 'border-purple-600 text-purple-600'}` 
                : `${isDark ? 'text-gray-400 hover:text-purple-400' : 'text-gray-600 hover:text-purple-600'}`}`}
            >
              📊 Dashboard
            </button>
            <button
              onClick={() => setActiveView('add')}
              className={`px-6 py-4 font-semibold transition-all ${activeView === 'add' 
                ? `border-b-2 ${isDark ? 'border-purple-500 text-purple-400' : 'border-purple-600 text-purple-600'}` 
                : `${isDark ? 'text-gray-400 hover:text-purple-400' : 'text-gray-600 hover:text-purple-600'}`}`}
            >
              ➕ Add Organism
            </button>
            <button
              onClick={() => setActiveView('manage')}
              className={`px-6 py-4 font-semibold transition-all ${activeView === 'manage' 
                ? `border-b-2 ${isDark ? 'border-purple-500 text-purple-400' : 'border-purple-600 text-purple-600'}` 
                : `${isDark ? 'text-gray-400 hover:text-purple-400' : 'text-gray-600 hover:text-purple-600'}`}`}
            >
              📝 Manage Organisms
            </button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className={`sm:hidden border-t ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
              <button
                onClick={() => { setActiveView('dashboard'); setMobileMenuOpen(false); }}
                className={`w-full text-left px-4 py-3 font-semibold ${activeView === 'dashboard' ? (isDark ? 'bg-purple-900 text-purple-300' : 'bg-purple-100 text-purple-700') : (isDark ? 'text-gray-300' : 'text-gray-700')}`}
              >
                📊 Dashboard
              </button>
              <button
                onClick={() => { setActiveView('add'); setMobileMenuOpen(false); }}
                className={`w-full text-left px-4 py-3 font-semibold ${activeView === 'add' ? (isDark ? 'bg-purple-900 text-purple-300' : 'bg-purple-100 text-purple-700') : (isDark ? 'text-gray-300' : 'text-gray-700')}`}
              >
                ➕ Add Organism
              </button>
              <button
                onClick={() => { setActiveView('manage'); setMobileMenuOpen(false); }}
                className={`w-full text-left px-4 py-3 font-semibold ${activeView === 'manage' ? (isDark ? 'bg-purple-900 text-purple-300' : 'bg-purple-100 text-purple-700') : (isDark ? 'text-gray-300' : 'text-gray-700')}`}
              >
                📝 Manage Organisms
              </button>
              <button
                onClick={() => { navigate('/'); setMobileMenuOpen(false); }}
                className={`w-full text-left px-4 py-3 font-semibold border-t ${isDark ? 'border-gray-700 text-gray-300' : 'border-gray-200 text-gray-700'}`}
              >
                🏠 Home
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-3 sm:px-4 py-6 sm:py-8">
        {activeView === 'dashboard' && (
          <DashboardView organisms={organisms} isDark={isDark} />
        )}
        {activeView === 'add' && (
          <AddOrganismForm 
            token={token} 
            isDark={isDark}
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
            isDark={isDark}
            onUpdate={fetchOrganisms}
            onEdit={setEditingOrganism}
          />
        )}
      </main>
    </div>
  );
};

// Dashboard View Component
const DashboardView = ({ organisms, isDark }) => {
  return (
    <div>
      <h2 className={`text-2xl sm:text-3xl font-semibold mb-6 ${isDark ? 'text-white' : 'text-gray-800'}`}>📊 Dashboard</h2>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-8">
        <div className={`p-6 rounded-lg transition-all ${isDark ? 'bg-green-900 border border-green-700' : 'bg-green-100'} hover:shadow-lg`}>
          <h3 className={`text-lg sm:text-xl font-semibold mb-2 ${isDark ? 'text-green-300' : 'text-green-800'}`}>Total Organisms</h3>
          <p className={`text-3xl sm:text-4xl font-bold ${isDark ? 'text-green-400' : 'text-green-600'}`}>{organisms.length}</p>
        </div>
        <div className={`p-6 rounded-lg transition-all ${isDark ? 'bg-blue-900 border border-blue-700' : 'bg-blue-100'} hover:shadow-lg`}>
          <h3 className={`text-lg sm:text-xl font-semibold mb-2 ${isDark ? 'text-blue-300' : 'text-blue-800'}`}>With Images</h3>
          <p className={`text-3xl sm:text-4xl font-bold ${isDark ? 'text-blue-400' : 'text-blue-600'}`}>
            {organisms.filter(org => org.images && org.images.length > 0).length}
          </p>
        </div>
        <div className={`p-6 rounded-lg transition-all ${isDark ? 'bg-purple-900 border border-purple-700' : 'bg-purple-100'} hover:shadow-lg`}>
          <h3 className={`text-lg sm:text-xl font-semibold mb-2 ${isDark ? 'text-purple-300' : 'text-purple-800'}`}>QR Codes</h3>
          <p className={`text-3xl sm:text-4xl font-bold ${isDark ? 'text-purple-400' : 'text-purple-600'}`}>{organisms.length}</p>
        </div>
      </div>
      
      <div className="mt-8">
        <h3 className={`text-xl sm:text-2xl font-semibold mb-4 ${isDark ? 'text-white' : 'text-gray-800'}`}>Recent Organisms</h3>
        <div className="space-y-3">
          {organisms.slice(0, 5).map((organism) => (
            <div key={organism.id} className={`flex items-center justify-between p-3 sm:p-4 rounded-lg transition-all ${isDark ? 'bg-gray-800 border border-gray-700 hover:border-purple-500' : 'bg-gray-50 hover:bg-gray-100 border border-gray-200'}`}>
              <div className="flex-1 min-w-0">
                <h4 className={`font-semibold truncate ${isDark ? 'text-white' : 'text-gray-800'}`}>{organism.name}</h4>
                <p className={`text-xs sm:text-sm italic truncate ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>{organism.scientific_name}</p>
              </div>
              <span className={`text-xs sm:text-sm ml-2 whitespace-nowrap ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                {organism.classification?.kingdom || 'Unknown'}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Add Organism Form Component
const AddOrganismForm = ({ token, isDark, onSuccess }) => {
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
  const [aiLoading, setAiLoading] = useState(false);
  const [aiOrganismName, setAiOrganismName] = useState('');
  const [showAiHelper, setShowAiHelper] = useState(false);

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

  const handleAiComplete = async () => {
    if (!aiOrganismName.trim()) {
      alert('Please enter an organism name');
      return;
    }

    setAiLoading(true);
    try {
      const response = await axios.post(`${API}/admin/organisms/ai-complete`, {
        organism_name: aiOrganismName
      }, {
        timeout: 60000 // 60 second timeout for AI
      });

      if (response.data.success) {
        const aiData = response.data.data;
        setFormData(prev => ({
          ...prev,
          name: aiData.name || prev.name,
          scientific_name: aiData.scientific_name || prev.scientific_name,
          classification: aiData.classification || prev.classification,
          morphology: aiData.morphology || prev.morphology,
          physiology: aiData.physiology || prev.physiology,
          description: aiData.general_description || prev.description
        }));
        setShowAiHelper(false);
        setAiOrganismName('');
        alert('✅ Organism data filled successfully! Review and adjust as needed.');
      }
    } catch (error) {
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to get AI response';
      alert('Error: ' + errorMsg);
    } finally {
      setAiLoading(false);
    }
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
      <div className="flex items-center justify-between mb-6 flex-col sm:flex-row gap-4">
        <h2 className={`text-2xl sm:text-3xl font-semibold ${isDark ? 'text-white' : 'text-gray-800'}`}>➕ Add New Organism</h2>
        <button
          type="button"
          onClick={() => setShowAiHelper(!showAiHelper)}
          className="w-full sm:w-auto bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white px-4 py-2 rounded-lg font-semibold transition-all flex items-center gap-2 justify-center"
        >
          <i className="fas fa-magic"></i> AI Helper
        </button>
      </div>

      {/* AI Helper Section */}
      {showAiHelper && (
        <div className={`mb-8 p-4 sm:p-6 rounded-xl border-2 shadow-lg ${isDark ? 'bg-purple-900 border-purple-700' : 'bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200'}`}>
          <div className="flex items-center gap-2 mb-4">
            <i className={`fas fa-robot text-2xl ${isDark ? 'text-purple-400' : 'text-purple-600'}`}></i>
            <h3 className={`text-base sm:text-lg font-bold ${isDark ? 'text-purple-300' : 'text-purple-800'}`}>🤖 AI Organism Assistant</h3>
          </div>
          <p className={`text-xs sm:text-sm mb-4 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
            Just enter the organism name and AI will automatically fill in all the biological information for you!
          </p>
          <div className="flex gap-2 sm:gap-3 flex-col sm:flex-row">
            <input
              type="text"
              value={aiOrganismName}
              onChange={(e) => setAiOrganismName(e.target.value)}
              placeholder="e.g., African Elephant, Tiger, Honeybee..."
              className={`flex-1 px-3 sm:px-4 py-2 rounded-lg focus:outline-none transition-all text-sm ${isDark ? 'bg-gray-700 border-2 border-purple-600 text-white focus:ring-2 focus:ring-purple-500' : 'border-2 border-purple-300 focus:border-purple-500 focus:ring-2 focus:ring-purple-200'}`}
              disabled={aiLoading}
            />
            <button
              type="button"
              onClick={handleAiComplete}
              disabled={aiLoading || !aiOrganismName.trim()}
              className="w-full sm:w-auto bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 sm:px-6 py-2 rounded-lg font-semibold transition-all flex items-center gap-2 justify-center text-sm"
            >
              {aiLoading ? (
                <>
                  <i className="fas fa-spinner fa-spin"></i>
                  <span className="hidden sm:inline">Loading...</span>
                </>
              ) : (
                <>
                  <i className="fas fa-sparkles"></i>
                  <span>Generate</span>
                </>
              )}
            </button>
          </div>
          {aiLoading && (
            <div className="mt-4 text-center">
              <p className={`font-semibold animate-pulse text-sm sm:text-base ${isDark ? 'text-purple-300' : 'text-purple-700'}`}>✨ AI is analyzing the organism...</p>
              <p className={`text-xs sm:text-sm mt-1 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>This may take a few seconds</p>
            </div>
          )}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-6">
        {/* Basic Information */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-6">
          <div>
            <label className={`block text-xs sm:text-sm font-semibold mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
              Common Name *
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
              className={`w-full px-3 sm:px-4 py-2 rounded-lg focus:outline-none transition-all text-sm ${isDark ? 'bg-gray-700 border-2 border-gray-600 text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500' : 'border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-purple-500'}`}
              placeholder="e.g., African Elephant"
            />
          </div>
          
          <div>
            <label className={`block text-xs sm:text-sm font-semibold mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
              Scientific Name *
            </label>
            <input
              type="text"
              name="scientific_name"
              value={formData.scientific_name}
              onChange={handleInputChange}
              required
              className={`w-full px-3 sm:px-4 py-2 rounded-lg focus:outline-none transition-all text-sm ${isDark ? 'bg-gray-700 border-2 border-gray-600 text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500' : 'border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-purple-500'}`}
              placeholder="e.g., Loxodonta africana"
            />
          </div>
        </div>

        {/* Classification */}
        <div>
          <h3 className={`text-base sm:text-lg font-semibold mb-3 sm:mb-4 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>🔬 Taxonomic Classification</h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2 sm:gap-4">
            {['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'].map((field) => (
              <div key={field}>
                <label className={`block text-xs font-medium mb-1 capitalize ${isDark ? 'text-gray-400' : 'text-gray-700'}`}>
                  {field}
                </label>
                <input
                  type="text"
                  name={`classification.${field}`}
                  value={formData.classification[field]}
                  onChange={handleInputChange}
                  className={`w-full px-2 sm:px-3 py-1 sm:py-2 rounded text-xs sm:text-sm focus:outline-none transition-all ${isDark ? 'bg-gray-700 border border-gray-600 text-white focus:border-purple-500' : 'border border-gray-300 focus:ring-2 focus:ring-purple-500'}`}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Description Fields */}
        <div className="space-y-3 sm:space-y-4">
          <div>
            <label className={`block text-xs sm:text-sm font-semibold mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
              🏗️ Morphology (Physical Structure) *
            </label>
            <textarea
              name="morphology"
              value={formData.morphology}
              onChange={handleInputChange}
              required
              rows="4"
              className={`w-full px-3 sm:px-4 py-2 rounded-lg focus:outline-none transition-all text-xs sm:text-sm ${isDark ? 'bg-gray-700 border-2 border-gray-600 text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500' : 'border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-purple-500'}`}
              placeholder="Describe the physical characteristics, size, shape, structure..."
            />
          </div>

          <div>
            <label className={`block text-xs sm:text-sm font-semibold mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
              ⚡ Physiology (Biological Functions) *
            </label>
            <textarea
              name="physiology"
              value={formData.physiology}
              onChange={handleInputChange}
              required
              rows="4"
              className={`w-full px-3 sm:px-4 py-2 rounded-lg focus:outline-none transition-all text-xs sm:text-sm ${isDark ? 'bg-gray-700 border-2 border-gray-600 text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500' : 'border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-purple-500'}`}
              placeholder="Describe biological processes, metabolism, reproduction, behavior..."
            />
          </div>

          <div>
            <label className={`block text-xs sm:text-sm font-semibold mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
              📝 General Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows="3"
              className={`w-full px-3 sm:px-4 py-2 rounded-lg focus:outline-none transition-all text-xs sm:text-sm ${isDark ? 'bg-gray-700 border-2 border-gray-600 text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500' : 'border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-purple-500'}`}
              placeholder="Additional information, conservation status, interesting facts..."
            />
          </div>
        </div>

        {/* Image Upload */}
        <div>
          <label className={`block text-xs sm:text-sm font-semibold mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
            📸 Images
          </label>
          
          <div className={`mb-3 sm:mb-4 p-3 sm:p-4 rounded-lg ${isDark ? 'bg-gray-700 border border-gray-600' : 'border border-gray-300'}`}>
            <div className="flex gap-2 mb-3 flex-col sm:flex-row">
              <input
                type="url"
                value={imageUrl}
                onChange={(e) => setImageUrl(e.target.value)}
                placeholder="Paste image URL..."
                className={`flex-1 px-3 sm:px-4 py-2 rounded-lg focus:outline-none transition-all text-xs sm:text-sm ${isDark ? 'bg-gray-600 border border-gray-500 text-white' : 'border border-gray-300'}`}
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
                className="w-full sm:w-auto bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm"
              >
                Add URL
              </button>
            </div>
            <div className={`text-center text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>or</div>
          </div>
          
          <div
            className={`border-2 border-dashed rounded-lg p-6 sm:p-8 text-center transition-colors ${
              dragActive 
                ? (isDark ? 'border-purple-500 bg-purple-900 bg-opacity-30' : 'border-purple-500 bg-purple-50') 
                : (isDark ? 'border-gray-600' : 'border-gray-300')
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="space-y-2">
              <div className="text-3xl sm:text-4xl">📁</div>
              <div>
                <label className={`cursor-pointer font-medium text-xs sm:text-sm ${isDark ? 'text-purple-400 hover:text-purple-300' : 'text-purple-600 hover:text-purple-700'}`}>
                  Click to upload images
                  <input
                    type="file"
                    multiple
                    accept="image/*"
                    onChange={(e) => handleImageUpload(Array.from(e.target.files))}
                    className="hidden"
                  />
                </label>
                <p className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>or drag and drop</p>
              </div>
              <p className={`text-xs ${isDark ? 'text-gray-500' : 'text-gray-400'}`}>PNG, JPG, GIF up to 10MB each</p>
            </div>
          </div>

          {/* Image Preview */}
          {formData.images.length > 0 && (
            <div className="mt-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2 sm:gap-4">
              {formData.images.map((image, index) => (
                <div key={index} className="relative group">
                  <img
                    src={image}
                    alt={`Preview ${index + 1}`}
                    className="w-full h-20 sm:h-24 object-cover rounded-lg"
                  />
                  <button
                    type="button"
                    onClick={() => removeImage(index)}
                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 sm:w-6 sm:h-6 text-xs hover:bg-red-600 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Submit Button */}
        <div className="flex justify-end pt-4 sm:pt-6">
          <button
            type="submit"
            disabled={loading}
            className={`w-full sm:w-auto px-6 sm:px-8 py-3 rounded-lg font-semibold text-white transition-all text-sm sm:text-base ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-green-600 hover:bg-green-700 shadow-lg hover:shadow-xl'
            }`}
          >
            {loading ? 'Adding Organism...' : '✅ Add Organism'}
          </button>
        </div>
      </form>
    </div>
  );
};

// Manage Organisms Component
const ManageOrganisms = ({ organisms, token, isDark, onUpdate }) => {
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
      <h2 className={`text-2xl sm:text-3xl font-semibold mb-6 ${isDark ? 'text-white' : 'text-gray-800'}`}>📝 Manage Organisms</h2>
      
      <div className="space-y-3 sm:space-y-4">
        {organisms.map((organism) => (
          <div key={organism.id} className={`rounded-lg p-3 sm:p-6 transition-all ${isDark ? 'bg-gray-800 border border-gray-700 hover:border-purple-500' : 'bg-white border border-gray-200 hover:shadow-lg'}`}>
            <div className="flex flex-col sm:flex-row items-start justify-between gap-3">
              <div className="flex-1 min-w-0 w-full sm:w-auto">
                <div className="flex items-center gap-2 sm:gap-4 mb-2 flex-wrap">
                  <h3 className={`text-base sm:text-xl font-semibold truncate ${isDark ? 'text-white' : 'text-gray-800'}`}>{organism.name}</h3>
                  <span className={`text-xs sm:text-sm px-2 py-1 rounded whitespace-nowrap ${isDark ? 'bg-blue-900 text-blue-300' : 'bg-blue-100 text-blue-800'}`}>
                    {organism.classification?.kingdom || 'Unknown'}
                  </span>
                </div>
                <p className={`text-xs sm:text-sm italic truncate mb-1 sm:mb-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>{organism.scientific_name}</p>
                <p className={`text-xs sm:text-sm line-clamp-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>{organism.description}</p>
                
                {organism.images && organism.images.length > 0 && (
                  <div className="mt-2 sm:mt-3 flex gap-1 sm:gap-2 flex-wrap">
                    {organism.images.slice(0, 3).map((image, index) => (
                      <img
                        key={index}
                        src={image}
                        alt={`${organism.name} ${index + 1}`}
                        className={`w-12 h-12 sm:w-16 sm:h-16 object-cover rounded border ${isDark ? 'border-gray-600' : 'border-gray-300'}`}
                      />
                    ))}
                    {organism.images.length > 3 && (
                      <div className={`w-12 h-12 sm:w-16 sm:h-16 rounded border flex items-center justify-center text-xs sm:text-sm ${isDark ? 'bg-gray-700 border-gray-600' : 'bg-gray-200 border-gray-300'}`}>
                        +{organism.images.length - 3}
                      </div>
                    )}
                  </div>
                )}
              </div>
              
              <div className="flex gap-2 ml-0 sm:ml-4 w-full sm:w-auto">
                <button
                  onClick={() => setEditingOrganism(organism)}
                  className="flex-1 sm:flex-none bg-blue-600 hover:bg-blue-700 text-white px-3 sm:px-4 py-2 rounded-lg font-medium text-xs sm:text-sm transition-all"
                >
                  ✏️ <span className="hidden sm:inline">Edit</span>
                </button>
                <button
                  onClick={() => handleDelete(organism.id, organism.name)}
                  className="flex-1 sm:flex-none bg-red-600 hover:bg-red-700 text-white px-3 sm:px-4 py-2 rounded-lg font-medium text-xs sm:text-sm transition-all"
                >
                  🗑️ <span className="hidden sm:inline">Delete</span>
                </button>
              </div>
            </div>
          </div>
        ))}
        
        {organisms.length === 0 && (
          <div className={`text-center py-12 rounded-lg ${isDark ? 'bg-gray-800 border border-gray-700' : 'bg-gray-50 border border-gray-200'}`}>
            <p className={`text-base sm:text-lg font-semibold ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>No organisms found.</p>
            <p className={`text-xs sm:text-sm mt-2 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>Add your first organism using the "Add Organism" tab.</p>
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

// Organisms Page Component
const OrganismsPage = () => {
  const [organisms, setOrganisms] = useState([]);
  const [allOrganisms, setAllOrganisms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedKingdom, setSelectedKingdom] = useState('');
  const [selectedPhylum, setSelectedPhylum] = useState('');
  const navigate = useNavigate();
  const { isDark, toggleTheme } = React.useContext(ThemeContext);

  useEffect(() => {
    fetchOrganisms();
  }, []);

  const fetchOrganisms = async () => {
    try {
      const response = await axios.get(`${API}/organisms`);
      setAllOrganisms(response.data);
      setOrganisms(response.data);
    } catch (error) {
      console.error('Error fetching organisms:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKingdomChange = (e) => {
    const kingdom = e.target.value;
    setSelectedKingdom(kingdom);
    filterOrganisms(kingdom, selectedPhylum);
  };

  const handlePhylumChange = (e) => {
    const phylum = e.target.value;
    setSelectedPhylum(phylum);
    filterOrganisms(selectedKingdom, phylum);
  };

  const filterOrganisms = (kingdom, phylum) => {
    let filtered = allOrganisms;
    
    if (kingdom) {
      filtered = filtered.filter(org => org.classification?.kingdom === kingdom);
    }
    
    if (phylum) {
      filtered = filtered.filter(org => org.classification?.phylum === phylum);
    }
    
    setOrganisms(filtered);
  };

  const getUniqueKingdoms = () => {
    return [...new Set(allOrganisms.map(org => org.classification?.kingdom).filter(Boolean))];
  };

  const getUniquePhyla = () => {
    return [...new Set(allOrganisms.map(org => org.classification?.phylum).filter(Boolean))];
  };

  if (loading) {
    return (
      <div className={`flex items-center justify-center min-h-screen ${isDark ? 'bg-gray-900' : 'bg-gray-50'}`}>
        <div className="text-center px-4">
          <div className="text-4xl mb-4">🧬</div>
          <div className={`text-lg sm:text-2xl font-bold ${isDark ? 'text-green-400' : 'text-green-600'}`}>Loading organisms...</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex flex-col min-h-screen ${isDark ? 'bg-gray-900' : 'bg-white'}`}>
      {/* Navbar */}
      <header className={`${isDark ? 'bg-gray-800 border-gray-700' : 'bg-gradient-to-r from-green-600 to-green-700 border-green-800'} shadow-lg border-b-4 sticky top-0 z-50`}>
        <div className="max-w-7xl mx-auto px-3 sm:px-4 py-2 sm:py-3 flex justify-between items-center">
          <h1 className="text-lg sm:text-2xl font-bold text-white">🌿 BioMuseum</h1>
          <div className="flex gap-2 sm:gap-3 items-center">
            <button
              onClick={toggleTheme}
              className={`${isDark ? 'bg-gray-700 hover:bg-gray-600 text-yellow-400' : 'bg-white hover:bg-gray-100 text-gray-800'} px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all`}
            >
              <i className={`fas ${isDark ? 'fa-sun' : 'fa-moon'}`}></i>
            </button>
            <button onClick={() => window.location.href = '/'} className={`${isDark ? 'bg-gray-700 hover:bg-gray-600 text-green-400' : 'bg-white hover:bg-gray-100 text-green-700'} px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all flex items-center gap-1 sm:gap-2 shadow-md`}>
              <i className="fas fa-arrow-left"></i><span className="hidden sm:inline">Back</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full py-6 sm:py-8 px-3 sm:px-4">
        <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-6 sm:mb-8 text-center text-gray-800">
          <i className="fas fa-binoculars mr-2 text-green-600"></i>Explore Organisms
        </h2>

        {/* Filter Section */}
        <div className={`mb-6 sm:mb-8 p-4 sm:p-6 rounded-xl shadow-md border-l-4 border-green-600 ${isDark ? 'bg-gray-800' : 'bg-white'}`}>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-6">
            {/* Kingdom Filter */}
            <div>
              <label className={`block font-semibold mb-2 text-sm sm:text-base ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                <i className="fas fa-filter mr-2 text-green-600"></i>Filter by Kingdom
              </label>
              <select
                value={selectedKingdom}
                onChange={handleKingdomChange}
                className={`w-full px-3 sm:px-4 py-2 rounded-lg focus:outline-none transition-all text-sm sm:text-base border-2 ${isDark ? 'bg-gray-700 border-gray-600 text-white focus:border-green-500 focus:ring-2 focus:ring-green-900' : 'border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200'}`}
              >
                <option value="">All Kingdoms</option>
                {getUniqueKingdoms().map(kingdom => (
                  <option key={kingdom} value={kingdom}>{kingdom}</option>
                ))}
              </select>
            </div>

            {/* Phylum Filter */}
            <div>
              <label className={`block font-semibold mb-2 text-sm sm:text-base ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                <i className="fas fa-filter mr-2 text-green-600"></i>Filter by Phylum
              </label>
              <select
                value={selectedPhylum}
                onChange={handlePhylumChange}
                className={`w-full px-3 sm:px-4 py-2 rounded-lg focus:outline-none transition-all text-sm sm:text-base border-2 ${isDark ? 'bg-gray-700 border-gray-600 text-white focus:border-green-500 focus:ring-2 focus:ring-green-900' : 'border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200'}`}
              >
                <option value="">All Phyla</option>
                {getUniquePhyla().map(phylum => (
                  <option key={phylum} value={phylum}>{phylum}</option>
                ))}
              </select>
            </div>
          </div>
          <p className={`text-xs sm:text-sm mt-3 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>Showing {organisms.length} organism{organisms.length !== 1 ? 's' : ''}</p>
        </div>

        {/* Organisms Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
          {organisms.map((organism) => (
            <div
              key={organism.id}
              onClick={() => navigate(`/organism/${organism.id}`)}
              className={`rounded-xl shadow-md hover:shadow-xl transition-all cursor-pointer transform hover:scale-105 duration-300 overflow-hidden border ${isDark ? 'bg-gray-800 border-gray-700 hover:border-green-500' : 'bg-white border-gray-200 hover:border-green-300'}`}
            >
              <div className={`flex items-center justify-center overflow-hidden h-40 sm:h-48 ${isDark ? 'bg-gray-700' : 'bg-gray-100'}`}>
                {organism.images && organism.images[0] ? (
                  <img
                    src={organism.images[0]}
                    alt={organism.name}
                    className="w-full h-full object-cover hover:brightness-110 transition-all"
                  />
                ) : (
                  <div className="text-3xl sm:text-4xl"><i className="fas fa-leaf text-green-600"></i></div>
                )}
              </div>
              <div className={`p-3 sm:p-4 text-center ${isDark ? 'bg-gray-800' : 'bg-white'}`}>
                <h3 className={`text-base sm:text-lg font-bold mb-1 line-clamp-2 ${isDark ? 'text-white' : 'text-gray-800'}`}>{organism.name}</h3>
                <p className={`text-xs sm:text-sm italic mb-2 sm:mb-3 line-clamp-1 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>{organism.scientific_name}</p>
                {organism.classification && (
                  <div className="mt-2 sm:mt-3">
                    <span className={`inline-block text-xs px-2 sm:px-3 py-1 rounded-full font-medium ${isDark ? 'bg-green-900 text-green-300' : 'bg-green-100 text-green-800'}`}>
                      {organism.classification.kingdom || 'Unknown'}
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {organisms.length === 0 && (
          <div className={`text-center py-12 sm:py-16 rounded-xl ${isDark ? 'bg-gray-800' : 'bg-gray-50'}`}>
            <div className="text-4xl mb-4">🔍</div>
            <p className={`text-base sm:text-lg font-semibold ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>No organisms found</p>
            <p className={`text-xs sm:text-sm mt-2 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>Try adjusting your search filters.</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className={`${isDark ? 'bg-gradient-to-b from-gray-800 to-gray-900 border-gray-700' : 'bg-gradient-to-b from-gray-900 to-gray-950 border-green-600'} text-white mt-10 sm:mt-12 border-t-4`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8">
            <div className="text-center sm:text-left">
              <h3 className="text-lg sm:text-xl font-bold mb-2 sm:mb-3 text-green-400">🌿 BioMuseum</h3>
              <p className={`text-xs sm:text-sm leading-relaxed ${isDark ? 'text-gray-400' : 'text-gray-300'}`}>
                Discover the wonders of life science through our interactive biology museum.
              </p>
            </div>
            <div className="text-center sm:text-left">
              <h4 className="text-sm sm:text-base font-semibold mb-2 sm:mb-3 text-green-400">Links</h4>
              <ul className={`space-y-1 sm:space-y-2 text-xs sm:text-sm ${isDark ? 'text-gray-400' : 'text-gray-300'}`}>
                <li><a href="/" className="hover:text-green-400 transition-colors flex items-center justify-center sm:justify-start gap-2"><i className="fas fa-home"></i><span>Home</span></a></li>
              </ul>
            </div>
            <div className="text-center sm:text-left">
              <h4 className="text-sm sm:text-base font-semibold mb-2 sm:mb-3 text-green-400">Contact</h4>
              <p className={`text-xs sm:text-sm ${isDark ? 'text-gray-400' : 'text-gray-300'}`}><i className="fas fa-envelope mr-2"></i><a href="mailto:sarthaknk07@outlook.com" className="hover:text-green-400">sarthaknk07@outlook.com</a></p>
            </div>
          </div>
          <div className={`border-t ${isDark ? 'border-gray-700' : 'border-gray-700'} mt-6 sm:mt-8 pt-4 sm:pt-6 text-center ${isDark ? 'text-gray-500' : 'text-gray-400'} text-xs sm:text-sm`}>
            <p>© Made with 💚 @ Chh. Sambhaji Nagar</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

function App() {
  return (
    <ThemeProvider>
      <AdminProvider>
        <div className="App">
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Homepage />} />
              <Route path="/organisms" element={<OrganismsPage />} />
              <Route path="/scanner" element={<QRScanner />} />
              <Route path="/organism/:id" element={<OrganismDetail />} />
              <Route path="/admin" element={<AdminPanel />} />
            </Routes>
          </BrowserRouter>
        </div>
      </AdminProvider>
    </ThemeProvider>
  );
}

export default App;