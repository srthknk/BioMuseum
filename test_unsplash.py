#!/usr/bin/env python3
"""Test Unsplash API directly"""

import requests
import json

UNSPLASH_KEY = 'vQ_yvjIskYKmvpXywThJ4u5kBjRzTAk1kDZkwYhwDbY'
API_URL = 'https://api.unsplash.com/search/photos'

print("Testing Unsplash API...")
print("=" * 70)
print(f"API Key: {UNSPLASH_KEY[:10]}...")
print(f"API URL: {API_URL}")
print("=" * 70)

try:
    # Test 1: Simple GET request
    print("\n1. Testing with basic parameters...")
    response = requests.get(
        API_URL,
        params={
            'query': 'dog',
            'client_id': UNSPLASH_KEY,
            'per_page': 5
        },
        timeout=10
    )
    
    print(f"   Status Code: {response.status_code}")
    print(f"   Reason: {response.reason}")
    print(f"   Content-Type: {response.headers.get('content-type')}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ SUCCESS - Found {len(data.get('results', []))} images")
        if data.get('results'):
            first_img = data['results'][0]
            print(f"   First image user: {first_img.get('user', {}).get('name')}")
            print(f"   First image URL: {first_img.get('urls', {}).get('regular', 'N/A')[:60]}...")
    else:
        print(f"   ❌ ERROR - Response: {response.text[:300]}")
        
except Exception as e:
    print(f"   ❌ Exception: {type(e).__name__}: {e}")

print("\n" + "=" * 70)
print("Test complete")
