# Unsplash Image Generation Setup

## Overview
The image generation system has been updated to use **Unsplash API** instead of Gemini. This provides:
- ✅ Direct access to real, high-quality images
- ✅ No Gemini keyword generation overhead
- ✅ Simple, reliable image retrieval
- ✅ Professional, curated images

## Setup Steps

### Step 1: Get Unsplash API Access Key

1. Go to [Unsplash Developers](https://unsplash.com/developers)
2. Click **"Your Apps"** (or create an account if you don't have one)
3. Click **"New Application"**
4. Agree to the Unsplash API terms
5. Fill in the application details (name, description, website)
6. Click **Create Application**
7. Copy your **Access Key** from the application dashboard

### Step 2: Add API Key to Backend

Edit `backend/.env` and replace the placeholder:

```env
# BEFORE:
UNSPLASH_ACCESS_KEY=your_unsplash_api_key_here

# AFTER:
UNSPLASH_ACCESS_KEY=your_actual_key_from_step_1
```

Example:
```env
UNSPLASH_ACCESS_KEY=abcdef1234567890ghijklmnopqrst
```

### Step 3: Restart Backend Server

```powershell
# Kill existing Python process
taskkill /F /IM python.exe

# Start backend with new key
cd c:\BioMuseum\backend
c:\BioMuseum\.venv\Scripts\python.exe -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

## How It Works

### Image Generation Flow

**When clicking "AI Images" button:**
1. Frontend sends organism name to `/admin/organisms/ai-generate-images`
2. Backend queries Unsplash API with organism name
3. Returns 5 high-quality image URLs
4. Frontend displays images in form

**When approving a suggestion:**
1. Backend generates organism data (name, morphology, etc.)
2. Searches Unsplash for images using organism name
3. Falls back to scientific name or common name if needed
4. Returns image URLs with complete data
5. Frontend auto-fills form with all data + images

### Fallback Logic

If Unsplash has no images for an organism:
1. Try searching with organism common name
2. Try searching with scientific name
3. Return empty list (user can retry with different search term)

## Testing

### Test 1: AI Images Button
```
1. Go to Admin > Add Organism
2. Type organism name (e.g., "Blue Jay")
3. Click "AI Images" button
4. Expected: 5 real Unsplash images load
```

### Test 2: Suggestion Approval
```
1. Go to Admin > Suggestions
2. Click "Approve" on any suggestion
3. Expected: Form fills with all data + real images from Unsplash
```

### Test 3: Backend Logs
Check for success messages:
```
INFO: Generated 5 images from Unsplash for term 'Blue Jay'
```

Or error if images not found:
```
WARNING: No images found on Unsplash for organism 'XYZ123'
```

## API Rate Limits

Unsplash API limits:
- **Free tier**: 50 requests per hour per API key
- **Production**: Consider upgrading for higher limits

If you hit rate limits, you'll see:
```
WARNING: Unsplash API error: 429
```

## Configuration

The system is now configured as:

```
Frontend (App.js)
    ↓
POST /admin/organisms/ai-generate-images
    ↓
get_images_from_unsplash()
    ↓
Unsplash API
    ↓
Returns: [{url}, {url}, {url}, {url}, {url}]
    ↓
Frontend displays images
```

## Troubleshooting

### Images Still Showing "Not Available"
- **Check:** Is UNSPLASH_ACCESS_KEY set in `.env`?
- **Check:** Did you restart backend after adding key?
- **Check:** Backend logs for error messages
- **Solution:** Restart backend and try again

### Getting 429 Rate Limit Errors
- **Cause:** Exceeded 50 requests/hour limit
- **Solution:** Wait an hour or upgrade Unsplash API plan

### Only Getting Images for Some Organisms
- **Normal:** Unsplash may not have images for very obscure organisms
- **Solution:** User can try with more common organism names

## Reverting to Gemini (if needed)

If you want to use Gemini for keyword generation again:
1. Set `USE_GEMINI_KEYWORDS=true` in `.env`
2. Restart backend
3. System will use Gemini to improve search terms before Unsplash

Note: This requires both GEMINI_API_KEY and UNSPLASH_ACCESS_KEY to be set.

## File Changes

Modified files:
- `backend/server.py` - Added `get_images_from_unsplash()` function
- `backend/server.py` - Updated `/admin/organisms/ai-generate-images` endpoint
- `backend/server.py` - Updated approval endpoint for suggestions
- `frontend/src/App.js` - Added auth header to image generation request
- `backend/.env` - Added UNSPLASH_ACCESS_KEY placeholder

## Next Steps

1. ✅ Get Unsplash API key (Step 1 above)
2. ✅ Add to `.env` file (Step 2 above)
3. ✅ Restart backend (Step 3 above)
4. ✅ Test image generation (use Test 1-3 above)

You're all set! Images should now load beautifully from Unsplash. 🎉
