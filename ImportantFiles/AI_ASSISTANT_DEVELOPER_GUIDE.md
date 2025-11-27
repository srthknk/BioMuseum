# 🔧 AI Assistant - Developer Extension Guide

## Architecture Overview

The AI Assistant is built as a modular, extensible system designed to support multiple data sources and AI backends.

### Current Architecture

```
┌─────────────────────────────────────────┐
│         AIAssistant.jsx (UI)            │
│  ┌─────────────────────────────────┐    │
│  │ - Modal interface               │    │
│  │ - Input/output handling         │    │
│  │ - Image gallery                 │    │
│  │ - Data preview & selection      │    │
│  └─────────────────────────────────┘    │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  aiService.js       │
        │  - generateOrganismData()
        │  - fetchOrganismImages()
        │  - fetchWikipediaInfo()
        └──────────┬──────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
[DATABASE]   [WIKIPEDIA]   [UNSPLASH API]
(Built-in)   (Optional)    (Optional)
```

## Current Implementation

### 1. Local Database (Working ✅)

**File**: `src/services/aiService.js`

```javascript
const ORGANISM_DATABASE = {
  lion: {
    name: 'Lion',
    scientific_name: 'Panthera leo',
    // ... complete data
  }
};
```

**Advantages**:
- ✅ Works offline
- ✅ Instant response
- ✅ No API keys needed
- ✅ No rate limits

**Limitations**:
- ❌ Limited to 5 organisms
- ❌ Manual updates required
- ❌ No real-time data

### 2. Wikipedia Integration (Ready 🔄)

**Currently**: Function exists but not actively used

```javascript
export const fetchWikipediaInfo = async (animalName) => {
  const response = await axios.get(
    `https://en.wikipedia.org/api/rest_v1/page/summary/${animalName}`,
    { timeout: 5000 }
  );
  return response.data;
};
```

**To Enable**:
1. Uncomment in `generateOrganismData()`
2. Parse Wikipedia extract for descriptions
3. Merge with database data

### 3. Unsplash Images (Ready 🔄)

**Currently**: Configured but needs API key

```javascript
const UNSPLASH_KEY = 'YOUR_UNSPLASH_KEY'; // Replace with real key
```

**To Enable**:
1. Get key from: https://unsplash.com/developers
2. Add to `aiService.js`
3. Uncomment API call in `fetchOrganismImages()`

## Extension Guide

### Adding Real AI Backend

Choose one of these approaches:

#### Option 1: OpenAI GPT-4 (Recommended)

**Setup**:
1. Get API key: https://platform.openai.com/api-keys
2. Add to environment: `.env.local`
   ```
   REACT_APP_OPENAI_KEY=sk-...
   ```

**Implementation** (`aiService.js`):

```javascript
import axios from 'axios';

const OPENAI_KEY = process.env.REACT_APP_OPENAI_KEY;

