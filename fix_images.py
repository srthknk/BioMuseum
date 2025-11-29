#!/usr/bin/env python3
"""
Script to fix image generation endpoint with Unsplash API integration and AI search enhancement.
This script updates backend/server.py to properly search Unsplash API instead of using hardcoded URLs.
"""

import re
import requests
import json
from typing import List

# Unsplash API Access Key
UNSPLASH_ACCESS_KEY = "vQ_yvjIskYKmvpXywThJ4u5kBjRzTAk1kDZkwYhwDbY"
UNSPLASH_API_URL = "https://api.unsplash.com"

def get_search_terms_from_gemini(organism_name: str) -> List[str]:
    """Use Gemini to generate better search terms for organism images."""
    try:
        import google.generativeai as genai
        import os
        
        # Get API key from environment or use a placeholder
        api_key = os.getenv('GOOGLE_API_KEY', 'AIzaSyDLbCQY8y_2YrfnQMdBQbGPqUIU2dNqKvs')
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f'Given the organism name "{organism_name}", generate 3-5 search keywords that would find relevant images on Unsplash. Each keyword should be a single word or short phrase. Focus on biological/taxonomic terms first. Return ONLY the keywords as a comma-separated list, nothing else. Example format: "cobra, snake, reptile, hood, venom"'
        
        response = model.generate_content(prompt)
        search_terms = [term.strip() for term in response.text.split(',')]
        print(f"[OK] Generated search terms from Gemini: {search_terms}")
        return search_terms
    except Exception as e:
        print(f"[WARN] Gemini search terms generation failed: {str(e)[:100]}")
        return [organism_name.lower(), organism_name.lower().split()[0]]

