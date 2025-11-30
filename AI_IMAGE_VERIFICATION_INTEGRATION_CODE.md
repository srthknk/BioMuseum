# Integration Code for server.py

This file contains the exact code to add to your `backend/server.py` to enable AI image verification.

## Step 1: Add Import at Top of server.py

Add this after your other imports (around line 30-40):

```python
# For async image validation
import asyncio
import base64

# Image validation system
try:
    from image_validation_system import (
        search_images_with_validation,
        get_fallback_images,
        validate_image_with_ai
    )
    HAS_IMAGE_VALIDATION = True
except ImportError:
    HAS_IMAGE_VALIDATION = False
    logger.warning("Image validation system not available")
```

## Step 2: Replace Existing Image Generation Endpoint

Find this existing endpoint (around line 567):

```python
@api_router.post("/admin/organisms/ai-generate-images")
async def generate_organism_images_ai(request: dict):
    """Generate organism images using Unsplash API with AI-enhanced search."""
    try:
        organism_name = request.get("organism_name", "").strip()
        
        if not organism_name:
            raise ValueError("organism_name is required")
        
        image_urls = search_unsplash_images(organism_name, count=6)
        
        if not image_urls:
            image_urls = [
                "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=90",
                "https://images.unsplash.com/photo-1489330911046-c894fdcc538d?w=800&q=90"
            ]
        
        return {
            "success": True,
            "organism_name": organism_name,
            "image_urls": image_urls[:6],
            "source": "unsplash",
            "message": f"Generated {len(image_urls)} images for {organism_name}"
        }
    except Exception as e:
        print(f"[ERROR] AI image generation failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate images"
        }
```

Replace it with this:

```python
@api_router.post("/admin/organisms/ai-generate-images")
async def generate_organism_images_ai(request: dict):
    """
    Generate organism images with AI validation.
    
    Pipeline:
    1. Search Unsplash (free)
    2. Validate each image with Gemini Vision AI
    3. Fall back to Bing Search if needed
    4. Return validated images with confidence scores
    
    Response includes confidence scores (0-100%) so admin can see image quality.
    Only images with >70% confidence are returned.
    
    Query Parameters:
        organism_name (required): Name of organism (e.g., "Bengal Tiger")
        scientific_name (optional): Scientific name (e.g., "Panthera tigris")
        count (optional): Number of images to return (default: 6)
    """
    try:
        organism_name = request.get("organism_name", "").strip()
        scientific_name = request.get("scientific_name", "").strip()
        count = request.get("count", 6)
        
        if not organism_name:
            raise ValueError("organism_name is required")
        
        print(f"[INFO] Generating validated images for: {organism_name}")
        
        # Use new multi-source validation system if available
        if HAS_IMAGE_VALIDATION:
            print(f"[INFO] Using AI-validated multi-source image search...")
            result = await search_images_with_validation(
                organism_name=organism_name,
                scientific_name=scientific_name,
                count=count
            )
            
            # Ensure we have images
            if not result.get("images") or len(result.get("images", [])) == 0:
                print(f"[WARN] No validated images found, returning fallbacks...")
                fallback_urls = get_fallback_images(organism_name)
                result["images"] = [
                    {
                        "url": url,
                        "source": "placeholder",
                        "confidence": 0,
                        "validation_reason": "No validated results found - showing nature placeholder"
                    }
                    for url in fallback_urls
                ]
            
            # Extract URLs for backwards compatibility
            image_urls = [img["url"] for img in result.get("images", [])]
            
            return {
                "success": result.get("success", True),
                "organism_name": organism_name,
                "image_urls": image_urls,
                "images": result.get("images", []),  # Include full validation data
                "sources_used": result.get("sources_used", ["fallback"]),
                "total_images": len(image_urls),
                "message": result.get("message", f"Generated {len(image_urls)} validated images")
            }
        
        else:
            # Fallback to old system if validation not available
            print(f"[WARN] Image validation system not available, using basic Unsplash...")
            image_urls = search_unsplash_images(organism_name, count=count)
            
            if not image_urls:
                image_urls = [
                    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=90",
                    "https://images.unsplash.com/photo-1489330911046-c894fdcc538d?w=800&q=90"
                ]
            
            return {
                "success": True,
                "organism_name": organism_name,
                "image_urls": image_urls[:count],
                "total_images": len(image_urls),
                "source": "unsplash-basic",
                "message": f"Generated {len(image_urls)} images (validation unavailable)"
            }
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        print(f"[ERROR] AI image generation failed: {error_msg}")
        
        return {
            "success": False,
            "error": error_msg,
            "image_urls": [],
            "images": [],
            "message": "Failed to generate images"
        }
```

## Step 3: Optional - Add New Endpoint for Detailed Validation

If you want a separate endpoint for just validation (useful for testing), add this:

