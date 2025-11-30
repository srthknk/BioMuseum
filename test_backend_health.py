#!/usr/bin/env python3
"""Test the backend API"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
ADMIN_TOKEN = "your_admin_token_here"

print("Testing BioMuseum Backend API...")
print("=" * 70)

# Wait for server to be ready
time.sleep(2)

try:
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Response: {data}")
    else:
        print(f"   ❌ Error: {response.text[:200]}")
        
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    print("\n   Make sure the backend server is running on http://localhost:8000")

print("\n" + "=" * 70)
