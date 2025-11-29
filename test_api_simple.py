#!/usr/bin/env python3
"""
Simple API Test - Does not kill the server
Tests all endpoints quickly
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"
TIMEOUT = 5

print("\n" + "="*80)
print("🧪 API ENDPOINT TESTS")
print("="*80 + "\n")

# Test 1: Health
print("[1/8] Testing API Health...")
try:
    r = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
    print(f"✓ {r.status_code}: {r.json()}")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Test 2: Get organisms
print("\n[2/8] Testing GET /organisms...")
try:
    r = requests.get(f"{BASE_URL}/organisms", timeout=TIMEOUT)
    orgs = r.json()
    print(f"✓ {r.status_code}: Found {len(orgs)} organisms")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Login
print("\n[3/8] Testing POST /admin/login...")
try:
    r = requests.post(f"{BASE_URL}/admin/login", 
                     json={"username": "admin", "password": "adminSBES"},
                     timeout=TIMEOUT)
    data = r.json()
    token = data.get('access_token')
    print(f"✓ {r.status_code}: Login successful")
    print(f"  Token: {token[:20]}...")
except Exception as e:
    print(f"✗ Error: {e}")
    token = None

# Test 4: Create organism
if token:
    print("\n[4/8] Testing POST /admin/organisms (Create)...")
    try:
        organism = {
            "name": "Lion",
            "scientific_name": "Panthera leo",
            "classification": {"kingdom": "Animalia", "phylum": "Chordata", "class": "Mammalia"},
            "morphology": "Large feline",
            "physiology": "Powerful predator",
            "description": "The king of beasts"
        }
        r = requests.post(f"{BASE_URL}/admin/organisms",
                         json=organism,
                         headers={"Authorization": f"Bearer {token}"},
                         timeout=TIMEOUT)
        org_data = r.json()
        org_id = org_data.get('id')
        print(f"✓ {r.status_code}: Created organism ID {org_id}")
    except Exception as e:
        print(f"✗ Error: {e}")
        org_id = None
else:
    org_id = None
    print("\n[4/8] Skipped (no auth token)")

# Test 5: Get specific organism
if org_id:
    print(f"\n[5/8] Testing GET /organisms/{{id}}...")
    try:
        r = requests.get(f"{BASE_URL}/organisms/{org_id}", timeout=TIMEOUT)
        org = r.json()
        print(f"✓ {r.status_code}: Retrieved {org.get('name')}")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("\n[5/8] Skipped (no organism ID)")

# Test 6: Search
print("\n[6/8] Testing GET /search...")
try:
    r = requests.get(f"{BASE_URL}/search?q=lion", timeout=TIMEOUT)
    results = r.json()
    print(f"✓ {r.status_code}: Found {len(results)} results")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 7: Update organism
if org_id and token:
    print(f"\n[7/8] Testing PUT /admin/organisms/{{id}} (Update)...")
    try:
        r = requests.put(f"{BASE_URL}/admin/organisms/{org_id}",
                        json={"description": "Updated description"},
                        headers={"Authorization": f"Bearer {token}"},
                        timeout=TIMEOUT)
        print(f"✓ {r.status_code}: Updated organism")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("\n[7/8] Skipped")

# Test 8: Delete organism
if org_id and token:
    print(f"\n[8/8] Testing DELETE /admin/organisms/{{id}}...")
    try:
        r = requests.delete(f"{BASE_URL}/admin/organisms/{org_id}",
                           headers={"Authorization": f"Bearer {token}"},
                           timeout=TIMEOUT)
        print(f"✓ {r.status_code}: Deleted organism")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("\n[8/8] Skipped")

print("\n" + "="*80)
print("✅ API TESTS COMPLETE")
print("="*80 + "\n")
