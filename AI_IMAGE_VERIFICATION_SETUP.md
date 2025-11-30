# AI Image Verification System - Setup & Integration Guide

## Quick Start (15 minutes)

### Phase 1: Minimal MVP - Unsplash + Gemini Vision (TODAY)

This gives you AI validation **without any new API costs** using your existing Gemini API.

#### Step 1: Update Backend Requirements

Add to `backend/requirements.txt`:
```
google-generativeai>=0.3.0  # (you likely already have this)
requests>=2.31.0
```

#### Step 2: Add Image Validation Module

Copy the complete `image_validation_system.py` to your backend folder.

#### Step 3: Import and Use in server.py

Add this to the top of `server.py`:
```python
from image_validation_system import search_images_with_validation, get_fallback_images
```

#### Step 4: Update the Image Generation Endpoint

Replace the existing `@api_router.post("/admin/organisms/ai-generate-images")` with:

```python
@api_router.post("/admin/organisms/ai-generate-images")
async def generate_organism_images_ai(request: dict):
    """Generate organism images with AI validation - validates each image to ensure it matches the organism."""
    try:
        organism_name = request.get("organism_name", "").strip()
        scientific_name = request.get("scientific_name", "").strip()
        count = request.get("count", 6)
        
        if not organism_name:
            raise ValueError("organism_name is required")
        
        # Use multi-source search with validation
        result = await search_images_with_validation(
            organism_name=organism_name,
            scientific_name=scientific_name,
            count=count
        )
        
        # If no validated images found, return fallback
        if not result.get("images"):
            fallback_urls = get_fallback_images(organism_name)
            result["images"] = [
                {
                    "url": url,
                    "source": "placeholder",
                    "confidence": 0,
                    "validation_reason": "No validated results found - showing placeholder"
                }
                for url in fallback_urls
            ]
        
        return {
            "success": result.get("success", True),
            "organism_name": organism_name,
            "image_urls": [img["url"] for img in result.get("images", [])],
            "images": result.get("images", []),  # Include full validation data
            "source": "multi-source-validated",
            "message": result.get("message", "Generated images with AI validation")
        }
    
    except Exception as e:
        print(f"[ERROR] AI image generation failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate images",
            "image_urls": []
        }
```

#### Step 5: Test It

1. Start backend: `python -m uvicorn server:app --reload`
2. Go to frontend admin panel
3. Try adding organism with "Generate" button
4. You should see:
   - Images loaded from Unsplash
   - Each with confidence score (e.g., "92%")
   - Source shown as "Unsplash"

**Cost**: $0 (Gemini vision is included in your free tier for development)

---

## Phase 2: Add Bing Fallback (Next - FREE)

### Step 1: Get Free Bing Search API Key

1. Go to: https://www.microsoft.com/en-us/bing/apis/bing-image-search-api
2. Click "Get free key"
3. Sign in with Microsoft account (create if needed)
4. Create new resource:
   - Choose region (e.g., "West Europe")
   - Pricing: **Free** (1,000 requests/month)
5. Copy key from "Keys and Endpoint"

### Step 2: Add to .env

```bash
BING_SEARCH_API_KEY=your-key-here
```

### Step 3: That's It!

The system will automatically use Bing if Unsplash doesn't find enough images.

**Cost**: $0 (1,000 free requests/month)

---

## Phase 3: Add iStock Premium (Future - Optional)

Skip this unless you're having trouble finding images.

### Step 1: Get iStock API Key

1. Go to: https://www.istockphoto.com/contribute/api
2. Click "Get started"
3. Register as developer
4. Create app to get API key & secret
5. Note: iStock is premium, images cost $2-5 each typically

### Step 2: Implement iStock Integration

The code is already in `image_validation_system.py` but commented out. To enable:

1. Add to `.env`:
```
ISTOCK_API_KEY=your-key
ISTOCK_API_SECRET=your-secret
```

2. Uncomment and complete the `search_istock_images()` function

3. iStock has detailed API docs at their developer portal

**Cost**: ~$2-5 per image downloaded (budget-dependent)

---

## Testing the System

### Test Case 1: Easy Organism (Should work immediately)

```bash
POST http://localhost:8000/api/admin/organisms/ai-generate-images
{
    "organism_name": "Bengal Tiger",
    "scientific_name": "Panthera tigris",
    "count": 6
}
```

**Expected Response**:
```json
{
    "success": true,
    "images": [
        {
            "url": "https://images.unsplash.com/...",
            "source": "unsplash",
            "confidence": 95,
            "validation_reason": "Clear image of a Bengal tiger with orange coat and black stripes"
        },
        ...
    ],
    "message": "Found 6 validated images from unsplash"
}
```

