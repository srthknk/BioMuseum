# AI-Verified Multi-Source Image Generation System

## Overview
Implement intelligent image verification using AI vision to validate that returned images actually match the organism. Falls back through multiple sources: Unsplash → iStock → Bing/Google Images.

## Architecture

### Pipeline Flow
```
User requests images for organism
    ↓
[1] UNSPLASH: Try free API first (cost-free)
    ↓
[2] AI VISION VALIDATION: Analyze each image
    - Check if image matches organism
    - Calculate confidence score (0-100%)
    - If confidence > 75% → ACCEPT ✅
    - If confidence < 75% → REJECT and continue
    ↓
[3] iSTOCK API: If Unsplash fails (premium API)
    - More curated, professional images
    - Higher accuracy expected
    - Validate again with AI
    ↓
[4] BING/GOOGLE: Fallback to web search
    - Uses Bing Search API (free tier available)
    - Returns Google Images results
    - Final validation with AI
    ↓
[5] RETURN: Best validated images or placeholder
```

## Required APIs & Keys

### 1. Vision API (Image Validation)
**Options:**
- **Claude Vision** (Recommended) - $0.30 per image
  - High accuracy for biological identification
  - Already have Anthropic API setup
  
- **Google Vision API** - $1.50 per 1000 requests
  - Alternative if needed
  - Lower cost at scale

### 2. iStock API
**Setup:**
- Visit: https://www.istockphoto.com/contribute/api
- Register as developer (free)
- Get API credentials
- Pricing: ~$2-5 per image depending on license

### 3. Bing Search API (Free Alternative)
**Setup:**
- Azure Cognitive Services
- Free tier: 1,000 requests/month
- Paid: $7 per 1,000 requests after free tier

## Implementation Steps

### Phase 1: AI Vision Validation Function
```python
async def validate_image_with_ai(image_url: str, organism_name: str) -> dict:
    """
    Validate if image matches organism using AI vision
    Returns: {
        "is_valid": bool,
        "confidence": 0-100,
        "reason": "description of validation"
    }
    """
    # Download image from URL
    # Send to Claude Vision or Google Vision API
    # Get response analyzing if it's the organism
    # Return confidence score
```

### Phase 2: Multi-Source Image Search
```python
async def search_images_with_validation(organism_name: str, count: int = 6):
    """
    Multi-stage image search with AI validation:
    1. Try Unsplash
    2. Validate with AI
    3. Fall back to iStock if needed
    4. Fall back to Bing if needed
    """
```

### Phase 3: Enhanced Endpoint
```python
POST /api/admin/organisms/ai-generate-images-verified
{
    "organism_name": "Taenia Solium",
    "count": 6
}

Response:
{
    "success": true,
    "images": [
        {
            "url": "...",
            "source": "unsplash/istock/bing",
            "confidence": 92,
            "validation_reason": "Clear image of Taenia Solium under microscope"
        }
    ]
}
```

## Code Implementation

### Step 1: Add to requirements.txt
```
anthropic>=0.7.0
```

### Step 2: Environment Variables (.env)
```
ANTHROPIC_API_KEY=your-key-here
ISTOCK_API_KEY=your-key-here
ISTOCK_API_SECRET=your-secret-here
BING_SEARCH_API_KEY=your-key-here
```

## Cost Analysis

### Scenario: Adding 100 organisms with 6 images each

**Current (Unsplash only):**
- Cost: $0
- Accuracy: ~40-50% (many irrelevant images)

**Proposed (Multi-source with AI validation):**
- Unsplash images: $0 (free API)
- AI validation: 100 organisms × 6 images × $0.30 (Claude) = $180
- **OR** use Google Vision: 100 × 6 × $0.0015 = $0.90
- Fallback APIs (needed ~20% of time):
  - iStock: 20 images × $3 = $60 (worst case)
  - Bing: $0 (free tier)
  
**Total estimated**: $0-60 for 100 organisms (vs. $0 but with poor quality)

## Optimization Tips

1. **Cache validation results** - Store confidence scores in DB
2. **Batch API calls** - Group images for validation
3. **Use free tier first** - Google Vision or Bing free tiers
4. **Progressive loading** - Show best images first while validating others
5. **User override** - Let admins manually approve/reject images

## Implementation Priority

### MVP (Week 1)
- [ ] Add Claude Vision validation function
- [ ] Update Unsplash search to validate results
- [ ] Return confidence scores in response
- [ ] Update frontend to show validation status

### Phase 2 (Week 2)
- [ ] Add iStock API integration
- [ ] Implement fallback logic
- [ ] Cache validation results

### Phase 3 (Week 3)
- [ ] Add Bing Search integration
- [ ] Advanced caching strategy
- [ ] Performance optimization

## Testing Strategy

1. **Test with edge cases:**
   - Taenia Solium (parasite - hard to find good images)
   - Common animals (easy to find - should validate quickly)
   - Scientific names (test synonym handling)

2. **Measure accuracy:**
   - Track validation scores
   - Compare with manual review
   - Iterate on prompts

3. **Load test:**
   - Test with 50+ organisms
   - Monitor API costs
   - Check fallback performance

## Frontend Updates Required

1. Show confidence scores for each image
2. Display source (Unsplash/iStock/Bing)
3. Allow manual validation before saving
4. Show loading state during validation
5. Display validation reason in tooltip

## Success Criteria

✅ Taenia Solium shows actual parasite images (not forests/beaches)
✅ Common organisms load from Unsplash only ($0 cost)
✅ Confidence scores > 80% for validated images
✅ Fallback works within 30 seconds
✅ Admin can see image validation reasons
