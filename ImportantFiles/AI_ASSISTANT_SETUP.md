# AI Assistant Setup Guide 🤖

This guide explains how to set up the AI assistant to auto-fill organism data with just a name input.

## Overview

The AI Assistant allows admins to add organisms by simply typing the animal name. The system will automatically generate:
- ✅ Common Name
- ✅ Scientific Name
- ✅ Classification (Kingdom, Phylum, Class, Order, Family, Genus, Species)
- ✅ Morphology (Physical description)
- ✅ Physiology (Biological functions & behavior)
- ✅ Description (Habitat, conservation status)
- ✅ Images (Automatically fetched with preview)

**No manual data entry required!** Just select an image and click "Use This Data".

---

## Quick Start (5 minutes)

### Step 1: Get a Gemini API Key (Free)

1. Go to: https://makersuite.google.com/app/apikeys
2. Click **"Get API Key"** button
3. Click **"Create API Key"**
4. Choose **"Create API key in new project"**
5. Copy the generated API key
6. Paste it in `frontend/.env.local`:
   ```
   REACT_APP_GEMINI_API_KEY=paste_your_key_here
   ```

### Step 2: Get a Pexels API Key (Free, Optional but Recommended)

1. Go to: https://www.pexels.com/api/
2. Click **"Register"** and sign up for free
3. Go to your **Dashboard** → **API**
4. Copy your API key
5. Paste it in `frontend/.env.local`:
   ```
   REACT_APP_PEXELS_API_KEY=paste_your_key_here
   ```

### Step 3: Restart Frontend

```bash
cd frontend
npm start
```

Done! 🎉 The AI Assistant is now active.

---

## How to Use

1. **Open Admin Panel** → **Add Organisms Tab**
2. **Click the "AI Assistant" button** (🤖 icon)
3. **Type an animal name** (e.g., "Rattle Snake", "Blue Whale", "Koala")
4. **Click "Generate"** button
5. **Wait for AI** to fetch data and images (~2-3 seconds)
6. **Review the data** (all fields auto-populated)
7. **Select an image** from the gallery
8. **Click "Use This Data"** → Form auto-fills
9. **Done!** Just upload your own image or click Save

---

## API Providers Explained

### Google Gemini API (Primary)

**Cost**: FREE  
**Rate Limit**: 60 requests/minute  
**What it does**: Generates biological data using AI

**Pros**:
- ✅ Free tier is generous
- ✅ Generates complete, accurate data
- ✅ Understands scientific names
- ✅ Returns properly formatted JSON

**Cons**:
- ⚠️ Requires key setup
- ⚠️ Rate limited to 60/minute

**Setup**: https://makersuite.google.com/app/apikeys

---

### Pexels API (Image Fetching)

**Cost**: FREE  
**Rate Limit**: 200 requests/hour  
**What it does**: Fetches high-quality animal images

**Pros**:
- ✅ Free unlimited images
- ✅ High quality photos
- ✅ No watermarks
- ✅ Great for wildlife photography

**Cons**:
- ⚠️ May not have very obscure animals

**Setup**: https://www.pexels.com/api/

---

### Fallback APIs (Automatic)

If primary APIs fail, the system automatically tries:

1. **Local Database** - 5 pre-loaded animals (Lion, Tiger, Elephant, etc.)
2. **Wikipedia API** - Free encyclopedia data (no key needed)
3. **Template** - Empty form with placeholders

So even without API keys, you can still use basic functionality!

---

## Troubleshooting

### "API Error" or "Failed to generate data"

**Solution 1**: Check if `.env.local` exists
```
frontend/.env.local
```
Should contain your API keys.

**Solution 2**: Verify API key is correct
- Copy the key again from the provider
- Make sure there are no extra spaces
- Restart `npm start`

**Solution 3**: Check API limits
- Gemini: 60 requests/minute
- Pexels: 200 requests/hour
- Wait a moment and try again

### "No images found" 

**Cause**: Pexels API key not set or rate limited

**Solution**: 
1. Add `REACT_APP_PEXELS_API_KEY` to `.env.local`
2. Or use Unsplash API instead (set `REACT_APP_UNSPLASH_KEY`)
3. Or manually upload images

### "Template showing instead of real data"