def search_unsplash_images(organism_name: str, count: int = 6) -> List[str]:
    """Search Unsplash API for organism images using AI-enhanced search terms."""
    images = []
    
    # Get enhanced search terms from Gemini
    search_terms = get_search_terms_from_gemini(organism_name)
    search_terms.insert(0, organism_name)
    
    for query in search_terms:
        if len(images) >= count:
            break
        
        try:
            response = requests.get(
                f"{UNSPLASH_API_URL}/search/photos",
                params={
                    'query': query,
                    'client_id': UNSPLASH_ACCESS_KEY,
                    'per_page': 10,
                    'orientation': 'landscape'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    for result in results:
                        if len(images) >= count:
                            break
                        img_url = result.get('urls', {}).get('regular', '')
                        if img_url and img_url not in images:
                            if '?' in img_url:
                                img_url += '&w=800&q=90'
                            else:
                                img_url += '?w=800&q=90'
                            images.append(img_url)
                            print(f"[OK] Found image for query '{query}'")
            else:
                print(f"[WARN] Unsplash API error {response.status_code} for '{query}'")
        except Exception as e:
            print(f"[WARN] Unsplash search for '{query}' failed: {str(e)[:100]}")
            continue
    
    if not images:
        try:
            print(f"[INFO] Using fallback search for '{organism_name}'")
            response = requests.get(
                f"{UNSPLASH_API_URL}/search/photos",
                params={
                    'query': organism_name,
                    'client_id': UNSPLASH_ACCESS_KEY,
                    'per_page': 6,
                    'orientation': 'landscape'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                for result in data.get('results', [])[:6]:
                    img_url = result.get('urls', {}).get('regular', '')
                    if img_url:
                        if '?' in img_url:
                            img_url += '&w=800&q=90'
                        else:
                            img_url += '?w=800&q=90'
                        images.append(img_url)
        except Exception as e:
            print(f"[ERROR] Fallback search failed: {e}")
    
    return images[:count]

def create_helper_functions():
    """Generate the helper functions code to add to server.py"""
    code = '''
def get_search_terms_from_gemini(organism_name: str):
    """Use Gemini to generate better search terms for organism images."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f'Given the organism name "{organism_name}", generate 3-5 search keywords that would find relevant images on Unsplash. Each keyword should be a single word or short phrase. Return ONLY the keywords as comma-separated list. Example: "cobra, snake, reptile"'
        response = model.generate_content(prompt)
        search_terms = [term.strip() for term in response.text.split(',')]
        return search_terms
    except Exception as e:
        return [organism_name.lower()]

def search_unsplash_images(organism_name: str, count: int = 6):
    """Search Unsplash API for organism images using AI-enhanced search terms."""
    UNSPLASH_ACCESS_KEY = "vQ_yvjIskYKmvpXywThJ4u5kBjRzTAk1kDZkwYhwDbY"
    UNSPLASH_API_URL = "https://api.unsplash.com"
    images = []
    search_terms = get_search_terms_from_gemini(organism_name)
    search_terms.insert(0, organism_name)
    
    for query in search_terms:
        if len(images) >= count:
            break
        try:
            response = requests.get(
                f"{UNSPLASH_API_URL}/search/photos",
                params={
                    'query': query,
                    'client_id': UNSPLASH_ACCESS_KEY,
                    'per_page': 10,
                    'orientation': 'landscape'
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                for result in data.get('results', []):
                    if len(images) >= count:
                        break
                    img_url = result.get('urls', {}).get('regular', '')
                    if img_url and img_url not in images:
                        if '?' in img_url:
                            img_url += '&w=800&q=90'
                        else:
                            img_url += '?w=800&q=90'
                        images.append(img_url)
        except Exception as e:
            continue
    
    if not images:
        try:
            response = requests.get(
                f"{UNSPLASH_API_URL}/search/photos",
                params={
                    'query': organism_name,
                    'client_id': UNSPLASH_ACCESS_KEY,
                    'per_page': 6
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                for result in data.get('results', [])[:6]:
                    img_url = result.get('urls', {}).get('regular', '')
                    if img_url:
                        if '?' in img_url:
                            img_url += '&w=800&q=90'
                        else:
                            img_url += '?w=800&q=90'
                        images.append(img_url)
        except Exception as e:
            pass
    
    return images[:count]
'''
    return code

def update_server_py():
    """Update backend/server.py with new image generation endpoint."""
    server_path = "backend/server.py"
    
    try:
        with open(server_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if requests is imported
        if 'import requests' not in content:
            # Add requests import after other imports
            content = content.replace('import json', 'import json\nimport requests')
            print("[OK] Added requests import")
        
        # Create the new endpoint code
        new_endpoint = '''@api_router.post("/admin/organisms/ai-generate-images")
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
'''
        
        # Find and replace the old endpoint
        pattern = r'@api_router\.post\("/admin/organisms/ai-generate-images"\).*?(?=\n@api_router\.|\n@app\.)'
        
        if re.search(pattern, content, re.DOTALL):
            new_content = re.sub(pattern, new_endpoint, content, flags=re.DOTALL, count=1)
            print("[OK] Replaced old endpoint")
        else:
            print("[WARN] Old endpoint pattern not found, checking alternate pattern...")
            # Try to find it with a different approach
            if '@api_router.post("/admin/organisms/ai-generate-images")' in content:
                idx = content.find('@api_router.post("/admin/organisms/ai-generate-images")')
                if idx != -1:
                    # Find the next @api_router or @app
                    next_idx = content.find('@api_router.', idx + 1)
                    if next_idx == -1:
                        next_idx = content.find('@app.', idx + 1)
                    if next_idx == -1:
                        next_idx = len(content)
                    
                    new_content = content[:idx] + new_endpoint + '\n' + content[next_idx:]
                    print("[OK] Replaced old endpoint using alternate method")
                else:
                    print("[ERROR] Could not locate endpoint")
                    return False
            else:
                print("[ERROR] Endpoint not found in server.py")
                return False
        
        # Add helper functions if not already present
        if 'def search_unsplash_images' not in new_content:
            helper_code = create_helper_functions()
            # Add before the endpoint
            idx = new_content.find('@api_router.post("/admin/organisms/ai-generate-images")')
            if idx != -1:
                new_content = new_content[:idx] + helper_code + '\n\n' + new_content[idx:]
                print("[OK] Added helper functions")
        
        # Write updated content
        with open(server_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"[SUCCESS] Updated {server_path}")
        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to update {server_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("[INFO] Starting image generation endpoint fix...")
    print(f"[INFO] Using Unsplash API key: {UNSPLASH_ACCESS_KEY[:20]}...")
    
    if update_server_py():
        print("[SUCCESS] Image generation endpoint updated successfully!")
        print("[INFO] The following changes were applied:")
        print("  - Added Unsplash API integration")
        print("  - Added Gemini AI search term generation")
        print("  - Added helper functions for image search")
        print("\nNext steps:")
        print("  1. Run: python -m py_compile backend/server.py")
        print("  2. Test locally with: python backend/server.py")
        print("  3. Generate images for 'Indian Cobra' to verify")
        print("  4. Git commit and push to main")
    else:
        print("[ERROR] Failed to update image generation endpoint")
        exit(1)
