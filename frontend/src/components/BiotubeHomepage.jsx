import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';

const BiotubeHomepage = ({ isDark }) => {
  const [videos, setVideos] = useState([]);
  const [filteredVideos, setFilteredVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilterModal, setShowFilterModal] = useState(false);
  const [showSuggestModal, setShowSuggestModal] = useState(false);
  const [userToken, setUserToken] = useState(localStorage.getItem('userToken'));
  const [userName, setUserName] = useState(localStorage.getItem('userName'));
  const [filters, setFilters] = useState({
    kingdom: '',
    phylum: '',
    class_name: '',
    species: ''
  });
  const [availableFilters, setAvailableFilters] = useState({
    kingdoms: [],
    phylums: [],
    classes: [],
    species: []
  });

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || (
    window.location.hostname.includes('vercel.app')
      ? 'https://biomuseum.onrender.com'
      : 'http://localhost:8000'
  );
  const API = `${BACKEND_URL}/api`;

  useEffect(() => {
    fetchVideos();
    fetchFilters();
  }, []);

  const fetchVideos = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/biotube/videos`);
      setVideos(response.data);
      setFilteredVideos(response.data);
    } catch (error) {
      console.error('Error fetching videos:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchFilters = async () => {
    try {
      const response = await axios.get(`${API}/biotube/filters`);
      setAvailableFilters(response.data);
    } catch (error) {
      console.error('Error fetching filters:', error);
    }
  };

  const handleSearch = (e) => {
    const query = e.target.value.toLowerCase();
    setSearchQuery(query);
    filterVideos(query, filters);
  };

  const handleFilterChange = (filterName, value) => {
    const newFilters = { ...filters, [filterName]: value };
    setFilters(newFilters);
    filterVideos(searchQuery, newFilters);
  };

  const filterVideos = (search, filterObj) => {
    let result = videos;

    // Apply filters
    if (filterObj.kingdom) {
      result = result.filter(v => v.kingdom.toLowerCase() === filterObj.kingdom.toLowerCase());
    }
    if (filterObj.phylum) {
      result = result.filter(v => v.phylum.toLowerCase() === filterObj.phylum.toLowerCase());
    }
    if (filterObj.class_name) {
      result = result.filter(v => v.class_name.toLowerCase() === filterObj.class_name.toLowerCase());
    }
    if (filterObj.species) {
      result = result.filter(v => v.species.toLowerCase() === filterObj.species.toLowerCase());
    }

    // Apply search
    if (search) {
      result = result.filter(v =>
        v.title.toLowerCase().includes(search) ||
        v.description.toLowerCase().includes(search) ||
        v.species.toLowerCase().includes(search)
      );
    }

    setFilteredVideos(result);
  };

  const clearFilters = () => {
    setFilters({
      kingdom: '',
      phylum: '',
      class_name: '',
      species: ''
    });
    setSearchQuery('');
    setFilteredVideos(videos);
  };

  const handleGoogleLoginSuccess = async (credentialResponse) => {
    try {
      console.log('Google login initiated with token');
      
      const response = await axios.post(`${API}/auth/gmail/login`, {
        token: credentialResponse.credential
      });
      
      console.log('Login successful:', response.data);
      
      setUserToken(response.data.access_token);
      setUserName(response.data.user.name);
      localStorage.setItem('userToken', response.data.access_token);
      localStorage.setItem('userName', response.data.user.name);
      localStorage.setItem('userEmail', response.data.user.email);
      
      alert(`✅ Welcome, ${response.data.user.name}!`);
    } catch (error) {
      console.error('Google login failed - Full error:', error);
      console.error('Error response data:', error.response?.data);
      console.error('Error status:', error.response?.status);
      console.error('Error message:', error.message);
      
      const errorMsg = error.response?.data?.detail || error.message || 'Login failed. Please try again.';
      alert(`❌ Login Error:\n${errorMsg}`);
    }
  };

  const handleLogout = () => {
    setUserToken(null);
    setUserName(null);
    localStorage.removeItem('userToken');
    localStorage.removeItem('userName');
    localStorage.removeItem('userEmail');
    alert('You have been logged out');
  };

  return (
    <div className={`min-h-screen ${isDark ? 'bg-gray-900' : 'bg-gray-50'}`}>
      {/* Header - Single line responsive navbar */}
      <header className={`${isDark ? 'bg-gray-800 border-gray-700' : 'bg-gradient-to-r from-purple-600 to-purple-700 border-purple-800'} shadow-lg border-b-4 sticky top-0 z-50`}>
        <div className="max-w-7xl mx-auto px-3 sm:px-6 py-2 sm:py-3">
          <div className="flex justify-between items-center gap-2 sm:gap-4">
            {/* Left: Back Button and Logo */}
            <div className="flex items-center gap-2 sm:gap-3 min-w-0">
              <a
                href="/"
                className={`${isDark ? 'bg-gray-700 hover:bg-gray-600 text-gray-300' : 'bg-white hover:bg-gray-100 text-purple-700'} px-2 sm:px-3 py-1.5 sm:py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all duration-200 whitespace-nowrap flex-shrink-0 shadow-md hover:shadow-lg`}
              >
                ← Back
              </a>
              <h1 className={`text-base sm:text-2xl font-bold whitespace-nowrap ${isDark ? 'text-white' : 'text-white'}`}>
                🎬 BioTube
              </h1>
            </div>

            {/* Right: Buttons */}
            <div className="flex gap-2 sm:gap-3 items-center flex-wrap justify-end">
              {/* Suggest Button */}
              <button
                onClick={() => setShowSuggestModal(true)}
                className={`${isDark ? 'bg-green-700 hover:bg-green-600 text-green-100' : 'bg-white hover:bg-gray-100 text-green-700'} px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all duration-200 flex items-center gap-1 sm:gap-2 shadow-md hover:shadow-lg`}
              >
                <i className="fas fa-lightbulb"></i> <span className="hidden sm:inline">Suggest</span>
              </button>

              {/* User Profile or Google Login */}
              {userToken && userName ? (
                <>
                  <div className={`px-2 sm:px-3 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-semibold whitespace-nowrap ${isDark ? 'bg-green-900 text-green-100' : 'bg-white text-green-700'}`}>
                    👤 <span className="hidden sm:inline">{userName}</span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className={`${isDark ? 'bg-red-700 hover:bg-red-600' : 'bg-white hover:bg-gray-100'} ${isDark ? 'text-red-100' : 'text-red-700'} px-2 sm:px-3 py-1.5 sm:py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all duration-200 shadow-md hover:shadow-lg`}
                  >
                    🚪 <span className="hidden sm:inline">Logout</span>
                  </button>
                </>
              ) : (
                <GoogleLoginButtonWrapper onSuccess={handleGoogleLoginSuccess} isDark={isDark} />
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Search and Filter Section */}
      <div className={`${isDark ? 'bg-gray-800' : 'bg-white'} py-4 sm:py-6 border-b ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
        <div className="max-w-7xl mx-auto px-3 sm:px-6">
          {/* Search Bar */}
          <div className="mb-3 sm:mb-4">
            <div className={`relative flex items-center ${isDark ? 'bg-gray-700' : 'bg-gray-100'} rounded-full px-3 sm:px-4 py-2`}>
              <span className="text-lg sm:text-2xl mr-2 sm:mr-3">🔍</span>
              <input
                type="text"
                placeholder="Search videos..."
                value={searchQuery}
                onChange={handleSearch}
                className={`flex-1 text-sm sm:text-base outline-none bg-transparent ${isDark ? 'text-white placeholder-gray-400' : 'text-gray-900 placeholder-gray-500'}`}
              />
            </div>
          </div>

          {/* Filter Controls */}
          <div className="flex gap-2 sm:gap-3 flex-wrap items-center text-xs sm:text-base">
            <button
              onClick={() => setShowFilterModal(!showFilterModal)}
              className={`px-2 sm:px-4 py-2 rounded-lg font-semibold transition-all flex items-center gap-1 sm:gap-2 text-xs sm:text-sm ${
                isDark
                  ? 'bg-purple-600 hover:bg-purple-700 text-white'
                  : 'bg-purple-500 hover:bg-purple-600 text-white'
              }`}
            >
              ⚙️ <span className="hidden sm:inline">Filters</span>
            </button>

            {Object.values(filters).some(f => f !== '') && (
              <button
                onClick={clearFilters}
                className={`px-2 sm:px-4 py-2 rounded-lg font-semibold transition-all text-xs sm:text-sm ${
                  isDark
                    ? 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                    : 'bg-gray-300 hover:bg-gray-400 text-gray-800'
                }`}
              >
                ✕ <span className="hidden sm:inline">Clear</span>
              </button>
            )}

            {/* Active Filter Tags */}
            <div className="flex gap-2 flex-wrap">
              {filters.kingdom && (
                <span className={`px-3 py-1 rounded-full text-sm ${isDark ? 'bg-green-900 text-green-200' : 'bg-green-100 text-green-800'}`}>
                  Kingdom: {filters.kingdom}
                </span>
              )}
              {filters.phylum && (
                <span className={`px-3 py-1 rounded-full text-sm ${isDark ? 'bg-blue-900 text-blue-200' : 'bg-blue-100 text-blue-800'}`}>
                  Phylum: {filters.phylum}
                </span>
              )}
              {filters.class_name && (
                <span className={`px-3 py-1 rounded-full text-sm ${isDark ? 'bg-purple-900 text-purple-200' : 'bg-purple-100 text-purple-800'}`}>
                  Class: {filters.class_name}
                </span>
              )}
              {filters.species && (
                <span className={`px-3 py-1 rounded-full text-sm ${isDark ? 'bg-orange-900 text-orange-200' : 'bg-orange-100 text-orange-800'}`}>
                  Species: {filters.species}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Filter Modal */}
      {showFilterModal && (
        <div className={`${isDark ? 'bg-gray-800' : 'bg-white'} py-4 sm:py-6 border-b ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
          <div className="max-w-7xl mx-auto px-3 sm:px-6">
            <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-4">
              {/* Kingdom Filter */}
              <div>
                <label className={`block text-xs sm:text-sm font-semibold mb-1 sm:mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                  Kingdom
                </label>
                <select
                  value={filters.kingdom}
                  onChange={(e) => handleFilterChange('kingdom', e.target.value)}
                  className={`w-full px-2 sm:px-3 py-1 sm:py-2 rounded border text-xs sm:text-base ${
                    isDark
                      ? 'bg-gray-700 border-gray-600 text-white'
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                >
                  <option value="">All Kingdoms</option>
                  {availableFilters.kingdoms.map(k => (
                    <option key={k} value={k}>{k}</option>
                  ))}
                </select>
              </div>

              {/* Phylum Filter */}
              <div>
                <label className={`block text-xs sm:text-sm font-semibold mb-1 sm:mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                  Phylum
                </label>
                <select
                  value={filters.phylum}
                  onChange={(e) => handleFilterChange('phylum', e.target.value)}
                  className={`w-full px-2 sm:px-3 py-1 sm:py-2 rounded border text-xs sm:text-base ${
                    isDark
                      ? 'bg-gray-700 border-gray-600 text-white'
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                >
                  <option value="">All Phylums</option>
                  {availableFilters.phylums.map(p => (
                    <option key={p} value={p}>{p}</option>
                  ))}
                </select>
              </div>

              {/* Class Filter */}
              <div>
                <label className={`block text-xs sm:text-sm font-semibold mb-1 sm:mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                  Class
                </label>
                <select
                  value={filters.class_name}
                  onChange={(e) => handleFilterChange('class_name', e.target.value)}
                  className={`w-full px-2 sm:px-3 py-1 sm:py-2 rounded border text-xs sm:text-base ${
                    isDark
                      ? 'bg-gray-700 border-gray-600 text-white'
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                >
                  <option value="">All Classes</option>
                  {availableFilters.classes.map(c => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              {/* Species Filter */}
              <div>
                <label className={`block text-xs sm:text-sm font-semibold mb-1 sm:mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                  Species
                </label>
                <select
                  value={filters.species}
                  onChange={(e) => handleFilterChange('species', e.target.value)}
                  className={`w-full px-2 sm:px-3 py-1 sm:py-2 rounded border text-xs sm:text-base ${
                    isDark
                      ? 'bg-gray-700 border-gray-600 text-white'
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                >
                  <option value="">All Species</option>
                  {availableFilters.species.map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Video Grid */}
      <div className="max-w-7xl mx-auto px-3 sm:px-6 py-6 sm:py-12">
        {loading ? (
          <div className="text-center py-12">
            <div className={`text-2xl mb-4 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>🎬</div>
            <p className={isDark ? 'text-gray-400' : 'text-gray-600'}>Loading videos...</p>
          </div>
        ) : filteredVideos.length === 0 ? (
          <div className={`text-center py-12 rounded-lg ${isDark ? 'bg-gray-800' : 'bg-gray-100'}`}>
            <div className={`text-4xl mb-4 ${isDark ? 'text-gray-600' : 'text-gray-400'}`}>📺</div>
            <p className={`text-lg font-semibold ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
              No videos found
            </p>
            <p className={`text-sm mt-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
              Try adjusting your search or filters
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-6">
            {filteredVideos.map((video) => (
              <a
                key={video.id}
                href={`/biotube/watch/${video.id}`}
                className={`group rounded-lg overflow-hidden transition-all hover:shadow-lg ${
                  isDark ? 'bg-gray-800 hover:bg-gray-700' : 'bg-white hover:bg-gray-50'
                }`}
              >
                {/* Thumbnail */}
                <div className="relative bg-gray-900 aspect-video overflow-hidden flex items-center justify-center">
                  <img
                    src={video.thumbnail_url || 'https://via.placeholder.com/320x180?text=No%20Thumbnail'}
                    alt={video.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    loading="lazy"
                    onError={(e) => {
                      console.warn(`Failed to load thumbnail for: ${video.title}`);
                      e.target.src = 'https://via.placeholder.com/320x180?text=Video%20Thumbnail';
                      e.target.style.backgroundColor = '#1f2937';
                    }}
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all flex items-center justify-center">
                    <div className="text-white text-4xl opacity-0 group-hover:opacity-100 transition-opacity drop-shadow-lg">
                      ▶
                    </div>
                  </div>
                </div>

                {/* Video Info */}
                <div className="p-2 sm:p-4">
                  <h3 className={`font-semibold line-clamp-2 mb-2 text-sm sm:text-base ${isDark ? 'text-white' : 'text-gray-900'}`}>
                    {video.title}
                  </h3>
                  
                  {/* Tags */}
                  <div className="flex gap-1 sm:gap-2 flex-wrap mb-2 sm:mb-3 text-xs">
                    <span className={`text-xs px-2 py-1 rounded ${isDark ? 'bg-green-900 text-green-200' : 'bg-green-100 text-green-800'}`}>
                      {video.kingdom}
                    </span>
                    <span className={`text-xs px-2 py-1 rounded ${isDark ? 'bg-blue-900 text-blue-200' : 'bg-blue-100 text-blue-800'}`}>
                      {video.species}
                    </span>
                  </div>

                  {/* Description Preview */}
                  <p className={`text-xs sm:text-sm line-clamp-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                    {video.description || 'No description available'}
                  </p>
                </div>
              </a>
            ))}
          </div>
        )}
      </div>

      {/* Suggest Video Modal */}
      {showSuggestModal && (
        <SuggestVideoModal
          isDark={isDark}
          onClose={() => setShowSuggestModal(false)}
          onSuccess={() => {
            setShowSuggestModal(false);
            fetchVideos();
          }}
          apiUrl={API}
        />
      )}
    </div>
  );
};

// Google Login Button Wrapper Component - Large, Responsive Design
const GoogleLoginButtonWrapper = ({ onSuccess, isDark }) => {
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef(null);

  const handleError = () => {
    console.error('Google login button error');
    alert('❌ Google authentication failed. Make sure:\n1. Google is enabled in your browser\n2. You have an active internet connection\n3. Your Google account is valid');
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <>
      {/* Mobile: Google Icon Button */}
      <div className="sm:hidden relative" ref={dropdownRef}>
        <button
          onClick={() => setShowDropdown(!showDropdown)}
          className={`${isDark ? 'bg-green-700 hover:bg-green-600 text-green-100' : 'bg-white hover:bg-gray-100 text-green-700'} px-3 py-1.5 rounded-lg font-semibold text-xs transition-all duration-200 flex items-center gap-1 shadow-md hover:shadow-lg`}
          title="Sign in with Google"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
          </svg>
        </button>
        
        {showDropdown && (
          <div className={`absolute top-12 right-0 ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border rounded-lg shadow-lg p-4 z-50 w-80`}>
            <GoogleOAuthProvider clientId="834932134878-mu46t9129ovalq4pcqofre2mgbu37aj1.apps.googleusercontent.com">
              <GoogleLogin 
                onSuccess={(response) => {
                  setShowDropdown(false);
                  onSuccess(response);
                }}
                onError={handleError}
                size="large"
                theme={isDark ? "filled_dark" : "outline"}
                locale="en"
              />
            </GoogleOAuthProvider>
          </div>
        )}
      </div>

      {/* Desktop: Full Google Login Button */}
      <div className="hidden sm:block">
        <GoogleOAuthProvider clientId="834932134878-mu46t9129ovalq4pcqofre2mgbu37aj1.apps.googleusercontent.com">
          <div className="google-signin-button-desktop">
            <style>{`
              .google-signin-button-desktop {
                display: flex !important;
                justify-content: center;
                align-items: center;
              }
              
              .google-signin-button-desktop > div {
                width: auto !important;
                height: auto !important;
              }
              
              .google-signin-button-desktop button {
                padding: 8px 14px !important;
                font-size: 12px !important;
                border-radius: 8px !important;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
                transition: all 0.3s ease !important;
                height: auto !important;
                min-height: 36px !important;
              }
              
              .google-signin-button-desktop button:hover {
                box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
                transform: translateY(-2px);
              }
              
              .google-signin-button-desktop svg {
                width: 15px !important;
                height: 15px !important;
              }
              
              .google-signin-button-desktop span {
                font-size: 12px !important;
              }
            `}</style>
            <GoogleLogin 
              onSuccess={onSuccess}
              onError={handleError}
              size="large"
              theme={isDark ? "filled_dark" : "outline"}
              locale="en"
              text="signin_with"
            />
          </div>
        </GoogleOAuthProvider>
      </div>
    </>
  );
};

// Suggest Video Modal Component
const SuggestVideoModal = ({ isDark, onClose, onSuccess, apiUrl }) => {
  const [formData, setFormData] = useState({
    user_name: '',
    user_class: '',
    video_title: '',
    video_description: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const educationalLevels = [
    '11th', '12th', 'B.Sc 1st Year', 'B.Sc 2nd Year', 'B.Sc 3rd Year', 'B.Sc 4th Year',
    'BCS', 'BCA', 'B.Voc', 'M.Sc', 'PhD', 'Teacher', 'Professional', 'Other'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.user_name.trim() || !formData.user_class || !formData.video_title.trim()) {
      setError('Please fill in all required fields');
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${apiUrl}/biotube/suggest-video`, formData);
      setSuccess(true);
      setTimeout(() => {
        onSuccess();
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error submitting suggestion');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className={`${isDark ? 'bg-gray-900' : 'bg-white'} rounded-xl p-6 w-full max-w-md shadow-2xl`}>
        <div className="flex justify-between items-center mb-4">
          <h2 className={`text-2xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
            💡 Suggest a Video
          </h2>
          <button
            onClick={onClose}
            className={`text-2xl ${isDark ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-black'}`}
          >
            ✕
          </button>
        </div>

        {success ? (
          <div className={`p-4 rounded-lg text-center ${isDark ? 'bg-green-900 text-green-100' : 'bg-green-100 text-green-900'}`}>
            <p className="font-semibold mb-2">✅ Thank you!</p>
            <p>Your suggestion has been submitted successfully.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className={`p-3 rounded ${isDark ? 'bg-red-900 text-red-100' : 'bg-red-100 text-red-900'}`}>
                {error}
              </div>
            )}

            <div>
              <label className={`block text-sm font-semibold mb-1 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                Your Name *
              </label>
              <input
                type="text"
                value={formData.user_name}
                onChange={(e) => setFormData({...formData, user_name: e.target.value})}
                className={`w-full px-3 py-2 rounded border ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-white border-gray-300'}`}
                placeholder="Enter your name"
              />
            </div>

            <div>
              <label className={`block text-sm font-semibold mb-1 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                Class / Standard *
              </label>
              <select
                value={formData.user_class}
                onChange={(e) => setFormData({...formData, user_class: e.target.value})}
                className={`w-full px-3 py-2 rounded border ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-white border-gray-300'}`}
              >
                <option value="">Select your class</option>
                {educationalLevels.map(level => (
                  <option key={level} value={level}>{level}</option>
                ))}
              </select>
            </div>

            <div>
              <label className={`block text-sm font-semibold mb-1 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                Video Title *
              </label>
              <input
                type="text"
                value={formData.video_title}
                onChange={(e) => setFormData({...formData, video_title: e.target.value})}
                className={`w-full px-3 py-2 rounded border ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-white border-gray-300'}`}
                placeholder="e.g., Lion Hunting Behavior"
              />
            </div>

            <div>
              <label className={`block text-sm font-semibold mb-1 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                Description (Optional)
              </label>
              <textarea
                value={formData.video_description}
                onChange={(e) => setFormData({...formData, video_description: e.target.value})}
                className={`w-full px-3 py-2 rounded border ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-white border-gray-300'}`}
                placeholder="Brief description or YouTube link"
                rows="3"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-500 text-white font-semibold rounded-lg transition-all"
            >
              {loading ? 'Submitting...' : '✅ Submit Suggestion'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default BiotubeHomepage;