### Test Case 2: Hard Organism (Will trigger Bing fallback)

```bash
POST http://localhost:8000/api/admin/organisms/ai-generate-images
{
    "organism_name": "Taenia Solium",
    "scientific_name": "Taenia solium",
    "count": 6
}
```

**Expected Response**:
- Unsplash finds images but they're wrong (beaches, forests, etc.)
- AI validation rejects them (confidence < 70%)
- System falls back to Bing
- Returns actual parasite/tapeworm images with high confidence

### Test Case 3: Scientific Name Only

```bash
POST http://localhost:8000/api/admin/organisms/ai-generate-images
{
    "organism_name": "Homo sapiens",
    "scientific_name": "Homo sapiens",
    "count": 4
}
```

---

## Frontend Updates Required

### Update the Image Generation Component

In `frontend/src/App.js`, find the image generation button response handler and update to show confidence scores:

```javascript
// After receiving image response, update to show validation data
if (e.data.success && e.data.images && e.data.images.length > 0) {
  const imgUrls = e.data.images.map(img => img.url);
  s(t => ({
    ...t,
    images: [...t.images, ...imgUrls]
  }));
  
  // Show validation info in tooltip/hover
  const validationInfo = e.data.images.map(img => 
    `Source: ${img.source} | Confidence: ${img.confidence}%`
  );
  
  console.log("Image Validation Results:", validationInfo);
  Qu(`✅ ${imgUrls.length} validated images loaded!`, "success", 3000);
} else {
  Qu("❌ No validated images found", "error", 3000);
}
```

### Show Validation Badge on Images

Add this to image preview display:
```html
<div className="relative">
  <img src={imageUrl} alt="preview" />
  <div className="absolute top-2 right-2 bg-green-600 text-white px-2 py-1 rounded text-xs">
    92% Match
  </div>
</div>
```

---

## API Costs Summary

| Source | Cost | Quality | Speed | Notes |
|--------|------|---------|-------|-------|
| **Unsplash** | FREE | Medium | Fast | 50+ per month |
| **Gemini Vision** | Included | Excellent | Medium | ~0.3s per image |
| **Bing Search** | FREE | Medium | Fast | 1,000/month free |
| **iStock** | $2-5/img | Very High | Slow | Premium option |

**Realistic Cost for Adding 100 Organisms**:
- Using Unsplash + Gemini validation only: **$0**
- Using Bing fallback for 20% of organisms: **$0** (within free tier)
- With iStock for tough cases: **$50-100** (optional)

---

## Troubleshooting

### Issue: "No images found even with Bing"

**Solution**: 
- Check Bing API key is in .env
- Test manually: `curl "https://api.bing.microsoft.com/v7.0/images/search?q=tiger" -H "Ocp-Apim-Subscription-Key: YOUR_KEY"`
- Check you haven't hit monthly quota

### Issue: "All images have low confidence scores"

**Causes**:
1. Gemini is being too strict
2. Search terms are too specific
3. Organism is very rare/specialized

**Fix**:
- Adjust confidence threshold in code (currently 70%, try lowering to 60%)
- Use common name instead of scientific name
- Manually add images through admin panel

### Issue: "Slow image generation (>10 seconds)"

**Causes**:
- Gemini Vision API is processing each image (takes ~0.3-1s per image)
- Network latency
- API rate limiting

**Solutions**:
- Cache validation results (already implemented)
- Reduce count from 6 to 4 images
- Use background job for bulk imports
- Implement async batching

### Issue: "Gemini API quota exceeded"

**Solution**:
- Gemini free tier is very generous (up to 15 req/min)
- For production, upgrade to Gemini Pro API ($0.075 per 1000 input tokens)
- Or use Google Vision API instead (~$1.50 per 1000 requests)

---

## Production Deployment Checklist

- [ ] Bing API key added to Render environment variables
- [ ] Gemini API key already configured
- [ ] Test image generation works on production
- [ ] Monitor API usage in first week
- [ ] Add caching to MongoDB to prevent duplicate validations
- [ ] Set up monitoring/logging for validation accuracy
- [ ] Create admin panel to see validation stats

---

## Next Steps

1. **Today**: Implement Phase 1 (Unsplash + Gemini validation)
2. **Tomorrow**: Add Bing fallback (Phase 2)
3. **This week**: Test with 20+ organisms, measure accuracy
4. **Next week**: Decide if iStock integration needed based on results

---

## Support & Questions

See `IMPLEMENTATION_PLAN_AI_IMAGE_VERIFICATION.md` for detailed architecture.

Key functions:
- `validate_image_with_ai(url, name)` - Validates single image
- `search_images_with_validation(name, count)` - Full pipeline
- `search_bing_images(name, count)` - Bing fallback