export const generateOrganismDataWithGPT = async (animalName) => {
  try {
    const prompt = `
      Provide detailed scientific information about the ${animalName} in JSON format:
      {
        "name": "Common name",
        "scientific_name": "Genus species",
        "kingdom": "...",
        "phylum": "...",
        "class": "...",
        "order": "...",
        "family": "...",
        "genus": "...",
        "species": "...",
        "morphology": "Physical description...",
        "physiology": "Biological functions...",
        "description": "General information..."
      }
      
      Ensure all information is scientifically accurate.
    `;

    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-4',
        messages: [
          { role: 'system', content: 'You are a zoology expert.' },
          { role: 'user', content: prompt }
        ],
        temperature: 0.7,
        max_tokens: 1000
      },
      {
        headers: {
          'Authorization': `Bearer ${OPENAI_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 30000
      }
    );

    // Parse the response
    const content = response.data.choices[0].message.content;
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    
    if (jsonMatch) {
      const data = JSON.parse(jsonMatch[0]);
      return { success: true, data, source: 'gpt-4' };
    }
    
    return { success: false, error: 'Failed to parse response' };
  } catch (error) {
    console.error('GPT-4 Error:', error);
    return { success: false, error: error.message };
  }
};
```

**Usage** (Update `generateOrganismData`):

```javascript
export const generateOrganismData = async (animalName) => {
  try {
    // First try local database (fast)
    const lowerName = animalName.toLowerCase().trim();
    if (ORGANISM_DATABASE[lowerName]) {
      return {
        success: true,
        data: ORGANISM_DATABASE[lowerName],
        source: 'database'
      };
    }

    // Then try GPT-4 (comprehensive)
    if (OPENAI_KEY) {
      return await generateOrganismDataWithGPT(animalName);
    }

    // Fallback to template
    return createTemplateData(animalName);
  } catch (error) {
    return createTemplateData(animalName);
  }
};
```

**Costs**:
- $0.03 per 1K input tokens
- $0.06 per 1K output tokens
- Typical request: ~$0.01-0.05

---

#### Option 2: Google Gemini API (Alternative)

**Setup**:
1. Get API key: https://makersuite.google.com/app/apikey
2. Add to `.env.local`
   ```
   REACT_APP_GEMINI_KEY=AIza...
   ```

**Implementation**:

```javascript
export const generateOrganismDataWithGemini = async (animalName) => {
  const GEMINI_KEY = process.env.REACT_APP_GEMINI_KEY;
  
  try {
    const prompt = `
      Provide detailed scientific information about the ${animalName}.
      Return as JSON with these fields:
      name, scientific_name, kingdom, phylum, class, order, family, 
      genus, species, morphology, physiology, description
    `;

    const response = await axios.post(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${GEMINI_KEY}`,
      {
        contents: [{
          parts: [{ text: prompt }]
        }]
      },
      { timeout: 30000 }
    );

    const content = response.data.candidates[0].content.parts[0].text;
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    
    if (jsonMatch) {
      const data = JSON.parse(jsonMatch[0]);
      return { success: true, data, source: 'gemini-pro' };
    }
    
    return { success: false, error: 'Failed to parse response' };
  } catch (error) {
    console.error('Gemini Error:', error);
    return { success: false, error: error.message };
  }
};
```

**Advantages**:
- Free tier: 60 requests/minute
- No credit card required
- Very fast responses

---

#### Option 3: HuggingFace Inference API (Budget-friendly)

```javascript
export const generateOrganismDataWithHuggingFace = async (animalName) => {
  const HF_KEY = process.env.REACT_APP_HF_KEY;
  
  try {
    const response = await axios.post(
      'https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat',
      {
        inputs: `Generate scientific info about ${animalName} as JSON...`
      },
      {
        headers: { Authorization: `Bearer ${HF_KEY}` },
        timeout: 30000
      }
    );

    const text = response.data[0].generated_text;
    // Parse JSON from response...
    return { success: true, data: parsedData };
  } catch (error) {
    console.error('HuggingFace Error:', error);
    return { success: false, error: error.message };
  }
};
```

---

### Adding Image Enhancement

#### Upgrade from Unsplash to Multiple Sources

```javascript
export const fetchOrganismImagesEnhanced = async (animalName) => {
  try {
    // Try multiple image sources in parallel
    const [unsplashResult, pixabayResult, pexelsResult] = await Promise.all([
      fetchFromUnsplash(animalName),
      fetchFromPixabay(animalName),
      fetchFromPexels(animalName)
    ]);

    // Combine and deduplicate results
    const allImages = [
      ...unsplashResult.images,
      ...pixabayResult.images,
      ...pexelsResult.images
    ].filter((img, idx, arr) => 
      arr.findIndex(i => i.url === img.url) === idx
    );

    return {
      success: true,
      images: allImages.slice(0, 10) // Top 10 images
    };
  } catch (error) {
    console.error('Image fetch error:', error);
    return { success: false, images: [] };
  }
};

// Individual source implementations
const fetchFromPixabay = async (query) => {
  const response = await axios.get(
    `https://pixabay.com/api/?q=${query}&key=${process.env.REACT_APP_PIXABAY_KEY}`
  );
  return {
    images: response.data.hits.map(hit => ({
      url: hit.largeImageURL,
      alt: `${query} image`,
      attribution: hit.user
    }))
  };
};

const fetchFromPexels = async (query) => {
  const response = await axios.get(
    `https://api.pexels.com/v1/search?query=${query}&per_page=5`,
    { headers: { Authorization: process.env.REACT_APP_PEXELS_KEY } }
  );
  return {
    images: response.data.photos.map(photo => ({
      url: photo.src.large,
      alt: photo.alt,
      attribution: photo.photographer
    }))
  };
};
```

### Adding Taxonomy Database Integration

**Using NCBI Taxonomy API** (Free, no key needed):

```javascript
export const fetchNCBITaxonomy = async (animalName) => {
  try {
    // Step 1: Search for organism
    const searchResponse = await axios.get(
      `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&term=${animalName}&rettype=json&retmax=1`
    );

    const uid = searchResponse.data.esearchresult.idlist[0];
    if (!uid) return { success: false };

    // Step 2: Fetch taxonomy details
    const detailResponse = await axios.get(
      `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id=${uid}&rettype=json`
    );

    const taxData = detailResponse.data.result[uid];
    
    return {
      success: true,
      taxonomy: {
        kingdom: taxData.kingdom,
        phylum: taxData.phylum,
        class: taxData.class,
        order: taxData.order,
        family: taxData.family,
        genus: taxData.genus,
        species: taxData.species
      }
    };
  } catch (error) {
    console.error('NCBI Error:', error);
    return { success: false };
  }
};
```

## Implementation Checklist

### Phase 1: Enable Existing Features (1 hour)
- [ ] Configure Unsplash API key
- [ ] Test image fetching
- [ ] Enable Wikipedia integration
- [ ] Test with multiple organisms

### Phase 2: Add GPT-4 (2-3 hours)
- [ ] Get OpenAI API key
- [ ] Add environment variables
- [ ] Implement `generateOrganismDataWithGPT()`
- [ ] Update main function with fallback logic
- [ ] Test with 10+ organisms
- [ ] Monitor API costs

### Phase 3: Multi-Source Images (2 hours)
- [ ] Get API keys from Pixabay and Pexels
- [ ] Implement `fetchOrganismImagesEnhanced()`
- [ ] Add deduplication logic
- [ ] Test image variety
- [ ] Update UI to show image source

### Phase 4: NCBI Taxonomy (1 hour)
- [ ] Implement `fetchNCBITaxonomy()`
- [ ] Integrate into data generation
- [ ] Test accuracy
- [ ] Add offline fallback

## Error Handling Best Practices

```javascript
// Implement cascading fallbacks
export const generateOrganismDataRobust = async (animalName) => {
  try {
    // Level 1: Local database (fastest)
    const dbResult = queryLocalDatabase(animalName);
    if (dbResult) return { ...dbResult, source: 'database', priority: 1 };
  } catch (e1) {
    console.warn('Database error:', e1);
  }

  try {
    // Level 2: Real AI API (comprehensive)
    const aiResult = await callAIAPI(animalName);
    if (aiResult.success) return { ...aiResult, priority: 2 };
  } catch (e2) {
    console.warn('AI API error:', e2);
  }

  try {
    // Level 3: Wikipedia (supplementary)
    const wikiResult = await fetchWikipediaInfo(animalName);
    if (wikiResult.success) return { ...wikiResult, priority: 3 };
  } catch (e3) {
    console.warn('Wikipedia error:', e3);
  }

  // Level 4: Template (always works)
  return { ...createTemplateData(animalName), priority: 4 };
};
```

## Performance Optimization

### Caching Strategy

```javascript
// Add caching layer
const cache = new Map();
const CACHE_TTL = 24 * 60 * 60 * 1000; // 24 hours