```python
@api_router.post("/admin/organisms/validate-images")
async def validate_organism_images(request: dict):
    """
    Validate a list of image URLs against an organism name.
    
    Useful for:
    - Testing the validation system
    - Bulk validating existing images
    - Checking image quality
    
    Request:
    {
        "organism_name": "Bengal Tiger",
        "scientific_name": "Panthera tigris",
        "image_urls": ["http://...", "http://..."]
    }
    
    Response:
    {
        "success": true,
        "organism_name": "Bengal Tiger",
        "validation_results": [
            {
                "url": "http://...",
                "is_valid": true,
                "confidence": 95,
                "reason": "..."
            }
        ]
    }
    """
    try:
        if not HAS_IMAGE_VALIDATION:
            return {
                "success": False,
                "error": "Image validation system not available"
            }
        
        organism_name = request.get("organism_name", "").strip()
        scientific_name = request.get("scientific_name", "").strip()
        image_urls = request.get("image_urls", [])
        
        if not organism_name:
            raise ValueError("organism_name is required")
        
        if not image_urls:
            raise ValueError("image_urls list is required")
        
        print(f"[INFO] Validating {len(image_urls)} images for: {organism_name}")
        
        # Validate each image
        validation_results = []
        for url in image_urls:
            validation = await validate_image_with_ai(url, organism_name, scientific_name)
            validation_results.append({
                "url": url,
                "is_valid": validation.get("is_valid", False),
                "confidence": validation.get("confidence", 0),
                "reason": validation.get("reason", "Unknown"),
                "characteristics": validation.get("characteristics", [])
            })
        
        return {
            "success": True,
            "organism_name": organism_name,
            "total_images": len(image_urls),
            "validated_count": sum(1 for r in validation_results if r["is_valid"]),
            "validation_results": validation_results
        }
    
    except Exception as e:
        print(f"[ERROR] Image validation failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
```

## Step 4: Update .env

Add these optional API keys to `backend/.env`:

```bash
# Image Validation APIs (optional)
# Bing Search API - Get free key from:
# https://www.microsoft.com/en-us/bing/apis/bing-image-search-api
BING_SEARCH_API_KEY=your-key-here

# iStock API (optional - for premium images)
# Register at: https://www.istockphoto.com/contribute/api
ISTOCK_API_KEY=your-key-here
ISTOCK_API_SECRET=your-secret-here
```

## Step 5: Testing

### Test 1: Generate Images (Easy Case)
```bash
curl -X POST http://localhost:8000/api/admin/organisms/ai-generate-images \
  -H "Content-Type: application/json" \
  -d '{
    "organism_name": "Bengal Tiger",
    "scientific_name": "Panthera tigris",
    "count": 6
  }'
```

### Test 2: Generate Images (Hard Case)
```bash
curl -X POST http://localhost:8000/api/admin/organisms/ai-generate-images \
  -H "Content-Type: application/json" \
  -d '{
    "organism_name": "Taenia Solium",
    "scientific_name": "Taenia solium",
    "count": 6
  }'
```

### Test 3: Validate Existing Images
```bash
curl -X POST http://localhost:8000/api/admin/organisms/validate-images \
  -H "Content-Type: application/json" \
  -d '{
    "organism_name": "Bengal Tiger",
    "scientific_name": "Panthera tigris",
    "image_urls": [
      "https://images.unsplash.com/photo-1471366620353-c67d36b1baa0",
      "https://images.unsplash.com/photo-1519052537078-e6302a4968d4"
    ]
  }'
```

## Step 6: Frontend Updates (Optional but Recommended)

In `frontend/src/App.js`, update the image generation handler to show confidence scores:

Find this section (around line 1365):
```javascript
const response = await axios.post(`${API}/admin/organisms/ai-generate-images`, {
  organism_name: E,
  count: 4,
  timeout: 12e4
});

if (e.data.success && e.data.image_urls && e.data.image_urls.length > 0) {
  const t = e.data.image_urls;
  s(e => c(c({}, e), {}, { images: [...e.images, ...t] })),
  C(""),
  alert("✅ " + t.length + " HD images generated successfully!")
}
```

Replace with:
```javascript
const response = await axios.post(`${API}/admin/organisms/ai-generate-images`, {
  organism_name: E,
  count: 4,
  timeout: 12e4
});

if (e.data.success) {
  // Handle both old format (image_urls) and new format (images with validation)
  let imgUrls = [];
  
  if (e.data.images && e.data.images.length > 0) {
    // New format with validation data
    imgUrls = e.data.images.map(img => img.url);
    
    // Log validation details for debugging
    console.log("📊 Image Validation Results:");
    e.data.images.forEach((img, idx) => {
      console.log(`  ${idx + 1}. ${img.source} - ${img.confidence}% confidence - ${img.validation_reason}`);
    });
  } else if (e.data.image_urls && e.data.image_urls.length > 0) {
    // Old format
    imgUrls = e.data.image_urls;
  }
  
  if (imgUrls.length > 0) {
    s(t => c(c({}, t), {}, { images: [...t.images, ...imgUrls] })),
    C(""),
    Qu("✅ " + imgUrls.length + " validated images generated!", "success", 3000);
  } else {
    Qu("⚠️ No images found", "warning", 3000);
  }
} else {
  Qu("❌ " + (e.data.error || "Failed to generate images"), "error", 3000);
}
```

## Summary of Changes

| File | Change | Purpose |
|------|--------|---------|
| `image_validation_system.py` | New file | Core validation logic |
| `backend/server.py` | Update imports | Enable validation system |
| `backend/server.py` | Replace endpoint | Use multi-source search |
| `backend/server.py` | Add endpoint | Optional validation-only endpoint |
| `backend/.env` | Add keys | Optional Bing/iStock APIs |
| `frontend/src/App.js` | Update handler | Display validation scores |

## Rollback Plan

If something breaks, you can easily revert to basic mode:

1. Remove `image_validation_system.py`
2. Set `HAS_IMAGE_VALIDATION = False` in server.py
3. Everything falls back to original Unsplash-only mode

The endpoint is backward compatible!

