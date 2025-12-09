import React, { useState, useEffect } from 'react';

const LanguageSelector = ({ isDark, onLanguageChange }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [isOpen, setIsOpen] = useState(false);

  const languages = {
    en: { name: 'English', flag: '🇺🇸' },
    es: { name: 'Español', flag: '🇪🇸' },
    fr: { name: 'Français', flag: '🇫🇷' },
    de: { name: 'Deutsch', flag: '🇩🇪' },
    hi: { name: 'हिन्दी', flag: '🇮🇳' },
    pt: { name: 'Português', flag: '🇵🇹' },
    ja: { name: '日本語', flag: '🇯🇵' },
    zh: { name: '中文', flag: '🇨🇳' }
  };

  useEffect(() => {
    const saved = localStorage.getItem('user_language') || 'en';
    setCurrentLanguage(saved);
  }, []);

  const handleLanguageChange = (lang) => {
    setCurrentLanguage(lang);
    localStorage.setItem('user_language', lang);
    onLanguageChange(lang);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      {/* Language Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`px-4 py-2 rounded-lg font-semibold flex items-center gap-2 transition ${
          isDark
            ? 'bg-gray-800 hover:bg-gray-700 text-white'
            : 'bg-gray-200 hover:bg-gray-300 text-gray-900'
        }`}
      >
        <span className="text-lg">{languages[currentLanguage].flag}</span>
        <span className="hidden sm:inline">{languages[currentLanguage].name}</span>
        <span className="text-xs">▼</span>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div
          className={`absolute right-0 mt-2 rounded-lg shadow-lg z-50 min-w-48 ${
            isDark ? 'bg-gray-800 border border-gray-700' : 'bg-white border border-gray-200'
          }`}
        >
          {Object.entries(languages).map(([code, { name, flag }]) => (
            <button
              key={code}
              onClick={() => handleLanguageChange(code)}
              className={`w-full text-left px-4 py-3 flex items-center gap-3 transition ${
                code === currentLanguage
                  ? isDark
                    ? 'bg-purple-600 text-white'
                    : 'bg-purple-100 text-purple-900'
                  : isDark
                  ? 'hover:bg-gray-700 text-white'
                  : 'hover:bg-gray-100 text-gray-900'
              }`}
            >
              <span className="text-lg">{flag}</span>
              <span className="font-semibold">{name}</span>
              {code === currentLanguage && <span className="ml-auto">✓</span>}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default LanguageSelector;