export const generateOrganismDataCached = async (animalName) => {
  const cacheKey = animalName.toLowerCase();
  const cached = cache.get(cacheKey);

  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }

  const result = await generateOrganismData(animalName);
  cache.set(cacheKey, { data: result, timestamp: Date.now() });
  return result;
};

// Or use localStorage for persistence
export const getCachedOrganismData = (animalName) => {
  const cached = localStorage.getItem(`organism_${animalName}`);
  if (cached) {
    const data = JSON.parse(cached);
    if (Date.now() - data.timestamp < CACHE_TTL) {
      return data.value;
    }
  }
  return null;
};
```

## Monitoring & Analytics

```javascript
// Track API usage and performance
export const logAIRequest = (animalName, source, duration, success) => {
  const log = {
    timestamp: new Date().toISOString(),
    organism: animalName,
    source,
    duration,
    success,
    userId: getCurrentUserId()
  };

  // Send to analytics
  axios.post('/api/analytics/ai-requests', log).catch(e => {
    console.warn('Analytics error:', e);
  });
};

// Monitor costs
export const trackAPICosts = (source, tokens) => {
  const costs = {
    'gpt-4': 0.00006, // per token
    'gemini': 0,      // free tier
    'huggingface': 0.00005,
    'unsplash': 0     // free
  };
  
  const cost = tokens * costs[source];
  console.log(`API Cost: $${cost.toFixed(4)} (${source})`);
};
```

## Testing Strategy

```javascript
// Unit tests for AI service
describe('AIService', () => {
  test('generateOrganismData returns valid structure', async () => {
    const result = await generateOrganismData('Lion');
    expect(result.data).toHaveProperty('name');
    expect(result.data).toHaveProperty('scientific_name');
    expect(result.success).toBe(true);
  });

  test('Unknown organism returns template', async () => {
    const result = await generateOrganismData('Xylozerptus');
    expect(result.data.name).toContain('Xylozerptus');
    expect(result.source).toBe('template');
  });

  test('API error falls back to database', async () => {
    // Mock API failure
    jest.spyOn(axios, 'get').mockRejectedValue(new Error('API Error'));
    const result = await generateOrganismData('Lion');
    expect(result.success).toBe(true);
  });
});
```

## Deployment Considerations

### Environment Variables Required

```
# .env.local or .env.production
REACT_APP_OPENAI_KEY=sk-...
REACT_APP_GEMINI_KEY=AIza...
REACT_APP_UNSPLASH_KEY=...
REACT_APP_PIXABAY_KEY=...
REACT_APP_PEXELS_KEY=...
REACT_APP_HF_KEY=hf_...
```

### Rate Limiting

```javascript
// Implement rate limiting to control costs
class RateLimiter {
  constructor(maxRequests = 100, timeWindow = 60000) {
    this.maxRequests = maxRequests;
    this.timeWindow = timeWindow;
    this.requests = [];
  }

  async allowRequest() {
    const now = Date.now();
    this.requests = this.requests.filter(t => t > now - this.timeWindow);
    
    if (this.requests.length < this.maxRequests) {
      this.requests.push(now);
      return true;
    }
    return false;
  }
}

const limiter = new RateLimiter(10, 60000); // 10 requests per minute
```

---

**Last Updated**: 2024  
**Status**: 📝 Extension Guide  
**Difficulty**: Intermediate - Advanced
