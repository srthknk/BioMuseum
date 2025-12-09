import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const API = `${BACKEND_URL}/api`;

const Leaderboard = ({ isDark }) => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [userStats, setUserStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('points');

  useEffect(() => {
    fetchLeaderboard();
  }, [filter]);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/leaderboard?sort_by=${filter}`);
      setLeaderboard(response.data);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const getBadgeEmoji = (badge_id) => {
    const badges = {
      'first_submission': '🌱',
      '10_submissions': '⭐',
      '25_submissions': '🌟',
      '50_submissions': '👑',
      'verified_master': '✅',
      '100_points': '💎',
      '500_points': '🧠'
    };
    return badges[badge_id] || '🏅';
  };

  const getLevelColor = (level) => {
    const colors = {
      1: 'bg-gray-400',
      2: 'bg-blue-400',
      3: 'bg-purple-400',
      4: 'bg-pink-400',
      5: 'bg-red-400',
      6: 'bg-yellow-400'
    };
    return colors[level] || 'bg-gray-400';
  };

  return (
    <div className={`min-h-screen ${isDark ? 'bg-gray-900' : 'bg-gray-50'} p-4 sm:p-6`}>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className={`text-3xl sm:text-4xl font-bold ${isDark ? 'text-white' : 'text-gray-900'} mb-2`}>
            🏆 Leaderboard
          </h1>
          <p className={isDark ? 'text-gray-400' : 'text-gray-600'}>
            Top contributors to BioMuseum
          </p>
        </div>

        {/* Filter Buttons */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {[
            { id: 'points', label: '⭐ Points' },
            { id: 'submissions', label: '📝 Submissions' },
            { id: 'verified', label: '✅ Verified' }
          ].map(btn => (
            <button
              key={btn.id}
              onClick={() => setFilter(btn.id)}
              className={`px-4 py-2 rounded-lg font-semibold whitespace-nowrap transition ${
                filter === btn.id
                  ? 'bg-purple-600 text-white'
                  : isDark
                  ? 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
              }`}
            >
              {btn.label}
            </button>
          ))}
        </div>

        {/* Leaderboard Table */}
        {loading ? (
          <div className={`text-center py-12 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Loading leaderboard...
          </div>
        ) : (
          <div className={`rounded-lg overflow-hidden shadow-lg ${isDark ? 'bg-gray-800' : 'bg-white'}`}>
            {leaderboard.map((user, index) => (
              <div
                key={index}
                className={`p-4 border-b ${
                  isDark ? 'border-gray-700 hover:bg-gray-700' : 'border-gray-200 hover:bg-gray-50'
                } transition flex items-center justify-between`}
              >
                <div className="flex items-center gap-4 flex-1">
                  {/* Rank */}
                  <div className={`font-bold text-lg w-8 ${
                    index < 3 ? 'text-yellow-400' : isDark ? 'text-gray-400' : 'text-gray-600'
                  }`}>
                    {index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : index + 1}
                  </div>

                  {/* User Info */}
                  <div className="flex-1">
                    <div className={`font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                      {user.user_name}
                    </div>
                    <div className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                      Level {user.level}
                    </div>
                  </div>

                  {/* Level Badge */}
                  <div className={`${getLevelColor(user.level)} text-white px-3 py-1 rounded-full font-bold`}>
                    LVL {user.level}
                  </div>

                  {/* Stats */}
                  <div className="text-right">
                    <div className={`text-lg font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                      {filter === 'points' && `${user.points} pts`}
                      {filter === 'submissions' && `${user.total_submissions} subs`}
                      {filter === 'verified' && `${user.verified_submissions} verified`}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Badges Section */}
        <div className={`mt-8 rounded-lg p-6 ${isDark ? 'bg-gray-800' : 'bg-white'} shadow-lg`}>
          <h2 className={`text-2xl font-bold mb-4 ${isDark ? 'text-white' : 'text-gray-900'}`}>
            🎖️ Available Badges
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            {[
              { emoji: '🌱', name: 'First Step', desc: '1 suggestion' },
              { emoji: '⭐', name: 'Active', desc: '10 suggestions' },
              { emoji: '🌟', name: 'Super', desc: '25 suggestions' },
              { emoji: '👑', name: 'Legend', desc: '50 suggestions' },
              { emoji: '✅', name: 'Verified', desc: '10 verified' },
              { emoji: '💎', name: 'Collector', desc: '100 points' },
              { emoji: '🧠', name: 'Master Mind', desc: '500 points' }
            ].map((badge, idx) => (
              <div
                key={idx}
                className={`p-4 rounded-lg text-center ${
                  isDark ? 'bg-gray-700' : 'bg-gray-100'
                }`}
              >
                <div className="text-4xl mb-2">{badge.emoji}</div>
                <div className={`font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  {badge.name}
                </div>
                <div className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                  {badge.desc}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
