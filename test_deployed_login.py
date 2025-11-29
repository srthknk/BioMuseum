#!/usr/bin/env python3
"""
Test deployed Render backend login
"""

import requests
import json

RENDER_API = "https://biomuseum.onrender.com/api"

print("\n" + "="*80)
print("🔐 TESTING RENDER BACKEND LOGIN")
print("="*80 + "\n")

# Test 1: Check if backend is alive
print("[1/3] Checking if Render backend is alive...")
try:
    response = requests.get(f"{RENDER_API}/", timeout=10)
    print(f"✓ Backend responded: {response.status_code}")
    print(f"  Response: {response.json()}")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Test 2: Try login with correct credentials
print("\n[2/3] Testing login with admin/adminSBES...")
try:
    response = requests.post(
        f"{RENDER_API}/admin/login",
        json={"username": "admin", "password": "adminSBES"},
        timeout=10
    )
    print(f"✓ Login response: {response.status_code}")
    data = response.json()
    print(f"  Response: {json.dumps(data, indent=2)}")
    
    if response.status_code == 200:
        token = data.get('access_token')
        print(f"\n✅ LOGIN SUCCESSFUL!")
        print(f"Token: {token[:30]}...")
    else:
        print(f"\n❌ Login failed with status {response.status_code}")
        
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Check CORS headers
print("\n[3/3] Checking CORS headers...")
try:
    response = requests.options(
        f"{RENDER_API}/admin/login",
        headers={
            "Origin": "https://bio-museum.vercel.app",
            "Access-Control-Request-Method": "POST"
        },
        timeout=10
    )
    print(f"✓ CORS preflight response: {response.status_code}")
    cors_origin = response.headers.get("Access-Control-Allow-Origin", "NOT SET")
    cors_methods = response.headers.get("Access-Control-Allow-Methods", "NOT SET")
    print(f"  Allow-Origin: {cors_origin}")
    print(f"  Allow-Methods: {cors_methods}")
    
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*80 + "\n")
