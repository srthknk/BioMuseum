#!/usr/bin/env python3
"""
Update App.js to:
1. Remove Cloudinary loading animation and replace with "Loading..." text
2. Add AI image generation feature in AddOrganismForm
"""

import re

# Read the file
with open(r'd:\BioMuseum\frontend\src\App.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================
# REPLACEMENT 1: Homepage loading screen
# ============================================
old_homepage_loading = '''  if (loading) {
    return (
      <div className={`min-h-screen ${isDark ? 'bg-gray-900' : 'bg-gradient-to-br from-green-50 to-blue-50'} flex items-center justify-center loading-container`}>
        <div className="text-center">
          <div className="mb-6 flex justify-center">
            <img 
              src="https://res.cloudinary.com/dhmgyv2ps/image/upload/v1764427279/346_xhjb6z.gif" 
              alt="Loading" 
              className="w-32 h-32 sm:w-40 sm:h-40 md:w-48 md:h-48 object-contain"
            />
          </div>
          <div className="mb-4">
            <h2 className={`text-2xl font-bold mb-2 ${isDark ? 'text-white' : 'text-gray-800'}`}>BioMuseum</h2>
            <p className={isDark ? 'text-gray-400' : 'text-gray-600'}>Discovering the wonders of life...</p>
          </div>
          <p className={`text-sm mt-6 ${isDark ? 'text-gray-500' : 'text-gray-500'}`}>Loading organisms...</p>
        </div>
      </div>
    );
  }'''

new_homepage_loading = '''  if (loading) {
    return (
      <div className={`min-h-screen ${isDark ? 'bg-gray-900' : 'bg-gradient-to-br from-green-50 to-blue-50'} flex items-center justify-center loading-container`}>
        <div className="text-center">
          <div className="mb-6">
            <h2 className={`text-3xl sm:text-4xl font-bold font-poppins ${isDark ? 'text-white' : 'text-gray-800'}`}>Loading</h2>
            <div className="flex justify-center mt-4">
              <div className="flex space-x-2">
                <div className={`w-2 h-2 rounded-full animate-bounce ${isDark ? 'bg-purple-400' : 'bg-purple-600'}`} style={{animationDelay: '0s'}}></div>
                <div className={`w-2 h-2 rounded-full animate-bounce ${isDark ? 'bg-purple-400' : 'bg-purple-600'}`} style={{animationDelay: '0.2s'}}></div>
                <div className={`w-2 h-2 rounded-full animate-bounce ${isDark ? 'bg-purple-400' : 'bg-purple-600'}`} style={{animationDelay: '0.4s'}}></div>
              </div>
            </div>
          </div>
          <div className="mb-4">
            <p className={`text-base sm:text-lg font-semibold ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>Discovering the wonders of life...</p>
          </div>
        </div>
      </div>
    );
  }'''

content = content.replace(old_homepage_loading, new_homepage_loading)

# ============================================
# REPLACEMENT 2: OrganismDetail loading screen
# ============================================
old_organism_detail_loading = '''  if (loading) {
    return (
      <div className={`min-h-screen ${isDark ? 'bg-gray-900' : 'bg-white'} flex items-center justify-center`}>
        <div className="text-center">
          <img 
            src="https://res.cloudinary.com/dhmgyv2ps/image/upload/v1764427279/346_xhjb6z.gif" 
            alt="Loading" 
            className="w-32 h-32 sm:w-40 sm:h-40 object-contain mx-auto mb-4"
          />
          <p className={`text-lg font-semibold ${isDark ? 'text-gray-300' : 'text-gray-800'}`}>Loading organism details...</p>
        </div>
      </div>
    );
  }'''

new_organism_detail_loading = '''  if (loading) {
    return (
      <div className={`min-h-screen ${isDark ? 'bg-gray-900' : 'bg-white'} flex items-center justify-center`}>
        <div className="text-center">
          <h2 className={`text-3xl sm:text-4xl font-bold font-poppins mb-6 ${isDark ? 'text-white' : 'text-gray-800'}`}>Loading</h2>
          <div className="flex justify-center mb-4">
            <div className="flex space-x-2">
              <div className={`w-3 h-3 rounded-full animate-bounce ${isDark ? 'bg-purple-400' : 'bg-purple-600'}`} style={{animationDelay: '0s'}}></div>
              <div className={`w-3 h-3 rounded-full animate-bounce ${isDark ? 'bg-purple-400' : 'bg-purple-600'}`} style={{animationDelay: '0.2s'}}></div>
              <div className={`w-3 h-3 rounded-full animate-bounce ${isDark ? 'bg-purple-400' : 'bg-purple-600'}`} style={{animationDelay: '0.4s'}}></div>
            </div>
          </div>
          <p className={`text-lg font-semibold ${isDark ? 'text-gray-300' : 'text-gray-800'}`}>Loading organism details...</p>
        </div>
      </div>
    );
  }'''

content = content.replace(old_organism_detail_loading, new_organism_detail_loading)

# ============================================
# REPLACEMENT 3: OrganismsPage loading screen
# ============================================
old_organisms_page_loading = '''      return (
        <div className={`min-h-screen ${isDark ? 'bg-gray-900' : 'bg-white'} flex items-center justify-center`}>
          <div className="text-center">
            <img 
              src="https://res.cloudinary.com/dhmgyv2ps/image/upload/v1764427279/346_xhjb6z.gif" 
              alt="Loading" 
              className="w-32 h-32 sm:w-40 sm:h-40 object-contain mx-auto mb-4"
            />
            <p className={`text-lg font-semibold ${isDark ? 'text-gray-300' : 'text-gray-800'}`}>Loading organisms...</p>
          </div>
        </div>
      );'''

new_organisms_page_loading = '''      return (
        <div className={`min-h-screen ${isDark ? 'bg-gray-900' : 'bg-white'} flex items-center justify-center`}>
          <div className="text-center">
            <h2 className={`text-3xl sm:text-4xl font-bold font-poppins mb-6 ${isDark ? 'text-white' : 'text-gray-800'}`}>Loading</h2>
            <div className="flex justify-center mb-4">
              <div className="flex space-x-2">
                <div className={`w-3 h-3 rounded-full animate-bounce ${isDark ? 'bg-purple-400' : 'bg-purple-600'}`} style={{animationDelay: '0s'}}></div>
                <div className={`w-3 h-3 rounded-full animate-bounce ${isDark ? 'bg-purple-400' : 'bg-purple-600'}`} style={{animationDelay: '0.2s'}}></div>
                <div className={`w-3 h-3 rounded-full animate-bounce ${isDark ? 'bg-purple-400' : 'bg-purple-600'}`} style={{animationDelay: '0.4s'}}></div>
              </div>
            </div>
            <p className={`text-lg font-semibold ${isDark ? 'text-gray-300' : 'text-gray-800'}`}>Loading organisms...</p>
          </div>
        </div>
      );'''

content = content.replace(old_organisms_page_loading, new_organisms_page_loading)

# ============================================
# REPLACEMENT 4: Add AI image generation state
# ============================================
old_state = '''  const [formData, setFormData] = useState({
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
  const [showAiHelper, setShowAiHelper] = useState(false);'''

new_state = '''  const [formData, setFormData] = useState({
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
  const [aiImageLoading, setAiImageLoading] = useState(false);
  const [aiImageOrganism, setAiImageOrganism] = useState('');'''

content = content.replace(old_state, new_state)

# ============================================
# REPLACEMENT 5: Add AI image generation function
# ============================================
old_ai_complete = '''  const handleAiComplete = async () => {
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
  };'''

new_ai_complete = '''  const handleAiComplete = async () => {
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

  const handleAiGenerateImages = async () => {
    if (!aiImageOrganism.trim()) {
      alert('Please enter an organism name for image generation');
      return;
    }

    setAiImageLoading(true);
    try {
      // Generate 3-4 images for the organism
      const response = await axios.post(`${API}/admin/organisms/ai-generate-images`, {
        organism_name: aiImageOrganism,
        count: 4
      }, {
        timeout: 120000 // 2 minute timeout for image generation
      });

      if (response.data.success && response.data.images && response.data.images.length > 0) {
        const newImages = response.data.images;
        setFormData(prev => ({
          ...prev,
          images: [...prev.images, ...newImages]
        }));
        setAiImageOrganism('');
        alert(`✅ ${newImages.length} HD images generated successfully!`);
      } else {
        alert('No images were generated. Please try again.');
      }
    } catch (error) {
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to generate images';
      alert('Error generating images: ' + errorMsg);
    } finally {
      setAiImageLoading(false);
    }
  };'''

content = content.replace(old_ai_complete, new_ai_complete)

# ============================================
# REPLACEMENT 6: Add AI image generation button in form
# ============================================
old_image_section = '''        {/* Image Upload */}
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
          </div>'''

new_image_section = '''        {/* Image Upload */}
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
            <div className={`flex flex-col sm:flex-row gap-2 items-center`}>
              <div className={`flex-1 text-center text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>or</div>
              <div className={`flex-1 flex gap-2`}>
                <input
                  type="text"
                  value={aiImageOrganism}
                  onChange={(e) => setAiImageOrganism(e.target.value)}
                  placeholder="Enter organism name for AI images..."
                  className={`flex-1 px-3 sm:px-4 py-2 rounded-lg focus:outline-none transition-all text-xs sm:text-sm ${isDark ? 'bg-gray-600 border border-gray-500 text-white' : 'border border-gray-300'}`}
                />
                <button
                  type="button"
                  onClick={handleAiGenerateImages}
                  disabled={aiImageLoading}
                  className={`w-full sm:w-auto px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all text-white ${
                    aiImageLoading 
                      ? 'bg-gray-400 cursor-not-allowed' 
                      : 'bg-blue-600 hover:bg-blue-700'
                  }`}
                >
                  {aiImageLoading ? '🔄 Generating...' : '🤖 AI Images'}
                </button>
              </div>
            </div>
          </div>'''

content = content.replace(old_image_section, new_image_section)

# Write the updated content
with open(r'd:\BioMuseum\frontend\src\App.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All updates completed successfully!")
print("Changes made:")
print("1. ✅ Replaced all Cloudinary loading animations with 'Loading...' text")
print("2. ✅ Added AI image generation feature to AddOrganismForm")
print("3. ✅ Added responsive bouncing dots animation for loading")
print("4. ✅ Images can now be generated with 'organism name' + AI button")
