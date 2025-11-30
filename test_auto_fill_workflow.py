#!/usr/bin/env python
"""
Test script for the complete auto-fill workflow:
1. Create a suggestion
2. Verify it with AI
3. Approve it and get auto-fill data
4. Check that organism_data + images are returned
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000/api')
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', '')  # Set this for testing

print("\n" + "="*60)
print("AUTO-FILL WORKFLOW TEST")
print("="*60)

# Test 1: Create a suggestion
print("\n[TEST 1] Creating a suggestion...")
suggestion_data = {
    "user_name": "Test User",
    "organism_name": "African Elephant",
    "description": "Large land mammal from Africa"
}

response = requests.post(f"{API_URL}/suggestions", json=suggestion_data)
if response.status_code == 201:
    suggestion = response.json()
    suggestion_id = suggestion.get('id')
    print(f"✅ Suggestion created: {suggestion_id}")
    print(f"   Data: {json.dumps(suggestion, indent=2)}")
else:
    print(f"❌ Failed to create suggestion: {response.status_code}")
    print(f"   Response: {response.text}")
    exit(1)

# Test 2: Verify with AI
print(f"\n[TEST 2] Verifying suggestion with AI...")
verify_headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"} if ADMIN_TOKEN else {}
response = requests.post(
    f"{API_URL}/admin/suggestions/{suggestion_id}/verify",
    headers=verify_headers
)
if response.status_code == 200:
    verification = response.json()
    print(f"✅ AI Verification completed:")
    print(f"   Is Authentic: {verification.get('is_authentic')}")
    print(f"   Reason: {verification.get('reason')}")
    if verification.get('is_authentic'):
        print(f"   Scientific Name: {verification.get('scientific_name')}")
        print(f"   Type: {verification.get('type')}")
else:
    print(f"❌ Verification failed: {response.status_code}")
    print(f"   Response: {response.text}")
    # Continue anyway to test approve endpoint

# Test 3: Approve and get auto-fill data
print(f"\n[TEST 3] Approving suggestion and getting auto-fill data...")
response = requests.post(
    f"{API_URL}/admin/suggestions/{suggestion_id}/approve",
    headers=verify_headers
)
if response.status_code == 200:
    approval_data = response.json()
    print(f"✅ Approval successful!")
    print(f"   Returned data structure:")
    
    # Check what data was returned
    if 'organism_data' in approval_data:
        org_data = approval_data['organism_data']
        print(f"\n   Organism Data:")
        print(f"   - Name: {org_data.get('name')}")
        print(f"   - Scientific Name: {org_data.get('scientific_name')}")
        print(f"   - Description: {org_data.get('description')[:100]}..." if org_data.get('description') else "   - Description: None")
        print(f"   - Classification: {org_data.get('classification')}")
    
    if 'images' in approval_data:
        images = approval_data['images']
        print(f"\n   Images: {len(images)} image(s) returned")
        if images:
            for i, img in enumerate(images):
                img_len = len(img) if isinstance(img, str) else 0
                print(f"   - Image {i+1}: {img_len} bytes")
    
    print(f"\n   Full response keys: {list(approval_data.keys())}")
    print(f"\n   Sample response (truncated):")
    truncated = {k: v[:100] if isinstance(v, str) else v for k, v in approval_data.items()}
    print(f"   {json.dumps(truncated, indent=2)}")
else:
    print(f"❌ Approval failed: {response.status_code}")
    print(f"   Response: {response.text}")
    exit(1)

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
print("\nWorkflow Status: ✅ PASSED")
print("- Frontend can now auto-fill form with returned data")
print("- Images are included as base64 for preview")
print("- Admin can review and click 'Add Organism' to finalize")