**Cause**: Animal name not recognized (might not be in Wikipedia)

**Solution**:
- Try exact name (e.g., "Rattlesnake" not "Rattle Snake")
- Try scientific name (e.g., "Panthera leo")
- Try common name with location (e.g., "African Elephant")
- If still blank, manually fill the form

### "Keys not working in production"

**Solution**: Environment variables must be set in your hosting platform

**For Vercel** (Frontend):
1. Go to Project Settings
2. Navigate to **Environment Variables**
3. Add: `REACT_APP_GEMINI_API_KEY` = your key
4. Add: `REACT_APP_PEXELS_API_KEY` = your key
5. Redeploy

**For Render** (Backend - if needed):
1. Go to Service Settings
2. Navigate to **Environment**
3. Add the keys
4. Deploy

---

## Advanced Configuration

### Change AI Provider

The system uses Gemini by default but supports multiple models.

**Using Claude instead** (Premium):

Edit `frontend/src/services/aiService.js`:

```javascript
// Change this line:
const CLAUDE_API_KEY = process.env.REACT_APP_CLAUDE_API_KEY;

// And add Claude logic in generateOrganismData()
```

### Batch Operations

Want to add 50 animals at once?

```bash
# Run batch script (if available)
node backend/batch_add_organisms.js
```

Or use CSV import (from Admin Panel).

### Caching Results

To avoid repeated API calls for same animal:

```javascript
// In aiService.js, add:
const cache = {};

export const generateOrganismData = async (animalName) => {
  if (cache[animalName]) {
    return cache[animalName];
  }
  // ... rest of function
  cache[animalName] = result;
  return result;
}
```

---

## Performance Tips

1. **Use Pexels over Unsplash** - Better rate limits
2. **Cache searches** - Don't request same animal twice in 1 hour
3. **Batch requests during off-hours** - Spread API calls
4. **Monitor API usage**:
   - Gemini: Check console logs for rate warnings
   - Pexels: Monitor via their dashboard

---

## Security Notes

⚠️ **IMPORTANT**: Never commit `.env.local` with real API keys to Git!

**What to do**:

1. Add to `.gitignore`:
   ```
   frontend/.env.local
   frontend/.env*.local
   ```

2. In production, use platform-specific environment variables (Vercel, Render, etc.)

3. Rotate keys periodically if exposed

4. Use separate keys for development and production

---

## Testing

### Test with these animals:

| Animal | Expected Result |
|--------|-----------------|
| Lion | ✅ Database entry (instant) |
| Tiger | ✅ Database entry (instant) |
| Rattlesnake | ✅ AI generated |
| Koala | ✅ AI generated |
| Axolotl | ✅ Wikipedia fallback |
| Pokemon | ⚠️ Template (not real animal) |

### Test API Status

In browser console:

```javascript
// Test Gemini
fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_KEY')
  .then(r => console.log('Gemini:', r.status))

// Test Pexels
fetch('https://api.pexels.com/v1/search?query=lion', {
  headers: { Authorization: 'YOUR_PEXELS_KEY' }
}).then(r => console.log('Pexels:', r.status))
```

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "YOUR_GEMINI_API_KEY" in form | Key not set in env | Check `.env.local` |
| Blank data returned | Animal name typo | Try exact spelling |
| 429 Error | Rate limited | Wait 1 minute, retry |
| CORS error | API blocking requests | Use backend proxy (advanced) |
| Old data showing | Browser cache | Hard refresh (Ctrl+Shift+R) |

---

## Additional Resources

- [Gemini API Docs](https://ai.google.dev/)
- [Pexels API Docs](https://www.pexels.com/api/documentation/)
- [Wikipedia API Docs](https://www.mediawiki.org/wiki/API:Main_page)
- [Environment Variables in React](https://create-react-app.dev/docs/adding-custom-environment-variables/)

---

## Support

If AI Assistant isn't working:

1. Check browser console for errors (F12 → Console tab)
2. Verify API keys in `.env.local`
3. Test API directly (see Testing section)
4. Check API provider's status page
5. Restart `npm start` after adding keys

---

**Last Updated**: 2025-01-27  
**Version**: 1.0  
**Status**: ✅ Production Ready
